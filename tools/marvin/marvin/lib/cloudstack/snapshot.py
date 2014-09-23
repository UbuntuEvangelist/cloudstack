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

from marvin.cloudstackAPI import createSnapshot,deleteSnapshot,listSnapshots,listSnapshotPolicies,createSnapshotPolicy,deleteSnapshotPolicies
from marvin.lib.cloudstack.utils import  validateList
from marvin.codes import BACKED_UP,BACKING_UP,FAIL,PASS


class Snapshot:
    """Manage Snapshot Lifecycle
    """
    '''Class level variables'''
    # Variables denoting possible Snapshot states - start
    BACKED_UP = BACKED_UP
    BACKING_UP = BACKING_UP
    # Variables denoting possible Snapshot states - end

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, volume_id, account=None,
               domainid=None, projectid=None):
        """Create Snapshot"""
        cmd = createSnapshot.createSnapshotCmd()
        cmd.volumeid = volume_id
        if account:
            cmd.account = account
        if domainid:
            cmd.domainid = domainid
        if projectid:
            cmd.projectid = projectid
        return Snapshot(apiclient.createSnapshot(cmd).__dict__)

    def delete(self, apiclient):
        """Delete Snapshot"""
        cmd = deleteSnapshot.deleteSnapshotCmd()
        cmd.id = self.id
        apiclient.deleteSnapshot(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List all snapshots matching criteria"""

        cmd = listSnapshots.listSnapshotsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listSnapshots(cmd))

    def validateState(self, apiclient, snapshotstate, timeout=600):
        """Check if snapshot is in required state
           returnValue: List[Result, Reason]
                 @Result: PASS if snapshot is in required state,
                          else FAIL
                 @Reason: Reason for failure in case Result is FAIL
        """
        isSnapshotInRequiredState = False
        try:
            while timeout >= 0:
                snapshots = Snapshot.list(apiclient, id=self.id)
                assert validateList(snapshots)[0] == PASS, "snapshots list\
                        validation failed"
                if str(snapshots[0].state).lower() == snapshotstate:
                    isSnapshotInRequiredState = True
                    break
                timeout -= 60
                time.sleep(60)
            #end while
            if isSnapshotInRequiredState:
                return[PASS, None]
            else:
                raise Exception("Snapshot not in required state")
        except Exception as e:
            return [FAIL, e]

class SnapshotPolicy:
    """Manage snapshot policies"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, volumeid, services):
        """Create Snapshot policy"""
        cmd = createSnapshotPolicy.createSnapshotPolicyCmd()
        cmd.intervaltype = services["intervaltype"]
        cmd.maxsnaps = services["maxsnaps"]
        cmd.schedule = services["schedule"]
        cmd.timezone = services["timezone"]
        cmd.volumeid = volumeid
        return SnapshotPolicy(apiclient.createSnapshotPolicy(cmd).__dict__)

    def delete(self, apiclient):
        """Delete Snapshot policy"""
        cmd = deleteSnapshotPolicies.deleteSnapshotPoliciesCmd()
        cmd.id = self.id
        apiclient.deleteSnapshotPolicies(cmd)
        return

    @classmethod
    def list(cls, apiclient, **kwargs):
        """Lists snapshot policies."""

        cmd = listSnapshotPolicies.listSnapshotPoliciesCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listSnapshotPolicies(cmd))
