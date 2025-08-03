from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
)

@router.get("/")
async def get_roles(
    page: int = Query(1, description="页码", ge=1),
    size: int = Query(10, description="每页数量", ge=1, le=100),
    status: Optional[str] = Query(None, description="状态筛选"),
    level: Optional[str] = Query(None, description="权限级别筛选")
):
    """获取角色列表 - 增强版本支持分页和筛选"""
    
    # 模拟角色数据
    all_roles = [
        {"id": 1, "name": "超级管理员", "description": "系统超级管理员", "permissions": ["all"], "status": "active", "level": "high", "user_count": 2},
        {"id": 2, "name": "考官", "description": "考试监考官", "permissions": ["exam_manage", "candidate_manage"], "status": "active", "level": "medium", "user_count": 15},
        {"id": 3, "name": "培训师", "description": "培训课程讲师", "permissions": ["course_manage", "student_manage"], "status": "active", "level": "medium", "user_count": 8},
        {"id": 4, "name": "学员", "description": "普通学员用户", "permissions": ["view_courses", "take_exam"], "status": "active", "level": "low", "user_count": 150},
        {"id": 5, "name": "审核员", "description": "资质审核专员", "permissions": ["audit_manage", "certificate_issue"], "status": "active", "level": "medium", "user_count": 5},
        {"id": 6, "name": "访客", "description": "临时访问用户", "permissions": ["view_public"], "status": "inactive", "level": "low", "user_count": 0}
    ]
    
    # 根据参数筛选数据
    filtered_roles = all_roles
    if status:
        filtered_roles = [r for r in filtered_roles if r["status"] == status]
    if level:
        filtered_roles = [r for r in filtered_roles if r["level"] == level]
    
    # 分页处理
    total = len(filtered_roles)
    start = (page - 1) * size
    end = start + size
    roles_page = filtered_roles[start:end]
    
    return {
        "message": "角色列表接口 - 支持分页和筛选",
        "data": roles_page,
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "pages": (total + size - 1) // size
        },
        "filters": {
            "status": status,
            "level": level
        }
    }

@router.get("/{role_id}")
async def get_role_by_id(role_id: int):
    """根据ID获取单个角色信息"""
    roles = {
        1: {"id": 1, "name": "超级管理员", "description": "系统超级管理员", "permissions": ["all"], "status": "active"},
        2: {"id": 2, "name": "考官", "description": "考试监考官", "permissions": ["exam_manage", "candidate_manage"], "status": "active"},
        3: {"id": 3, "name": "培训师", "description": "培训课程讲师", "permissions": ["course_manage", "student_manage"], "status": "active"}
    }
    
    if role_id not in roles:
        return {"error": "角色不存在", "role_id": role_id}
    
    return {
        "message": "角色详情",
        "data": roles[role_id]
    }
