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

from marvin.cloudstackAPI import *
from marvin.lib.cloudstack.utils import random_gen
class PublicIPAddress:
    """Manage Public IP Addresses"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, accountid=None, zoneid=None, domainid=None,
               services=None, networkid=None, projectid=None, vpcid=None,
               isportable=False):
        """Associate Public IP address"""
        cmd = associateIpAddress.associateIpAddressCmd()

        if accountid:
            cmd.account = accountid
        elif services and "account" in services:
            cmd.account = services["account"]

        if zoneid:
            cmd.zoneid = zoneid
        elif "zoneid" in services:
            cmd.zoneid = services["zoneid"]

        if domainid:
            cmd.domainid = domainid
        elif services and "domainid" in services:
            cmd.domainid = services["domainid"]

        if isportable:
            cmd.isportable = isportable

        if networkid:
            cmd.networkid = networkid

        if projectid:
            cmd.projectid = projectid

        if vpcid:
            cmd.vpcid = vpcid
        return PublicIPAddress(apiclient.associateIpAddress(cmd).__dict__)

    def delete(self, apiclient):
        """Dissociate Public IP address"""
        cmd = disassociateIpAddress.disassociateIpAddressCmd()
        cmd.id = self.ipaddress.id
        apiclient.disassociateIpAddress(cmd)
        return

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List all Public IPs matching criteria"""

        cmd = listPublicIpAddresses.listPublicIpAddressesCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listPublicIpAddresses(cmd))


class NATRule:
    """Manage port forwarding rule"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, virtual_machine, services, ipaddressid=None,
               projectid=None, openfirewall=False, networkid=None, vpcid=None,
               vmguestip=None):
        """Create Port forwarding rule"""
        cmd = createPortForwardingRule.createPortForwardingRuleCmd()

        if ipaddressid:
            cmd.ipaddressid = ipaddressid
        elif "ipaddressid" in services:
            cmd.ipaddressid = services["ipaddressid"]

        cmd.privateport = services["privateport"]
        cmd.publicport = services["publicport"]
        if "privateendport" in services:
            cmd.privateendport = services["privateendport"]
        if "publicendport" in services:
            cmd.publicendport = services["publicendport"]
        cmd.protocol = services["protocol"]
        cmd.virtualmachineid = virtual_machine.id

        if projectid:
            cmd.projectid = projectid

        if openfirewall:
            cmd.openfirewall = True

        if networkid:
            cmd.networkid = networkid

        if vpcid:
            cmd.vpcid = vpcid

        if vmguestip:
            cmd.vmguestip = vmguestip

        return NATRule(apiclient.createPortForwardingRule(cmd).__dict__)

    def delete(self, apiclient):
        """Delete port forwarding"""
        cmd = deletePortForwardingRule.deletePortForwardingRuleCmd()
        cmd.id = self.id
        apiclient.deletePortForwardingRule(cmd)
        return

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List all NAT rules matching criteria"""

        cmd = listPortForwardingRules.listPortForwardingRulesCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listPortForwardingRules(cmd))


class StaticNATRule:
    """Manage Static NAT rule"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, services, ipaddressid=None,
               networkid=None, vpcid=None):
        """Creates static ip forwarding rule"""

        cmd = createFirewallRule.createFirewallRuleCmd()
        cmd.protocol = services["protocol"]
        cmd.startport = services["startport"]

        if "endport" in services:
            cmd.endport = services["endport"]

        if "cidrlist" in services:
            cmd.cidrlist = services["cidrlist"]

        if ipaddressid:
            cmd.ipaddressid = ipaddressid
        elif "ipaddressid" in services:
            cmd.ipaddressid = services["ipaddressid"]

        if networkid:
            cmd.networkid = networkid

        if vpcid:
            cmd.vpcid = vpcid
        return StaticNATRule(apiclient.createFirewallRule(cmd).__dict__)

    @classmethod
    def createIpForwardingRule(cls, apiclient, startport, endport, protocol, ipaddressid, openfirewall):
        """Creates static ip forwarding rule"""

        cmd = createIpForwardingRule.createIpForwardingRuleCmd()
        cmd.startport = startport
        cmd.endport = endport
        cmd.protocol = protocol
        cmd.openfirewall = openfirewall
        cmd.ipaddressid = ipaddressid
        return StaticNATRule(apiclient.createIpForwardingRule(cmd).__dict__)

    def delete(self, apiclient):
        """Delete IP forwarding rule"""
        cmd = deleteIpForwardingRule.deleteIpForwardingRuleCmd()
        cmd.id = self.id
        apiclient.deleteIpForwardingRule(cmd)
        return

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List all IP forwarding rules matching criteria"""

        cmd = listIpForwardingRules.listIpForwardingRulesCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listIpForwardingRules(cmd))

    @classmethod
    def enable(cls, apiclient, ipaddressid, virtualmachineid, networkid=None,
               vmguestip=None):
        """Enables Static NAT rule"""

        cmd = enableStaticNat.enableStaticNatCmd()
        cmd.ipaddressid = ipaddressid
        cmd.virtualmachineid = virtualmachineid
        if networkid:
            cmd.networkid = networkid

        if vmguestip:
            cmd.vmguestip = vmguestip
        apiclient.enableStaticNat(cmd)
        return

    @classmethod
    def disable(cls, apiclient, ipaddressid, virtualmachineid=None):
        """Disables Static NAT rule"""

        cmd = disableStaticNat.disableStaticNatCmd()
        cmd.ipaddressid = ipaddressid
        apiclient.disableStaticNat(cmd)
        return


