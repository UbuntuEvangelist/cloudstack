/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
package com.cloud.hypervisor.xen.resource;

import java.io.File;
import java.net.URI;
import java.util.HashMap;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.TimeoutException;

import org.apache.cloudstack.storage.command.CopyCmdAnswer;
import org.apache.cloudstack.storage.command.CopyCommand;
import org.apache.cloudstack.storage.to.PrimaryDataStoreTO;
import org.apache.cloudstack.storage.to.SnapshotObjectTO;
import org.apache.cloudstack.storage.to.TemplateObjectTO;
import org.apache.cloudstack.storage.to.VolumeObjectTO;
import org.apache.log4j.Logger;

import com.cloud.agent.api.Answer;
import com.cloud.agent.api.to.DataObjectType;
import com.cloud.agent.api.to.DataStoreTO;
import com.cloud.agent.api.to.DataTO;
import com.cloud.agent.api.to.NfsTO;
import com.cloud.agent.api.to.S3TO;
import com.cloud.agent.api.to.SwiftTO;
import com.cloud.exception.InternalErrorException;
import com.cloud.storage.Storage;
import com.cloud.utils.exception.CloudRuntimeException;
import com.xensource.xenapi.Connection;
import com.xensource.xenapi.SR;
import com.xensource.xenapi.Task;
import com.xensource.xenapi.Types;
import com.xensource.xenapi.VDI;

public class Xenserver620StorageProcessor extends XenServerStorageProcessor {
    private static final Logger s_logger = Logger.getLogger(XenServerStorageProcessor.class);

    public Xenserver620StorageProcessor(CitrixResourceBase resource) {
        super(resource);
    }
    protected boolean mountNfs(Connection conn, String remoteDir, String localDir) {
        if (localDir == null) {
            localDir = "/var/cloud_mount/" + UUID.randomUUID().toString();
        }
        String results = hypervisorResource.callHostPluginAsync(conn, "cloud-plugin-snapshot", "mountNfsSecondaryStorage", 100 * 1000,
                "localDir", localDir, "remoteDir", remoteDir);
        if (results == null || results.isEmpty()) {
            String errMsg = "Could not mount secondary storage " + remoteDir + " on host ";
            s_logger.warn(errMsg);
            throw new CloudRuntimeException(errMsg);
        }
        return true;
    }
    protected SR createFileSr(Connection conn, String remotePath, String dir) {
        String localDir = "/var/cloud_mount/" + UUID.randomUUID().toString();
        mountNfs(conn, remotePath, localDir);
        SR sr = hypervisorResource.createFileSR(conn, localDir + "/" + dir);
        return sr;
    }

