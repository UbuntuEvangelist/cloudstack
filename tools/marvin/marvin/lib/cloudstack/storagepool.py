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

from marvin.cloudstackAPI import createStoragePool,enableStorageMaintenance,deleteStoragePool,listStoragePools,findStoragePoolsForMigration
import time
class StoragePool:
    """Manage Storage pools (Primary Storage)"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, services, scope=None, clusterid=None,
               zoneid=None, podid=None, provider=None, tags=None,
               capacityiops=None, capacitybytes=None, hypervisor=None):
        """Create Storage pool (Primary Storage)"""

        cmd = createStoragePool.createStoragePoolCmd()
        cmd.name = services["name"]

        if podid:
            cmd.podid = podid
        elif "podid" in services:
            cmd.podid = services["podid"]

        cmd.url = services["url"]
        if clusterid:
            cmd.clusterid = clusterid
        elif "clusterid" in services:
            cmd.clusterid = services["clusterid"]

        if zoneid:
            cmd.zoneid = zoneid
        else:
            cmd.zoneid = services["zoneid"]

        if scope:
            cmd.scope = scope
        elif "scope" in services:
            cmd.scope = services["scope"]

        if provider:
            cmd.provider = provider
        elif "provider" in services:
            cmd.provider = services["provider"]

        if tags:
            cmd.tags = tags
        elif "tags" in services:
            cmd.tags = services["tags"]

        if capacityiops:
            cmd.capacityiops = capacityiops
        elif "capacityiops" in services:
            cmd.capacityiops = services["capacityiops"]

        if capacitybytes:
            cmd.capacitybytes = capacitybytes
        elif "capacitybytes" in services:
            cmd.capacitybytes = services["capacitybytes"]

        if hypervisor:
            cmd.hypervisor = hypervisor
        elif "hypervisor" in services:
            cmd.hypervisor = services["hypervisor"]

        return StoragePool(apiclient.createStoragePool(cmd).__dict__)

    def delete(self, apiclient):
        """Delete Storage pool (Primary Storage)"""

        # Storage pool must be in maintenance mode before deletion
        cmd = enableStorageMaintenance.enableStorageMaintenanceCmd()
        cmd.id = self.id
        apiclient.enableStorageMaintenance(cmd)
        time.sleep(30)
        cmd = deleteStoragePool.deleteStoragePoolCmd()
        cmd.id = self.id
        apiclient.deleteStoragePool(cmd)
        return

    def enableMaintenance(self, apiclient):
        """enables maintenance mode Storage pool"""

        cmd = enableStorageMaintenance.enableStorageMaintenanceCmd()
        cmd.id = self.id
        return apiclient.enableStorageMaintenance(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List all storage pools matching criteria"""

        cmd = listStoragePools.listStoragePoolsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listStoragePools(cmd))

    @classmethod
    def listForMigration(cls, apiclient, **kwargs):
        """List all storage pools for migration matching criteria"""

        cmd = findStoragePoolsForMigration.findStoragePoolsForMigrationCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.findStoragePoolsForMigration(cmd))

