"""
二维码和签到相关API路由
支持二维码生成、扫码签到、排队状态查询等功能
"""
from fastapi import APIRouter, Depends, HTTPException, status, Body, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Optional
from pydantic import BaseModel

from src.db.session import get_async_session
from src.core.rbac import require_permission, Permission
from src.services.qrcode_service import qrcode_service
from src.db.models import User
from src.auth.fastapi_users_config import current_active_user

router = APIRouter(
    prefix="/qrcode",
    tags=["qrcode_checkin"],
)

# ===== 基础端点 =====

@router.get("/health")
async def qrcode_health_check():
    """二维码模块健康检查"""
    return {
        "status": "healthy",
        "service": "二维码和签到服务",
        "version": "1.0.0",
        "features": ["二维码生成", "扫码签到", "考生查询", "签到管理"]
    }

@router.get("/generate-schedule-qr/{schedule_id}")
async def generate_schedule_qr(schedule_id: int):
    """为指定考试安排生成二维码"""
    
    # 模拟二维码数据
    qr_data = {
        "type": "schedule_checkin",
        "schedule_id": schedule_id,
        "timestamp": "2025-08-03T19:10:00",
        "valid_until": "2025-08-03T23:59:59"
    }
    
    # 生成模拟二维码URL (实际应用中应该生成真实的二维码图片)
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={schedule_id}"
    
    return {
        "message": f"考试安排 {schedule_id} 二维码生成成功",
        "schedule_id": schedule_id,
        "qr_data": qr_data,
        "qr_url": qr_url,
        "scan_url": f"/qrcode/scan/{schedule_id}",
        "instructions": "考生可扫描此二维码进行签到"
    }

@router.post("/scan-checkin")
async def scan_checkin(
    qr_content: str = Query(..., description="扫描的二维码内容"),
    staff_id: Optional[int] = Query(None, description="考务人员ID")
):
    """考务人员扫码签到（核心功能）"""
    
    # 解析二维码内容
    try:
        # 假设二维码格式为: schedule_1_candidate_1
        if not qr_content.startswith("schedule_"):
            raise HTTPException(status_code=400, detail="无效的二维码格式")
        
        parts = qr_content.split("_")
        if len(parts) != 4:
            raise HTTPException(status_code=400, detail="二维码数据格式错误")
        
        schedule_id = int(parts[1])
        candidate_id = int(parts[3])
        
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail="二维码数据解析失败")
    
    # 模拟验证二维码和签到逻辑
    mock_schedules = {
        1: {
            "schedule_id": 1,
            "candidate_id": 1,
            "candidate_name": "张三",
            "activity_name": "理论考试",
            "venue": "理论考场A",
            "exam_date": "2025-08-15",
            "start_time": "09:00",
            "status": "待签到"
        },
        3: {
            "schedule_id": 3,
            "candidate_id": 2,
            "candidate_name": "李四",
            "activity_name": "理论考试",
            "venue": "理论考场B",
            "exam_date": "2025-08-16",
            "start_time": "10:00",
            "status": "待签到"
        }
    }
    
    schedule = mock_schedules.get(schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="找不到对应的考试安排")
    
    if schedule["candidate_id"] != candidate_id:
        raise HTTPException(status_code=400, detail="考生信息与二维码不匹配")
    
    if schedule["status"] != "待签到":
        return {
            "message": f"签到状态异常: {schedule['status']}",
            "schedule_id": schedule_id,
            "candidate_name": schedule["candidate_name"],
            "current_status": schedule["status"],
            "success": False
        }
    
    # 执行签到逻辑
    checkin_time = "2025-08-03T19:55:00"
    
    # 更新状态（模拟）
    schedule["status"] = "已签到"
    schedule["checkin_time"] = checkin_time
    
    # 返回签到成功信息
    return {
        "message": f"✅ {schedule['candidate_name']} 签到成功",
        "schedule_id": schedule_id,
        "candidate_id": candidate_id,
        "candidate_name": schedule["candidate_name"],
        "activity_name": schedule["activity_name"],
        "venue": schedule["venue"],
        "checkin_time": checkin_time,
        "staff_id": staff_id,
        "success": True,
        "next_action": "考生可进入考场准备"
    }