    @Override
    public Answer copyTemplateToPrimaryStorage(CopyCommand cmd) {
        DataTO srcData = cmd.getSrcTO();
        DataTO destData = cmd.getDestTO();
        int wait = cmd.getWait();
        DataStoreTO srcStore = srcData.getDataStore();
        Connection conn = hypervisorResource.getConnection();
        SR srcSr = null;
        try {
            if ((srcStore instanceof NfsTO) && (srcData.getObjectType() == DataObjectType.TEMPLATE)) {
                NfsTO srcImageStore = (NfsTO)srcStore;
                TemplateObjectTO srcTemplate = (TemplateObjectTO)srcData;
                String storeUrl = srcImageStore.getUrl();
                URI uri = new URI(storeUrl);
                String volumePath = srcData.getPath();

                int index = volumePath.lastIndexOf("/");
                String volumeDirectory = volumePath.substring(0, index);
                srcSr = createFileSr(conn, uri.getHost() + ":" + uri.getPath(), volumeDirectory);
                Set<VDI> vdis = srcSr.getVDIs(conn);
                if (vdis.size() != 1) {
                    return new CopyCmdAnswer("Can't find template VDI under: " + uri.getHost() + ":" + uri.getPath() + "/" + volumeDirectory);
                }

                VDI srcVdi = vdis.iterator().next();

                PrimaryDataStoreTO destStore = (PrimaryDataStoreTO)destData.getDataStore();
                String poolName = destStore.getUuid();


                SR poolsr = null;
                Set<SR> srs = SR.getByNameLabel(conn, poolName);
                if (srs.size() != 1) {
                    String msg = "There are " + srs.size() + " SRs with same name: " + poolName;
                    s_logger.warn(msg);
                    return new CopyCmdAnswer(msg);
                } else {
                    poolsr = srs.iterator().next();
                }
                String pUuid = poolsr.getUuid(conn);
                boolean isISCSI = IsISCSI(poolsr.getType(conn));
                Task task = srcVdi.copyAsync(conn, poolsr, null, null);
                // poll every 1 seconds ,
                hypervisorResource.waitForTask(conn, task, 1000, wait * 1000);
                hypervisorResource.checkForSuccess(conn, task);
                VDI tmpl = Types.toVDI(task, conn);
                VDI snapshotvdi = tmpl.snapshot(conn, new HashMap<String, String>());
                String snapshotUuid = snapshotvdi.getUuid(conn);
                snapshotvdi.setNameLabel(conn, "Template " + srcTemplate.getName());
                String parentuuid = getVhdParent(conn, pUuid, snapshotUuid, isISCSI);
                VDI parent = getVDIbyUuid(conn, parentuuid);
                Long phySize = parent.getPhysicalUtilisation(conn);
                tmpl.destroy(conn);
                poolsr.scan(conn);
                try{
                    Thread.sleep(5000);
                } catch (Exception e) {
                }

                TemplateObjectTO newVol = new TemplateObjectTO();
                newVol.setUuid(snapshotvdi.getUuid(conn));
                newVol.setPath(newVol.getUuid());
                newVol.setFormat(Storage.ImageFormat.VHD);
                return new CopyCmdAnswer(newVol);
            }
        }catch (Exception e) {
            String msg = "Catch Exception " + e.getClass().getName() + " for template + " + " due to " + e.toString();
            s_logger.warn(msg, e);
            return new CopyCmdAnswer(msg);
        } finally {
            if (srcSr != null) {
                hypervisorResource.removeSR(conn, srcSr);
            }
        }
        return new CopyCmdAnswer("not implemented yet");
    }

    protected String backupSnapshot(Connection conn, String primaryStorageSRUuid, String localMountPoint, String path, String secondaryStorageMountPath, String snapshotUuid, String prevBackupUuid, String prevSnapshotUuid, Boolean isISCSI, int wait) {
        String errMsg = null;
        boolean mounted = false;
        boolean filesrcreated = false;
        boolean copied = false;
        if (prevBackupUuid == null) {
            prevBackupUuid = "";
        }
        SR ssSR = null;

        String remoteDir = secondaryStorageMountPath;

        try {
            ssSR = createFileSr(conn, remoteDir, path);
            filesrcreated = true;

            VDI snapshotvdi = VDI.getByUuid(conn, snapshotUuid);
            Task task = null;
            if (wait == 0) {
                wait = 2 * 60 * 60;
            }
            VDI dvdi = null;
            try {
                VDI previousSnapshotVdi = null;
                if (prevSnapshotUuid != null) {
                    previousSnapshotVdi = VDI.getByUuid(conn,prevSnapshotUuid);
                }
                task = snapshotvdi.copyAsync(conn, ssSR, previousSnapshotVdi, null);
                // poll every 1 seconds ,
                hypervisorResource.waitForTask(conn, task, 1000, wait * 1000);
                hypervisorResource.checkForSuccess(conn, task);
                dvdi = Types.toVDI(task, conn);
                copied = true;
            } catch (TimeoutException e) {
                throw new CloudRuntimeException(e.toString());
            } finally {
                if (task != null) {
                    try {
                        task.destroy(conn);
                    } catch (Exception e1) {
                        s_logger.warn("unable to destroy task(" + task.toString() + ") on host("
                                + ") due to ", e1);
                    }
                }
            }
            String backupUuid = dvdi.getUuid(conn);
            return backupUuid;
        } catch (Exception e) {
            String msg = "Exception in backupsnapshot stage due to " + e.toString();
            s_logger.debug(msg);
            throw new CloudRuntimeException(msg, e);
        } finally {
            try {
                if (filesrcreated && ssSR != null) {
                    hypervisorResource.removeSR(conn, ssSR);
                }
            } catch (Exception e) {
                s_logger.debug("Exception in backupsnapshot cleanup stage due to " + e.toString());
            }
        }
    }

