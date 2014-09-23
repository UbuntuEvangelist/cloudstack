#!/usr/bin/env python
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
import pytest
from marvin.lib.cloudstack.base import SimulatorMock
from marvin.cloudstackException import CloudstackAPIException

#volume stucks in creating state if creating volume from snapshot failed
@pytest.mark.tags(hypervisor_in=["simulator"])
def test_CS_18306(vm, api_client):
    nvm = vm.vm
    mock = SimulatorMock.create(api_client,"CreateSnapshotCmd", zoneid=vm.zone.id)

    rootVol = nvm.getRootVolume()
    snapshot = rootVol.takeSnapshot()

    with pytest.raises(CloudstackAPIException) as snapshotFailure:
        nvol = snapshot.createVolume()

    assert snapshotFailure is not None






