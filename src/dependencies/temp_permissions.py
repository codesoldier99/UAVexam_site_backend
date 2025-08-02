from fastapi import Depends, HTTPException, status
from src.models.user import User
from src.auth.fastapi_users_config import current_active_user

def temp_permission_bypass():
    """临时的权限绕过依赖，用于测试"""
    async def bypass_dependency(user: User = Depends(current_active_user)):
        # 临时允许所有用户访问，用于测试
        return user
    return bypass_dependency

# 临时的权限依赖
temp_exam_product_read = temp_permission_bypass()
temp_exam_product_create = temp_permission_bypass()
temp_exam_product_update = temp_permission_bypass()
temp_exam_product_delete = temp_permission_bypass()

temp_venue_read = temp_permission_bypass()
temp_venue_create = temp_permission_bypass()
temp_venue_update = temp_permission_bypass()
temp_venue_delete = temp_permission_bypass()

temp_candidate_read = temp_permission_bypass()
temp_candidate_create = temp_permission_bypass()
temp_candidate_update = temp_permission_bypass()
temp_candidate_delete = temp_permission_bypass()

temp_schedule_read = temp_permission_bypass()
temp_schedule_create = temp_permission_bypass()
temp_schedule_update = temp_permission_bypass()
temp_schedule_delete = temp_permission_bypass()

temp_user_read = temp_permission_bypass()
temp_user_create = temp_permission_bypass()
temp_user_update = temp_permission_bypass()
temp_user_delete = temp_permission_bypass()

temp_role_read = temp_permission_bypass()
temp_role_create = temp_permission_bypass()
temp_role_update = temp_permission_bypass()
temp_role_delete = temp_permission_bypass()

temp_permission_read = temp_permission_bypass()
temp_permission_create = temp_permission_bypass()
temp_permission_update = temp_permission_bypass()
temp_permission_delete = temp_permission_bypass()

temp_institution_read = temp_permission_bypass()
temp_institution_create = temp_permission_bypass()
temp_institution_update = temp_permission_bypass()
temp_institution_delete = temp_permission_bypass()