    @Override
    public Answer backupSnapshot(CopyCommand cmd) {
        Connection conn = hypervisorResource.getConnection();
        DataTO srcData = cmd.getSrcTO();
        DataTO cacheData = cmd.getCacheTO();
        DataTO destData = cmd.getDestTO();
        int wait = cmd.getWait();
        PrimaryDataStoreTO primaryStore = (PrimaryDataStoreTO)srcData.getDataStore();
        String primaryStorageNameLabel = primaryStore.getUuid();
        String secondaryStorageUrl = null;
        NfsTO cacheStore = null;
        String destPath = null;
        if (cacheData != null) {
            cacheStore = (NfsTO)cacheData.getDataStore();
            secondaryStorageUrl = cacheStore.getUrl();
            destPath = cacheData.getPath();
        } else {
            cacheStore = (NfsTO)destData.getDataStore();
            secondaryStorageUrl = cacheStore.getUrl();
            destPath = destData.getPath();
        }

        SnapshotObjectTO snapshotTO = (SnapshotObjectTO)srcData;
        SnapshotObjectTO snapshotOnImage = (SnapshotObjectTO)destData;
        String snapshotUuid = snapshotTO.getPath();

        String prevBackupUuid = snapshotOnImage.getParentSnapshotPath();
        String prevSnapshotUuid = snapshotTO.getParentSnapshotPath();

        // By default assume failure
        String details = null;
        String snapshotBackupUuid = null;
        boolean fullbackup = true;
        try {
            SR primaryStorageSR = hypervisorResource.getSRByNameLabelandHost(conn, primaryStorageNameLabel);
            if (primaryStorageSR == null) {
                throw new InternalErrorException("Could not backup snapshot because the primary Storage SR could not be created from the name label: " + primaryStorageNameLabel);
            }
            String psUuid = primaryStorageSR.getUuid(conn);
            Boolean isISCSI = IsISCSI(primaryStorageSR.getType(conn));

            VDI snapshotVdi = getVDIbyUuid(conn, snapshotUuid);
            String snapshotPaUuid = null;
            if ( prevBackupUuid != null ) {
                try {
                    snapshotPaUuid = getVhdParent(conn, psUuid, snapshotUuid, isISCSI);
                    if( snapshotPaUuid != null ) {
                        String snashotPaPaPaUuid = getVhdParent(conn, psUuid, snapshotPaUuid, isISCSI);
                        String prevSnashotPaUuid = getVhdParent(conn, psUuid, prevSnapshotUuid, isISCSI);
                        if (snashotPaPaPaUuid != null && prevSnashotPaUuid!= null && prevSnashotPaUuid.equals(snashotPaPaPaUuid)) {
                            fullbackup = false;
                        }
                    }
                } catch (Exception e) {
                }
            }

            URI uri = new URI(secondaryStorageUrl);
            String secondaryStorageMountPath = uri.getHost() + ":" + uri.getPath();
            DataStoreTO destStore = destData.getDataStore();
            String folder = destPath;
            String finalPath = null;

            String localMountPoint =  BaseMountPointOnHost + File.separator + UUID.nameUUIDFromBytes(secondaryStorageUrl.getBytes()).toString();
            if (fullbackup) {
                // the first snapshot is always a full snapshot

                if( !hypervisorResource.createSecondaryStorageFolder(conn, secondaryStorageMountPath, folder)) {
                    details = " Filed to create folder " + folder + " in secondary storage";
                    s_logger.warn(details);
                    return new CopyCmdAnswer(details);
                }
                SR snapshotSr = null;
                try {
                    snapshotSr = createFileSr(conn, secondaryStorageMountPath, folder);
                    Task task = snapshotVdi.copyAsync(conn, snapshotSr, null, null);
                    // poll every 1 seconds ,
                    hypervisorResource.waitForTask(conn, task, 1000, wait * 1000);
                    hypervisorResource.checkForSuccess(conn, task);
                    VDI backedVdi = Types.toVDI(task, conn);
                    snapshotBackupUuid = backedVdi.getUuid(conn);

                    if( destStore instanceof SwiftTO) {
                        try {
                            String container = "S-" + snapshotTO.getVolume().getVolumeId().toString();
                            String destSnapshotName = swiftBackupSnapshot(conn, (SwiftTO)destStore, snapshotSr.getUuid(conn), snapshotBackupUuid, container, false, wait);
                            String swiftPath = container + File.separator + destSnapshotName;
                            finalPath = swiftPath;
                        } finally {
                            try {
                                deleteSnapshotBackup(conn, localMountPoint, folder, secondaryStorageMountPath, snapshotBackupUuid);
                            } catch (Exception e) {
                                s_logger.debug("Failed to delete snapshot on cache storages" ,e);
                            }
                        }

                    } else if (destStore instanceof S3TO) {
                        try {
                            finalPath = backupSnapshotToS3(conn, (S3TO) destStore, snapshotSr.getUuid(conn), folder, snapshotBackupUuid, isISCSI, wait);
                            if (finalPath == null) {
                                throw new CloudRuntimeException("S3 upload of snapshots " + snapshotBackupUuid + " failed");
                            }
                        } finally {
                            try {
                                deleteSnapshotBackup(conn, localMountPoint, folder, secondaryStorageMountPath, snapshotBackupUuid);
                            } catch (Exception e) {
                                s_logger.debug("Failed to delete snapshot on cache storages" ,e);
                            }
                        }
                        // finalPath = folder + File.separator + snapshotBackupUuid;
                    } else {
                        finalPath = folder + File.separator + snapshotBackupUuid;
                    }

                } finally {
                    if( snapshotSr != null) {
                        hypervisorResource.removeSR(conn, snapshotSr);
                    }
                }
            } else {
                String primaryStorageSRUuid = primaryStorageSR.getUuid(conn);
                if( destStore instanceof SwiftTO ) {
                    String container = "S-" + snapshotTO.getVolume().getVolumeId().toString();
                    snapshotBackupUuid = swiftBackupSnapshot(conn, (SwiftTO)destStore, primaryStorageSRUuid, snapshotPaUuid, "S-" + snapshotTO.getVolume().getVolumeId().toString(), isISCSI, wait);
                    finalPath = container + File.separator + snapshotBackupUuid;
                } else if (destStore instanceof S3TO ) {
                    finalPath = backupSnapshotToS3(conn, (S3TO) destStore, primaryStorageSRUuid, folder, snapshotPaUuid, isISCSI, wait);
                    if (finalPath == null) {
                        throw new CloudRuntimeException("S3 upload of snapshots " + snapshotPaUuid + " failed");
                    }
                } else {
                    snapshotBackupUuid = backupSnapshot(conn, primaryStorageSRUuid, localMountPoint, folder,
                            secondaryStorageMountPath, snapshotUuid, prevBackupUuid, prevSnapshotUuid, isISCSI, wait);

                    finalPath = folder + File.separator + snapshotBackupUuid;
                }
            }
            String volumeUuid = snapshotTO.getVolume().getPath();
            destroySnapshotOnPrimaryStorageExceptThis(conn, volumeUuid, snapshotUuid);

            SnapshotObjectTO newSnapshot = new SnapshotObjectTO();
            newSnapshot.setPath(finalPath);
            if (fullbackup) {
                newSnapshot.setParentSnapshotPath(null);
            } else {
                newSnapshot.setParentSnapshotPath(prevBackupUuid);
            }
            return new CopyCmdAnswer(newSnapshot);
        } catch (Types.XenAPIException e) {
            details = "BackupSnapshot Failed due to " + e.toString();
            s_logger.warn(details, e);
        } catch (Exception e) {
            details = "BackupSnapshot Failed due to " + e.getMessage();
            s_logger.warn(details, e);
        }

        return new CopyCmdAnswer(details);
    }

