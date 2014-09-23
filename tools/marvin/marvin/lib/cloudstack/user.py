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
from marvin.cloudstackAPI import createUser,deleteUser,listUsers,registerUserKeys,updateUser,login
from marvin.lib.cloudstack.utils import random_gen
class User:
    """ User Life Cycle """
    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, services, account, domainid):
        cmd = createUser.createUserCmd()
        """Creates an user"""

        cmd.account = account
        cmd.domainid = domainid
        cmd.email = services["email"]
        cmd.firstname = services["firstname"]
        cmd.lastname = services["lastname"]

        if "userUUID" in services:
            cmd.userid = "-".join([services["userUUID"], random_gen()])

        cmd.password = services["password"]
        cmd.username = "-".join([services["username"], random_gen()])
        user = apiclient.createUser(cmd)

        return User(user.__dict__)

    def delete(self, apiclient):
        """Delete an account"""
        cmd = deleteUser.deleteUserCmd()
        cmd.id = self.id
        apiclient.deleteUser(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """Lists users and provides detailed account information for
        listed users"""

        cmd = listUsers.listUsersCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listUsers(cmd))

    @classmethod
    def registerUserKeys(cls, apiclient, userid):
        cmd = registerUserKeys.registerUserKeysCmd()
        cmd.id = userid
        return apiclient.registerUserKeys(cmd)

    def update(self, apiclient, **kwargs):
        """Updates the user details"""

        cmd = updateUser.updateUserCmd()
        cmd.id = self.id
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return (apiclient.updateUser(cmd))

    @classmethod
    def update(cls, apiclient, id, **kwargs):
        """Updates the user details (class method)"""

        cmd = updateUser.updateUserCmd()
        cmd.id = id
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return (apiclient.updateUser(cmd))

    @classmethod
    def login(cls, apiclient, username, password, domain=None, domainid=None):
        """Logins to the CloudStack"""

        cmd = login.loginCmd()
        cmd.username = username
        cmd.password = password
        if domain:
            cmd.domain = domain
        if domainid:
            cmd.domainId = domainid
        return apiclient.login(cmd)