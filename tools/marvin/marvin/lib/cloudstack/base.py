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

""" Base class for all Cloudstack resources
    -Virtual machine, Volume, Snapshot etc
"""

from marvin.cloudstackAPI import *
# Import System modules

class Hypervisor:
    """Manage Hypervisor"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """Lists hypervisors"""

        cmd = listHypervisors.listHypervisorsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listHypervisors(cmd))


class Configurations:
    """Manage Configuration"""

    @classmethod
    def update(cls, apiclient, name, value=None):
        """Updates the specified configuration"""

        cmd = updateConfiguration.updateConfigurationCmd()
        cmd.name = name
        cmd.value = value
        apiclient.updateConfiguration(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """Lists configurations"""

        cmd = listConfigurations.listConfigurationsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listConfigurations(cmd))

    @classmethod
    def listCapabilities(cls, apiclient, **kwargs):
        """Lists capabilities"""
        cmd = listCapabilities.listCapabilitiesCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.listCapabilities(cmd))



class Tag:
    """Manage tags"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, resourceIds, resourceType, tags):
        """Create tags"""

        cmd = createTags.createTagsCmd()
        cmd.resourceIds = resourceIds
        cmd.resourcetype = resourceType
        cmd.tags = []
        for key, value in tags.items():
            cmd.tags.append({
                'key': key,
                'value': value
            })
        return Tag(apiclient.createTags(cmd).__dict__)

    def delete(self, apiclient, resourceIds, resourceType, tags):
        """Delete tags"""

        cmd = deleteTags.deleteTagsCmd()
        cmd.resourceIds = resourceIds
        cmd.resourcetype = resourceType
        cmd.tags = []
        for key, value in tags.items():
            cmd.tags.append({
                'key': key,
                'value': value
            })
        apiclient.deleteTags(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List all tags matching the criteria"""

        cmd = listTags.listTagsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listTags(cmd))


class AffinityGroup:
    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, aff_grp, account=None, domainid=None):
        cmd = createAffinityGroup.createAffinityGroupCmd()
        cmd.name = aff_grp['name']
        cmd.displayText = aff_grp['name']
        cmd.type = aff_grp['type']
        if account:
            cmd.account = account
        if domainid:
            cmd.domainid = domainid
        return AffinityGroup(apiclient.createAffinityGroup(cmd).__dict__)

    def update(self, apiclient):
        pass

    def delete(self, apiclient):
        cmd = deleteAffinityGroup.deleteAffinityGroupCmd()
        cmd.id = self.id
        return apiclient.deleteAffinityGroup(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        cmd = listAffinityGroups.listAffinityGroupsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return apiclient.listAffinityGroups(cmd)




class VNMC:
    """Manage VNMC lifecycle"""
    def __init__(self, items):
        self.__dict__.update(items)

    def create(cls, apiclient, hostname, username, password,
               physicalnetworkid):
        """Registers VNMC appliance"""

        cmd = addCiscoVnmcResource.addCiscoVnmcResourceCmd()
        cmd.hostname = hostname
        cmd.username = username
        cmd.password = password
        cmd.physicalnetworkid = physicalnetworkid
        return VNMC(apiclient.addCiscoVnmcResource(cmd))

    def delete(self, apiclient):
        """Removes VNMC appliance"""

        cmd = deleteCiscoVnmcResource.deleteCiscoVnmcResourceCmd()
        cmd.resourceid = self.resourceid
        return apiclient.deleteCiscoVnmcResource(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List VNMC appliances"""

        cmd = listCiscoVnmcResources.listCiscoVnmcResourcesCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listCiscoVnmcResources(cmd))


class SSHKeyPair:
    """Manage SSH Key pairs"""

    def __init__(self, items, services):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, name=None, account=None,
               domainid=None, projectid=None):
        """Creates SSH keypair"""
        cmd = createSSHKeyPair.createSSHKeyPairCmd()
        cmd.name = name
        if account is not None:
            cmd.account = account
        if domainid is not None:
            cmd.domainid = domainid
        if projectid is not None:
            cmd.projectid = projectid
        return (apiclient.createSSHKeyPair(cmd))

    @classmethod
    def register(cls, apiclient, name, publickey):
        """Registers SSH keypair"""
        cmd = registerSSHKeyPair.registerSSHKeyPairCmd()
        cmd.name = name
        cmd.publickey = publickey
        return (apiclient.registerSSHKeyPair(cmd))

    def delete(self, apiclient):
        """Delete SSH key pair"""
        cmd = deleteSSHKeyPair.deleteSSHKeyPairCmd()
        cmd.name = self.name
        apiclient.deleteSSHKeyPair(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List all SSH key pairs"""
        cmd = listSSHKeyPairs.listSSHKeyPairsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listSSHKeyPairs(cmd))


class Capacities:
    """Manage Capacities"""

    @classmethod
    def list(cls, apiclient, **kwargs):
        """Lists capacities"""

        cmd = listCapacity.listCapacityCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listCapacity(cmd))


class Alert:
    """Manage alerts"""

    @classmethod
    def list(cls, apiclient, **kwargs):
        """Lists alerts"""

        cmd = listAlerts.listAlertsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listAlerts(cmd))


class Resources:
    """Manage resource limits"""

    def __init__(self, items, services):
        self.__dict__.update(items)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """Lists resource limits"""

        cmd = listResourceLimits.listResourceLimitsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listResourceLimits(cmd))

    @classmethod
    def updateLimit(cls, apiclient, **kwargs):
        """Updates resource limits"""

        cmd = updateResourceLimit.updateResourceLimitCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.updateResourceLimit(cmd))

    @classmethod
    def updateCount(cls, apiclient, **kwargs):
        """Updates resource count"""

        cmd = updateResourceCount.updateResourceCountCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.updateResourceCount(cmd))


class SimulatorMock:
    """Manage simulator mock lifecycle"""
    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, command, zoneid=None, podid=None,
               clusterid=None, hostid=None, value="result:fail",
               count=None, jsonresponse=None, method="GET"):
        """Creates simulator mock"""
        cmd = configureSimulator.configureSimulatorCmd()
        cmd.zoneid = zoneid
        cmd.podid = podid
        cmd.clusterid = clusterid
        cmd.hostid = hostid
        cmd.name = command
        cmd.value = value
        cmd.count = count
        cmd.jsonresponse = jsonresponse
        try:
            simulatormock = apiclient.configureSimulator(cmd, method=method)
            if simulatormock is not None:
                return SimulatorMock(simulatormock.__dict__)
        except Exception as e:
            raise e

    def delete(self, apiclient):
        """Removes simulator mock"""
        cmd = cleanupSimulatorMock.cleanupSimulatorMockCmd()
        cmd.id = self.id
        return apiclient.cleanupSimulatorMock(cmd)

    def query(self, apiclient):
        """Queries simulator mock"""
        cmd = querySimulatorMock.querySimulatorMockCmd()
        cmd.id = self.id
        try:
            simulatormock = apiclient.querySimulatorMock(cmd)
            if simulatormock is not None:
                return SimulatorMock(simulatormock.__dict__)
        except Exception as e:
            raise e


