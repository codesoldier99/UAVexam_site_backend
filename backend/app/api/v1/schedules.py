from typing import List, Optional
from datetime import datetime, time, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from app.api.deps import get_async_db, get_current_exam_admin, get_current_user
from app.models.schedule import Schedule, ScheduleStatus, ActivityType
from app.models.candidate import Candidate, CandidateStatus
from app.models.venue import Venue
from app.schemas.schedule import (
    ScheduleCreate,
    ScheduleBatchCreate,
    Schedule as ScheduleSchema,
    ScheduleWithDetails,
    ScheduleCheckIn,
    VenueQueueStatus
)

router = APIRouter()

@router.post("/batch", response_model=List[ScheduleSchema])
async def batch_create_schedules(
    batch_data: ScheduleBatchCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_exam_admin)
):
    """批量创建排期（按机构批量安排）"""
    created_schedules = []
    current_time = batch_data.start_time
    
    for candidate_id in batch_data.candidate_ids:
        # 计算结束时间
        end_time = (datetime.combine(batch_data.exam_date, current_time) + 
                   timedelta(minutes=batch_data.duration_minutes)).time()
        
        # 创建排期
        schedule = Schedule(
            candidate_id=candidate_id,
            venue_id=batch_data.venue_id,
            exam_date=batch_data.exam_date,
            start_time=current_time,
            end_time=end_time,
            activity_type=batch_data.activity_type,
            activity_name=batch_data.activity_name
        )
        db.add(schedule)
        created_schedules.append(schedule)
        
        # 更新下一个考生的开始时间
        current_time = end_time
        
        # 更新考生状态
        candidate = await db.execute(
            select(Candidate).where(Candidate.id == candidate_id)
        )
        candidate = candidate.scalar_one()
        candidate.status = CandidateStatus.SCHEDULED
    
    await db.commit()
    for schedule in created_schedules:
        await db.refresh(schedule)
    
    return created_schedules

@router.post("/checkin", response_model=dict)
async def checkin_schedule(
    checkin_data: ScheduleCheckIn,
    db: AsyncSession = Depends(get_async_db),
    current_user = Depends(get_current_user)
):
    """扫码签到"""
    # 获取排期
    result = await db.execute(
        select(Schedule).where(Schedule.id == checkin_data.schedule_id)
    )
    schedule = result.scalar_one_or_none()
    
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )
    
    if schedule.status != ScheduleStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Schedule already checked in or completed"
        )
    
    # 更新签到信息
    schedule.status = ScheduleStatus.CHECKED_IN
    schedule.check_in_time = datetime.now()
    schedule.check_in_staff_id = current_user.id
    
    # 更新考生状态
    candidate = await db.execute(
        select(Candidate).where(Candidate.id == schedule.candidate_id)
    )
    candidate = candidate.scalar_one()
    
    if schedule.activity_type == ActivityType.THEORY_EXAM:
        candidate.status = CandidateStatus.THEORY_WAITING
    elif schedule.activity_type == ActivityType.PRACTICE_EXAM:
        candidate.status = CandidateStatus.PRACTICE_WAITING
        
    await db.commit()
    
    return {
        "message": f"Check-in successful for {candidate.name}",
        "candidate_name": candidate.name,
        "activity": schedule.activity_name,
        "venue_id": schedule.venue_id
    }

@router.get("/my-schedules", response_model=List[ScheduleWithDetails])
async def get_my_schedules(
    db: AsyncSession = Depends(get_async_db),
    candidate_id: Optional[int] = None  # 从token或查询参数获取
):
    """获取考生的排期（小程序用）"""
    if not candidate_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Candidate ID required"
        )
    
    result = await db.execute(
        select(Schedule)
        .where(Schedule.candidate_id == candidate_id)
        .order_by(Schedule.exam_date, Schedule.start_time)
    )
    schedules = result.scalars().all()
    
    detailed_schedules = []
    for schedule in schedules:
        # 获取场地名称
        venue = await db.execute(
            select(Venue).where(Venue.id == schedule.venue_id)
        )
        venue = venue.scalar_one_or_none()
        
        # 获取排队位置
        if schedule.activity_type == ActivityType.PRACTICE_EXAM and schedule.status == ScheduleStatus.PENDING:
            # 计算前面还有多少人
            queue_count = await db.execute(
                select(func.count(Schedule.id))
                .where(and_(
                    Schedule.venue_id == schedule.venue_id,
                    Schedule.exam_date == schedule.exam_date,
                    Schedule.start_time < schedule.start_time,
                    Schedule.status.in_([ScheduleStatus.PENDING, ScheduleStatus.CHECKED_IN])
                ))
            )
            queue_position = queue_count.scalar() + 1
        else:
            queue_position = None
        
        detailed = ScheduleWithDetails(
            **schedule.__dict__,
            venue_name=venue.name if venue else None,
            queue_position=queue_position
        )
        detailed_schedules.append(detailed)
    
    return detailed_schedules

@router.get("/venue-queue/{venue_id}", response_model=VenueQueueStatus)
async def get_venue_queue_status(
    venue_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """获取考场排队状态（公共看板）"""
    # 获取考场信息
    venue_result = await db.execute(
        select(Venue).where(Venue.id == venue_id)
    )
    venue = venue_result.scalar_one_or_none()
    
    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found"
        )
    
    # 获取当前正在进行的考生
    current_result = await db.execute(
        select(Schedule)
        .where(and_(
            Schedule.venue_id == venue_id,
            Schedule.exam_date == datetime.now().date(),
            Schedule.status == ScheduleStatus.IN_PROGRESS
        ))
        .limit(1)
    )
    current_schedule = current_result.scalar_one_or_none()
    
    current_candidate_name = None
    if current_schedule:
        candidate = await db.execute(
            select(Candidate).where(Candidate.id == current_schedule.candidate_id)
        )
        candidate = candidate.scalar_one()
        # 脱敏处理
        current_candidate_name = candidate.name[0] + "*" * (len(candidate.name) - 1)
    
    # 获取等待队列
    waiting_result = await db.execute(
        select(Schedule)
        .where(and_(
            Schedule.venue_id == venue_id,
            Schedule.exam_date == datetime.now().date(),
            Schedule.status.in_([ScheduleStatus.PENDING, ScheduleStatus.CHECKED_IN])
        ))
        .order_by(Schedule.start_time)
    )
    waiting_schedules = waiting_result.scalars().all()
    
    queue_list = []
    for idx, schedule in enumerate(waiting_schedules):
        candidate = await db.execute(
            select(Candidate).where(Candidate.id == schedule.candidate_id)
        )
        candidate = candidate.scalar_one()
        queue_list.append({
            "position": idx + 1,
            "name": candidate.name[0] + "*" * (len(candidate.name) - 1),
            "scheduled_time": schedule.start_time.strftime("%H:%M")
        })
    
    return VenueQueueStatus(
        venue_id=venue_id,
        venue_name=venue.name,
        current_candidate=current_candidate_name,
        waiting_count=len(waiting_schedules),
        queue_list=queue_list[:10]  # 只显示前10个
    )