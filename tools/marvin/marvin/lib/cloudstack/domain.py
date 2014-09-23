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

from marvin.cloudstackAPI import createDomain,deleteDomain,listDomains
from marvin.lib.cloudstack.utils import random_gen
class Domain:
    """ Domain Life Cycle """
    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, services, name=None, networkdomain=None,
               parentdomainid=None):
        """Creates an domain"""

        cmd = createDomain.createDomainCmd()

        if "domainUUID" in services:
            cmd.domainid = "-".join([services["domainUUID"], random_gen()])

        if name:
            cmd.name = "-".join([name, random_gen()])
        elif "name" in services:
            cmd.name = "-".join([services["name"], random_gen()])

        if networkdomain:
            cmd.networkdomain = networkdomain
        elif "networkdomain" in services:
            cmd.networkdomain = services["networkdomain"]

        if parentdomainid:
            cmd.parentdomainid = parentdomainid
        elif "parentdomainid" in services:
            cmd.parentdomainid = services["parentdomainid"]
        try:
            domain = apiclient.createDomain(cmd)
            if domain is not None:
                return Domain(domain.__dict__)
        except Exception as e:
            raise e

    def delete(self, apiclient, cleanup=None):
        """Delete an domain"""
        cmd = deleteDomain.deleteDomainCmd()
        cmd.id = self.id
        if cleanup:
            cmd.cleanup = cleanup
        apiclient.deleteDomain(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """Lists domains"""
        cmd = listDomains.listDomainsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listDomains(cmd))

