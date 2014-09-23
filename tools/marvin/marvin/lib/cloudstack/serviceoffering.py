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

from marvin.cloudstackAPI import createServiceOffering,deleteServiceOffering,listServiceOfferings
class ServiceOffering:

    """Manage service offerings cycle"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, services, domainid=None, **kwargs):
        """Create Service offering"""
        cmd = createServiceOffering.createServiceOfferingCmd()
        cmd.cpunumber = services["cpunumber"]
        cmd.cpuspeed = services["cpuspeed"]
        cmd.displaytext = services["displaytext"]
        cmd.memory = services["memory"]
        cmd.name = services["name"]
        if "storagetype" in services:
            cmd.storagetype = services["storagetype"]

        if "systemvmtype" in services:
            cmd.systemvmtype = services['systemvmtype']

        if "issystem" in services:
            cmd.issystem = services['issystem']

        if "tags" in services:
            cmd.tags = services["tags"]

        if "hosttags" in services:
            cmd.hosttags = services["hosttags"]

        if "deploymentplanner" in services:
            cmd.deploymentplanner = services["deploymentplanner"]

        if "serviceofferingdetails" in services:
            count = 1
            for i in services["serviceofferingdetails"]:
                for key, value in i.items():
                    setattr(cmd, "serviceofferingdetails[%d].key" % count, key)
                    setattr(cmd, "serviceofferingdetails[%d].value" % count, value)
                count = count + 1

        if "isvolatile" in services:
            cmd.isvolatile = services["isvolatile"]

        if "miniops" in services:
            cmd.miniops = services["miniops"]

        if "maxiops" in services:
            cmd.maxiops = services["maxiops"]

        if "customizediops" in services:
            cmd.customizediops = services["customizediops"]

        if "offerha" in services:
            cmd.offerha = services["offerha"]

        # Service Offering private to that domain
        if domainid:
            cmd.domainid = domainid

        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return ServiceOffering(apiclient.createServiceOffering(cmd).__dict__)

    def delete(self, apiclient):
        """Delete Service offering"""
        cmd = deleteServiceOffering.deleteServiceOfferingCmd()
        cmd.id = self.id
        apiclient.deleteServiceOffering(cmd)
        return

    @classmethod
    def list(cls, apiclient, **kwargs):
        """Lists all available service offerings."""

        cmd = listServiceOfferings.listServiceOfferingsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listServiceOfferings(cmd))