    @Override
    public Answer createTemplateFromVolume(CopyCommand cmd) {
        Connection conn = hypervisorResource.getConnection();
        VolumeObjectTO volume = (VolumeObjectTO)cmd.getSrcTO();
        TemplateObjectTO template = (TemplateObjectTO)cmd.getDestTO();
        NfsTO destStore = (NfsTO)cmd.getDestTO().getDataStore();
        int wait = cmd.getWait();

        String secondaryStoragePoolURL = destStore.getUrl();
        String volumeUUID = volume.getPath();

        String userSpecifiedName = template.getName();


        String details = null;
        SR tmpltSR = null;
        boolean result = false;
        String secondaryStorageMountPath = null;
        String installPath = null;
        try {
            URI uri = new URI(secondaryStoragePoolURL);
            secondaryStorageMountPath = uri.getHost() + ":" + uri.getPath();
            installPath = template.getPath();
            if( !hypervisorResource.createSecondaryStorageFolder(conn, secondaryStorageMountPath, installPath)) {
                details = " Filed to create folder " + installPath + " in secondary storage";
                s_logger.warn(details);
                return new CopyCmdAnswer(details);
            }

            VDI vol = getVDIbyUuid(conn, volumeUUID);
            // create template SR
            tmpltSR = createFileSr(conn, uri.getHost() + ":" + uri.getPath(), installPath);

            // copy volume to template SR
            Task task = vol.copyAsync(conn, tmpltSR, null, null);
            // poll every 1 seconds ,
            hypervisorResource.waitForTask(conn, task, 1000, wait * 1000);
            hypervisorResource.checkForSuccess(conn, task);
            VDI tmpltVDI = Types.toVDI(task, conn);
            // scan makes XenServer pick up VDI physicalSize
            tmpltSR.scan(conn);
            if (userSpecifiedName != null) {
                tmpltVDI.setNameLabel(conn, userSpecifiedName);
            }

            String tmpltUUID = tmpltVDI.getUuid(conn);
            String tmpltFilename = tmpltUUID + ".vhd";
            long virtualSize = tmpltVDI.getVirtualSize(conn);
            long physicalSize = tmpltVDI.getPhysicalUtilisation(conn);
            // create the template.properties file
            String templatePath = secondaryStorageMountPath + "/" + installPath;
            result = hypervisorResource.postCreatePrivateTemplate(conn, templatePath, tmpltFilename, tmpltUUID, userSpecifiedName, null, physicalSize, virtualSize, template.getId());
            if (!result) {
                throw new CloudRuntimeException("Could not create the template.properties file on secondary storage dir");
            }
            installPath = installPath + "/" + tmpltFilename;
            hypervisorResource.removeSR(conn, tmpltSR);
            tmpltSR = null;
            TemplateObjectTO newTemplate = new TemplateObjectTO();
            newTemplate.setPath(installPath);
            newTemplate.setFormat(Storage.ImageFormat.VHD);
            newTemplate.setSize(virtualSize);
            newTemplate.setPhysicalSize(physicalSize);
            newTemplate.setName(tmpltUUID);
            CopyCmdAnswer answer = new CopyCmdAnswer(newTemplate);
            return answer;
        } catch (Exception e) {
            if (tmpltSR != null) {
                hypervisorResource.removeSR(conn, tmpltSR);
            }
            if ( secondaryStorageMountPath != null) {
                hypervisorResource.deleteSecondaryStorageFolder(conn, secondaryStorageMountPath, installPath);
            }
            details = "Creating template from volume " + volumeUUID + " failed due to " + e.toString();
            s_logger.error(details, e);
        }
        return new CopyCmdAnswer(details);
    }

