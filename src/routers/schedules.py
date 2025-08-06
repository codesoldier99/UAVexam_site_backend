from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional
from src.core.rbac import require_permission, Permission
from src.db.models import User

router = APIRouter(
    prefix="/schedules",
    tags=["schedules"],
)

@router.get("/")
async def get_schedules(
    page: int = Query(1, description="页码", ge=1),
    size: int = Query(10, description="每页数量", ge=1, le=100),
    status: Optional[str] = Query(None, description="状态筛选"),
    exam_type: Optional[str] = Query(None, description="考试类型筛选"),
    venue_name: Optional[str] = Query(None, description="考场筛选"),
    current_user: User = Depends(require_permission(Permission.SCHEDULE_READ))
):
    """获取考试安排列表 - 增强版本支持分页和筛选"""
    
    # 模拟考试安排数据
    all_schedules = [
        {"id": 1, "exam_product_name": "无人机驾驶员考试", "venue_name": "北京考场1", "exam_date": "2025-08-10", "exam_time": "09:00", "duration": 120, "max_candidates": 50, "status": "scheduled", "exam_type": "理论+实操"},
        {"id": 2, "exam_product_name": "航拍摄影师认证", "venue_name": "北京考场2", "exam_date": "2025-08-12", "exam_time": "14:00", "duration": 90, "max_candidates": 30, "status": "scheduled", "exam_type": "实操"},
        {"id": 3, "exam_product_name": "无人机维修技师", "venue_name": "上海考场1", "exam_date": "2025-08-15", "exam_time": "09:00", "duration": 150, "max_candidates": 40, "status": "completed", "exam_type": "理论"},
        {"id": 4, "exam_product_name": "植保飞行考试", "venue_name": "深圳考场1", "exam_date": "2025-08-18", "exam_time": "10:00", "duration": 100, "max_candidates": 35, "status": "scheduled", "exam_type": "实操"},
        {"id": 5, "exam_product_name": "消防救援飞行", "venue_name": "广州考场1", "exam_date": "2025-08-20", "exam_time": "08:30", "duration": 160, "max_candidates": 25, "status": "cancelled", "exam_type": "理论+实操"},
        {"id": 6, "exam_product_name": "无人机驾驶员考试", "venue_name": "北京考场1", "exam_date": "2025-08-22", "exam_time": "13:30", "duration": 120, "max_candidates": 50, "status": "scheduled", "exam_type": "理论+实操"}
    ]
    
    # 根据参数筛选数据
    filtered_schedules = all_schedules
    if status:
        filtered_schedules = [s for s in filtered_schedules if s["status"] == status]
    if exam_type:
        filtered_schedules = [s for s in filtered_schedules if s["exam_type"] == exam_type]
    if venue_name:
        filtered_schedules = [s for s in filtered_schedules if venue_name in s["venue_name"]]
    
    # 分页处理
    total = len(filtered_schedules)
    start = (page - 1) * size
    end = start + size
    schedules_page = filtered_schedules[start:end]
    
    return {
        "message": "考试安排列表接口 - 支持分页和筛选",
        "data": schedules_page,
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "pages": (total + size - 1) // size
        },
        "filters": {
            "status": status,
            "exam_type": exam_type,
            "venue_name": venue_name
        }
    }

@router.get("/{schedule_id}")
async def get_schedule_by_id(schedule_id: int):
    """根据ID获取单个考试安排信息"""
    schedules = {
        1: {"id": 1, "exam_product_name": "无人机驾驶员考试", "venue_name": "北京考场1", "exam_date": "2025-08-10", "exam_time": "09:00", "duration": 120, "status": "scheduled"},
        2: {"id": 2, "exam_product_name": "航拍摄影师认证", "venue_name": "北京考场2", "exam_date": "2025-08-12", "exam_time": "14:00", "duration": 90, "status": "scheduled"},
        3: {"id": 3, "exam_product_name": "无人机维修技师", "venue_name": "上海考场1", "exam_date": "2025-08-15", "exam_time": "09:00", "duration": 150, "status": "completed"}
    }
    
    if schedule_id not in schedules:
        return {"error": "考试安排不存在", "schedule_id": schedule_id}
    
    return {
        "message": "考试安排详情",
        "data": schedules[schedule_id]
    }

@router.get("/pending/candidates")
async def get_pending_candidates(
    scheduled_date: str = Query(..., description="排期日期 YYYY-MM-DD")
):
    """获取指定日期需要排期的考生列表"""
    
    # 模拟待排期考生数据
    mock_candidates = [
        {
            "id": 1,
            "name": "张三",
            "id_number": "110101199001011234",
            "phone": "13800138001",
            "status": "待排期",
            "exam_product_id": 1,
            "exam_product_name": "无人机驾驶员考试",
            "institution_id": 1,
            "institution_name": "北京航空培训中心",
            "registration_date": "2025-08-01"
        },
        {
            "id": 2,
            "name": "李四",
            "id_number": "110101199002021234",
            "phone": "13800138002",
            "status": "待排期",
            "exam_product_id": 1,
            "exam_product_name": "无人机驾驶员考试",
            "institution_id": 2,
            "institution_name": "上海飞行学院",
            "registration_date": "2025-08-02"
        },
        {
            "id": 3,
            "name": "王五",
            "id_number": "110101199003031234",
            "phone": "13800138003",
            "status": "待排期",
            "exam_product_id": 2,
            "exam_product_name": "航拍摄影师认证",
            "institution_id": 1,
            "institution_name": "北京航空培训中心",
            "registration_date": "2025-08-03"
        }
    ]
    
    return {
        "message": f"获取{scheduled_date}待排期考生成功",
        "scheduled_date": scheduled_date,
        "data": mock_candidates,
        "total": len(mock_candidates),
        "summary": {
            "total_candidates": len(mock_candidates),
            "by_exam_product": {
                "无人机驾驶员考试": 2,
                "航拍摄影师认证": 1
            },
            "by_institution": {
                "北京航空培训中心": 2,
                "上海飞行学院": 1
            }
        }
    }
