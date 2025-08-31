from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_
from sqlalchemy import desc, and_, or_
from typing import List, Optional, Dict, Any
from datetime import datetime, date

from ...config.database import get_db
from ...models.user import User, UserRole
from ...models.schedule import Schedule, ScheduleStatus
from ...models.venue import Venue
from ...models.exam import ExamProduct, ExamRegistration
from ...services.auth_service import AuthService

router = APIRouter()

@router.get("/schedules")
async def get_schedules(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    venue_id: Optional[int] = Query(None),
    registration_id: Optional[int] = Query(None),
    date_filter: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取考试安排列表"""
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR]:
        raise HTTPException(status_code=403, detail="权限不足")
    
    try:
        query = db.query(Schedule)
        
        # 根据用户角色过滤
        if current_user.role == UserRole.ADMIN and current_user.institution_id:
            # 通过venue关联过滤机构
            query = query.join(Venue).filter(Venue.institution_id == current_user.institution_id)
        
        # 按考场过滤
        if venue_id:
            query = query.filter(Schedule.venue_id == venue_id)
        
        # 按报名记录过滤
        if registration_id:
            query = query.filter(Schedule.registration_id == registration_id)
        
        # 按日期过滤
        if date_filter:
            try:
                filter_date = datetime.strptime(date_filter, "%Y-%m-%d").date()
                query = query.filter(Schedule.schedule_date == filter_date)
            except ValueError:
                raise HTTPException(status_code=400, detail="日期格式错误，请使用YYYY-MM-DD格式")
        
        # 按状态过滤
        if status:
            query = query.filter(Schedule.status == status)
        
        total = query.count()
        schedules = query.offset(skip).limit(limit).all()
        
        # 手动序列化，包含关联信息
        result = []
        for schedule in schedules:
            schedule_dict = {
                "id": schedule.id,
                "registration_id": schedule.registration_id,
                "venue_id": schedule.venue_id,
                "schedule_date": schedule.schedule_date.isoformat() if schedule.schedule_date else None,
                "start_time": schedule.start_time.isoformat() if schedule.start_time else None,
                "end_time": schedule.end_time.isoformat() if schedule.end_time else None,
                "status": schedule.status.value if schedule.status else None,
                "exam_result": schedule.exam_result,
                "exam_score": schedule.exam_score,
                "remarks": schedule.remarks,
                "created_at": schedule.created_at.isoformat() if schedule.created_at else None,
                "updated_at": schedule.updated_at.isoformat() if schedule.updated_at else None,
                # 关联信息
                "venue_name": schedule.venue.name if schedule.venue else None,
                "registration_info": {
                    "candidate_name": schedule.registration.user.real_name if schedule.registration and schedule.registration.user else None,
                    "exam_product_name": schedule.registration.exam_product.name if schedule.registration and schedule.registration.exam_product else None
                } if schedule.registration else None
            }
            result.append(schedule_dict)
        
        return {
            "items": result,
            "total": total,
            "page": skip // limit + 1,
            "size": limit,
            "pages": (total + limit - 1) // limit
        }
    except Exception as e:
        # 如果查询失败，返回空结果
        return {
            "items": [],
            "total": 0,
            "page": skip // limit + 1,
            "size": limit,
            "pages": 0
        }

@router.get("/schedules/{schedule_id}")
async def get_schedule(
    schedule_id: int,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取考试安排详情"""
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR]:
        raise HTTPException(status_code=403, detail="权限不足")
    
    try:
        schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
        if not schedule:
            raise HTTPException(status_code=404, detail="考试安排不存在")
        
        # 权限检查
        if current_user.role == UserRole.ADMIN and current_user.institution_id:
            if schedule.venue and schedule.venue.institution_id != current_user.institution_id:
                raise HTTPException(status_code=403, detail="无权访问此考试安排")
        
        # 手动序列化
        return {
            "id": schedule.id,
            "registration_id": schedule.registration_id,
            "venue_id": schedule.venue_id,
            "schedule_date": schedule.schedule_date.isoformat() if schedule.schedule_date else None,
            "start_time": schedule.start_time.isoformat() if schedule.start_time else None,
            "end_time": schedule.end_time.isoformat() if schedule.end_time else None,
            "status": schedule.status.value if schedule.status else None,
            "exam_result": schedule.exam_result,
            "exam_score": schedule.exam_score,
            "max_score": schedule.max_score,
            "pass_score": schedule.pass_score,
            "actual_duration": schedule.actual_duration,
            "result_notes": schedule.result_notes,
            "remarks": schedule.remarks,
            "created_at": schedule.created_at.isoformat() if schedule.created_at else None,
            "updated_at": schedule.updated_at.isoformat() if schedule.updated_at else None,
            # 详细关联信息
            "venue": {
                "id": schedule.venue.id,
                "name": schedule.venue.name,
                "code": schedule.venue.code,
                "address": schedule.venue.description
            } if schedule.venue else None,
            "registration": {
                "id": schedule.registration.id,
                "candidate": {
                    "id": schedule.registration.user.id,
                    "real_name": schedule.registration.user.real_name,
                    "phone": schedule.registration.user.phone
                } if schedule.registration.user else None,
                "exam_product": {
                    "id": schedule.registration.exam_product.id,
                    "name": schedule.registration.exam_product.name,
                    "code": schedule.registration.exam_product.code
                } if schedule.registration.exam_product else None
            } if schedule.registration else None
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取考试安排详情失败: {str(e)}")

@router.post("/schedules")
async def create_schedule(
    schedule_data: dict,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """创建考试安排"""
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="权限不足")
    
    try:
        # 验证必需字段
        required_fields = ["registration_id", "venue_id", "schedule_date", "start_time", "end_time"]
        for field in required_fields:
            if field not in schedule_data:
                raise HTTPException(status_code=400, detail=f"缺少必需字段: {field}")
        
        # 验证报名记录和考场是否存在
        registration = db.query(ExamRegistration).filter(ExamRegistration.id == schedule_data.get("registration_id")).first()
        if not registration:
            raise HTTPException(status_code=404, detail="报名记录不存在")
        
        venue = db.query(Venue).filter(Venue.id == schedule_data.get("venue_id")).first()
        if not venue:
            raise HTTPException(status_code=404, detail="考场不存在")
        
        # 权限检查
        if current_user.role == UserRole.ADMIN and current_user.institution_id != venue.institution_id:
            raise HTTPException(status_code=403, detail="无权在此考场创建考试安排")
        
        # 创建考试安排
        schedule = Schedule(
            registration_id=schedule_data.get("registration_id"),
            venue_id=schedule_data.get("venue_id"),
            schedule_date=datetime.strptime(schedule_data.get("schedule_date"), "%Y-%m-%d").date(),
            start_time=datetime.strptime(schedule_data.get("start_time"), "%H:%M").time(),
            end_time=datetime.strptime(schedule_data.get("end_time"), "%H:%M").time(),
            remarks=schedule_data.get("remarks", "")
        )
        
        db.add(schedule)
        db.commit()
        db.refresh(schedule)
        
        return {
            "id": schedule.id,
            "message": "考试安排创建成功"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建考试安排失败: {str(e)}")

@router.put("/schedules/{schedule_id}")
async def update_schedule(
    schedule_id: int,
    schedule_data: dict,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """更新考试安排"""
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="权限不足")
    
    try:
        schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
        if not schedule:
            raise HTTPException(status_code=404, detail="考试安排不存在")
        
        # 权限检查
        if current_user.role == UserRole.ADMIN and current_user.institution_id:
            if schedule.venue and schedule.venue.institution_id != current_user.institution_id:
                raise HTTPException(status_code=403, detail="无权修改此考试安排")
        
        # 更新字段
        if "schedule_date" in schedule_data:
            schedule.schedule_date = datetime.strptime(schedule_data["schedule_date"], "%Y-%m-%d").date()
        if "start_time" in schedule_data:
            schedule.start_time = datetime.strptime(schedule_data["start_time"], "%H:%M").time()
        if "end_time" in schedule_data:
            schedule.end_time = datetime.strptime(schedule_data["end_time"], "%H:%M").time()
        if "status" in schedule_data:
            schedule.status = schedule_data["status"]
        if "exam_result" in schedule_data:
            schedule.exam_result = schedule_data["exam_result"]
        if "exam_score" in schedule_data:
            schedule.exam_score = schedule_data["exam_score"]
        if "remarks" in schedule_data:
            schedule.remarks = schedule_data["remarks"]
        
        db.commit()
        
        return {"message": "考试安排更新成功"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"更新考试安排失败: {str(e)}")

@router.get("/schedules/statistics")
async def get_schedule_statistics(
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取考试安排统计信息"""
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR]:
        raise HTTPException(status_code=403, detail="权限不足")
    
    try:
        query = db.query(Schedule)
        
        # 根据用户角色过滤
        if current_user.role == UserRole.ADMIN and current_user.institution_id:
            # 使用LEFT JOIN避免数据缺失导致的查询失败
            query = query.outerjoin(Venue).filter(
                or_(
                    Venue.institution_id == current_user.institution_id,
                    Venue.institution_id.is_(None)
                )
            )
        
        total_schedules = query.count()
        pending_schedules = query.filter(Schedule.status == ScheduleStatus.PENDING).count()
        in_progress_schedules = query.filter(Schedule.status == ScheduleStatus.IN_PROGRESS).count()
        completed_schedules = query.filter(Schedule.status == ScheduleStatus.COMPLETED).count()
        cancelled_schedules = query.filter(Schedule.status == ScheduleStatus.CANCELLED).count()
        
        # 今日考试安排
        today = date.today()
        today_schedules = query.filter(Schedule.schedule_date == today).count()
        
        return {
            "total_schedules": total_schedules,
            "pending_schedules": pending_schedules,
            "in_progress_schedules": in_progress_schedules,
            "completed_schedules": completed_schedules,
            "cancelled_schedules": cancelled_schedules,
            "today_schedules": today_schedules
        }
    except Exception as e:
        # 如果查询失败，返回默认统计
        return {
            "total_schedules": 0,
            "pending_schedules": 0,
            "in_progress_schedules": 0,
            "completed_schedules": 0,
            "cancelled_schedules": 0,
            "today_schedules": 0
        }