class EgressFireWallRule:

    """Manage Egress Firewall rule"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, networkid, protocol, cidrlist=None,
               startport=None, endport=None):
        """Create Egress Firewall Rule"""
        cmd = createEgressFirewallRule.createEgressFirewallRuleCmd()
        cmd.networkid = networkid
        cmd.protocol = protocol
        if cidrlist:
            cmd.cidrlist = cidrlist
        if startport:
            cmd.startport = startport
        if endport:
            cmd.endport = endport

        return EgressFireWallRule(
            apiclient.createEgressFirewallRule(cmd).__dict__)

    def delete(self, apiclient):
        """Delete Egress Firewall rule"""
        cmd = deleteEgressFirewallRule.deleteEgressFirewallRuleCmd()
        cmd.id = self.id
        apiclient.deleteEgressFirewallRule(cmd)
        return

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List all Egress Firewall Rules matching criteria"""

        cmd = listEgressFirewallRules.listEgressFirewallRulesCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listEgressFirewallRules(cmd))


class FireWallRule:

    """Manage Firewall rule"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, ipaddressid, protocol, cidrlist=None,
               startport=None, endport=None, projectid=None, vpcid=None):
        """Create Firewall Rule"""
        cmd = createFirewallRule.createFirewallRuleCmd()
        cmd.ipaddressid = ipaddressid
        cmd.protocol = protocol
        if cidrlist:
            cmd.cidrlist = cidrlist
        if startport:
            cmd.startport = startport
        if endport:
            cmd.endport = endport

        if projectid:
            cmd.projectid = projectid

        if vpcid:
            cmd.vpcid = vpcid

        return FireWallRule(apiclient.createFirewallRule(cmd).__dict__)

    def delete(self, apiclient):
        """Delete Firewall rule"""
        cmd = deleteFirewallRule.deleteFirewallRuleCmd()
        cmd.id = self.id
        apiclient.deleteFirewallRule(cmd)
        return

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List all Firewall Rules matching criteria"""

        cmd = listFirewallRules.listFirewallRulesCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listFirewallRules(cmd))

class LoadBalancerRule:
    """Manage Load Balancer rule"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, services, ipaddressid=None, accountid=None,
               networkid=None, vpcid=None, projectid=None, domainid=None):
        """Create Load balancing Rule"""

        cmd = createLoadBalancerRule.createLoadBalancerRuleCmd()

        if ipaddressid:
            cmd.publicipid = ipaddressid
        elif "ipaddressid" in services:
            cmd.publicipid = services["ipaddressid"]

        if accountid:
            cmd.account = accountid
        elif "account" in services:
            cmd.account = services["account"]

        if domainid:
            cmd.domainid = domainid

        if vpcid:
            cmd.vpcid = vpcid
        cmd.name = services["name"]
        cmd.algorithm = services["alg"]
        cmd.privateport = services["privateport"]
        cmd.publicport = services["publicport"]

        if "openfirewall" in services:
            cmd.openfirewall = services["openfirewall"]

        if projectid:
            cmd.projectid = projectid

        if networkid:
            cmd.networkid = networkid
        return LoadBalancerRule(apiclient.createLoadBalancerRule(cmd).__dict__)

    def delete(self, apiclient):
        """Delete load balancing rule"""
        cmd = deleteLoadBalancerRule.deleteLoadBalancerRuleCmd()
        cmd.id = self.id
        apiclient.deleteLoadBalancerRule(cmd)
        return

    def assign(self, apiclient, vms=None, vmidipmap=None):
        """Assign virtual machines to load balancing rule"""
        cmd = assignToLoadBalancerRule.assignToLoadBalancerRuleCmd()
        cmd.id = self.id
        if vmidipmap:
            cmd.vmidipmap = vmidipmap
        if vms:
            cmd.virtualmachineids = [str(vm.id) for vm in vms]
        apiclient.assignToLoadBalancerRule(cmd)
        return

    def remove(self, apiclient, vms=None, vmidipmap=None):
        """Remove virtual machines from load balancing rule"""
        cmd = removeFromLoadBalancerRule.removeFromLoadBalancerRuleCmd()
        cmd.id = self.id
        if vms:
            cmd.virtualmachineids = [str(vm.id) for vm in vms]
        if vmidipmap:
            cmd.vmidipmap = vmidipmap
        apiclient.removeFromLoadBalancerRule(cmd)
        return

    def update(self, apiclient, algorithm=None,
               description=None, name=None, **kwargs):
        """Updates the load balancing rule"""
        cmd = updateLoadBalancerRule.updateLoadBalancerRuleCmd()
        cmd.id = self.id
        if algorithm:
            cmd.algorithm = algorithm
        if description:
            cmd.description = description
        if name:
            cmd.name = name

        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return apiclient.updateLoadBalancerRule(cmd)

    def createSticky(
            self, apiclient, methodname, name, description=None, param=None):
        """Creates a sticky policy for the LB rule"""

        cmd = createLBStickinessPolicy.createLBStickinessPolicyCmd()
        cmd.lbruleid = self.id
        cmd.methodname = methodname
        cmd.name = name
        if description:
            cmd.description = description
        if param:
            cmd.param = []
            for name, value in param.items():
                cmd.param.append({'name': name, 'value': value})
        return apiclient.createLBStickinessPolicy(cmd)

    def deleteSticky(self, apiclient, id):
        """Deletes stickyness policy"""

        cmd = deleteLBStickinessPolicy.deleteLBStickinessPolicyCmd()
        cmd.id = id
        return apiclient.deleteLBStickinessPolicy(cmd)

    @classmethod
    def listStickyPolicies(cls, apiclient, lbruleid, **kwargs):
        """Lists stickiness policies for load balancing rule"""

        cmd = listLBStickinessPolicies.listLBStickinessPoliciesCmd()
        cmd.lbruleid = lbruleid
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return apiclient.listLBStickinessPolicies(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List all Load balancing rules matching criteria"""

        cmd = listLoadBalancerRules.listLoadBalancerRulesCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listLoadBalancerRules(cmd))

    @classmethod
    def listLoadBalancerRuleInstances(cls, apiclient, id, lbvmips=False, applied=None, **kwargs):
        """Lists load balancing rule Instances"""

        cmd = listLoadBalancerRuleInstances.listLoadBalancerRuleInstancesCmd()
        cmd.id = id
        if applied:
            cmd.applied = applied
        cmd.lbvmips = lbvmips

        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return apiclient.listLoadBalancerRuleInstances(cmd)


