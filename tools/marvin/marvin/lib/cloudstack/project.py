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

from marvin.cloudstackAPI import createProject,deleteProject,updateProject,activateProject,suspendProject,addAccountToProject,deleteAccountFromProject,listProjectAccounts,\
    listProjects,listProjectInvitations,updateProjectInvitation,deleteProjectInvitation
from marvin.lib.cloudstack.utils import random_gen
class Project:
    """Manage Project life cycle"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, services, account=None, domainid=None):
        """Create project"""

        cmd = createProject.createProjectCmd()
        cmd.displaytext = services["displaytext"]
        cmd.name = "-".join([services["name"], random_gen()])
        if account:
            cmd.account = account
        if domainid:
            cmd.domainid = domainid

        return Project(apiclient.createProject(cmd).__dict__)

    def delete(self, apiclient):
        """Delete Project"""

        cmd = deleteProject.deleteProjectCmd()
        cmd.id = self.id
        apiclient.deleteProject(cmd)

    def update(self, apiclient, **kwargs):
        """Updates the project"""

        cmd = updateProject.updateProjectCmd()
        cmd.id = self.id
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return apiclient.updateProject(cmd)

    def activate(self, apiclient):
        """Activates the suspended project"""

        cmd = activateProject.activateProjectCmd()
        cmd.id = self.id
        return apiclient.activateProject(cmd)

    def suspend(self, apiclient):
        """Suspend the active project"""

        cmd = suspendProject.suspendProjectCmd()
        cmd.id = self.id
        return apiclient.suspendProject(cmd)

    def addAccount(self, apiclient, account=None, email=None):
        """Add account to project"""

        cmd = addAccountToProject.addAccountToProjectCmd()
        cmd.projectid = self.id
        if account:
            cmd.account = account
        if email:
            cmd.email = email
        return apiclient.addAccountToProject(cmd)

    def deleteAccount(self, apiclient, account):
        """Delete account from project"""

        cmd = deleteAccountFromProject.deleteAccountFromProjectCmd()
        cmd.projectid = self.id
        cmd.account = account
        return apiclient.deleteAccountFromProject(cmd)

    @classmethod
    def listAccounts(cls, apiclient, **kwargs):
        """Lists all accounts associated with projects."""

        cmd = listProjectAccounts.listProjectAccountsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listProjectAccounts(cmd))

    @classmethod
    def list(cls, apiclient, **kwargs):
        """Lists all projects."""

        cmd = listProjects.listProjectsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listProjects(cmd))


class ProjectInvitation:
    """Manage project invitations"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def update(cls, apiclient, projectid, accept, account=None, token=None):
        """Updates the project invitation for that account"""

        cmd = updateProjectInvitation.updateProjectInvitationCmd()
        cmd.projectid = projectid
        cmd.accept = accept
        if account:
            cmd.account = account
        if token:
            cmd.token = token

        return (apiclient.updateProjectInvitation(cmd).__dict__)

    def delete(self, apiclient, id):
        """Deletes the project invitation"""

        cmd = deleteProjectInvitation.deleteProjectInvitationCmd()
        cmd.id = id
        return apiclient.deleteProjectInvitation(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """Lists project invitations"""

        cmd = listProjectInvitations.listProjectInvitationsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listProjectInvitations(cmd))