    @Override
    public Answer createVolumeFromSnapshot(CopyCommand cmd) {
        Connection conn = hypervisorResource.getConnection();
        DataTO srcData = cmd.getSrcTO();
        SnapshotObjectTO snapshot = (SnapshotObjectTO)srcData;
        DataTO destData = cmd.getDestTO();
        PrimaryDataStoreTO pool = (PrimaryDataStoreTO)destData.getDataStore();
        DataStoreTO imageStore = srcData.getDataStore();

        if (!(imageStore instanceof NfsTO)) {
            return new CopyCmdAnswer("unsupported protocol");
        }

        NfsTO nfsImageStore = (NfsTO)imageStore;
        String primaryStorageNameLabel = pool.getUuid();
        String secondaryStorageUrl = nfsImageStore.getUrl();
        int wait = cmd.getWait();
        boolean result = false;
        // Generic error message.
        String details = null;
        String volumeUUID = null;

        if (secondaryStorageUrl == null) {
            details += " because the URL passed: " + secondaryStorageUrl + " is invalid.";
            return new CopyCmdAnswer(details);
        }
        SR srcSr = null;
        try {
            SR primaryStorageSR = hypervisorResource.getSRByNameLabelandHost(conn, primaryStorageNameLabel);
            if (primaryStorageSR == null) {
                throw new InternalErrorException("Could not create volume from snapshot because the primary Storage SR could not be created from the name label: "
                        + primaryStorageNameLabel);
            }
            // Get the absolute path of the snapshot on the secondary storage.
            String snapshotInstallPath = snapshot.getPath();
            int index = snapshotInstallPath.lastIndexOf(File.separator);
            String snapshotUuid = snapshotInstallPath.substring(index + 1);
            String snapshotDirectory = snapshotInstallPath.substring(0, index);
            index = snapshotUuid.lastIndexOf(".");
            if (index != -1) {
                snapshotUuid = snapshotUuid.substring(0, index);
            }

            URI uri = new URI(secondaryStorageUrl);

            srcSr = createFileSr(conn, uri.getHost() + ":" + uri.getPath(), snapshotDirectory);

            VDI snapshotVdi = VDI.getByUuid(conn, snapshotUuid);
            Task task = snapshotVdi.copyAsync(conn, primaryStorageSR, null, null);
            // poll every 1 seconds ,
            hypervisorResource.waitForTask(conn, task, 1000, wait * 1000);
            hypervisorResource.checkForSuccess(conn, task);
            VDI volumeVdi = Types.toVDI(task, conn);
            volumeUUID = volumeVdi.getUuid(conn);
            result = true;
            VDI volume = VDI.getByUuid(conn, volumeUUID);
            VDI.Record vdir = volume.getRecord(conn);
            VolumeObjectTO newVol = new VolumeObjectTO();
            newVol.setPath(volumeUUID);
            newVol.setSize(vdir.virtualSize);
            return new CopyCmdAnswer(newVol);
        } catch (Types.XenAPIException e) {
            details += " due to " + e.toString();
            s_logger.warn(details, e);
        } catch (Exception e) {
            details += " due to " + e.getMessage();
            s_logger.warn(details, e);
        } finally {
            if (srcSr != null) {
                hypervisorResource.removeSR(conn, srcSr);
            }
        }
        if (!result) {
            // Is this logged at a higher level?
            s_logger.error(details);
        }

        // In all cases return something.
        return new CopyCmdAnswer(details);
    }

