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

from marvin.lib.cloudstack.serviceoffering import ServiceOffering

service_offerings = {
        "tiny": {
            "name": "Tiny Instance",
            "displaytext": "Tiny Instance",
            "cpunumber": 1,
            "cpuspeed": 100,
            "memory": 128,
        },
        "small": {
            "name": "Small Instance",
            "displaytext": "Small Instance",
            "cpunumber": 1,
            "cpuspeed": 100,
            "memory": 256
        },
        "medium": {
            "name": "Medium Instance",
            "displaytext": "Medium Instance",
            "cpunumber": 1,
            "cpuspeed": 100,
            "memory": 256,
        },
        "big": {
            "name": "BigInstance",
            "displaytext": "BigInstance",
            "cpunumber": 1,
            "cpuspeed": 100,
            "memory": 512,
        },
        "hasmall": {
            "name": "HA Small Instance",
            "displaytext": "HA Small Instance",
            "cpunumber": 1,
            "cpuspeed": 100,
            "memory": 256,
            "hosttags": "ha",
            "offerha": True,
        },
        "taggedsmall": {
            "name": "Tagged Small Instance",
            "displaytext": "Tagged Small Instance",
            "cpunumber": 1,
            "cpuspeed": 100,
            "memory": 256,
            "hosttags": "vmsync",
        }
}
def createTinyServiceOffering(apiClient,zone):
    global service_offerings
    params = service_offerings["tiny"]
    if zone.localstorageenabled:
        params["storagetype"] = "local"

    return ServiceOffering.create(apiClient, params)


def createSmallServiceOffering(apiClient, zone):
    global service_offerings
    params = service_offerings["small"]
    if zone.localstorageenabled:
        params["storagetype"] = "local"

    return ServiceOffering.create(apiClient, params)

#and so on