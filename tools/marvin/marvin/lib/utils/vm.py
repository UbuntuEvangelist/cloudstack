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

from marvin.lib.utils.zone import getCurrentZone
from marvin.lib.utils.domain import getCurrentDomain
from marvin.lib.utils.serviceoffering import createTinyServiceOffering
from marvin.lib.utils.account import createAccount
from marvin.lib.utils.template import getDefaultUservmTemplate
from marvin.lib.cloudstack import vm
from marvin.lib.utils.volume import getRootVolume
virtualmachines = {
    "vm":{
        "displayname": "testserver",
        "username": "root",
        "password": "password",
        "ssh_port": 22,
        "hypervisor": "XenServer",
        "privateport": 22,
        "publicport": 22,
        "protocol": 'TCP',
    }
}

class VirtualMachine:
    def __init__(self):
        self.zone = None
        self.domain = None
        self.account = None
        self.serviceOffering = None
        self.template = None
        self.vm = None
        self.apiClient = None

    def delete(self):
        if self.vm is not None:
            self.vm.delete(self.apiClient)
        if self.serviceOffering is not None:
            self.serviceOffering.delete(self.apiClient)
        if self.account is not None:
            self.account.delete(self.apiClient)

    def getRootVolume(self):
        return getRootVolume(self)

def createvm(apiClient):
    virtm = VirtualMachine()
    virtm.apiClient = apiClient
    try:
        virtm.zone = getCurrentZone(apiClient)
        virtm.domain = getCurrentDomain(apiClient)
        virtm.account = createAccount(apiClient,virtm.domain)
        virtm.serviceOffering = createTinyServiceOffering(apiClient, virtm.zone)
        virtm.template = getDefaultUservmTemplate(apiClient)

        global virtualmachines
        params = virtualmachines["vm"]
        virtm.vm = vm.VirtualMachine.create(
            apiClient,
            params,
            zoneid=virtm.zone.id,
            templateid=virtm.template.id,
            accountid=virtm.account.name,
            domainid=virtm.account.domainid,
            serviceofferingid=virtm.serviceOffering.id,
            mode=virtm.zone.networktype
        )
        return virtm
    except:
        virtm.delete()
        raise