    @Override
    public Answer copyVolumeFromPrimaryToSecondary(CopyCommand cmd) {
        Connection conn = hypervisorResource.getConnection();
        VolumeObjectTO srcVolume = (VolumeObjectTO)cmd.getSrcTO();
        VolumeObjectTO destVolume = (VolumeObjectTO)cmd.getDestTO();
        int wait = cmd.getWait();
        DataStoreTO destStore = destVolume.getDataStore();

        if (destStore instanceof NfsTO) {
            SR secondaryStorage = null;
            try {
                NfsTO nfsStore = (NfsTO)destStore;
                URI uri = new URI(nfsStore.getUrl());
                // Create the volume folder
                if (!hypervisorResource.createSecondaryStorageFolder(conn, uri.getHost() + ":" + uri.getPath(), destVolume.getPath())) {
                    throw new InternalErrorException("Failed to create the volume folder.");
                }

                // Create a SR for the volume UUID folder
                secondaryStorage = createFileSr(conn, uri.getHost() + ":" + uri.getPath(), destVolume.getPath());
                // Look up the volume on the source primary storage pool
                VDI srcVdi = getVDIbyUuid(conn, srcVolume.getPath());
                // Copy the volume to secondary storage
                Task task = srcVdi.copyAsync(conn, secondaryStorage, null, null);
                // poll every 1 seconds ,
                hypervisorResource.waitForTask(conn, task, 1000, wait * 1000);
                hypervisorResource.checkForSuccess(conn, task);
                VDI destVdi = Types.toVDI(task, conn);
                String destVolumeUUID = destVdi.getUuid(conn);

                VolumeObjectTO newVol = new VolumeObjectTO();
                newVol.setPath(destVolume.getPath() + File.separator + destVolumeUUID + ".vhd");
                newVol.setSize(srcVolume.getSize());
                return new CopyCmdAnswer(newVol);
            } catch (Exception e) {
                s_logger.debug("Failed to copy volume to secondary: " + e.toString());
                return new CopyCmdAnswer("Failed to copy volume to secondary: " + e.toString());
            } finally {
                hypervisorResource.removeSR(conn, secondaryStorage);
            }
        }
        return new CopyCmdAnswer("unsupported protocol");
    }

