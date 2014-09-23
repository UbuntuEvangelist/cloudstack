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

from marvin.cloudstackAPI import createTemplate,listOsTypes,registerTemplate,extractTemplate,deleteTemplate,updateTemplatePermissions,copyTemplate,updateTemplate,listTemplates
from marvin.lib.cloudstack.utils import random_gen


class Template:
    """Manage template life cycle"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, services, volumeid=None,
               account=None, domainid=None, projectid=None):
        """Create template from Volume"""
        # Create template from Virtual machine and Volume ID
        cmd = createTemplate.createTemplateCmd()
        cmd.displaytext = services["displaytext"]
        cmd.name = "-".join([services["name"], random_gen()])
        if "ostypeid" in services:
            cmd.ostypeid = services["ostypeid"]
        elif "ostype" in services:
            # Find OSTypeId from Os type
            sub_cmd = listOsTypes.listOsTypesCmd()
            sub_cmd.description = services["ostype"]
            ostypes = apiclient.listOsTypes(sub_cmd)

            if not isinstance(ostypes, list):
                raise Exception(
                    "Unable to find Ostype id with desc: %s" %
                    services["ostype"])
            cmd.ostypeid = ostypes[0].id
        else:
            raise Exception(
                "Unable to find Ostype is required for creating template")

        cmd.isfeatured = services[
            "isfeatured"] if "isfeatured" in services else False
        cmd.ispublic = services[
            "ispublic"] if "ispublic" in services else False
        cmd.isextractable = services[
            "isextractable"] if "isextractable" in services else False
        cmd.passwordenabled = services[
            "passwordenabled"] if "passwordenabled" in services else False

        if volumeid:
            cmd.volumeid = volumeid

        if account:
            cmd.account = account

        if domainid:
            cmd.domainid = domainid

        if projectid:
            cmd.projectid = projectid
        return Template(apiclient.createTemplate(cmd).__dict__)

    @classmethod
    def register(cls, apiclient, services, zoneid=None,
                 account=None, domainid=None, hypervisor=None,
                 projectid=None):
        """Create template from URL"""

        # Create template from Virtual machine and Volume ID
        cmd = registerTemplate.registerTemplateCmd()
        cmd.displaytext = services["displaytext"]
        cmd.name = "-".join([services["name"], random_gen()])
        cmd.format = services["format"]
        if hypervisor:
            cmd.hypervisor = hypervisor
        elif "hypervisor" in services:
            cmd.hypervisor = services["hypervisor"]

        if "ostypeid" in services:
            cmd.ostypeid = services["ostypeid"]
        elif "ostype" in services:
            # Find OSTypeId from Os type
            sub_cmd = listOsTypes.listOsTypesCmd()
            sub_cmd.description = services["ostype"]
            ostypes = apiclient.listOsTypes(sub_cmd)

            if not isinstance(ostypes, list):
                raise Exception(
                    "Unable to find Ostype id with desc: %s" %
                    services["ostype"])
            cmd.ostypeid = ostypes[0].id
        else:
            raise Exception(
                "Unable to find Ostype is required for registering template")

        cmd.url = services["url"]

        if zoneid:
            cmd.zoneid = zoneid
        else:
            cmd.zoneid = services["zoneid"]

        cmd.isfeatured = services[
            "isfeatured"] if "isfeatured" in services else False
        cmd.ispublic = services[
            "ispublic"] if "ispublic" in services else False
        cmd.isextractable = services[
            "isextractable"] if "isextractable" in services else False
        cmd.passwordenabled = services[
            "passwordenabled"] if "passwordenabled" in services else False

        if account:
            cmd.account = account

        if domainid:
            cmd.domainid = domainid

        if projectid:
            cmd.projectid = projectid
        elif "projectid" in services:
            cmd.projectid = services["projectid"]

        # Register Template
        template = apiclient.registerTemplate(cmd)

        if isinstance(template, list):
            return Template(template[0].__dict__)

    @classmethod
    def extract(cls, apiclient, id, mode, zoneid=None):
        "Extract template "

        cmd = extractTemplate.extractTemplateCmd()
        cmd.id = id
        cmd.mode = mode
        cmd.zoneid = zoneid

        return apiclient.extractTemplate(cmd)

    @classmethod
    def create_from_snapshot(cls, apiclient, snapshot, services,
                             random_name=True):
        """Create Template from snapshot"""
        # Create template from Virtual machine and Snapshot ID
        cmd = createTemplate.createTemplateCmd()
        cmd.displaytext = services["displaytext"]
        cmd.name = "-".join([
            services["name"],
            random_gen()
        ]) if random_name else services["name"]

        if "ostypeid" in services:
            cmd.ostypeid = services["ostypeid"]
        elif "ostype" in services:
            # Find OSTypeId from Os type
            sub_cmd = listOsTypes.listOsTypesCmd()
            sub_cmd.description = services["ostype"]
            ostypes = apiclient.listOsTypes(sub_cmd)

            if not isinstance(ostypes, list):
                raise Exception(
                    "Unable to find Ostype id with desc: %s" %
                    services["ostype"])
            cmd.ostypeid = ostypes[0].id
        else:
            raise Exception(
                "Unable to find Ostype is required for creating template")

        cmd.snapshotid = snapshot.id
        return Template(apiclient.createTemplate(cmd).__dict__)

    def delete(self, apiclient):
        """Delete Template"""

        cmd = deleteTemplate.deleteTemplateCmd()
        cmd.id = self.id
        apiclient.deleteTemplate(cmd)

    def download(self, apiclient, timeout=5, interval=60):
        """Download Template"""
        # Sleep to ensure template is in proper state before download
        time.sleep(interval)

        while True:
            template_response = Template.list(
                apiclient,
                id=self.id,
                zoneid=self.zoneid,
                templatefilter='self'
            )
            if isinstance(template_response, list):

                template = template_response[0]
                # If template is ready,
                # template.status = Download Complete
                # Downloading - x% Downloaded
                # Error - Any other string
                if template.status == 'Download Complete':
                    break

                elif 'Downloaded' in template.status:
                    time.sleep(interval)

                elif 'Installing' not in template.status:
                    raise Exception(
                        "Error in downloading template: status - %s" %
                        template.status)

            elif timeout == 0:
                break

            else:
                time.sleep(interval)
                timeout = timeout - 1
        return

    def updatePermissions(self, apiclient, **kwargs):
        """Updates the template permissions"""

        cmd = updateTemplatePermissions.updateTemplatePermissionsCmd()
        cmd.id = self.id
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.updateTemplatePermissions(cmd))

    def update(self, apiclient, **kwargs):
        """Updates the template details"""

        cmd = updateTemplate.updateTemplateCmd()
        cmd.id = self.id
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.updateTemplate(cmd))

    @classmethod
    def copy(cls, apiclient, id, sourcezoneid, destzoneid):
        "Copy Template from source Zone to Destination Zone"

        cmd = copyTemplate.copyTemplateCmd()
        cmd.id = id
        cmd.sourcezoneid = sourcezoneid
        cmd.destzoneid = destzoneid

        return apiclient.copyTemplate(cmd)

    def copy(self, apiclient, sourcezoneid, destzoneid):
        "Copy Template from source Zone to Destination Zone"

        cmd = copyTemplate.copyTemplateCmd()
        cmd.id = self.id
        cmd.sourcezoneid = sourcezoneid
        cmd.destzoneid = destzoneid

        return apiclient.copyTemplate(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """List all templates matching criteria"""

        cmd = listTemplates.listTemplatesCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listTemplates(cmd))

