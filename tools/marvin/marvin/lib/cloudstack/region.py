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

from marvin.cloudstackAPI import addRegion,listRegions,updateRegion,removeRegion
class Region:
    """ Regions related Api """
    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, services):
        cmd = addRegion.addRegionCmd()
        cmd.id = services["regionid"]
        cmd.endpoint = services["regionendpoint"]
        cmd.name = services["regionname"]
        try:
            region = apiclient.addRegion(cmd)
            if region is not None:
                return Region(region.__dict__)
        except Exception as e:
            raise e

    @classmethod
    def list(cls, apiclient, **kwargs):
        cmd = listRegions.listRegionsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        region = apiclient.listRegions(cmd)
        return region

    def update(self, apiclient, services):
        cmd = updateRegion.updateRegionCmd()
        cmd.id = self.id
        if services["regionendpoint"]:
            cmd.endpoint = services["regionendpoint"]
        if services["regionname"]:
            cmd.name = services["regionname"]
        region = apiclient.updateRegion(cmd)
        return region

    def delete(self, apiclient):
        cmd = removeRegion.removeRegionCmd()
        cmd.id = self.id
        region = apiclient.removeRegion(cmd)
        return region