class Network:
    """Manage Network pools"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, services, accountid=None, domainid=None,
               networkofferingid=None, projectid=None,
               subdomainaccess=None, zoneid=None,
               gateway=None, netmask=None, vpcid=None, aclid=None, vlan=None):
        """Create Network for account"""
        cmd = createNetwork.createNetworkCmd()
        cmd.name = services["name"]
        cmd.displaytext = services["displaytext"]

        if networkofferingid:
            cmd.networkofferingid = networkofferingid
        elif "networkoffering" in services:
            cmd.networkofferingid = services["networkoffering"]

        if zoneid:
            cmd.zoneid = zoneid
        elif "zoneid" in services:
            cmd.zoneid = services["zoneid"]

        if subdomainaccess is not None:
            cmd.subdomainaccess = subdomainaccess

        if gateway:
            cmd.gateway = gateway
        elif "gateway" in services:
            cmd.gateway = services["gateway"]
        if netmask:
            cmd.netmask = netmask
        elif "netmask" in services:
            cmd.netmask = services["netmask"]
        if "startip" in services:
            cmd.startip = services["startip"]
        if "endip" in services:
            cmd.endip = services["endip"]
        if vlan:
            cmd.vlan = vlan
        elif "vlan" in services:
            cmd.vlan = services["vlan"]
        if "acltype" in services:
            cmd.acltype = services["acltype"]

        if accountid:
            cmd.account = accountid
        if domainid:
            cmd.domainid = domainid
        if projectid:
            cmd.projectid = projectid
        if vpcid:
            cmd.vpcid = vpcid
        if aclid:
            cmd.aclid = aclid
        return Network(apiclient.createNetwork(cmd).__dict__)

    def delete(self, apiclient):
        """Delete Account"""

        cmd = deleteNetwork.deleteNetworkCmd()
        cmd.id = self.id
        apiclient.deleteNetwork(cmd)

    def update(self, apiclient, **kwargs):
        """Updates network with parameters passed"""

        cmd = updateNetwork.updateNetworkCmd()
        cmd.id = self.id
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.updateNetwork(cmd))

    def restart(self, apiclient, cleanup=None):
        """Restarts the network"""

        cmd = restartNetwork.restartNetworkCmd()
        cmd.id = self.id
        if cleanup:
            cmd.cleanup = cleanup
        return(apiclient.restartNetwork(cmd))

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List all Networks matching criteria"""

        cmd = listNetworks.listNetworksCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listNetworks(cmd))


class NetworkACL:
    """Manage Network ACL lifecycle"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, services, networkid=None, protocol=None,
               number=None, aclid=None, action='Allow',
               traffictype=None, cidrlist=[]):
        """Create network ACL rules(Ingress/Egress)"""

        cmd = createNetworkACL.createNetworkACLCmd()
        if "networkid" in services:
            cmd.networkid = services["networkid"]
        elif networkid:
            cmd.networkid = networkid

        if "protocol" in services:
            cmd.protocol = services["protocol"]
            if services["protocol"] == 'ICMP':
                cmd.icmptype = -1
                cmd.icmpcode = -1
        elif protocol:
            cmd.protocol = protocol

        if "startport" in services:
            cmd.startport = services["startport"]
        if "endport" in services:
            cmd.endport = services["endport"]

        if "cidrlist" in services:
            cmd.cidrlist = services["cidrlist"]
        elif cidrlist:
            cmd.cidrlist = cidrlist

        if "traffictype" in services:
            cmd.traffictype = services["traffictype"]
        elif traffictype:
            cmd.traffictype = traffictype

        if "action" in services:
            cmd.action = services["action"]
        elif action:
            cmd.action = action

        if "number" in services:
            cmd.number = services["number"]
        elif number:
            cmd.number = number

        if "aclid" in services:
            cmd.aclid = services["aclid"]
        elif aclid:
            cmd.aclid = aclid

        # Defaulted to Ingress
        return NetworkACL(apiclient.createNetworkACL(cmd).__dict__)

    def delete(self, apiclient):
        """Delete network acl"""

        cmd = deleteNetworkACL.deleteNetworkACLCmd()
        cmd.id = self.id
        return apiclient.deleteNetworkACL(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List Network ACLs"""

        cmd = listNetworkACLs.listNetworkACLsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listNetworkACLs(cmd))


class NetworkACLList:
    """Manage Network ACL lists lifecycle"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(
            cls, apiclient, services, name=None, description=None, vpcid=None):
        """Create network ACL container list"""

        cmd = createNetworkACLList.createNetworkACLListCmd()
        if "name" in services:
            cmd.name = services["name"]
        elif name:
            cmd.name = name

        if "description" in services:
            cmd.description = services["description"]
        elif description:
            cmd.description = description

        if "vpcid" in services:
            cmd.vpcid = services["vpcid"]
        elif vpcid:
            cmd.vpcid = vpcid

        return NetworkACLList(apiclient.createNetworkACLList(cmd).__dict__)

    def delete(self, apiclient):
        """Delete network acl list"""

        cmd = deleteNetworkACLList.deleteNetworkACLListCmd()
        cmd.id = self.id
        return apiclient.deleteNetworkACLList(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List Network ACL lists"""

        cmd = listNetworkACLLists.listNetworkACLListsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listNetworkACLLists(cmd))


