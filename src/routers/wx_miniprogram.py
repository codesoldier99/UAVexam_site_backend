from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from src.dependencies.get_db import get_db
from src.dependencies.get_current_user import get_current_user
from src.models.user import User
from src.models.candidate import Candidate, CandidateStatus
from src.models.schedule import Schedule
from src.models.venue import Venue
from src.schemas.wx_miniprogram import WxLoginRequest, WxLoginResponse, QrCodeResponse
from src.services.wx_miniprogram import WxMiniprogramService
from src.services.venue import VenueService
from src.core.auth import create_access_token
from src.core.config import settings

router = APIRouter(prefix="/wx", tags=["微信小程序"])

@router.post("/login", response_model=WxLoginResponse)
def wx_login(
    request: WxLoginRequest,
    db: Session = Depends(get_db)
):
    """考生登录/绑定"""
    try:
        # 验证身份证号格式
        if not request.id_card or len(request.id_card) != 18:
            raise HTTPException(status_code=400, detail="身份证号格式不正确")
        
        # 查找考生
        candidate = db.query(Candidate).filter(Candidate.id_number == request.id_card).first()
        if not candidate:
            raise HTTPException(status_code=404, detail="未找到该身份证号对应的考生信息")
        
        # 验证考生状态
        if candidate.status not in [CandidateStatus.APPROVED, CandidateStatus.ACTIVE]:
            raise HTTPException(status_code=403, detail="考生状态不允许登录")
        
        # 生成JWT token
        token_data = {
            "sub": str(candidate.id),
            "type": "candidate",
            "candidate_id": candidate.id,
            "institution_id": candidate.institution_id
        }
        access_token = create_access_token(token_data)
        
        return WxLoginResponse(
            access_token=access_token,
            token_type="bearer",
            candidate_id=candidate.id,
            candidate_name=candidate.name,
            phone=candidate.phone,
            status=candidate.status
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"登录失败: {str(e)}")

@router.get("/me/qrcode", response_model=QrCodeResponse)
def get_my_qrcode(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取我的二维码内容"""
    try:
        # 验证用户类型
        if not hasattr(current_user, 'candidate_id') or not current_user.candidate_id:
            raise HTTPException(status_code=403, detail="只有考生可以获取二维码")
        
        candidate_id = current_user.candidate_id
        
        # 查找考生的下一个待办日程
        next_schedule = db.query(Schedule).filter(
            Schedule.candidate_id == candidate_id,
            Schedule.status.in_(['PENDING', 'CONFIRMED']),
            Schedule.scheduled_date >= datetime.now().date()
        ).order_by(Schedule.scheduled_date, Schedule.start_time).first()
        
        if not next_schedule:
            raise HTTPException(status_code=404, detail="没有待办的考试日程")
        
        return QrCodeResponse(
            schedule_id=next_schedule.id,
            exam_date=next_schedule.scheduled_date,
            start_time=next_schedule.start_time,
            end_time=next_schedule.end_time,
            venue_name=next_schedule.venue.name if next_schedule.venue else None,
            exam_product_name=next_schedule.exam_product.name if next_schedule.exam_product else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取二维码失败: {str(e)}") 