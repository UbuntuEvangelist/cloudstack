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
import time
import base64

from marvin.codes import (FAIL, PASS, RUNNING, STOPPED,
                          STARTING, DESTROYED, EXPUNGING,
                          STOPPING)
from marvin.cloudstackException import CloudstackAPIException
from marvin.lib.cloudstack.utils import validateList, is_server_ssh_ready, random_gen
from marvin.lib.cloudstack.zone import Zone
from marvin.lib.cloudstack.network import SecurityGroup,PublicIPAddress,NATRule,FireWallRule,EgressFireWallRule
from marvin.cloudstackAPI import deployVirtualMachine,startVirtualMachine,stopVirtualMachine,rebootVirtualMachine,recoverVirtualMachine,\
    restoreVirtualMachine,resetSSHKeyForVirtualMachine,updateVirtualMachine,destroyVirtualMachine,expungeVirtualMachine,migrateVirtualMachine,\
    attachVolume,detachVolume,addNicToVirtualMachine,removeNicFromVirtualMachine,updateDefaultNicForVirtualMachine,attachIso,detachIso,scaleVirtualMachine,\
    changeServiceForVirtualMachine,listVirtualMachines,resetPasswordForVirtualMachine,assignVirtualMachine,updateVMAffinityGroup,createVMSnapshot,deleteVMSnapshot,\
    listVMSnapshot,createInstanceGroup,deleteInstanceGroup,listInstanceGroups,updateInstanceGroup,revertToVMSnapshot