class Vpn:
    """Manage VPN life cycle"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, publicipid, account=None, domainid=None,
               projectid=None, networkid=None, vpcid=None, openfirewall=None):
        """Create VPN for Public IP address"""
        cmd = createRemoteAccessVpn.createRemoteAccessVpnCmd()
        cmd.publicipid = publicipid
        if account:
            cmd.account = account
        if domainid:
            cmd.domainid = domainid
        if projectid:
            cmd.projectid = projectid
        if networkid:
            cmd.networkid = networkid
        if vpcid:
            cmd.vpcid = vpcid
        if openfirewall:
            cmd.openfirewall = openfirewall
        return Vpn(apiclient.createRemoteAccessVpn(cmd).__dict__)

    @classmethod
    def createVpnGateway(cls, apiclient, vpcid):
        """Create VPN Gateway """
        cmd = createVpnGateway.createVpnGatewayCmd()
        cmd.vpcid = vpcid
        return (apiclient.createVpnGateway(cmd).__dict__)

    @classmethod
    def createVpnConnection(cls, apiclient, s2scustomergatewayid, s2svpngatewayid):
        """Create VPN Connection """
        cmd = createVpnConnection.createVpnConnectionCmd()
        cmd.s2scustomergatewayid = s2scustomergatewayid
        cmd.s2svpngatewayid = s2svpngatewayid
        return (apiclient.createVpnGateway(cmd).__dict__)

    @classmethod
    def resetVpnConnection(cls, apiclient, id):
        """Reset VPN Connection """
        cmd = resetVpnConnection.resetVpnConnectionCmd()
        cmd.id = id
        return (apiclient.resetVpnConnection(cmd).__dict__)

    @classmethod
    def deleteVpnConnection(cls, apiclient, id):
        """Delete VPN Connection """
        cmd = deleteVpnConnection.deleteVpnConnectionCmd()
        cmd.id = id
        return (apiclient.deleteVpnConnection(cmd).__dict__)

    @classmethod
    def listVpnGateway(cls, apiclient, **kwargs):
        """List all VPN Gateways matching criteria"""
        cmd = listVpnGateways.listVpnGatewaysCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.listVpnGateways(cmd))

    @classmethod
    def listVpnConnection(cls, apiclient, **kwargs):
        """List all VPN Connections matching criteria"""
        cmd = listVpnConnections.listVpnConnectionsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.listVpnConnections(cmd))

    def delete(self, apiclient):
        """Delete remote VPN access"""

        cmd = deleteRemoteAccessVpn.deleteRemoteAccessVpnCmd()
        cmd.publicipid = self.publicipid
        apiclient.deleteRemoteAccessVpn(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List all VPN matching criteria"""

        cmd = listRemoteAccessVpns.listRemoteAccessVpnsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listRemoteAccessVpns(cmd))


class VpnUser:
    """Manage VPN user"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, username, password, account=None, domainid=None,
               projectid=None, rand_name=True):
        """Create VPN user"""
        cmd = addVpnUser.addVpnUserCmd()
        cmd.username = "-".join([username,
                                 random_gen()]) if rand_name else username
        cmd.password = password

        if account:
            cmd.account = account
        if domainid:
            cmd.domainid = domainid
        if projectid:
            cmd.projectid = projectid
        return VpnUser(apiclient.addVpnUser(cmd).__dict__)

    def delete(self, apiclient, projectid=None):
        """Remove VPN user"""

        cmd = removeVpnUser.removeVpnUserCmd()
        cmd.username = self.username
        if projectid:
            cmd.projectid = projectid
        else:
            cmd.account = self.account
            cmd.domainid = self.domainid
        apiclient.removeVpnUser(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List all VPN Users matching criteria"""

        cmd = listVpnUsers.listVpnUsersCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listVpnUsers(cmd))

class PublicIpRange:
    """Manage VlanIpRange"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, services):
        """Create VlanIpRange"""

        cmd = createVlanIpRange.createVlanIpRangeCmd()
        cmd.gateway = services["gateway"]
        cmd.netmask = services["netmask"]
        cmd.forvirtualnetwork = services["forvirtualnetwork"]
        cmd.startip = services["startip"]
        cmd.endip = services["endip"]
        cmd.zoneid = services["zoneid"]
        if "podid" in services:
            cmd.podid = services["podid"]
        cmd.vlan = services["vlan"]

        return PublicIpRange(apiclient.createVlanIpRange(cmd).__dict__)

    def delete(self, apiclient):
        """Delete VlanIpRange"""

        cmd = deleteVlanIpRange.deleteVlanIpRangeCmd()
        cmd.id = self.vlan.id
        apiclient.deleteVlanIpRange(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """Lists all VLAN IP ranges."""

        cmd = listVlanIpRanges.listVlanIpRangesCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listVlanIpRanges(cmd))

    @classmethod
    def dedicate(
            cls, apiclient, id, account=None, domainid=None, projectid=None):
        """Dedicate VLAN IP range"""

        cmd = dedicatePublicIpRange.dedicatePublicIpRangeCmd()
        cmd.id = id
        cmd.account = account
        cmd.domainid = domainid
        cmd.projectid = projectid
        return PublicIpRange(apiclient.dedicatePublicIpRange(cmd).__dict__)

    def release(self, apiclient):
        """Release VLAN IP range"""

        cmd = releasePublicIpRange.releasePublicIpRangeCmd()
        cmd.id = self.vlan.id
        return apiclient.releasePublicIpRange(cmd)


class PortablePublicIpRange:
    """Manage portable public Ip Range"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, services):
        """Create portable public Ip Range"""

        cmd = createPortableIpRange.createPortableIpRangeCmd()
        cmd.gateway = services["gateway"]
        cmd.netmask = services["netmask"]
        cmd.startip = services["startip"]
        cmd.endip = services["endip"]
        cmd.regionid = services["regionid"]

        if "vlan" in services:
            cmd.vlan = services["vlan"]

        return PortablePublicIpRange(
            apiclient.createPortableIpRange(cmd).__dict__)

    def delete(self, apiclient):
        """Delete portable IpRange"""

        cmd = deletePortableIpRange.deletePortableIpRangeCmd()
        cmd.id = self.id
        apiclient.deletePortableIpRange(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """Lists all portable public IP ranges."""

        cmd = listPortableIpRanges.listPortableIpRangesCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listPortableIpRanges(cmd))

