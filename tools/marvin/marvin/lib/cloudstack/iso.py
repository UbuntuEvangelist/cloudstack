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

from marvin.cloudstackAPI import registerIso,listOsTypes,deleteIso,listIsos,extractIso,updateIso,copyIso
import time
class Iso:
    """Manage ISO life cycle"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def create(cls, apiclient, services, account=None, domainid=None,
               projectid=None):
        """Create an ISO"""
        # Create ISO from URL
        cmd = registerIso.registerIsoCmd()
        cmd.displaytext = services["displaytext"]
        cmd.name = services["name"]
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
                "Unable to find Ostype is required for creating ISO")

        cmd.url = services["url"]
        cmd.zoneid = services["zoneid"]

        if "isextractable" in services:
            cmd.isextractable = services["isextractable"]
        if "isfeatured" in services:
            cmd.isfeatured = services["isfeatured"]
        if "ispublic" in services:
            cmd.ispublic = services["ispublic"]

        if account:
            cmd.account = account
        if domainid:
            cmd.domainid = domainid
        if projectid:
            cmd.projectid = projectid
        # Register ISO
        iso = apiclient.registerIso(cmd)

        if iso:
            return Iso(iso[0].__dict__)

    def delete(self, apiclient):
        """Delete an ISO"""
        cmd = deleteIso.deleteIsoCmd()
        cmd.id = self.id
        apiclient.deleteIso(cmd)
        return

    def download(self, apiclient, timeout=5, interval=60):
        """Download an ISO"""
        # Ensuring ISO is successfully downloaded
        while True:
            time.sleep(interval)

            cmd = listIsos.listIsosCmd()
            cmd.id = self.id
            iso_response = apiclient.listIsos(cmd)

            if isinstance(iso_response, list):
                response = iso_response[0]
                # Again initialize timeout to avoid listISO failure
                timeout = 5
                # Check whether download is in progress(for Ex:10% Downloaded)
                # or ISO is 'Successfully Installed'
                if response.status == 'Successfully Installed':
                    return
                elif 'Downloaded' not in response.status and \
                        'Installing' not in response.status:
                    raise Exception(
                        "Error In Downloading ISO: ISO Status - %s" %
                        response.status)

            elif timeout == 0:
                raise Exception("ISO download Timeout Exception")
            else:
                timeout = timeout - 1
        return

    @classmethod
    def extract(cls, apiclient, id, mode, zoneid=None):
        "Extract ISO "

        cmd = extractIso.extractIsoCmd()
        cmd.id = id
        cmd.mode = mode
        cmd.zoneid = zoneid

        return apiclient.extractIso(cmd)

    def update(self, apiclient, **kwargs):
        """Updates the ISO details"""

        cmd = updateIso.updateIsoCmd()
        cmd.id = self.id
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.updateIso(cmd))

    @classmethod
    def copy(cls, apiclient, id, sourcezoneid, destzoneid):
        "Copy ISO from source Zone to Destination Zone"

        cmd = copyIso.copyIsoCmd()
        cmd.id = id
        cmd.sourcezoneid = sourcezoneid
        cmd.destzoneid = destzoneid

        return apiclient.copyIso(cmd)

    @classmethod
    def list(cls, apiclient, **kwargs):
        """Lists all available ISO files."""

        cmd = listIsos.listIsosCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        if 'account' in kwargs.keys() and 'domainid' in kwargs.keys():
            cmd.listall = True
        return(apiclient.listIsos(cmd))
