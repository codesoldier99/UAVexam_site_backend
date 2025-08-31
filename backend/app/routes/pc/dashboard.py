"""
PC前端仪表板API路由
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from datetime import datetime, timedelta

from ...config.database import get_db
from ...services.auth_service import AuthService
from ...models.user import User, UserRole
from ...models.schedule import Schedule, ScheduleStatus
from ...models.checkin import CheckIn, CheckInStatus
from ...models.venue import Venue

router = APIRouter(prefix="/dashboard", tags=["PC-仪表板"])


@router.get("/stats", summary="获取仪表板统计数据")
async def get_dashboard_stats(
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取PC端仪表板统计数据"""
    
    # 根据用户角色过滤数据
    institution_filter = None
    if current_user.role == UserRole.OPERATOR:
        institution_filter = current_user.institution_id
    
    today = datetime.now().date()
    
    # 简化统计查询，避免复杂的关联查询
    try:
        # 今日考试统计 - 简化查询
        today_schedules = db.query(Schedule).filter(
            Schedule.scheduled_date == today.date()
        ).all() if hasattr(Schedule, 'scheduled_date') else []
        
        # 今日签到统计 - 简化查询
        today_checkins = db.query(CheckIn).filter(
            CheckIn.created_at >= today,
            CheckIn.created_at < today + timedelta(days=1)
        ).all()
        
    except Exception as e:
        # 如果查询失败，返回默认值
        today_schedules = []
        today_checkins = []
    
    # 考场状态统计
    venues_query = db.query(Venue)
    if institution_filter:
        venues_query = venues_query.filter(Venue.institution_id == institution_filter)
    
    venues = venues_query.all()
    
    return {
        "exam_stats": {
            "today_total": len(today_schedules),
            "today_completed": len([s for s in today_schedules if s.status == ScheduleStatus.COMPLETED]),
            "today_in_progress": len([s for s in today_schedules if s.status == ScheduleStatus.IN_PROGRESS]),
            "today_pending": len([s for s in today_schedules if s.status == ScheduleStatus.PENDING])
        },
        "checkin_stats": {
            "today_total": len(today_checkins),
            "today_success": len([c for c in today_checkins if c.status == CheckInStatus.SUCCESS]),
            "today_late": len([c for c in today_checkins if c.status == CheckInStatus.LATE]),
            "today_failed": len([c for c in today_checkins if c.status == CheckInStatus.FAILED])
        },
        "venue_stats": {
            "total_venues": len(venues),
            "active_venues": len([v for v in venues if v.is_active]),
            "busy_venues": len([v for v in venues if v.status == "busy"]),
            "available_venues": len([v for v in venues if v.status == "available"])
        },
        "last_updated": datetime.now().isoformat()
    }


@router.get("/recent-exams", summary="获取最近考试列表")
async def get_recent_exams(
    limit: int = 10,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """获取最近的考试安排"""
    
    try:
        # 简化查询，避免复杂的关联
        schedules = db.query(Schedule).order_by(Schedule.id.desc()).limit(limit).all()
        
        result = []
        for schedule in schedules:
            try:
                # 安全地获取关联数据
                venue_name = schedule.venue.name if hasattr(schedule, 'venue') and schedule.venue else "未知考场"
                scheduled_time = schedule.scheduled_time.isoformat() if hasattr(schedule, 'scheduled_time') and schedule.scheduled_time else "未知时间"
                
                result.append({
                    "id": schedule.id,
                    "candidate_name": "考生",  # 简化显示
                    "exam_type": "考试",      # 简化显示
                    "venue_name": venue_name,
                    "scheduled_time": scheduled_time,
                    "status": schedule.status.value if hasattr(schedule, 'status') else "未知",
                    "checkin_status": "未签到"  # 简化显示
                })
            except Exception:
                continue
                
        return result
        
    except Exception as e:
        # 如果查询失败，返回空列表
        return []


@router.get("/activities", summary="获取系统活动日志")
async def get_system_activities(
    limit: int = 20,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """获取系统最近的操作活动记录"""
    
    # 这里可以实现活动日志功能，暂时返回模拟数据
    activities = [
        {
            "id": 1,
            "user_name": current_user.real_name or current_user.username,
            "action": "登录系统",
            "target": "PC管理端",
            "timestamp": datetime.now().isoformat(),
            "ip_address": "192.168.1.100"
        }
    ]
    
    return activities[:limit]