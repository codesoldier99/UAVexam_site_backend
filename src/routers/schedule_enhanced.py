"""
增强版排期管理API路由
支持考务排期、批量操作、时间线展示等功能
"""
from fastapi import APIRouter, Query, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from datetime import date, time, datetime
from pydantic import BaseModel

from src.db.session import get_async_session
from src.core.rbac import require_permission, Permission
from src.services.schedule_management import schedule_management_service
from src.db.models import User
from src.auth.fastapi_users_config import current_active_user

router = APIRouter(
    prefix="/schedules/enhanced",
    tags=["schedule_management"],
)

# ===== 请求模型 =====

class BatchScheduleRequest(BaseModel):
    candidate_ids: List[int]
    exam_type: str  # "theory" 或 "practical"
    venue_id: int
    start_date: date
    start_time: time

class ScheduleUpdateRequest(BaseModel):
    status: Optional[str] = None
    venue_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    notes: Optional[str] = None

# ===== 排期管理接口 =====

@router.get("/pending-candidates")
async def get_pending_candidates(
    exam_date: date = Query(..., description="考试日期"),
    institution_id: Optional[int] = Query(None, description="机构ID筛选"),
    exam_product_id: Optional[int] = Query(None, description="考试产品ID筛选"),
    status: str = Query("待排期", description="考生状态"),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_permission(Permission.SCHEDULE_READ))
):
    """获取待排期考生列表"""
    
    # 机构用户只能查看自己机构的考生
    if current_user.institution_id:
        institution_id = current_user.institution_id
    
    candidates = await schedule_management_service.get_pending_candidates(
        db, exam_date, institution_id, exam_product_id, status
    )
    
    # 按机构分组
    grouped_candidates = await schedule_management_service.group_candidates_by_institution(candidates)
    
    return {
        "message": "待排期考生列表",
        "exam_date": exam_date.isoformat(),
        "total_candidates": len(candidates),
        "grouped_by_institution": grouped_candidates,
        "flat_list": candidates
    }

@router.post("/batch-schedule")
async def create_batch_schedule(
    schedule_request: BatchScheduleRequest,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_permission(Permission.SCHEDULE_BATCH_MANAGE))
):
    """批量创建排期"""
    
    result = await schedule_management_service.create_batch_schedule(
        db=db,
        candidate_ids=schedule_request.candidate_ids,
        exam_type=schedule_request.exam_type,
        venue_id=schedule_request.venue_id,
        start_date=schedule_request.start_date,
        start_time=schedule_request.start_time,
        current_user=current_user
    )
    
    return result

@router.get("/timeline")
async def get_schedule_timeline(
    start_date: date = Query(..., description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    venue_id: Optional[int] = Query(None, description="场地ID筛选"),
    institution_id: Optional[int] = Query(None, description="机构ID筛选"),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_permission(Permission.SCHEDULE_READ))
):
    """获取排期时间线"""
    
    # 机构用户只能查看自己机构的排期
    if current_user.institution_id:
        institution_id = current_user.institution_id
    
    timeline = await schedule_management_service.get_schedule_timeline(
        db, start_date, end_date, venue_id, institution_id
    )
    
    return {
        "message": "排期时间线",
        **timeline
    }

@router.get("/venues/available")
async def get_available_venues(
    venue_type: str = Query(..., description="场地类型"),
    start_time: datetime = Query(..., description="开始时间"),
    end_time: datetime = Query(..., description="结束时间"),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_permission(Permission.SCHEDULE_CREATE))
):
    """获取指定时间段可用的场地"""
    
    venues = await schedule_management_service.get_available_venues(
        db, venue_type, start_time, end_time
    )
    
    return {
        "message": "可用场地列表",
        "venue_type": venue_type,
        "time_range": {
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        },
        "available_venues": venues
    }

@router.put("/{schedule_id}")
async def update_schedule(
    schedule_id: int,
    update_request: ScheduleUpdateRequest,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_permission(Permission.SCHEDULE_UPDATE))
):
    """更新排期信息"""
    
    from src.models.schedule import Schedule
    from sqlalchemy import select, and_
    
    # 构建查询条件
    query = select(Schedule).where(Schedule.id == schedule_id)
    
    # 机构用户权限检查（通过考生机构验证）
    if current_user.institution_id:
        from src.models.candidate import Candidate
        query = query.join(Candidate).where(Candidate.institution_id == current_user.institution_id)
    
    result = await db.execute(query)
    schedule = result.scalar_one_or_none()
    
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="排期记录不存在或无权访问"
        )
    
    # 更新字段
    for field, value in update_request.model_dump(exclude_unset=True).items():
        setattr(schedule, field, value)
    
    schedule.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(schedule)
    
    return {
        "message": "排期更新成功",
        "schedule_id": schedule.id,
        "updated_fields": list(update_request.model_dump(exclude_unset=True).keys())
    }