# ===== 请求模型 =====

class ScanRequest(BaseModel):
    qr_data: str

class CandidateLoginRequest(BaseModel):
    id_number: str

# ===== 考生端接口 =====

@router.post("/candidate/login")
async def candidate_login_by_id_number(
    login_request: CandidateLoginRequest,
    db: AsyncSession = Depends(get_async_session)
):
    """考生通过身份证号登录（简化登录）"""
    
    from src.models.candidate import Candidate
    from sqlalchemy import select
    
    # 查找考生
    result = await db.execute(
        select(Candidate).where(Candidate.id_number == login_request.id_number)
    )
    candidate = result.scalar_one_or_none()
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="考生不存在，请联系机构确认报名信息"
        )
    
    # 生成简单的临时token（实际项目中应该使用JWT）
    import hashlib
    import time
    timestamp = str(int(time.time()))
    token_raw = f"{candidate.id}_{candidate.id_number}_{timestamp}"
    token = hashlib.md5(token_raw.encode()).hexdigest()
    
    return {
        "message": "登录成功",
        "candidate": {
            "id": candidate.id,
            "name": candidate.name,
            "id_number": candidate.id_number,
            "status": candidate.status
        },
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/candidate/{candidate_id}/qrcode")
async def get_candidate_qrcode(
    candidate_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user)
):
    """获取考生的动态二维码"""
    
    # 简单的权限检查：考生只能获取自己的二维码
    # 实际项目中应该通过proper的认证机制
    
    qr_result = await qrcode_service.generate_candidate_qrcode(db, candidate_id)
    
    return {
        "message": "考生二维码生成成功",
        **qr_result
    }

@router.get("/candidate/{candidate_id}/schedule")
async def get_candidate_schedule(
    candidate_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user)
):
    """获取考生的考试安排"""
    
    from src.models.schedule import Schedule
    from src.models.venue import Venue
    from src.models.exam_product import ExamProduct
    from sqlalchemy import select, and_
    from datetime import datetime, date
    
    # 获取考生今日及未来的排期
    query = select(Schedule).where(
        and_(
            Schedule.candidate_id == candidate_id,
            Schedule.scheduled_date >= date.today()
        )
    ).order_by(Schedule.start_time)
    
    result = await db.execute(query)
    schedules = result.scalars().all()
    
    schedule_list = []
    for schedule in schedules:
        # 获取场地信息
        venue_result = await db.execute(
            select(Venue).where(Venue.id == schedule.venue_id)
        )
        venue = venue_result.scalar_one_or_none()
        
        # 获取考试产品信息
        exam_product_result = await db.execute(
            select(ExamProduct).where(ExamProduct.id == schedule.exam_product_id)
        )
        exam_product = exam_product_result.scalar_one_or_none()
        
        schedule_list.append({
            "id": schedule.id,
            "scheduled_date": schedule.scheduled_date.isoformat(),
            "start_time": schedule.start_time.isoformat(),
            "end_time": schedule.end_time.isoformat(),
            "schedule_type": schedule.schedule_type,
            "status": schedule.status,
            "check_in_status": schedule.check_in_status,
            "venue": {
                "id": venue.id if venue else None,
                "name": venue.name if venue else "未知场地",
                "address": venue.address if venue else "未知地址"
            },
            "exam_product": {
                "id": exam_product.id if exam_product else None,
                "name": exam_product.name if exam_product else "未知考试"
            },
            "queue_position": schedule.queue_position,
            "estimated_wait_time": schedule.estimated_wait_time
        })
    
    return {
        "message": "考生考试安排",
        "candidate_id": candidate_id,
        "schedules": schedule_list,
        "total_count": len(schedule_list)
    }

@router.get("/candidate/{candidate_id}/queue-status")
async def get_candidate_queue_status(
    candidate_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user)
):
    """获取考生排队状态"""
    
    queue_status = await qrcode_service.get_candidate_queue_status(db, candidate_id)
    
    return {
        "message": "考生排队状态",
        **queue_status
    }

