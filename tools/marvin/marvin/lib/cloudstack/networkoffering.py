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
from marvin.cloudstackAPI import createNetworkOffering,deleteNetworkOffering,updateNetworkOffering,listNetworkOfferings
from marvin.lib.cloudstack.utils import random_gen
class NetworkOffering:
    """Manage network offerings cycle"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, services, **kwargs):
        """Create network offering"""

        cmd = createNetworkOffering.createNetworkOfferingCmd()
        cmd.displaytext = "-".join([services["displaytext"], random_gen()])
        cmd.name = "-".join([services["name"], random_gen()])
        cmd.guestiptype = services["guestiptype"]
        cmd.supportedservices = ''
        if "supportedservices" in services:
            cmd.supportedservices = services["supportedservices"]
        cmd.traffictype = services["traffictype"]

        if "useVpc" in services:
            cmd.useVpc = services["useVpc"]
        cmd.serviceproviderlist = []
        if "serviceProviderList" in services:
            for service, provider in services["serviceProviderList"].items():
                cmd.serviceproviderlist.append({
                    'service': service,
                    'provider': provider
                })
        if "serviceCapabilityList" in services:
            cmd.servicecapabilitylist = []
            for service, capability in services["serviceCapabilityList"].\
                                       items():
                for ctype, value in capability.items():
                    cmd.servicecapabilitylist.append({
                        'service': service,
                        'capabilitytype': ctype,
                        'capabilityvalue': value
                    })
        if "specifyVlan" in services:
            cmd.specifyVlan = services["specifyVlan"]
        if "specifyIpRanges" in services:
            cmd.specifyIpRanges = services["specifyIpRanges"]
        if "ispersistent" in services:
            cmd.ispersistent = services["ispersistent"]
        if "egress_policy" in services:
            cmd.egressdefaultpolicy = services["egress_policy"]

        cmd.availability = 'Optional'

        [setattr(cmd, k, v) for k, v in kwargs.items()]

        return NetworkOffering(apiclient.createNetworkOffering(cmd).__dict__)

    def delete(self, apiclient):
        """Delete network offering"""
        cmd = deleteNetworkOffering.deleteNetworkOfferingCmd()
        cmd.id = self.id
        apiclient.deleteNetworkOffering(cmd)
        return

    def update(self, apiclient, **kwargs):
        """Lists all available network offerings."""

        cmd = updateNetworkOffering.updateNetworkOfferingCmd()
        cmd.id = self.id
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.updateNetworkOffering(cmd))

    @classmethod
    def list(cls, apiclient, **kwargs):
        """Lists all available network offerings."""

        cmd = listNetworkOfferings.listNetworkOfferingsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listNetworkOfferings(cmd))