    @Override
    public Answer copyVolumeFromImageCacheToPrimary(CopyCommand cmd) {
        Connection conn = hypervisorResource.getConnection();
        DataTO srcData = cmd.getSrcTO();
        DataTO destData = cmd.getDestTO();
        int wait = cmd.getWait();
        VolumeObjectTO srcVolume = (VolumeObjectTO)srcData;
        VolumeObjectTO destVolume = (VolumeObjectTO)destData;
        PrimaryDataStoreTO primaryStore = (PrimaryDataStoreTO)destVolume.getDataStore();
        DataStoreTO srcStore = srcVolume.getDataStore();

        if (srcStore instanceof NfsTO) {
            NfsTO nfsStore = (NfsTO)srcStore;
            String volumePath = srcVolume.getPath();
            int index = volumePath.lastIndexOf("/");
            String volumeDirectory = volumePath.substring(0, index);
            String volumeUuid = volumePath.substring(index + 1);
            index = volumeUuid.indexOf(".");
            if (index != -1) {
                volumeUuid = volumeUuid.substring(0, index);
            }
            URI uri = null;
            try {
                uri = new URI(nfsStore.getUrl());
            } catch (Exception e) {
                return new CopyCmdAnswer(e.toString());
            }
            SR srcSr = createFileSr(conn, uri.getHost() + ":" + uri.getPath(), volumeDirectory);
            try {
                SR primaryStoragePool = hypervisorResource.getStorageRepository(conn, primaryStore.getUuid());
                VDI srcVdi = VDI.getByUuid(conn, volumeUuid);
                Task task = srcVdi.copyAsync(conn, primaryStoragePool, null, null);
                // poll every 1 seconds ,
                hypervisorResource.waitForTask(conn, task, 1000, wait * 1000);
                hypervisorResource.checkForSuccess(conn, task);
                VDI destVdi = Types.toVDI(task, conn);
                VolumeObjectTO newVol = new VolumeObjectTO();
                newVol.setPath(destVdi.getUuid(conn));
                newVol.setSize(srcVolume.getSize());

                return new CopyCmdAnswer(newVol);
            } catch (Exception e) {
                String msg = "Catch Exception " + e.getClass().getName() + " due to " + e.toString();
                s_logger.warn(msg, e);
                return new CopyCmdAnswer(e.toString());
            } finally {
                if (srcSr != null) {
                    hypervisorResource.removeSR(conn, srcSr);
                }
            }
        }

        s_logger.debug("unsupported protocol");
        return new CopyCmdAnswer("unsupported protocol");
    }

}