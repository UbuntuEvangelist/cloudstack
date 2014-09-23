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

class IAMGroup:
    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, iam_grp, account=None, domainid=None):
        cmd = createIAMGroup.createIAMGroupCmd()
        cmd.name = iam_grp['name']
        cmd.description = iam_grp['description']
        if account:
            cmd.account = account
        if domainid:
            cmd.domainid = domainid
        return IAMGroup(apiclient.createIAMGroup(cmd).__dict__)

    def update(self, apiclient):
        pass

    def delete(self, apiclient):
        cmd = deleteIAMGroup.deleteIAMGroupCmd()
        cmd.id = self.id
        return apiclient.deleteIAMGroup(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        cmd = listIAMGroups.listIAMGroupsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return apiclient.listIAMGroups(cmd)

    def addAccount(self, apiclient, accts):
        """Add accounts to iam group"""
        cmd = addAccountToIAMGroup.addAccountToIAMGroupCmd()
        cmd.id = self.id
        cmd.accounts = [str(acct.id) for acct in accts]
        apiclient.addAccountToIAMGroup(cmd)
        return

    def removeAccount(self, apiclient, accts):
        """ Remove accounts from iam group"""
        cmd = removeAccountFromIAMGroup.removeAccountFromIAMGroupCmd()
        cmd.id = self.id
        cmd.accounts = [str(acct.id) for acct in accts]
        apiclient.removeAccountFromIAMGroup(cmd)
        return

    def attachPolicy(self, apiclient, policies):
        """Add policies to iam group"""
        cmd = attachIAMPolicyToIAMGroup.attachIAMPolicyToIAMGroupCmd()
        cmd.id = self.id
        cmd.policies = [str(policy.id) for policy in policies]
        apiclient.attachIAMPolicyToIAMGroup(cmd)
        return

    def detachPolicy(self, apiclient, policies):
        """Remove policies from iam group"""
        cmd = removeIAMPolicyFromIAMGroup.removeIAMPolicyFromIAMGroupCmd()
        cmd.id = self.id
        cmd.policies = [str(policy.id) for policy in policies]
        apiclient.removeIAMPolicyFromIAMGroup(cmd)
        return

class IAMPolicy:
    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, iam_policy, account=None, domainid=None):
        cmd = createIAMPolicy.createIAMPolicyCmd()
        cmd.name = iam_policy['name']
        cmd.description = iam_policy['description']
        if account:
            cmd.account = account
        if domainid:
            cmd.domainid = domainid
        return IAMPolicy(apiclient.createIAMPolicy(cmd).__dict__)

    def update(self, apiclient):
        pass

    def delete(self, apiclient):
        cmd = deleteIAMPolicy.deleteIAMPolicyCmd()
        cmd.id = self.id
        return apiclient.deleteIAMPolicy(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        cmd = listIAMPolicies.listIAMPoliciesCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return apiclient.listIAMPoliciesCmd(cmd)

    def addPermission(self, apiclient, permission):
        """Add permission to iam policy"""
        cmd = addIAMPermissionToIAMPolicy.addIAMPermissionToIAMPolicyCmd()
        cmd.id = self.id
        cmd.action = permission['action']
        cmd.entitytype = permission['entitytype']
        cmd.scope = permission['scope']
        cmd.scopeid = permission['scopeid']
        apiclient.addIAMPermissionToIAMPolicy(cmd)
        return

    def removePermission(self, apiclient, permission):
        """Remove permission from iam policy"""
        cmd = removeIAMPermissionFromIAMPolicy.\
            removeIAMPermissionFromIAMPolicyCmd()
        cmd.id = self.id
        cmd.action = permission['action']
        cmd.entitytype = permission['entitytype']
        cmd.scope = permission['scope']
        cmd.scopeid = permission['scopeid']
        apiclient.removeIAMPermissionFromIAMPolicy(cmd)
        return

    def attachAccount(self, apiclient, accts):
        """Attach iam policy to accounts"""
        cmd = attachIAMPolicyToAccount.attachIAMPolicyToAccountCmd()
        cmd.id = self.id
        cmd.accounts = [str(acct.id) for acct in accts]
        apiclient.attachIAMPolicyToAccount(cmd)
        return

    def detachAccount(self, apiclient, accts):
        """Detach iam policy from accounts"""
        cmd = removeIAMPolicyFromAccount.removeIAMPolicyFromAccountCmd()
        cmd.id = self.id
        cmd.accounts = [str(acct.id) for acct in accts]
        apiclient.removeIAMPolicyFromAccount(cmd)
        return
