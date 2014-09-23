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

import pytest

from marvin.lib.utils.zone import getCurrentZone
from marvin.lib.utils.domain import getCurrentDomain
from marvin.lib.utils.serviceoffering import createTinyServiceOffering
from marvin.lib.utils.account import createAccount
from marvin.lib.utils.template import getDefaultUservmTemplate
from marvin.lib.utils.vm import createvm
@pytest.fixture()
def test_client(request):
    if request.cls is not None:
        return request.node.cls.testClient
    else:
        return request.node.testClient

@pytest.fixture()
def api_client(test_client):
    return test_client.getApiClient()

@pytest.fixture()
def zone(api_client):
    return getCurrentZone(api_client)

@pytest.fixture()
def tiny_service_offering(api_client, zone):
    return createTinyServiceOffering(api_client,zone)

@pytest.fixture()
def domain(api_client):
    return getCurrentDomain(api_client)

@pytest.fixture()
def account(api_client, domain):
    return createAccount(api_client,domain)

@pytest.fixture()
def template(api_client):
    return getDefaultUservmTemplate(api_client)

@pytest.fixture()
def vm(api_client, request):
    vm = createvm(api_client)
    request.addfinalizer(vm.delete)
    return vm
