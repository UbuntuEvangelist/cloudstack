# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import time

from marvin.cloudstackAPI import createVolume,deleteVolume,listVolumes,resizeVolume,uploadVolume,extractVolume,migrateVolume
from marvin.lib.cloudstack.utils import random_gen


class Volume:
    """Manage Volume Life cycle
    """
    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, services, zoneid=None, account=None,
               domainid=None, diskofferingid=None, projectid=None):
        """Create Volume"""
        cmd = createVolume.createVolumeCmd()
        cmd.name = services["diskname"]

        if diskofferingid:
            cmd.diskofferingid = diskofferingid
        elif "diskofferingid" in services:
            cmd.diskofferingid = services["diskofferingid"]

        if zoneid:
            cmd.zoneid = zoneid
        elif "zoneid" in services:
            cmd.zoneid = services["zoneid"]

        if account:
            cmd.account = account
        elif "account" in services:
            cmd.account = services["account"]

        if domainid:
            cmd.domainid = domainid
        elif "domainid" in services:
            cmd.domainid = services["domainid"]

        if projectid:
            cmd.projectid = projectid
        return Volume(apiclient.createVolume(cmd).__dict__)

    @classmethod
    def create_custom_disk(cls, apiclient, services, account=None,
                           domainid=None, diskofferingid=None):
        """Create Volume from Custom disk offering"""
        cmd = createVolume.createVolumeCmd()
        cmd.name = services["diskname"]

        if diskofferingid:
            cmd.diskofferingid = diskofferingid
        elif "customdiskofferingid" in services:
            cmd.diskofferingid = services["customdiskofferingid"]

        cmd.size = services["customdisksize"]
        cmd.zoneid = services["zoneid"]

        if account:
            cmd.account = account
        else:
            cmd.account = services["account"]

        if domainid:
            cmd.domainid = domainid
        else:
            cmd.domainid = services["domainid"]

        return Volume(apiclient.createVolume(cmd).__dict__)

    @classmethod
    def create_from_snapshot(cls, apiclient, snapshot_id, services,
                             account=None, domainid=None):
        """Create Volume from snapshot"""
        cmd = createVolume.createVolumeCmd()
        cmd.name = "-".join([services["diskname"], random_gen()])
        cmd.snapshotid = snapshot_id
        cmd.zoneid = services["zoneid"]
        cmd.size = services["size"]
        if account:
            cmd.account = account
        else:
            cmd.account = services["account"]
        if domainid:
            cmd.domainid = domainid
        else:
            cmd.domainid = services["domainid"]
        return Volume(apiclient.createVolume(cmd).__dict__)

    def delete(self, apiclient):
        """Delete Volume"""
        cmd = deleteVolume.deleteVolumeCmd()
        cmd.id = self.id
        apiclient.deleteVolume(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List all volumes matching criteria"""

        cmd = listVolumes.listVolumesCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listVolumes(cmd))

    def resize(self, apiclient, **kwargs):
        """Resize a volume"""
        cmd = resizeVolume.resizeVolumeCmd()
        cmd.id = self.id
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.resizeVolume(cmd))

    @classmethod
    def upload(cls, apiclient, services, zoneid=None,
               account=None, domainid=None, url=None):
        """Uploads the volume to specified account"""

        cmd = uploadVolume.uploadVolumeCmd()
        if zoneid:
            cmd.zoneid = zoneid
        if account:
            cmd.account = account
        if domainid:
            cmd.domainid = domainid
        cmd.format = services["format"]
        cmd.name = services["diskname"]
        if url:
            cmd.url = url
        else:
            cmd.url = services["url"]
        return Volume(apiclient.uploadVolume(cmd).__dict__)

    def wait_for_upload(self, apiclient, timeout=10, interval=60):
        """Wait for upload"""
        # Sleep to ensure template is in proper state before download
        time.sleep(interval)

        while True:
            volume_response = Volume.list(
                apiclient,
                id=self.id,
                zoneid=self.zoneid,
            )
            if isinstance(volume_response, list):

                volume = volume_response[0]
                # If volume is ready,
                # volume.state = Allocated
                if volume.state == 'Uploaded':
                    break

                elif 'Uploading' in volume.state:
                    time.sleep(interval)

                elif 'Installing' not in volume.state:
                    raise Exception(
                        "Error in uploading volume: status - %s" %
                        volume.state)
            elif timeout == 0:
                break

            else:
                time.sleep(interval)
                timeout = timeout - 1
        return

    @classmethod
    def extract(cls, apiclient, volume_id, zoneid, mode):
        """Extracts the volume"""

        cmd = extractVolume.extractVolumeCmd()
        cmd.id = volume_id
        cmd.zoneid = zoneid
        cmd.mode = mode
        return Volume(apiclient.extractVolume(cmd).__dict__)

    @classmethod
    def migrate(cls, apiclient, **kwargs):
        """Migrate a volume"""
        cmd = migrateVolume.migrateVolumeCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.migrateVolume(cmd))
