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

from marvin.cloudstackAPI import createDiskOffering,deleteDiskOffering,listDiskOfferings
class DiskOffering:
    """Manage disk offerings cycle"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, services, custom=False, domainid=None):
        """Create Disk offering"""
        cmd = createDiskOffering.createDiskOfferingCmd()
        cmd.displaytext = services["displaytext"]
        cmd.name = services["name"]
        if custom:
            cmd.customized = True
        else:
            cmd.disksize = services["disksize"]

        if domainid:
            cmd.domainid = domainid

        if "storagetype" in services:
            cmd.storagetype = services["storagetype"]

        if "customizediops" in services:
            cmd.customizediops = services["customizediops"]

        if "disksize" in services:
            cmd.disksize = services["disksize"]

        if "maxiops" in services:
            cmd.maxiops = services["maxiops"]

        if "miniops" in services:
            cmd.miniops = services["miniops"]

        if "tags" in services:
            cmd.tags = services["tags"]

        if "provisioningtype" in services:
            cmd.provisioningtype = services["provisioningtype"]

        return DiskOffering(apiclient.createDiskOffering(cmd).__dict__)

    def delete(self, apiclient):
        """Delete Disk offering"""
        cmd = deleteDiskOffering.deleteDiskOfferingCmd()
        cmd.id = self.id
        apiclient.deleteDiskOffering(cmd)
        return

    @classmethod
    def list(cls, apiclient, **kwargs):
        """Lists all available disk offerings."""

        cmd = listDiskOfferings.listDiskOfferingsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listDiskOfferings(cmd))
