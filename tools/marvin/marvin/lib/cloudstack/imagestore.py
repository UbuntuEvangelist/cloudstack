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
from marvin.cloudstackAPI import createSecondaryStagingStore,deleteSecondaryStagingStore,listSecondaryStagingStores,addImageStore,deleteImageStore,listImageStores
class SecondaryStagingStore:
    """Manage Staging Store"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, url, provider, services=None):
        """Create Staging Storage"""
        cmd = createSecondaryStagingStore.createSecondaryStagingStoreCmd()
        cmd.url = url
        cmd.provider = provider
        if services:
            if "zoneid" in services:
                cmd.zoneid = services["zoneid"]
            if "details" in services:
                cmd.details = services["details"]
            if "scope" in services:
                cmd.scope = services["scope"]

        return SecondaryStagingStore(apiclient.createSecondaryStagingStore(cmd).__dict__)

    def delete(self, apiclient):
        """Delete Staging Storage"""
        cmd = deleteSecondaryStagingStore.deleteSecondaryStagingStoreCmd()
        cmd.id = self.id
        apiclient.deleteSecondaryStagingStore(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        cmd = listSecondaryStagingStores.listSecondaryStagingStoresCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listSecondaryStagingStores(cmd))


class ImageStore:
    """Manage image stores"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, url, provider, services=None):
        """Add Image Store"""
        cmd = addImageStore.addImageStoreCmd()
        cmd.url = url
        cmd.provider = provider
        if services:
            if "zoneid" in services:
                cmd.zoneid = services["zoneid"]
            if "details" in services:
                cmd.details = services["details"]
            if "scope" in services:
                cmd.scope = services["scope"]

        return ImageStore(apiclient.addImageStore(cmd).__dict__)

    def delete(self, apiclient):
        """Delete Image Store"""
        cmd = deleteImageStore.deleteImageStoreCmd()
        cmd.id = self.id
        apiclient.deleteImageStore(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        cmd = listImageStores.listImageStoresCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listImageStores(cmd))




