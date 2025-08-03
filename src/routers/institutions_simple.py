"""
机构管理API路由 (简化测试版)
移除认证要求，专用于功能测试
"""
from fastapi import APIRouter, Query, HTTPException, status
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

router = APIRouter(
    prefix="/institutions",
    tags=["institutions_simple"],
)

# 简化的数据模型
class InstitutionCreate(BaseModel):
    name: str
    contact_person: str
    phone: str

class InstitutionRead(BaseModel):
    id: int
    name: str
    contact_person: str
    phone: str
    status: str
    created_at: str
    updated_at: str

# 模拟数据存储
mock_institutions = {
    1: {
        "id": 1,
        "name": "北京航空培训中心",
        "contact_person": "张经理",
        "phone": "010-12345678",
        "status": "active",
        "created_at": "2025-08-01T10:00:00",
        "updated_at": "2025-08-01T10:00:00"
    },
    2: {
        "id": 2,
        "name": "上海飞行学院",
        "contact_person": "李主任",
        "phone": "021-87654321",
        "status": "active",
        "created_at": "2025-08-02T14:30:00",
        "updated_at": "2025-08-02T14:30:00"
    },
    3: {
        "id": 3,
        "name": "深圳无人机培训基地",
        "contact_person": "王老师",
        "phone": "0755-11223344",
        "status": "active",
        "created_at": "2025-08-03T09:15:00",
        "updated_at": "2025-08-03T09:15:00"
    },
    4: {
        "id": 4,
        "name": "广州航空职业学校",
        "contact_person": "刘校长",
        "phone": "020-99887766",
        "status": "inactive",
        "created_at": "2025-07-25T16:45:00",
        "updated_at": "2025-08-01T11:20:00"
    }
}

@router.get("/")
async def get_institutions(
    page: int = Query(1, description="页码", ge=1),
    size: int = Query(10, description="每页数量", ge=1, le=100),
    status: Optional[str] = Query(None, description="状态筛选"),
    name: Optional[str] = Query(None, description="机构名称筛选"),
    contact_person: Optional[str] = Query(None, description="联系人筛选")
):
    """获取机构列表 - 支持分页、筛选（简化版，无需认证）"""
    
    # 获取所有机构数据
    institutions_list = list(mock_institutions.values())
    
    # 应用筛选条件
    filtered_institutions = institutions_list
    if status:
        filtered_institutions = [i for i in filtered_institutions if i["status"] == status]
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
            "status": status,
            "name": name,
            "contact_person": contact_person
        }
    }

@router.get("/{institution_id}")
async def get_institution_by_id(institution_id: int):
    """根据ID获取单个机构信息"""
    
    institution = mock_institutions.get(institution_id)
    if not institution:
        return {"error": "机构不存在", "institution_id": institution_id}
    
    # 添加统计信息
    institution_with_stats = institution.copy()
    institution_with_stats["stats"] = {
        "total_candidates": 156 if institution_id == 1 else 89,
        "active_candidates": 45 if institution_id == 1 else 23,
        "completed_exams": 111 if institution_id == 1 else 66
    }
    
    return {
        "message": "机构详情",
        "data": institution_with_stats
    }

