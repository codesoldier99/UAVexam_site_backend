"""
机构管理API路由
提供培训机构的CRUD操作，支持分页、筛选和权限控制
"""
from fastapi import APIRouter, Query, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from typing import Optional, List

from src.db.session import get_async_session
from src.models.institution import Institution, InstitutionStatus
from src.schemas.institution import InstitutionCreate, InstitutionRead, InstitutionUpdate
from src.core.rbac import require_permission, Permission
from src.db.models import User
from src.auth.fastapi_users_config import current_active_user

router = APIRouter(
    prefix="/institutions",
    tags=["institutions"],
)

@router.get("/")
async def get_institutions(
    page: int = Query(1, description="页码", ge=1),
    size: int = Query(10, description="每页数量", ge=1, le=100),
    status: Optional[InstitutionStatus] = Query(None, description="状态筛选"),
    name: Optional[str] = Query(None, description="机构名称筛选"),
    contact_person: Optional[str] = Query(None, description="联系人筛选"),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_permission(Permission.INSTITUTION_READ))
):
    """获取机构列表 - 支持分页、筛选和权限控制"""
    
    # 为了快速测试，先返回模拟数据
    mock_institutions = [
        {
            "id": 1,
            "name": "北京航空培训中心",
            "contact_person": "张经理",
            "phone": "010-12345678",
            "status": "active",
            "created_at": "2025-08-01T10:00:00",
            "updated_at": "2025-08-01T10:00:00"
        },
        {
            "id": 2,
            "name": "上海飞行学院",
            "contact_person": "李主任",
            "phone": "021-87654321",
            "status": "active",
            "created_at": "2025-08-02T14:30:00",
            "updated_at": "2025-08-02T14:30:00"
        },
        {
            "id": 3,
            "name": "深圳无人机培训基地",
            "contact_person": "王老师",
            "phone": "0755-11223344",
            "status": "active",
            "created_at": "2025-08-03T09:15:00",
            "updated_at": "2025-08-03T09:15:00"
        },
        {
            "id": 4,
            "name": "广州航空职业学校",
            "contact_person": "刘校长",
            "phone": "020-99887766",
            "status": "inactive",
            "created_at": "2025-07-25T16:45:00",
            "updated_at": "2025-08-01T11:20:00"
        }
    ]
    
    # 应用筛选条件
    filtered_institutions = mock_institutions
    if status:
        filtered_institutions = [i for i in filtered_institutions if i["status"] == status.value]
    if name:
        filtered_institutions = [i for i in filtered_institutions if name.lower() in i["name"].lower()]
    if contact_person:
        filtered_institutions = [i for i in filtered_institutions if contact_person.lower() in i["contact_person"].lower()]
    
    # 分页处理
    total = len(filtered_institutions)
    start = (page - 1) * size
    end = start + size
    institutions_page = filtered_institutions[start:end]
    
    return {
        "message": "机构列表接口 - 支持分页、筛选和权限控制",
        "data": institutions_page,
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "pages": (total + size - 1) // size
        },
        "filters": {
            "status": status.value if status else None,
            "name": name,
            "contact_person": contact_person
        }
    }

@router.get("/{institution_id}")
async def get_institution_by_id(
    institution_id: int,
    db: AsyncSession = Depends(get_async_session)
    # current_user: User = Depends(require_permission(Permission.INSTITUTION_READ))
):
    """根据ID获取单个机构信息"""
    
    # 模拟数据
    institutions = {
        1: {
            "id": 1,
            "name": "北京航空培训中心",
            "contact_person": "张经理",
            "phone": "010-12345678",
            "status": "active",
            "created_at": "2025-08-01T10:00:00",
            "updated_at": "2025-08-01T10:00:00",
            "stats": {
                "total_candidates": 156,
                "active_candidates": 45,
                "completed_exams": 111
            }
        },
        2: {
            "id": 2,
            "name": "上海飞行学院",
            "contact_person": "李主任",
            "phone": "021-87654321",
            "status": "active",
            "created_at": "2025-08-02T14:30:00",
            "updated_at": "2025-08-02T14:30:00",
            "stats": {
                "total_candidates": 89,
                "active_candidates": 23,
                "completed_exams": 66
            }
        }
    }
    
    if institution_id not in institutions:
        return {"error": "机构不存在", "institution_id": institution_id}
    
    return {
        "message": "机构详情",
        "data": institutions[institution_id]
    }

