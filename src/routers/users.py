from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/")
async def get_users(
    page: int = Query(1, description="页码", ge=1),
    size: int = Query(10, description="每页数量", ge=1, le=100),
    role: Optional[str] = Query(None, description="角色筛选"),
    status: Optional[str] = Query(None, description="状态筛选")
):
    """获取用户列表 - 增强版本支持分页和筛选"""
    
    # 模拟用户数据
    all_users = [
        {"id": 1, "username": "admin", "email": "admin@example.com", "role": "admin", "status": "active", "created_at": "2025-01-01"},
        {"id": 2, "username": "examiner1", "email": "examiner1@example.com", "role": "examiner", "status": "active", "created_at": "2025-01-15"},
        {"id": 3, "username": "student1", "email": "student1@example.com", "role": "student", "status": "active", "created_at": "2025-02-01"},
        {"id": 4, "username": "inactive_user", "email": "inactive@example.com", "role": "student", "status": "inactive", "created_at": "2025-01-10"},
        {"id": 5, "username": "teacher1", "email": "teacher1@example.com", "role": "teacher", "status": "active", "created_at": "2025-01-20"},
        {"id": 6, "username": "student2", "email": "student2@example.com", "role": "student", "status": "active", "created_at": "2025-02-05"}
    ]
    
    # 根据参数筛选数据
    filtered_users = all_users
    if role:
        filtered_users = [u for u in filtered_users if u["role"] == role]
    if status:
        filtered_users = [u for u in filtered_users if u["status"] == status]
    
    # 分页处理
    total = len(filtered_users)
    start = (page - 1) * size
    end = start + size
    users_page = filtered_users[start:end]
    
    return {
        "message": "用户列表接口 - 支持分页和筛选",
        "data": users_page,
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "pages": (total + size - 1) // size
        },
        "filters": {
            "role": role,
            "status": status
        }
    }

@router.get("/{user_id}")
async def get_user_by_id(user_id: int):
    """根据ID获取单个用户信息"""
    users = {
        1: {"id": 1, "username": "admin", "email": "admin@example.com", "role": "admin", "status": "active"},
        2: {"id": 2, "username": "examiner1", "email": "examiner1@example.com", "role": "examiner", "status": "active"},
        3: {"id": 3, "username": "student1", "email": "student1@example.com", "role": "student", "status": "active"}
    }
    
    if user_id not in users:
        return {"error": "用户不存在", "user_id": user_id}
    
    return {
        "message": "用户详情",
        "data": users[user_id]
    }
