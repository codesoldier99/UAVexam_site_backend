from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter(
    prefix="/permissions",
    tags=["permissions"],
)

@router.get("/")
async def get_permissions(
    page: int = Query(1, description="页码", ge=1),
    size: int = Query(10, description="每页数量", ge=1, le=100),
    category: Optional[str] = Query(None, description="权限类别筛选"),
    status: Optional[str] = Query(None, description="状态筛选")
):
    """获取权限列表 - 增强版本支持分页和筛选"""
    
    # 模拟权限数据
    all_permissions = [
        {"id": 1, "name": "用户管理", "code": "user_manage", "description": "管理系统用户", "category": "user", "status": "active"},
        {"id": 2, "name": "考试管理", "code": "exam_manage", "description": "管理考试安排", "category": "exam", "status": "active"},
        {"id": 3, "name": "场地管理", "code": "venue_manage", "description": "管理考试场地", "category": "venue", "status": "active"},
        {"id": 4, "name": "考生管理", "code": "candidate_manage", "description": "管理考生信息", "category": "exam", "status": "active"},
        {"id": 5, "name": "证书颁发", "code": "certificate_issue", "description": "颁发考试证书", "category": "certificate", "status": "active"},
        {"id": 6, "name": "财务管理", "code": "finance_manage", "description": "管理财务收支", "category": "finance", "status": "active"},
        {"id": 7, "name": "系统配置", "code": "system_config", "description": "系统参数配置", "category": "system", "status": "active"},
        {"id": 8, "name": "数据导出", "code": "data_export", "description": "导出系统数据", "category": "data", "status": "inactive"}
    ]
    
    # 根据参数筛选数据
    filtered_permissions = all_permissions
    if category:
        filtered_permissions = [p for p in filtered_permissions if p["category"] == category]
    if status:
        filtered_permissions = [p for p in filtered_permissions if p["status"] == status]
    
    # 分页处理
    total = len(filtered_permissions)
    start = (page - 1) * size
    end = start + size
    permissions_page = filtered_permissions[start:end]
    
    return {
        "message": "权限列表接口 - 支持分页和筛选",
        "data": permissions_page,
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "pages": (total + size - 1) // size
        },
        "filters": {
            "category": category,
            "status": status
        }
    }

@router.get("/{permission_id}")
async def get_permission_by_id(permission_id: int):
    """根据ID获取单个权限信息"""
    permissions = {
        1: {"id": 1, "name": "用户管理", "code": "user_manage", "description": "管理系统用户", "category": "user", "status": "active"},
        2: {"id": 2, "name": "考试管理", "code": "exam_manage", "description": "管理考试安排", "category": "exam", "status": "active"},
        3: {"id": 3, "name": "场地管理", "code": "venue_manage", "description": "管理考试场地", "category": "venue", "status": "active"}
    }
    
    if permission_id not in permissions:
        return {"error": "权限不存在", "permission_id": permission_id}
    
    return {
        "message": "权限详情",
        "data": permissions[permission_id]
    }
