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

from marvin.cloudstackAPI import addHost,prepareHostForMaintenance,deleteHost,cancelHostMaintenance,listHosts,findHostsForMigration,updateHost
from marvin.lib.cloudstack.utils import validateList
from marvin.codes import (FAILED, PASS)
from marvin.cloudstackException import GetDetailExceptionInfo


class Host:
    """Manage Host life cycle"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, cluster, services, zoneid=None, podid=None, hypervisor=None):
        """
        1. Creates the host based upon the information provided.
        2. Verifies the output of the adding host and its state post addition
           Returns FAILED in case of an issue, else an instance of Host
        """
        try:
            cmd = addHost.addHostCmd()
            cmd.hypervisor = hypervisor
            cmd.url = services["url"]
            cmd.clusterid = cluster.id

            if zoneid:
                cmd.zoneid = zoneid
            else:
                cmd.zoneid = services["zoneid"]

            if podid:
                cmd.podid = podid
            else:
                cmd.podid = services["podid"]

            if "clustertype" in services:
                cmd.clustertype = services["clustertype"]
            if "username" in services:
                cmd.username = services["username"]
            if "password" in services:
                cmd.password = services["password"]

            '''
            Adds a Host,
            If response is valid and host is up return
            an instance of Host.
            If response is invalid, returns FAILED.
            If host state is not up, verify through listHosts call
            till host status is up and return accordingly. Max 3 retries
            '''
            host = apiclient.addHost(cmd)
            ret = validateList(host)
            if ret[0] == PASS:
                if str(host[0].state).lower() == 'up':
                    return Host(host[0].__dict__)
                retries = 3
                while retries:
                    lh_resp = apiclient.listHosts(host[0].id)
                    ret = validateList(lh_resp)
                    if (ret[0] == PASS) and \
                            (str(ret[1].state).lower() == 'up'):
                        return Host(host[0].__dict__)
                    retries += -1
            return FAILED
        except Exception as e:
            print "Exception Occurred Under Host.create : %s" % \
                  GetDetailExceptionInfo(e)
            return FAILED

    def delete(self, apiclient):
        """Delete Host"""
        # Host must be in maintenance mode before deletion
        cmd = prepareHostForMaintenance.prepareHostForMaintenanceCmd()
        cmd.id = self.id
        apiclient.prepareHostForMaintenance(cmd)
        time.sleep(30)

        cmd = deleteHost.deleteHostCmd()
        cmd.id = self.id
        apiclient.deleteHost(cmd)
        return

    def enableMaintenance(self, apiclient):
        """enables maintenance mode Host"""

        cmd = prepareHostForMaintenance.prepareHostForMaintenanceCmd()
        cmd.id = self.id
        return apiclient.prepareHostForMaintenance(cmd)

    @classmethod
    def enableMaintenance(cls, apiclient, id):
        """enables maintenance mode Host"""

        cmd = prepareHostForMaintenance.prepareHostForMaintenanceCmd()
        cmd.id = id
        return apiclient.prepareHostForMaintenance(cmd)

    def cancelMaintenance(self, apiclient):
        """Cancels maintenance mode Host"""

        cmd = cancelHostMaintenance.cancelHostMaintenanceCmd()
        cmd.id = self.id
        return apiclient.cancelHostMaintenance(cmd)

    @classmethod
    def cancelMaintenance(cls, apiclient, id):
        """Cancels maintenance mode Host"""

        cmd = cancelHostMaintenance.cancelHostMaintenanceCmd()
        cmd.id = id
        return apiclient.cancelHostMaintenance(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List all Hosts matching criteria"""

        cmd = listHosts.listHostsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listHosts(cmd))

    @classmethod
    def listForMigration(cls, apiclient, **kwargs):
        """List all Hosts for migration matching criteria"""

        cmd = findHostsForMigration.findHostsForMigrationCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.findHostsForMigration(cmd))

    @classmethod
    def update(cls, apiclient, **kwargs):
        """Update host information"""

        cmd = updateHost.updateHostCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.updateHost(cmd))

