// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.
package org.apache.cloudstack.iam.server.dao;
import java.util.List;

import org.apache.cloudstack.iam.api.IAMPolicyPermission.Permission;
import org.apache.cloudstack.iam.server.IAMPolicyPermissionVO;

import com.cloud.utils.db.GenericDao;

public interface IAMPolicyPermissionDao extends GenericDao<IAMPolicyPermissionVO, Long> {

    List<IAMPolicyPermissionVO> listByPolicy(long policyId);

    IAMPolicyPermissionVO findByPolicyAndEntity(long policyId, String entityType, String scope, Long scopeId,
            String action, Permission perm);

    List<IAMPolicyPermissionVO> listGrantedByActionAndScope(long policyId, String action, String scope);

    List<IAMPolicyPermissionVO> listByPolicyActionAndEntity(long policyId, String action, String entityType);

    List<IAMPolicyPermissionVO> listByPolicyAccessAndEntity(long policyId, String accessType, String entityType);

    List<IAMPolicyPermissionVO> listByEntity(String entityType, Long entityId);
}