class PhysicalNetwork:
    """Manage physical network storage"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, services, zoneid, domainid=None):
        """Create physical network"""
        cmd = createPhysicalNetwork.createPhysicalNetworkCmd()

        cmd.name = services["name"]
        cmd.zoneid = zoneid
        if domainid:
            cmd.domainid = domainid
        return PhysicalNetwork(apiclient.createPhysicalNetwork(cmd).__dict__)

    def delete(self, apiclient):
        """Delete Physical Network"""

        cmd = deletePhysicalNetwork.deletePhysicalNetworkCmd()
        cmd.id = self.id
        apiclient.deletePhysicalNetwork(cmd)

    def update(self, apiclient, **kwargs):
        """Update Physical network state"""

        cmd = updatePhysicalNetwork.updatePhysicalNetworkCmd()
        cmd.id = self.id
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return apiclient.updatePhysicalNetwork(cmd)

    def addTrafficType(self, apiclient, type):
        """Add Traffic type to Physical network"""

        cmd = addTrafficType.addTrafficTypeCmd()
        cmd.physicalnetworkid = self.id
        cmd.traffictype = type
        return apiclient.addTrafficType(cmd)

    @classmethod
    def dedicate(cls, apiclient, vlanrange, physicalnetworkid,
                 account=None, domainid=None, projectid=None):
        """Dedicate guest vlan range"""

        cmd = dedicateGuestVlanRange.dedicateGuestVlanRangeCmd()
        cmd.vlanrange = vlanrange
        cmd.physicalnetworkid = physicalnetworkid
        cmd.account = account
        cmd.domainid = domainid
        cmd.projectid = projectid
        return PhysicalNetwork(apiclient.dedicateGuestVlanRange(cmd).__dict__)

    def release(self, apiclient):
        """Release guest vlan range"""

        cmd = releaseDedicatedGuestVlanRange.\
            releaseDedicatedGuestVlanRangeCmd()
        cmd.id = self.id
        return apiclient.releaseDedicatedGuestVlanRange(cmd)

    @classmethod
    def listDedicated(cls, apiclient, **kwargs):
        """Lists all dedicated guest vlan ranges"""

        cmd = listDedicatedGuestVlanRanges.listDedicatedGuestVlanRangesCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return apiclient.listDedicatedGuestVlanRanges(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """Lists all physical networks"""

        cmd = listPhysicalNetworks.listPhysicalNetworksCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return map(lambda pn: PhysicalNetwork(
            pn.__dict__), apiclient.listPhysicalNetworks(cmd))


class SecurityGroup:
    """Manage Security Groups"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, services, account=None, domainid=None,
               description=None, projectid=None):
        """Create security group"""
        cmd = createSecurityGroup.createSecurityGroupCmd()

        cmd.name = "-".join([services["name"], random_gen()])
        if account:
            cmd.account = account
        if domainid:
            cmd.domainid = domainid
        if description:
            cmd.description = description
        if projectid:
            cmd.projectid = projectid

        return SecurityGroup(apiclient.createSecurityGroup(cmd).__dict__)

    def delete(self, apiclient):
        """Delete Security Group"""

        cmd = deleteSecurityGroup.deleteSecurityGroupCmd()
        cmd.id = self.id
        apiclient.deleteSecurityGroup(cmd)

    def authorize(self, apiclient, services,
                  account=None, domainid=None, projectid=None):
        """Authorize Ingress Rule"""

        cmd = authorizeSecurityGroupIngress.authorizeSecurityGroupIngressCmd()

        if domainid:
            cmd.domainid = domainid
        if account:
            cmd.account = account

        if projectid:
            cmd.projectid = projectid
        cmd.securitygroupid = self.id
        cmd.protocol = services["protocol"]

        if services["protocol"] == 'ICMP':
            cmd.icmptype = -1
            cmd.icmpcode = -1
        else:
            cmd.startport = services["startport"]
            cmd.endport = services["endport"]

        cmd.cidrlist = services["cidrlist"]
        return (apiclient.authorizeSecurityGroupIngress(cmd).__dict__)

    def revoke(self, apiclient, id):
        """Revoke ingress rule"""

        cmd = revokeSecurityGroupIngress.revokeSecurityGroupIngressCmd()
        cmd.id = id
        return apiclient.revokeSecurityGroupIngress(cmd)

    def authorizeEgress(self, apiclient, services, account=None, domainid=None,
                        projectid=None, user_secgrp_list={}):
        """Authorize Egress Rule"""

        cmd = authorizeSecurityGroupEgress.authorizeSecurityGroupEgressCmd()

        if domainid:
            cmd.domainid = domainid
        if account:
            cmd.account = account

        if projectid:
            cmd.projectid = projectid
        cmd.securitygroupid = self.id
        cmd.protocol = services["protocol"]

        if services["protocol"] == 'ICMP':
            cmd.icmptype = -1
            cmd.icmpcode = -1
        else:
            cmd.startport = services["startport"]
            cmd.endport = services["endport"]

        cmd.cidrlist = services["cidrlist"]

        cmd.usersecuritygrouplist = []
        for account, group in user_secgrp_list.items():
            cmd.usersecuritygrouplist.append({
                'account': account,
                'group': group
            })

        return (apiclient.authorizeSecurityGroupEgress(cmd).__dict__)

    def revokeEgress(self, apiclient, id):
        """Revoke Egress rule"""

        cmd = revokeSecurityGroupEgress.revokeSecurityGroupEgressCmd()
        cmd.id = id
        return apiclient.revokeSecurityGroupEgress(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """Lists all security groups."""

        cmd = listSecurityGroups.listSecurityGroupsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listSecurityGroups(cmd))