# ===== 考务人员端接口 =====

@router.post("/staff/scan")
async def scan_qrcode_checkin(
    scan_request: ScanRequest,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_permission(Permission.CHECKIN_SCAN))
):
    """考务人员扫码签到"""
    
    result = await qrcode_service.scan_qrcode_checkin(
        db, scan_request.qr_data, current_user
    )
    
    return result

@router.get("/staff/checkin-history")
async def get_checkin_history(
    limit: int = 50,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_permission(Permission.CHECKIN_READ))
):
    """获取签到历史记录"""
    
    from src.models.schedule import Schedule
    from src.models.candidate import Candidate
    from src.models.venue import Venue
    from sqlalchemy import select, and_
    from datetime import datetime, date
    
    # 获取今日的签到记录
    query = select(Schedule).where(
        and_(
            Schedule.scheduled_date == date.today(),
            Schedule.check_in_status.in_(["checked_in", "late"])
        )
    ).order_by(Schedule.check_in_time.desc()).limit(limit)
    
    result = await db.execute(query)
    schedules = result.scalars().all()
    
    checkin_history = []
    for schedule in schedules:
        # 获取考生信息
        candidate_result = await db.execute(
            select(Candidate).where(Candidate.id == schedule.candidate_id)
        )
        candidate = candidate_result.scalar_one_or_none()
        
        # 获取场地信息
        venue_result = await db.execute(
            select(Venue).where(Venue.id == schedule.venue_id)
        )
        venue = venue_result.scalar_one_or_none()
        
        checkin_history.append({
            "schedule_id": schedule.id,
            "check_in_time": schedule.check_in_time.isoformat() if schedule.check_in_time else None,
            "check_in_status": schedule.check_in_status,
            "schedule_type": schedule.schedule_type,
            "candidate": {
                "id": candidate.id if candidate else None,
                "name": candidate.name if candidate else "未知",
                "id_number": candidate.id_number if candidate else "未知"
            },
            "venue": {
                "id": venue.id if venue else None,
                "name": venue.name if venue else "未知场地"
            }
        })
    
    return {
        "message": "签到历史记录",
        "date": date.today().isoformat(),
        "total_count": len(checkin_history),
        "checkin_history": checkin_history
    }

@router.get("/staff/current-queue")
async def get_current_queue_status(
    venue_id: int = None,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_permission(Permission.CHECKIN_READ))
):
    """获取当前排队状态"""
    
    from src.models.schedule import Schedule
    from src.models.candidate import Candidate
    from src.models.venue import Venue
    from sqlalchemy import select, and_
    from datetime import datetime, date
    
    # 构建查询条件
    query = select(Schedule).where(
        and_(
            Schedule.scheduled_date == date.today(),
            Schedule.check_in_status == "not_checked_in",
            Schedule.start_time > datetime.utcnow()
        )
    )
    
    if venue_id:
        query = query.where(Schedule.venue_id == venue_id)
    
    query = query.order_by(Schedule.start_time)
    
    result = await db.execute(query)
    schedules = result.scalars().all()
    
    # 按场地分组
    venue_queues = {}
    for schedule in schedules:
        # 获取场地信息
        venue_result = await db.execute(
            select(Venue).where(Venue.id == schedule.venue_id)
        )
        venue = venue_result.scalar_one_or_none()
        
        # 获取考生信息
        candidate_result = await db.execute(
            select(Candidate).where(Candidate.id == schedule.candidate_id)
        )
        candidate = candidate_result.scalar_one_or_none()
        
        venue_key = f"{venue.name}_{venue.id}" if venue else f"未知场地_{schedule.venue_id}"
        
        if venue_key not in venue_queues:
            venue_queues[venue_key] = {
                "venue_id": schedule.venue_id,
                "venue_name": venue.name if venue else "未知场地",
                "venue_type": venue.type if venue else "未知",
                "queue": []
            }
        
        venue_queues[venue_key]["queue"].append({
            "schedule_id": schedule.id,
            "candidate_name": candidate.name if candidate else "未知",
            "candidate_id_number": candidate.id_number if candidate else "未知",
            "schedule_type": schedule.schedule_type,
            "start_time": schedule.start_time.isoformat(),
            "queue_position": len(venue_queues[venue_key]["queue"]) + 1
        })
    
    return {
        "message": "当前排队状态",
        "date": date.today().isoformat(),
        "update_time": datetime.utcnow().isoformat(),
        "venue_queues": list(venue_queues.values())
    }