@router.delete("/{schedule_id}")
async def cancel_schedule(
    schedule_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_permission(Permission.SCHEDULE_DELETE))
):
    """取消排期"""
    
    from src.models.schedule import Schedule
    from src.models.candidate import Candidate
    from sqlalchemy import select
    
    # 构建查询条件
    query = select(Schedule).where(Schedule.id == schedule_id)
    
    # 机构用户权限检查
    if current_user.institution_id:
        query = query.join(Candidate).where(Candidate.institution_id == current_user.institution_id)
    
    result = await db.execute(query)
    schedule = result.scalar_one_or_none()
    
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="排期记录不存在或无权访问"
        )
    
    # 检查是否已签到
    if schedule.check_in_status == "checked_in":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="已签到的排期无法取消"
        )
    
    # 更新考生状态
    candidate_result = await db.execute(
        select(Candidate).where(Candidate.id == schedule.candidate_id)
    )
    candidate = candidate_result.scalar_one_or_none()
    if candidate:
        candidate.status = "待排期"
    
    # 删除排期记录
    await db.delete(schedule)
    await db.commit()
    
    return {
        "message": "排期取消成功",
        "schedule_id": schedule_id,
        "candidate_status_updated": "待排期"
    }

# ===== 统计和分析接口 =====

@router.get("/statistics/daily")
async def get_daily_statistics(
    target_date: date = Query(..., description="目标日期"),
    institution_id: Optional[int] = Query(None, description="机构ID筛选"),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_permission(Permission.SCHEDULE_READ))
):
    """获取每日排期统计"""
    
    from src.models.schedule import Schedule
    from src.models.candidate import Candidate
    from src.models.venue import Venue
    from sqlalchemy import select, func, and_
    
    # 机构用户只能查看自己机构的统计
    if current_user.institution_id:
        institution_id = current_user.institution_id
    
    # 构建基础查询
    base_query = select(Schedule).where(Schedule.scheduled_date == target_date)
    
    if institution_id:
        base_query = base_query.join(Candidate).where(Candidate.institution_id == institution_id)
    
    # 总排期数
    total_result = await db.execute(base_query)
    total_schedules = len(total_result.scalars().all())
    
    # 按类型统计
    theory_result = await db.execute(
        base_query.where(Schedule.schedule_type == "theory")
    )
    theory_count = len(theory_result.scalars().all())
    
    practical_result = await db.execute(
        base_query.where(Schedule.schedule_type == "practical")
    )
    practical_count = len(practical_result.scalars().all())
    
    # 按状态统计
    status_stats = {}
    for status_value in ["待确认", "confirmed", "completed", "cancelled"]:
        status_result = await db.execute(
            base_query.where(Schedule.status == status_value)
        )
        status_stats[status_value] = len(status_result.scalars().all())
    
    # 按签到状态统计
    checkin_stats = {}
    for checkin_status in ["not_checked_in", "checked_in", "late"]:
        checkin_result = await db.execute(
            base_query.where(Schedule.check_in_status == checkin_status)
        )
        checkin_stats[checkin_status] = len(checkin_result.scalars().all())
    
    return {
        "message": "每日排期统计",
        "target_date": target_date.isoformat(),
        "institution_id": institution_id,
        "statistics": {
            "total_schedules": total_schedules,
            "by_type": {
                "theory": theory_count,
                "practical": practical_count
            },
            "by_status": status_stats,
            "by_checkin_status": checkin_stats
        }
    }

@router.get("/export/excel")
async def export_schedules_excel(
    start_date: date = Query(..., description="开始日期"),
    end_date: date = Query(..., description="结束日期"),
    institution_id: Optional[int] = Query(None, description="机构ID筛选"),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_permission(Permission.SCHEDULE_READ))
):
    """导出排期数据为Excel"""
    
    # 机构用户只能导出自己机构的数据
    if current_user.institution_id:
        institution_id = current_user.institution_id
    
    # 获取排期数据
    timeline = await schedule_management_service.get_schedule_timeline(
        db, start_date, end_date, None, institution_id
    )
    
    # 这里应该实现Excel生成逻辑
    # 暂时返回数据结构，后续可以集成openpyxl
    
    return {
        "message": "排期数据导出（开发中）",
        "data_preview": timeline,
        "note": "Excel导出功能正在开发中，当前返回数据预览"
    }