class VpnCustomerGateway:
    """Manage VPN Customer Gateway"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, services, name, gateway, cidrlist,
               account=None, domainid=None):
        """Create VPN Customer Gateway"""
        cmd = createVpnCustomerGateway.createVpnCustomerGatewayCmd()
        cmd.name = name
        cmd.gateway = gateway
        cmd.cidrlist = cidrlist
        if "ipsecpsk" in services:
            cmd.ipsecpsk = services["ipsecpsk"]
        if "ikepolicy" in services:
            cmd.ikepolicy = services["ikepolicy"]
        if "ikelifetime" in services:
            cmd.ikelifetime = services["ikelifetime"]
        if "esppolicy" in services:
            cmd.esppolicy = services["esppolicy"]
        if "esplifetime" in services:
            cmd.esplifetime = services["esplifetime"]
        if "dpd" in services:
            cmd.dpd = services["dpd"]
        if account:
            cmd.account = account
        if domainid:
            cmd.domainid = domainid
        return VpnCustomerGateway(
            apiclient.createVpnCustomerGateway(cmd).__dict__)

    def update(self, apiclient, services, name, gateway, cidrlist):
        """Updates VPN Customer Gateway"""

        cmd = updateVpnCustomerGateway.updateVpnCustomerGatewayCmd()
        cmd.id = self.id
        cmd.name = name
        cmd.gateway = gateway
        cmd.cidrlist = cidrlist
        if "ipsecpsk" in services:
            cmd.ipsecpsk = services["ipsecpsk"]
        if "ikepolicy" in services:
            cmd.ikepolicy = services["ikepolicy"]
        if "ikelifetime" in services:
            cmd.ikelifetime = services["ikelifetime"]
        if "esppolicy" in services:
            cmd.esppolicy = services["esppolicy"]
        if "esplifetime" in services:
            cmd.esplifetime = services["esplifetime"]
        if "dpd" in services:
            cmd.dpd = services["dpd"]
        return(apiclient.updateVpnCustomerGateway(cmd))

    def delete(self, apiclient):
        """Delete VPN Customer Gateway"""

        cmd = deleteVpnCustomerGateway.deleteVpnCustomerGatewayCmd()
        cmd.id = self.id
        apiclient.deleteVpnCustomerGateway(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List all VPN customer Gateway"""

        cmd = listVpnCustomerGateways.listVpnCustomerGatewaysCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listVpnCustomerGateways(cmd))

class NetScaler:
    """Manage external netscaler device"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def add(cls, apiclient, services, physicalnetworkid,
            username=None, password=None):
        """Add external netscaler device to cloudstack"""

        cmd = addNetscalerLoadBalancer.addNetscalerLoadBalancerCmd()
        cmd.physicalnetworkid = physicalnetworkid
        if username:
            cmd.username = username
        else:
            cmd.username = services["username"]

        if password:
            cmd.password = password
        else:
            cmd.password = services["password"]

        cmd.networkdevicetype = services["networkdevicetype"]

        # Generate the URL
        url = 'https://' + str(services["ipaddress"]) + '?'
        url = url + 'publicinterface=' + str(services["publicinterface"]) + '&'
        url = url + 'privateinterface=' + \
            str(services["privateinterface"]) + '&'
        url = url + 'numretries=' + str(services["numretries"]) + '&'

        if not services["lbdevicededicated"] and \
           "lbdevicecapacity" in services:
            url = url + 'lbdevicecapacity=' + \
                str(services["lbdevicecapacity"]) + '&'

        url = url + 'lbdevicededicated=' + str(services["lbdevicededicated"])

        cmd.url = url
        return NetScaler(apiclient.addNetscalerLoadBalancer(cmd).__dict__)

    def delete(self, apiclient):
        """Deletes a netscaler device from CloudStack"""

        cmd = deleteNetscalerLoadBalancer.deleteNetscalerLoadBalancerCmd()
        cmd.lbdeviceid = self.lbdeviceid
        apiclient.deleteNetscalerLoadBalancer(cmd)
        return

    def configure(self, apiclient, **kwargs):
        """List already registered netscaler devices"""

        cmd = configureNetscalerLoadBalancer.\
            configureNetscalerLoadBalancerCmd()
        cmd.lbdeviceid = self.lbdeviceid
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.configureNetscalerLoadBalancer(cmd))

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List already registered netscaler devices"""

        cmd = listNetscalerLoadBalancers.listNetscalerLoadBalancersCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listNetscalerLoadBalancers(cmd))