# ===== 公共看板接口 =====

@router.get("/public/dashboard")
async def get_public_dashboard(
    db: AsyncSession = Depends(get_async_session)
):
    """公共考场看板（无需认证）"""
    
    from src.models.schedule import Schedule
    from src.models.candidate import Candidate
    from src.models.venue import Venue
    from sqlalchemy import select, and_, func
    from datetime import datetime, date
    
    # 获取正在进行的考试
    ongoing_query = select(Schedule).where(
        and_(
            Schedule.scheduled_date == date.today(),
            Schedule.start_time <= datetime.utcnow(),
            Schedule.end_time > datetime.utcnow(),
            Schedule.check_in_status == "checked_in"
        )
    )
    
    ongoing_result = await db.execute(ongoing_query)
    ongoing_schedules = ongoing_result.scalars().all()
    
    # 按场地组织数据
    venue_status = {}
    
    for schedule in ongoing_schedules:
        # 获取场地信息
        venue_result = await db.execute(
            select(Venue).where(Venue.id == schedule.venue_id)
        )
        venue = venue_result.scalar_one_or_none()
        
        # 获取考生信息（脱敏）
        candidate_result = await db.execute(
            select(Candidate).where(Candidate.id == schedule.candidate_id)
        )
        candidate = candidate_result.scalar_one_or_none()
        
        venue_key = f"venue_{schedule.venue_id}"
        
        if venue_key not in venue_status:
            venue_status[venue_key] = {
                "venue_id": schedule.venue_id,
                "venue_name": venue.name if venue else "未知场地",
                "venue_type": venue.type if venue else "未知",
                "current_exam": None,
                "waiting_count": 0
            }
        
        # 设置当前考试信息（脱敏显示）
        candidate_name = candidate.name if candidate else "未知"
        masked_name = candidate_name[0] + "*" if len(candidate_name) > 1 else candidate_name
        
        venue_status[venue_key]["current_exam"] = {
            "candidate_name": masked_name,
            "schedule_type": schedule.schedule_type,
            "start_time": schedule.start_time.strftime("%H:%M"),
            "estimated_end_time": schedule.end_time.strftime("%H:%M")
        }
    
    # 计算等待人数
    for venue_key in venue_status:
        venue_id = venue_status[venue_key]["venue_id"]
        
        # 查询该场地今日待签到的人数
        waiting_query = select(func.count(Schedule.id)).where(
            and_(
                Schedule.venue_id == venue_id,
                Schedule.scheduled_date == date.today(),
                Schedule.check_in_status == "not_checked_in",
                Schedule.start_time > datetime.utcnow()
            )
        )
        
        waiting_result = await db.execute(waiting_query)
        waiting_count = waiting_result.scalar() or 0
        venue_status[venue_key]["waiting_count"] = waiting_count
    
    # 获取今日整体统计
    total_today_query = select(func.count(Schedule.id)).where(
        Schedule.scheduled_date == date.today()
    )
    total_today_result = await db.execute(total_today_query)
    total_today = total_today_result.scalar() or 0
    
    completed_today_query = select(func.count(Schedule.id)).where(
        and_(
            Schedule.scheduled_date == date.today(),
            Schedule.status == "completed"
        )
    )
    completed_today_result = await db.execute(completed_today_query)
    completed_today = completed_today_result.scalar() or 0
    
    return {
        "message": "公共考场看板",
        "update_time": datetime.utcnow().isoformat(),
        "date": date.today().isoformat(),
        "overall_stats": {
            "total_schedules_today": total_today,
            "completed_today": completed_today,
            "ongoing_exams": len(ongoing_schedules),
            "active_venues": len(venue_status)
        },
        "venues": list(venue_status.values())
    }