@router.post("/")
async def create_institution(institution_data: InstitutionCreate):
    """创建新机构"""
    
    # 检查名称是否重复
    for inst in mock_institutions.values():
        if inst["name"] == institution_data.name:
            raise HTTPException(
                status_code=400, 
                detail="机构名称已存在"
            )
    
    # 生成新ID
    new_id = max(mock_institutions.keys()) + 1 if mock_institutions else 1
    
    # 创建新机构
    new_institution = {
        "id": new_id,
        "name": institution_data.name,
        "contact_person": institution_data.contact_person,
        "phone": institution_data.phone,
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    # 保存到模拟存储
    mock_institutions[new_id] = new_institution
    
    return {
        "message": "机构创建成功",
        "data": new_institution
    }

@router.put("/{institution_id}")
async def update_institution(
    institution_id: int,
    name: Optional[str] = None,
    contact_person: Optional[str] = None,
    phone: Optional[str] = None,
    status: Optional[str] = None
):
    """更新机构信息"""
    
    if institution_id not in mock_institutions:
        raise HTTPException(status_code=404, detail="机构不存在")
    
    # 更新机构信息
    institution = mock_institutions[institution_id]
    if name:
        institution["name"] = name
    if contact_person:
        institution["contact_person"] = contact_person
    if phone:
        institution["phone"] = phone
    if status:
        institution["status"] = status
    
    institution["updated_at"] = datetime.now().isoformat()
    
    return {
        "message": f"机构 {institution_id} 更新成功",
        "data": institution
    }

@router.delete("/{institution_id}")
async def delete_institution(institution_id: int):
    """删除机构（软删除）"""
    
    if institution_id not in mock_institutions:
        raise HTTPException(status_code=404, detail="机构不存在")
    
    # 软删除：更新状态为inactive
    mock_institutions[institution_id]["status"] = "inactive"
    mock_institutions[institution_id]["updated_at"] = datetime.now().isoformat()
    
    return {
        "message": f"机构 {institution_id} 删除成功",
        "institution_id": institution_id,
        "action": "soft_delete",
        "timestamp": datetime.now().isoformat()
    }

@router.get("/{institution_id}/candidates")
async def get_institution_candidates(
    institution_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100)
):
    """获取机构下的考生列表"""
    
    if institution_id not in mock_institutions:
        raise HTTPException(status_code=404, detail="机构不存在")
    
    # 模拟机构考生数据
    candidates_by_institution = {
        1: [
            {
                "id": 1,
                "name": "张三",
                "id_number": "110101199001011234",
                "status": "待排期",
                "exam_product": "无人机驾驶员考试",
                "registration_date": "2025-08-01"
            },
            {
                "id": 3,
                "name": "王五",
                "id_number": "110101199003031234",
                "status": "待排期",
                "exam_product": "航拍摄影师认证",
                "registration_date": "2025-08-03"
            }
        ],
        2: [
            {
                "id": 2,
                "name": "李四",
                "id_number": "110101199002021234",
                "status": "已完成",
                "exam_product": "无人机驾驶员考试",
                "registration_date": "2025-08-02"
            }
        ]
    }
    
    candidates = candidates_by_institution.get(institution_id, [])
    
    return {
        "message": f"机构 {institution_id} 的考生列表",
        "institution_id": institution_id,
        "institution_name": mock_institutions[institution_id]["name"],
        "data": candidates,
        "pagination": {
            "page": page,
            "size": size,
            "total": len(candidates),
            "pages": 1
        }
    }

@router.get("/{institution_id}/stats")
async def get_institution_stats(institution_id: int):
    """获取机构统计信息"""
    
    if institution_id not in mock_institutions:
        raise HTTPException(status_code=404, detail="机构不存在")
    
    # 模拟统计数据
    stats_data = {
        1: {
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
        },
        2: {
            "total_candidates": 89,
            "candidates_by_status": {
                "待排期": 23,
                "已排期": 34,
                "考试中": 8,
                "已完成": 24
            },
            "candidates_by_exam_product": {
                "无人机驾驶员考试": 67,
                "航拍摄影师认证": 22
            },
            "monthly_registrations": {
                "2025-08": 23,
                "2025-07": 34,
                "2025-06": 32
            }
        }
    }
    
    stats = stats_data.get(institution_id, {
        "total_candidates": 0,
        "candidates_by_status": {},
        "candidates_by_exam_product": {},
        "monthly_registrations": {}
    })
    
    return {
        "message": f"机构 {institution_id} 统计信息",
        "institution_id": institution_id,
        "institution_name": mock_institutions[institution_id]["name"],
        "data": stats
    }