class NetworkServiceProvider:
    """Manage network serivce providers for CloudStack"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def add(cls, apiclient, name, physicalnetworkid, servicelist):
        """Adds network service provider"""

        cmd = addNetworkServiceProvider.addNetworkServiceProviderCmd()
        cmd.name = name
        cmd.physicalnetworkid = physicalnetworkid
        cmd.servicelist = servicelist
        return NetworkServiceProvider(
            apiclient.addNetworkServiceProvider(cmd).__dict__)

    def delete(self, apiclient):
        """Deletes network service provider"""

        cmd = deleteNetworkServiceProvider.deleteNetworkServiceProviderCmd()
        cmd.id = self.id
        return apiclient.deleteNetworkServiceProvider(cmd)

    def update(self, apiclient, **kwargs):
        """Updates network service provider"""

        cmd = updateNetworkServiceProvider.updateNetworkServiceProviderCmd()
        cmd.id = self.id
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return apiclient.updateNetworkServiceProvider(cmd)

    @classmethod
    def update(cls, apiclient, id, **kwargs):
        """Updates network service provider"""

        cmd = updateNetworkServiceProvider.updateNetworkServiceProviderCmd()
        cmd.id = id
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return apiclient.updateNetworkServiceProvider(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List network service providers"""

        cmd = listNetworkServiceProviders.listNetworkServiceProvidersCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listNetworkServiceProviders(cmd))


class Router:
    """Manage router life cycle"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def start(cls, apiclient, id):
        """Starts the router"""
        cmd = startRouter.startRouterCmd()
        cmd.id = id
        return apiclient.startRouter(cmd)

    @classmethod
    def stop(cls, apiclient, id, forced=None):
        """Stops the router"""
        cmd = stopRouter.stopRouterCmd()
        cmd.id = id
        if forced:
            cmd.forced = forced
        return apiclient.stopRouter(cmd)

    @classmethod
    def reboot(cls, apiclient, id):
        """Reboots the router"""
        cmd = rebootRouter.rebootRouterCmd()
        cmd.id = id
        return apiclient.rebootRouter(cmd)

    @classmethod
    def destroy(cls, apiclient, id):
        """Destroy the router"""
        cmd = destroyRouter.destroyRouterCmd()
        cmd.id = id
        return apiclient.destroyRouter(cmd)

    @classmethod
    def change_service_offering(cls, apiclient, id, serviceofferingid):
        """Change service offering of the router"""
        cmd = changeServiceForRouter.changeServiceForRouterCmd()
        cmd.id = id
        cmd.serviceofferingid = serviceofferingid
        return apiclient.changeServiceForRouter(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List routers"""

        cmd = listRouters.listRoutersCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listRouters(cmd))


class VpcOffering:
    """Manage VPC offerings"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, services):
        """Create vpc offering"""

        cmd = createVPCOffering.createVPCOfferingCmd()
        cmd.name = "-".join([services["name"], random_gen()])
        cmd.displaytext = services["displaytext"]
        cmd.supportedServices = services["supportedservices"]
        if "serviceProviderList" in services:
            for service, provider in services["serviceProviderList"].items():
                cmd.serviceproviderlist.append({
                    'service': service,
                    'provider': provider
                })
        if "serviceCapabilityList" in services:
            cmd.servicecapabilitylist = []
            for service, capability in \
                services["serviceCapabilityList"].items():
                for ctype, value in capability.items():
                    cmd.servicecapabilitylist.append({
                        'service': service,
                        'capabilitytype': ctype,
                        'capabilityvalue': value
                    })
        return VpcOffering(apiclient.createVPCOffering(cmd).__dict__)

    def update(self, apiclient, name=None, displaytext=None, state=None):
        """Updates existing VPC offering"""

        cmd = updateVPCOffering.updateVPCOfferingCmd()
        cmd.id = self.id
        if name:
            cmd.name = name
        if displaytext:
            cmd.displaytext = displaytext
        if state:
            cmd.state = state
        return apiclient.updateVPCOffering(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List the VPC offerings based on criteria specified"""

        cmd = listVPCOfferings.listVPCOfferingsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listVPCOfferings(cmd))

    def delete(self, apiclient):
        """Deletes existing VPC offering"""

        cmd = deleteVPCOffering.deleteVPCOfferingCmd()
        cmd.id = self.id
        return apiclient.deleteVPCOffering(cmd)


class VPC:
    """Manage Virtual Private Connection"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, services, vpcofferingid,
               zoneid, networkDomain=None, account=None,
               domainid=None, **kwargs):
        """Creates the virtual private connection (VPC)"""

        cmd = createVPC.createVPCCmd()
        cmd.name = "-".join([services["name"], random_gen()])
        cmd.displaytext = "-".join([services["displaytext"], random_gen()])
        cmd.vpcofferingid = vpcofferingid
        cmd.zoneid = zoneid
        if "cidr" in services:
            cmd.cidr = services["cidr"]
        if account:
            cmd.account = account
        if domainid:
            cmd.domainid = domainid
        if networkDomain:
            cmd.networkDomain = networkDomain
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return VPC(apiclient.createVPC(cmd).__dict__)

    def update(self, apiclient, name=None, displaytext=None):
        """Updates VPC configurations"""

        cmd = updateVPC.updateVPCCmd()
        cmd.id = self.id
        if name:
            cmd.name = name
        if displaytext:
            cmd.displaytext = displaytext
        return (apiclient.updateVPC(cmd))

    def delete(self, apiclient):
        """Delete VPC network"""

        cmd = deleteVPC.deleteVPCCmd()
        cmd.id = self.id
        return apiclient.deleteVPC(cmd)

    def restart(self, apiclient):
        """Restarts the VPC connections"""

        cmd = restartVPC.restartVPCCmd()
        cmd.id = self.id
        return apiclient.restartVPC(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List VPCs"""

        cmd = listVPCs.listVPCsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listVPCs(cmd))

