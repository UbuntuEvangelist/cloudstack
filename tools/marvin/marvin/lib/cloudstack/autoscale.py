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

from marvin.cloudstackAPI import listCounters,createCondition,listConditions,listAutoScalePolicies,createAutoScalePolicy,updateAutoScalePolicy,listAutoScaleVmProfiles,createAutoScaleVmProfile,\
    updateAutoScaleVmProfile,createAutoScaleVmGroup,listAutoScaleVmGroups,enableAutoScaleVmGroup,disableAutoScaleVmGroup,updateAutoScaleVmGroup
class Autoscale:

    """Manage Auto scale"""

    def __init__(self, items):
        self.__dict__.update(items)

    @classmethod
    def listCounters(cls, apiclient, **kwargs):
        """Lists all available Counters."""

        cmd = listCounters.listCountersCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.listCounters(cmd))

    @classmethod
    def createCondition(cls, apiclient, counterid, relationaloperator, threshold):
        """creates condition."""

        cmd = createCondition.createConditionCmd()
        cmd.counterid = counterid
        cmd.relationaloperator = relationaloperator
        cmd.threshold = threshold
        return(apiclient.createCondition(cmd))

    @classmethod
    def listConditions(cls, apiclient, **kwargs):
        """Lists all available Conditions."""

        cmd = listConditions.listConditionsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.listConditions(cmd))

    @classmethod
    def listAutoscalePolicies(cls, apiclient, **kwargs):
        """Lists all available Autoscale Policies."""

        cmd = listAutoScalePolicies.listAutoScalePoliciesCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.listAutoScalePolicies(cmd))

    @classmethod
    def createAutoscalePolicy(cls, apiclient, action, conditionids, duration, quiettime=None):
        """creates condition."""

        cmd = createAutoScalePolicy.createAutoScalePolicyCmd()
        cmd.action = action
        cmd.conditionids = conditionids
        cmd.duration = duration
        if quiettime:
            cmd.quiettime = quiettime

        return(apiclient.createAutoScalePolicy(cmd))

    @classmethod
    def updateAutoscalePolicy(cls, apiclient, id, **kwargs):
        """Updates Autoscale Policy."""

        cmd = updateAutoScalePolicy.updateAutoScalePolicyCmd()
        cmd.id = id
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.updateAutoScalePolicy(cmd))

    @classmethod
    def listAutoscaleVmPofiles(cls, apiclient, **kwargs):
        """Lists all available AutoscaleVM  Profiles."""

        cmd = listAutoScaleVmProfiles.listAutoScaleVmProfilesCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.listAutoScaleVmProfiles(cmd))

    @classmethod
    def createAutoscaleVmProfile(cls, apiclient, serviceofferingid, zoneid, templateid,
                                 autoscaleuserid=None, destroyvmgraceperiod=None, counterparam=None):
        """creates Autoscale VM Profile."""

        cmd = createAutoScaleVmProfile.createAutoScaleVmProfileCmd()
        cmd.serviceofferingid = serviceofferingid
        cmd.zoneid = zoneid
        cmd.templateid = templateid
        if autoscaleuserid:
            cmd.autoscaleuserid = autoscaleuserid

        if destroyvmgraceperiod:
            cmd.destroyvmgraceperiod = destroyvmgraceperiod

        if counterparam:
            for name, value in counterparam.items():
                cmd.counterparam.append({
                    'name': name,
                    'value': value
                })

        return(apiclient.createAutoScaleVmProfile(cmd))

    @classmethod
    def updateAutoscaleVMProfile(cls, apiclient, id, **kwargs):
        """Updates Autoscale Policy."""

        cmd = updateAutoScaleVmProfile.updateAutoScaleVmProfileCmd()
        cmd.id = id
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.updateAutoScaleVmProfile(cmd))

    @classmethod
    def createAutoscaleVmGroup(cls, apiclient, lbruleid, minmembers, maxmembers,
                                 scaledownpolicyids, scaleuppolicyids, vmprofileid, interval=None):
        """creates Autoscale VM Group."""

        cmd = createAutoScaleVmGroup.createAutoScaleVmGroupCmd()
        cmd.lbruleid = lbruleid
        cmd.minmembers = minmembers
        cmd.maxmembers = maxmembers
        cmd.scaledownpolicyids = scaledownpolicyids
        cmd.scaleuppolicyids = scaleuppolicyids
        cmd.vmprofileid = vmprofileid
        if interval:
            cmd.interval = interval

        return(apiclient.createAutoScaleVmGroup(cmd))

    @classmethod
    def listAutoscaleVmGroup(cls, apiclient, **kwargs):
        """Lists all available AutoscaleVM  Group."""

        cmd = listAutoScaleVmGroups.listAutoScaleVmGroupsCmd()
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.listAutoScaleVmGroups(cmd))

    @classmethod
    def enableAutoscaleVmGroup(cls, apiclient, id, **kwargs):
        """Enables AutoscaleVM  Group."""

        cmd = enableAutoScaleVmGroup.enableAutoScaleVmGroupCmd()
        cmd.id = id
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.enableAutoScaleVmGroup(cmd))

    @classmethod
    def disableAutoscaleVmGroup(cls, apiclient, id, **kwargs):
        """Disables AutoscaleVM  Group."""

        cmd = disableAutoScaleVmGroup.disableAutoScaleVmGroupCmd()
        cmd.id = id
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.disableAutoScaleVmGroup(cmd))

    @classmethod
    def updateAutoscaleVMGroup(cls, apiclient, id, **kwargs):
        """Updates Autoscale VM Group."""

        cmd = updateAutoScaleVmGroup.updateAutoScaleVmGroupCmd()
        cmd.id = id
        [setattr(cmd, k, v) for k, v in kwargs.items()]
        return(apiclient.updateAutoScaleVmGroup(cmd))

