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

from marvin.cloudstackAPI import createPod,deletePod,listPods
class Pod:
    """Manage Pod"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, services):
        """Create Pod"""
        cmd = createPod.createPodCmd()
        cmd.gateway = services["gateway"]
        cmd.netmask = services["netmask"]
        cmd.name = services["name"]
        cmd.startip = services["startip"]
        cmd.endip = services["endip"]
        cmd.zoneid = services["zoneid"]

        return Pod(apiclient.createPod(cmd).__dict__)

    def delete(self, apiclient):
        """Delete Pod"""

        cmd = deletePod.deletePodCmd()
        cmd.id = self.id
        apiclient.deletePod(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        "Returns a default pod for specified zone"

        cmd = listPods.listPodsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return apiclient.listPods(cmd)