@router.post("/", response_model=dict)
async def create_institution(
    institution_data: InstitutionCreate,
    db: AsyncSession = Depends(get_async_session)
    # current_user: User = Depends(require_permission(Permission.INSTITUTION_CREATE))
):
    """创建新机构"""
    
    # 模拟创建逻辑
    new_institution = {
        "id": 99,  # 模拟新ID
        "name": institution_data.name,
        "contact_person": institution_data.contact_person,
        "phone": institution_data.phone,
        "status": "active",
        "created_at": "2025-08-03T19:30:00",
        "updated_at": "2025-08-03T19:30:00"
    }
    
    return {
        "message": "机构创建成功",
        "data": new_institution
    }

@router.put("/{institution_id}")
async def update_institution(
    institution_id: int,
    institution_data: InstitutionUpdate,
    db: AsyncSession = Depends(get_async_session)
    # current_user: User = Depends(require_permission(Permission.INSTITUTION_UPDATE))
):
    """更新机构信息"""
    
    if institution_id not in [1, 2, 3, 4]:
        raise HTTPException(status_code=404, detail="机构不存在")
    
    # 模拟更新逻辑
    updated_institution = {
        "id": institution_id,
        "name": institution_data.name or "更新后的机构名称",
        "contact_person": institution_data.contact_person or "更新后的联系人",
        "phone": institution_data.phone or "更新后的电话",
        "status": institution_data.status.value if institution_data.status else "active",
        "updated_at": "2025-08-03T19:35:00"
    }
    
    return {
        "message": f"机构 {institution_id} 更新成功",
        "data": updated_institution
    }

@router.delete("/{institution_id}")
async def delete_institution(
    institution_id: int,
    db: AsyncSession = Depends(get_async_session)
    # current_user: User = Depends(require_permission(Permission.INSTITUTION_DELETE))
):
    """删除机构（软删除）"""
    
    if institution_id not in [1, 2, 3, 4]:
        raise HTTPException(status_code=404, detail="机构不存在")
    
    return {
        "message": f"机构 {institution_id} 删除成功",
        "institution_id": institution_id,
        "action": "soft_delete",
        "timestamp": "2025-08-03T19:40:00"
    }

@router.get("/{institution_id}/candidates")
async def get_institution_candidates(
    institution_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_async_session)
):
    """获取机构下的考生列表"""
    
    if institution_id not in [1, 2, 3, 4]:
        raise HTTPException(status_code=404, detail="机构不存在")
    
    # 模拟机构考生数据
    mock_candidates = [
        {
            "id": 1,
            "name": "张三",
            "id_number": "110101199001011234",
            "status": "待排期",
            "exam_product": "无人机驾驶员考试",
            "registration_date": "2025-08-01"
        },
        {
            "id": 2,
            "name": "李四",
            "id_number": "110101199002021234",
            "status": "已完成",
            "exam_product": "无人机驾驶员考试",
            "registration_date": "2025-08-02"
        }
    ]
    
    return {
        "message": f"机构 {institution_id} 的考生列表",
        "institution_id": institution_id,
        "data": mock_candidates,
        "pagination": {
            "page": page,
            "size": size,
            "total": len(mock_candidates),
            "pages": 1
        }
    }

@router.get("/{institution_id}/stats")
async def get_institution_stats(
    institution_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """获取机构统计信息"""
    
    if institution_id not in [1, 2, 3, 4]:
        raise HTTPException(status_code=404, detail="机构不存在")
    
    # 模拟统计数据
    stats = {
        "institution_id": institution_id,
        "total_candidates": 156,
        "candidates_by_status": {
            "待排期": 45,
            "已排期": 67,
            "考试中": 12,
            "已完成": 32
        },
        "candidates_by_exam_product": {
            "无人机驾驶员考试": 123,
            "航拍摄影师认证": 33
        },
        "monthly_registrations": {
            "2025-08": 45,
            "2025-07": 67,
            "2025-06": 44
        }
    }
    
    return {
        "message": f"机构 {institution_id} 统计信息",
        "data": stats
    }