class VirtualMachine:
    """Manage virtual machine lifecycle"""

    '''Class level variables'''
    # Variables denoting VM state - start
    STOPPED = STOPPED
    RUNNING = RUNNING
    DESTROYED = DESTROYED
    EXPUNGING = EXPUNGING
    STOPPING = STOPPING
    STARTING = STARTING
    # Varibles denoting VM state - end

    def __init__(self, items, services):
        self.__dict__.update(items)
        if "username" in services:
            self.username = services["username"]
        else:
            self.username = 'root'
        if "password" in services:
            self.password = services["password"]
        else:
            self.password = 'password'
        if "ssh_port" in services:
            self.ssh_port = services["ssh_port"]
        else:
            self.ssh_port = 22
        self.ssh_client = None
        # extract out the ipaddress
        self.ipaddress = self.nic[0].ipaddress

    @classmethod
    def ssh_access_group(cls, apiclient, cmd):
        """
        Programs the security group with SSH
         access before deploying virtualmachine
        @return:
        """
        zone_list = Zone.list(
            apiclient,
            id=cmd.zoneid if cmd.zoneid else None,
            domainid=cmd.domainid if cmd.domainid else None
        )
        zone = zone_list[0]
        # check if security groups settings is enabled for the zone
        if zone.securitygroupsenabled:
            list_security_groups = SecurityGroup.list(
                apiclient,
                account=cmd.account,
                domainid=cmd.domainid,
                listall=True,
                securitygroupname="basic_sec_grp"
            )

            if not isinstance(list_security_groups, list):
                basic_mode_security_group = SecurityGroup.create(
                    apiclient,
                    {"name": "basic_sec_grp"},
                    cmd.account,
                    cmd.domainid,
                )
                sec_grp_services = {
                    "protocol": "TCP",
                    "startport": 22,
                    "endport": 22,
                    "cidrlist": "0.0.0.0/0"
                }
                # Authorize security group for above ingress rule
                basic_mode_security_group.authorize(apiclient,
                                                    sec_grp_services,
                                                    account=cmd.account,
                                                    domainid=cmd.domainid)
            else:
                basic_mode_security_group = list_security_groups[0]

            if isinstance(cmd.securitygroupids, list):
                cmd.securitygroupids.append(basic_mode_security_group.id)
            else:
                cmd.securitygroupids = [basic_mode_security_group.id]

    @classmethod
    def access_ssh_over_nat(
            cls, apiclient, services, virtual_machine, allow_egress=False,
            networkid=None):
        """
        Program NAT and PF rules to open up ssh access to deployed guest
        @return:
        """
        public_ip = PublicIPAddress.create(
            apiclient=apiclient,
            accountid=virtual_machine.account,
            zoneid=virtual_machine.zoneid,
            domainid=virtual_machine.domainid,
            services=services,
            networkid=networkid
        )
        FireWallRule.create(
            apiclient=apiclient,
            ipaddressid=public_ip.ipaddress.id,
            protocol='TCP',
            cidrlist=['0.0.0.0/0'],
            startport=22,
            endport=22
        )
        nat_rule = NATRule.create(
            apiclient=apiclient,
            virtual_machine=virtual_machine,
            services=services,
            ipaddressid=public_ip.ipaddress.id
        )
        if allow_egress:
            try:
                EgressFireWallRule.create(
                    apiclient=apiclient,
                    networkid=virtual_machine.nic[0].networkid,
                    protocol='All',
                    cidrlist='0.0.0.0/0'
                )
            except CloudstackAPIException, e:
                # This could fail because we've already set up the same rule
                if not "There is already a firewall rule specified".lower() in e.errorMsg.lower():
                    raise
        virtual_machine.ssh_ip = nat_rule.ipaddress
        virtual_machine.public_ip = nat_rule.ipaddress

    @classmethod
    def create(cls, apiclient, services, templateid=None, accountid=None,
               domainid=None, zoneid=None, networkids=None,
               serviceofferingid=None, securitygroupids=None,
               projectid=None, startvm=None, diskofferingid=None,
               affinitygroupnames=None, affinitygroupids=None, group=None,
               hostid=None, keypair=None, ipaddress=None, mode='default',
               method='GET', hypervisor=None, customcpunumber=None,
               customcpuspeed=None, custommemory=None, rootdisksize=None):
        """Create the instance"""

        cmd = deployVirtualMachine.deployVirtualMachineCmd()

        if serviceofferingid:
            cmd.serviceofferingid = serviceofferingid
        elif "serviceoffering" in services:
            cmd.serviceofferingid = services["serviceoffering"]

        if zoneid:
            cmd.zoneid = zoneid
        elif "zoneid" in services:
            cmd.zoneid = services["zoneid"]

        if hypervisor:
            cmd.hypervisor = hypervisor

        if "displayname" in services:
            cmd.displayname = services["displayname"]

        if "name" in services:
            cmd.name = services["name"]

        if accountid:
            cmd.account = accountid
        elif "account" in services:
            cmd.account = services["account"]

        if domainid:
            cmd.domainid = domainid
        elif "domainid" in services:
            cmd.domainid = services["domainid"]

        if networkids:
            cmd.networkids = networkids
            allow_egress = False
        elif "networkids" in services:
            cmd.networkids = services["networkids"]
            allow_egress = False
        else:
            # When no networkids are passed, network
            # is created using the "defaultOfferingWithSourceNAT"
            # which has an egress policy of DENY. But guests in tests
            # need access to test network connectivity
            allow_egress = True

        if templateid:
            cmd.templateid = templateid
        elif "template" in services:
            cmd.templateid = services["template"]

        if diskofferingid:
            cmd.diskofferingid = diskofferingid
        elif "diskoffering" in services:
            cmd.diskofferingid = services["diskoffering"]

        if keypair:
            cmd.keypair = keypair
        elif "keypair" in services:
            cmd.keypair = services["keypair"]

        if ipaddress:
            cmd.ipaddress = ipaddress
        elif ipaddress in services:
            cmd.ipaddress = services["ipaddress"]

        if securitygroupids:
            cmd.securitygroupids = [str(sg_id) for sg_id in securitygroupids]

        if "affinitygroupnames" in services:
            cmd.affinitygroupnames = services["affinitygroupnames"]
        elif affinitygroupnames:
            cmd.affinitygroupnames = affinitygroupnames

        if affinitygroupids:
            cmd.affinitygroupids = affinitygroupids

        if projectid:
            cmd.projectid = projectid

        if startvm is not None:
            cmd.startvm = startvm

        if hostid:
            cmd.hostid = hostid

        if "userdata" in services:
            cmd.userdata = base64.urlsafe_b64encode(services["userdata"])

        cmd.details = [{}]

        if customcpunumber:
            cmd.details[0]["cpuNumber"] = customcpunumber

        if customcpuspeed:
            cmd.details[0]["cpuSpeed"] = customcpuspeed

        if custommemory:
            cmd.details[0]["memory"] = custommemory

        if rootdisksize >= 0:
            cmd.details[0]["rootdisksize"] = rootdisksize

        if group:
            cmd.group = group

        # program default access to ssh
        if mode.lower() == 'basic':
            cls.ssh_access_group(apiclient, cmd)

        virtual_machine = apiclient.deployVirtualMachine(cmd, method=method)

        virtual_machine.ssh_ip = virtual_machine.nic[0].ipaddress
        if startvm is False:
            virtual_machine.public_ip = virtual_machine.nic[0].ipaddress
            return VirtualMachine(virtual_machine.__dict__, services)

        # program ssh access over NAT via PF
        if mode.lower() == 'advanced':
            cls.access_ssh_over_nat(
                apiclient,
                services,
                virtual_machine,
                allow_egress=allow_egress,
                networkid=cmd.networkids[0] if cmd.networkids else None)
        elif mode.lower() == 'basic':
            if virtual_machine.publicip is not None:
                # EIP/ELB (netscaler) enabled zone
                vm_ssh_ip = virtual_machine.publicip
            else:
                # regular basic zone with security group
                vm_ssh_ip = virtual_machine.nic[0].ipaddress
            virtual_machine.ssh_ip = vm_ssh_ip
            virtual_machine.public_ip = vm_ssh_ip

        return VirtualMachine(virtual_machine.__dict__, services)

    def start(self, apiclient):
        """Start the instance"""
        cmd = startVirtualMachine.startVirtualMachineCmd()
        cmd.id = self.id
        apiclient.startVirtualMachine(cmd)
        response = self.getState(apiclient, VirtualMachine.RUNNING)
        if response[0] == FAIL:
            raise Exception(response[1])
        return

    def stop(self, apiclient, forced=None):
        """Stop the instance"""
        cmd = stopVirtualMachine.stopVirtualMachineCmd()
        cmd.id = self.id
        if forced:
            cmd.forced = forced
        apiclient.stopVirtualMachine(cmd)
        response = self.getState(apiclient, VirtualMachine.STOPPED)
        if response[0] == FAIL:
            raise Exception(response[1])
        return

    def reboot(self, apiclient):
        """Reboot the instance"""
        cmd = rebootVirtualMachine.rebootVirtualMachineCmd()
        cmd.id = self.id
        apiclient.rebootVirtualMachine(cmd)

    def recover(self, apiclient):
        """Recover the instance"""
        cmd = recoverVirtualMachine.recoverVirtualMachineCmd()
        cmd.id = self.id
        apiclient.recoverVirtualMachine(cmd)

    def restore(self, apiclient, templateid=None):
        """Restore the instance"""
        cmd = restoreVirtualMachine.restoreVirtualMachineCmd()
        cmd.virtualmachineid = self.id
        if templateid:
            cmd.templateid = templateid
        return apiclient.restoreVirtualMachine(cmd)

    def get_ssh_client(
            self, ipaddress=None, reconnect=False, port=None,
            keyPairFileLocation=None):
        """Get SSH object of VM"""

        # If NAT Rules are not created while VM deployment in Advanced mode
        # then, IP address must be passed
        if ipaddress is not None:
            self.ssh_ip = ipaddress
        if port:
            self.ssh_port = port

        if keyPairFileLocation is not None:
            self.password = None

        if reconnect:
            self.ssh_client = is_server_ssh_ready(
                self.ssh_ip,
                self.ssh_port,
                self.username,
                self.password,
                keyPairFileLocation=keyPairFileLocation
            )
        self.ssh_client = self.ssh_client or is_server_ssh_ready(
            self.ssh_ip,
            self.ssh_port,
            self.username,
            self.password,
            keyPairFileLocation=keyPairFileLocation
        )
        return self.ssh_client

    def getState(self, apiclient, state, timeout=600):
        """List VM and check if its state is as expected
        @returnValue - List[Result, Reason]
                       1) Result - FAIL if there is any exception
                       in the operation or VM state does not change
                       to expected state in given time else PASS
                       2) Reason - Reason for failure"""

        returnValue = [FAIL, "VM state not trasited to %s,\
                        operation timed out" % state]

        while timeout > 0:
            try:
                projectid = None
                if hasattr(self, "projectid"):
                    projectid = self.projectid
                vms = VirtualMachine.list(apiclient, projectid=projectid,
				          id=self.id, listAll=True)
                validationresult = validateList(vms)
                if validationresult[0] == FAIL:
                    raise Exception("VM list validation failed: %s" % validationresult[2])
                elif str(vms[0].state).lower().decode("string_escape") == str(state).lower():
                    returnValue = [PASS, None]
                    break
            except Exception as e:
                returnValue = [FAIL, e]
                break
            time.sleep(60)
            timeout -= 60
        return returnValue

    def resetSshKey(self, apiclient, **kwargs):
        """Resets SSH key"""

        cmd = resetSSHKeyForVirtualMachine.resetSSHKeyForVirtualMachineCmd()
        cmd.id = self.id
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.resetSSHKeyForVirtualMachine(cmd))

    def update(self, apiclient, **kwargs):
        """Updates the VM data"""

        cmd = updateVirtualMachine.updateVirtualMachineCmd()
        cmd.id = self.id
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.updateVirtualMachine(cmd))

    def delete(self, apiclient, expunge=True, **kwargs):
        """Destroy an Instance"""
        cmd = destroyVirtualMachine.destroyVirtualMachineCmd()
        cmd.id = self.id
        cmd.expunge = expunge
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        apiclient.destroyVirtualMachine(cmd)

    def expunge(self, apiclient):
        """Expunge an Instance"""
        cmd = expungeVirtualMachine.expungeVirtualMachineCmd()
        cmd.id = self.id
        apiclient.expungeVirtualMachine(cmd)

    def migrate(self, apiclient, hostid=None):
        """migrate an Instance"""
        cmd = migrateVirtualMachine.migrateVirtualMachineCmd()
        cmd.virtualmachineid = self.id
        if hostid:
            cmd.hostid = hostid
        apiclient.migrateVirtualMachine(cmd)

    def attach_volume(self, apiclient, volume):
        """Attach volume to instance"""
        cmd = attachVolume.attachVolumeCmd()
        cmd.id = volume.id
        cmd.virtualmachineid = self.id
        return apiclient.attachVolume(cmd)

    def detach_volume(self, apiclient, volume):
        """Detach volume to instance"""
        cmd = detachVolume.detachVolumeCmd()
        cmd.id = volume.id
        return apiclient.detachVolume(cmd)

    def add_nic(self, apiclient, networkId, ipaddress=None):
        """Add a NIC to a VM"""
        cmd = addNicToVirtualMachine.addNicToVirtualMachineCmd()
        cmd.virtualmachineid = self.id
        cmd.networkid = networkId

        if ipaddress:
            cmd.ipaddress = ipaddress

        return apiclient.addNicToVirtualMachine(cmd)

    def remove_nic(self, apiclient, nicId):
        """Remove a NIC to a VM"""
        cmd = removeNicFromVirtualMachine.removeNicFromVirtualMachineCmd()
        cmd.nicid = nicId
        cmd.virtualmachineid = self.id
        return apiclient.removeNicFromVirtualMachine(cmd)

    def update_default_nic(self, apiclient, nicId):
        """Set a NIC to be the default network adapter for a VM"""
        cmd = updateDefaultNicForVirtualMachine.\
            updateDefaultNicForVirtualMachineCmd()
        cmd.nicid = nicId
        cmd.virtualmachineid = self.id
        return apiclient.updateDefaultNicForVirtualMachine(cmd)

    def attach_iso(self, apiclient, iso):
        """Attach ISO to instance"""
        cmd = attachIso.attachIsoCmd()
        cmd.id = iso.id
        cmd.virtualmachineid = self.id
        return apiclient.attachIso(cmd)

    def detach_iso(self, apiclient):
        """Detach ISO to instance"""
        cmd = detachIso.detachIsoCmd()
        cmd.virtualmachineid = self.id
        return apiclient.detachIso(cmd)

    def scale_virtualmachine(self, apiclient, serviceOfferingId):
        """ Scale up of service offering for the Instance"""
        cmd = scaleVirtualMachine.scaleVirtualMachineCmd()
        cmd.id = self.id
        cmd.serviceofferingid = serviceOfferingId
        return apiclient.scaleVirtualMachine(cmd)

    def change_service_offering(self, apiclient, serviceOfferingId):
        """Change service offering of the instance"""
        cmd = changeServiceForVirtualMachine.\
            changeServiceForVirtualMachineCmd()
        cmd.id = self.id
        cmd.serviceofferingid = serviceOfferingId
        return apiclient.changeServiceForVirtualMachine(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List all VMs matching criteria"""

        cmd = listVirtualMachines.listVirtualMachinesCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listVirtualMachines(cmd))

    def resetPassword(self, apiclient):
        """Resets VM password if VM created using password enabled template"""

        cmd = resetPasswordForVirtualMachine.\
            resetPasswordForVirtualMachineCmd()
        cmd.id = self.id
        try:
            response = apiclient.resetPasswordForVirtualMachine(cmd)
        except Exception as e:
            raise Exception("Reset Password failed! - %s" % e)
        if response is not None:
            return response.password

    def assign_virtual_machine(self, apiclient, account, domainid):
        """Move a user VM to another user under same domain."""

        cmd = assignVirtualMachine.assignVirtualMachineCmd()
        cmd.virtualmachineid = self.id
        cmd.account = account
        cmd.domainid = domainid
        try:
            response = apiclient.assignVirtualMachine(cmd)
            return response
        except Exception as e:
            raise Exception("assignVirtualMachine failed - %s" % e)

    def update_affinity_group(self, apiclient, affinitygroupids=None,
                              affinitygroupnames=None):
        """Update affinity group of a VM"""
        cmd = updateVMAffinityGroup.updateVMAffinityGroupCmd()
        cmd.id = self.id

        if affinitygroupids:
            cmd.affinitygroupids = affinitygroupids

        if affinitygroupnames:
            cmd.affinitygroupnames = affinitygroupnames

        return apiclient.updateVMAffinityGroup(cmd)

    def scale(self, apiclient, serviceOfferingId,
            customcpunumber=None, customcpuspeed=None, custommemory=None):
        """Change service offering of the instance"""
        cmd = scaleVirtualMachine.scaleVirtualMachineCmd()
        cmd.id = self.id
        cmd.serviceofferingid = serviceOfferingId
        cmd.details = [{"cpuNumber": "", "cpuSpeed": "", "memory": ""}]
        if customcpunumber:
            cmd.details[0]["cpuNumber"] = customcpunumber
        if customcpuspeed:
            cmd.details[0]["cpuSpeed"] = customcpuspeed
        if custommemory:
            cmd.details[0]["memory"] = custommemory
        return apiclient.scaleVirtualMachine(cmd)


class VmSnapshot:
    """Manage VM Snapshot life cycle"""
    def __init__(self, items):
        self.__dict__.update(items)
    @classmethod
    def create(cls, apiclient, vmid, snapshotmemory="false",
               name=None, description=None):
        cmd = createVMSnapshot.createVMSnapshotCmd()
        cmd.virtualmachineid = vmid

        if snapshotmemory:
            cmd.snapshotmemory = snapshotmemory
        if name:
            cmd.name = name
        if description:
            cmd.description = description
        return VmSnapshot(apiclient.createVMSnapshot(cmd).__dict__)

    @classmethod
    def list(cls, apiclient, **kwargs):
        cmd = listVMSnapshot.listVMSnapshotCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listVMSnapshot(cmd))

    @classmethod
    def revertToSnapshot(cls, apiclient, vmsnapshotid):
        cmd = revertToVMSnapshot.revertToVMSnapshotCmd()
        cmd.vmsnapshotid = vmsnapshotid
        return apiclient.revertToVMSnapshot(cmd)

    @classmethod
    def deleteVMSnapshot(cls, apiclient, vmsnapshotid):
        cmd = deleteVMSnapshot.deleteVMSnapshotCmd()
        cmd.vmsnapshotid = vmsnapshotid
        return apiclient.deleteVMSnapshot(cmd)


class InstanceGroup:
    """Manage VM instance groups"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, name=None, account=None, domainid=None,
               projectid=None, networkid=None, rand_name=True):
        """Creates instance groups"""

        cmd = createInstanceGroup.createInstanceGroupCmd()
        cmd.name = "-".join([name, random_gen()]) if rand_name else name
        if account is not None:
            cmd.account = account
        if domainid is not None:
            cmd.domainid = domainid
        if projectid is not None:
            cmd.projectid = projectid
        if networkid is not None:
            cmd.networkid = networkid
        return InstanceGroup(apiclient.createInstanceGroup(cmd).__dict__)

    def delete(self, apiclient):
        """Delete instance group"""
        cmd = deleteInstanceGroup.deleteInstanceGroupCmd()
        cmd.id = self.id
        apiclient.deleteInstanceGroup(cmd)

    def update(self, apiclient, **kwargs):
        """Updates the instance groups"""
        cmd = updateInstanceGroup.updateInstanceGroupCmd()
        cmd.id = self.id
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return (apiclient.updateInstanceGroup(cmd))

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List all instance groups"""
        cmd = listInstanceGroups.listInstanceGroupsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return (apiclient.listInstanceGroups(cmd))

    def startInstances(self, apiclient):
        """Starts all instances in a VM tier"""

        cmd = startVirtualMachine.startVirtualMachineCmd()
        cmd.group = self.id
        return apiclient.startVirtualMachine(cmd)

    def stopInstances(self, apiclient):
        """Stops all instances in a VM tier"""

        cmd = stopVirtualMachine.stopVirtualMachineCmd()
        cmd.group = self.id
        return apiclient.stopVirtualMachine(cmd)

    def rebootInstances(self, apiclient):
        """Reboot all instances in a VM tier"""

        cmd = rebootVirtualMachine.rebootVirtualMachineCmd()
        cmd.group = self.id
        return apiclient.rebootVirtualMachine(cmd)

    def deleteInstances(self, apiclient):
        """Stops all instances in a VM tier"""

        cmd = destroyVirtualMachine.destroyVirtualMachineCmd()
        cmd.group = self.id
        return apiclient.destroyVirtualMachine(cmd)

    def changeServiceOffering(self, apiclient, serviceOfferingId):
        """Change service offering of the vm tier"""

        cmd = changeServiceForVirtualMachine.\
            changeServiceForVirtualMachineCmd()
        cmd.group = self.id
        cmd.serviceofferingid = serviceOfferingId
        return apiclient.changeServiceForVirtualMachine(cmd)

    def recoverInstances(self, apiclient):
        """Recover the instances from vm tier"""
        cmd = recoverVirtualMachine.recoverVirtualMachineCmd()
        cmd.group = self.id
        apiclient.recoverVirtualMachine(cmd)