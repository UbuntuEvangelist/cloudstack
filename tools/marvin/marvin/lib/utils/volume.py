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
from marvin.lib.utils.snapshot import createSnapshot
class Volume:
    def __init__(self, apiClient, vol, vm, snapshot):
        self.apiClient = apiClient
        self.volume = vol
        self.vm = vm
        self.snapshot = snapshot

    def takeSnapshot(self):
        return createSnapshot(self)

    def delete(self):
        self.volume.delete(self.apiClient)

def getRootVolume(vm):
    vol = Volume(vm.apiClient)
    vmId = vm.id
    vols = Volume.list(vm.apiClient, virtualmachineid=vmId, type="ROOT")
    vol.volume = vols[0]
    vol.vm = vm
    return vol

def createVolumeFromSnapshot(snapshot):
    vol = Volume(snapshot.apiClient, snapshot=Volume.create_from_snapshot(snapshot.apiClient, snapshot.id))
    return vol