class PrivateGateway:
    """Manage private gateway lifecycle"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, gateway, ipaddress, netmask, vlan, vpcid,
               physicalnetworkid=None, aclid=None):
        """Create private gateway"""

        cmd = createPrivateGateway.createPrivateGatewayCmd()
        cmd.gateway = gateway
        cmd.ipaddress = ipaddress
        cmd.netmask = netmask
        cmd.vlan = vlan
        cmd.vpcid = vpcid
        if physicalnetworkid:
            cmd.physicalnetworkid = physicalnetworkid
        if aclid:
            cmd.aclid = aclid

        return PrivateGateway(apiclient.createPrivateGateway(cmd).__dict__)

    def delete(self, apiclient):
        """Delete private gateway"""

        cmd = deletePrivateGateway.deletePrivateGatewayCmd()
        cmd.id = self.id
        return apiclient.deletePrivateGateway(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List private gateways"""

        cmd = listPrivateGateways.listPrivateGatewaysCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listPrivateGateways(cmd))


class StaticRoute:
    """Manage static route lifecycle"""
    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, cidr, gatewayid):
        """Create static route"""

        cmd = createStaticRoute.createStaticRouteCmd()
        cmd.cidr = cidr
        cmd.gatewayid = gatewayid
        return StaticRoute(apiclient.createStaticRoute(cmd).__dict__)

    def delete(self, apiclient):
        """Delete static route"""

        cmd = deleteStaticRoute.deleteStaticRouteCmd()
        cmd.id = self.id
        return apiclient.deleteStaticRoute(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List static route"""

        cmd = listStaticRoutes.listStaticRoutesCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listStaticRoutes(cmd))

class ASA1000V:
    """Manage ASA 1000v lifecycle"""
    def create(cls, apiclient, hostname, insideportprofile,
               clusterid, physicalnetworkid):
        """Registers ASA 1000v appliance"""

        cmd = addCiscoAsa1000vResource.addCiscoAsa1000vResourceCmd()
        cmd.hostname = hostname
        cmd.insideportprofile = insideportprofile
        cmd.clusterid = clusterid
        cmd.physicalnetworkid = physicalnetworkid
        return ASA1000V(apiclient.addCiscoAsa1000vResource(cmd))

    def delete(self, apiclient):
        """Removes ASA 1000v appliance"""

        cmd = deleteCiscoAsa1000vResource.deleteCiscoAsa1000vResourceCmd()
        cmd.resourceid = self.resourceid
        return apiclient.deleteCiscoAsa1000vResource(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List ASA 1000v appliances"""

        cmd = listCiscoAsa1000vResources.listCiscoAsa1000vResourcesCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listCiscoAsa1000vResources(cmd))

class ApplicationLoadBalancer:
    """Manage Application Load Balancers in VPC"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, services, name=None, sourceport=None,
               instanceport=22, algorithm="roundrobin", scheme="internal",
               sourcenetworkid=None, networkid=None):
        """Create Application Load Balancer"""
        cmd = createLoadBalancer.createLoadBalancerCmd()

        if "name" in services:
            cmd.name = services["name"]
        elif name:
            cmd.name = name

        if "sourceport" in services:
            cmd.sourceport = services["sourceport"]
        elif sourceport:
            cmd.sourceport = sourceport

        if "instanceport" in services:
            cmd.instanceport = services["instanceport"]
        elif instanceport:
            cmd.instanceport = instanceport

        if "algorithm" in services:
            cmd.algorithm = services["algorithm"]
        elif algorithm:
            cmd.algorithm = algorithm

        if "scheme" in services:
            cmd.scheme = services["scheme"]
        elif scheme:
            cmd.scheme = scheme

        if "sourceipaddressnetworkid" in services:
            cmd.sourceipaddressnetworkid = services["sourceipaddressnetworkid"]
        elif sourcenetworkid:
            cmd.sourceipaddressnetworkid = sourcenetworkid

        if "networkid" in services:
            cmd.networkid = services["networkid"]
        elif networkid:
            cmd.networkid = networkid

        return LoadBalancerRule(apiclient.createLoadBalancer(cmd).__dict__)

    def delete(self, apiclient):
        """Delete application load balancer"""
        cmd = deleteLoadBalancer.deleteLoadBalancerCmd()
        cmd.id = self.id
        apiclient.deleteLoadBalancerRule(cmd)
        return

    def assign(self, apiclient, vms=None, vmidipmap=None):
        """Assign virtual machines to load balancing rule"""
        cmd = assignToLoadBalancerRule.assignToLoadBalancerRuleCmd()
        cmd.id = self.id
        if vmidipmap:
            cmd.vmidipmap = vmidipmap
        if vms:
            cmd.virtualmachineids = [str(vm.id) for vm in vms]
        apiclient.assignToLoadBalancerRule(cmd)
        return

    def remove(self, apiclient, vms=None, vmidipmap=None):
        """Remove virtual machines from load balancing rule"""
        cmd = removeFromLoadBalancerRule.removeFromLoadBalancerRuleCmd()
        cmd.id = self.id
        if vms:
            cmd.virtualmachineids = [str(vm.id) for vm in vms]
        if vmidipmap:
            cmd.vmidipmap = vmidipmap
        apiclient.removeFromLoadBalancerRule(cmd)
        return

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List all appln load balancers"""
        cmd = listLoadBalancers.listLoadBalancersCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listLoadBalancerRules(cmd))


class NIC:
    """NIC related API"""
    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def addIp(cls, apiclient, id, ipaddress=None):
        """Add Ip (secondary) to NIC"""
        cmd = addIpToNic.addIpToNicCmd()
        cmd.nicid = id
        if ipaddress:
            cmd.ipaddress = ipaddress
        return(apiclient.addIpToNic(cmd))

    @classmethod
    def removeIp(cls, apiclient, ipaddressid):
        """Remove secondary Ip from NIC"""
        cmd = removeIpFromNic.removeIpFromNicCmd()
        cmd.id = ipaddressid
        return(apiclient.addIpToNic(cmd))

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List NICs belonging to a virtual machine"""

        cmd = listNics.listNicsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listNics(cmd))
