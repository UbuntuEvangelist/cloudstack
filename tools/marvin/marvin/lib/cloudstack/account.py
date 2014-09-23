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


from marvin.cloudstackAPI import createAccount,deleteAccount,listAccounts,disableAccount

from marvin.lib.cloudstack.utils import random_gen

class Account:
    """ Account Life Cycle """
    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, services, admin=False, domainid=None):
        """Creates an account"""
        cmd = createAccount.createAccountCmd()

        # 0 - User, 1 - Root Admin, 2 - Domain Admin
        cmd.accounttype = 2 if (admin and domainid) else int(admin)

        cmd.email = services["email"]
        cmd.firstname = services["firstname"]
        cmd.lastname = services["lastname"]

        cmd.password = services["password"]
        username = services["username"]
        # Limit account username to 99 chars to avoid failure
        # 6 chars start string + 85 chars apiclientid + 6 chars random string + 2 chars joining hyphen string = 99
        username = username[:6]
        apiclientid = apiclient.id[-85:] if len(apiclient.id) > 85 else apiclient.id
        cmd.username = "-".join([username,
                             random_gen(id=apiclientid, size=6)])

        if "accountUUID" in services:
            cmd.accountid = "-".join([services["accountUUID"], random_gen()])

        if "userUUID" in services:
            cmd.userid = "-".join([services["userUUID"], random_gen()])


        if domainid:
            cmd.domainid = domainid
        account = apiclient.createAccount(cmd)

        return Account(account.__dict__)

    def delete(self, apiclient):
        """Delete an account"""
        cmd = deleteAccount.deleteAccountCmd()
        cmd.id = self.id
        apiclient.deleteAccount(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """Lists accounts and provides detailed account information for
        listed accounts"""

        cmd = listAccounts.listAccountsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listAccounts(cmd))

    def disable(self, apiclient, lock=False):
        """Disable an account"""
        cmd = disableAccount.disableAccountCmd()
        cmd.id = self.id
        cmd.lock = lock
        apiclient.disableAccount(cmd)

