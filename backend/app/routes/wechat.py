"""
微信小程序专用API路由
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import qrcode
import io
import base64

from ..config.database import get_db
from ..services.auth_service import AuthService
from ..services.wechat_service import WeChatService
from ..services.schedule_service import ScheduleService
from ..services.manual_checkin_service import ManualCheckinService
from ..models.user import User, UserRole
from ..schemas.wechat import (
    CandidateInfoByIdCardRequest,
    CandidateInfoResponse,
    QRCodeRefreshRequest,
    QRCodeRefreshResponse,
    CheckinHistoryResponse,
    ExamResultResponse,
    VenueStatusResponse,
    ExamScheduleItem,
    CandidateScheduleResponse,
    QRCodeGenerationResponse,
    DashboardStatistics,
    ManualCheckinQueryRequest,
    ManualCheckinQueryResponse,
    ManualCheckinConfirmRequest,
    ManualCheckinConfirmResponse,
    DashboardVenue,
    DashboardAnnouncement,
    DashboardResponse,
    WeChatLoginRequest,
    WeChatLoginResponse,
    CheckInRequest,
    CheckInResponse,
    ExamScheduleInfo,
    QRCodeData,
    ManualCheckinQueryRequest,
    ManualCheckinQueryResponse,
    ManualCheckinConfirmRequest,
    ManualCheckinConfirmResponse
)

router = APIRouter(prefix="/wechat", tags=["微信小程序"])


@router.post("/login", response_model=WeChatLoginResponse, summary="微信小程序登录")
async def wechat_login(
    login_data: WeChatLoginRequest,
    db: Session = Depends(get_db)
):
    """微信小程序登录（身份证号登录）"""
    service = WeChatService(db)
    try:
        result = service.login_by_id_card(login_data.id_card, login_data.openid)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/candidate/schedule", response_model=CandidateScheduleResponse, summary="获取考生日程")
async def get_candidate_schedule(
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前考生的日程安排"""
    service = WeChatService(db)
    try:
        schedule = await service.get_candidate_schedule(current_user.id)
        return schedule
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取考试日程失败: {str(e)}"
        )


@router.get("/candidate/qrcode", response_model=QRCodeGenerationResponse, summary="获取考生二维码")
async def get_candidate_qrcode(
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取考生的动态二维码"""
    service = WeChatService(db)
    try:
        qr_code = await service.generate_candidate_qrcode(current_user.id)
        return qr_code
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"生成二维码失败: {str(e)}"
        )


@router.get("/venues/status", response_model=List[VenueStatusResponse], summary="获取考场状态")
async def get_venues_status(
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取所有考场的实时状态"""
    service = WeChatService(db)
    venues = await service.get_venues_status()
    return venues


@router.post("/checkin", response_model=CheckInResponse, summary="扫码签到")
async def checkin_candidate(
    checkin_data: CheckInRequest,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """考务人员扫码签到"""
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.EXAMINER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有考务人员可以执行签到操作"
        )
    
    service = WeChatService(db)
    try:
        result = service.process_checkin(
            examiner_id=current_user.id,
            qr_code_data=checkin_data.qr_code_data
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/candidate/queue-position", summary="获取排队位置")
async def get_queue_position(
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取考生在当前考场的排队位置"""
    if current_user.role != UserRole.CANDIDATE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有考生可以访问此接口"
        )
    
    service = ScheduleService(db)
    position = service.get_candidate_queue_position(current_user.id)
    return position


@router.get("/dashboard", response_model=DashboardResponse, summary="获取看板数据")
async def get_dashboard_data(
    db: Session = Depends(get_db)
):
    """获取小程序看板数据（公共接口）"""
    service = WeChatService(db)
    try:
        dashboard = await service.get_dashboard_data()
        return dashboard
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取看板数据失败: {str(e)}"
        )


# 现有的4个关键接口

@router.get("/candidate/info-by-idcard", response_model=CandidateInfoResponse, summary="根据身份证获取考生信息")
async def get_candidate_info_by_id_card(
    id_card: str,
    db: Session = Depends(get_db)
):
    """根据身份证号获取考生信息（公开接口）"""
    service = WeChatService(db)
    candidate = await service.get_candidate_by_id_card(id_card)
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="考生信息未找到"
        )
    
    return candidate


@router.post("/candidate/qrcode/refresh", response_model=QRCodeRefreshResponse, summary="刷新考生二维码")
async def refresh_candidate_qrcode(
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """刷新考生的动态二维码"""
    if current_user.role.value != 'candidate':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有考生可以刷新二维码"
        )
    
    service = WeChatService(db)
    
    try:
        result = await service.refresh_qr_code(current_user.id)
        return QRCodeRefreshResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"刷新二维码失败: {str(e)}"
        )


@router.get("/candidate/checkin-history", response_model=List[CheckinHistoryResponse], summary="获取考生签到历史")
async def get_candidate_checkin_history(
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取考生的签到历史记录"""
    service = WeChatService(db)
    history = await service.get_checkin_history(current_user.id)
    return history


@router.get("/candidate/exam-results", response_model=List[ExamResultResponse], summary="获取考生考试结果")
async def get_candidate_exam_results(
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取考生的考试结果"""
    service = WeChatService(db)
    results = await service.get_exam_results(current_user.id)
    return results


# 新增：手动签到相关接口

@router.post("/manual-checkin/query", response_model=ManualCheckinQueryResponse, summary="查询考生信息用于手动签到")
async def query_candidate_for_manual_checkin(
    query_data: ManualCheckinQueryRequest,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """第一步：根据考生姓名和身份证查询考试信息"""
    # 检查权限：只有考务人员可以进行手动签到查询
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.EXAMINER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有考务人员可以进行手动签到操作"
        )
    
    service = WeChatService(db)
    try:
        result = service.query_candidate_for_manual_checkin(
            real_name=query_data.real_name,
            id_card=query_data.id_card
        )
        return ManualCheckinQueryResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/manual-checkin/confirm", response_model=ManualCheckinConfirmResponse, summary="确认手动签到")
async def confirm_manual_checkin(
    confirm_data: ManualCheckinConfirmRequest,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """第二步：确认执行手动签到"""
    # 检查权限：只有考务人员可以进行手动签到确认
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.EXAMINER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有考务人员可以进行手动签到操作"
        )
    
    service = WeChatService(db)
    try:
        # 构建操作员信息
        operator_info = confirm_data.operator_info or f"工作人员({current_user.real_name or current_user.username})"
        
        result = service.confirm_manual_checkin(
            candidate_id=confirm_data.candidate_id,
            schedule_id=confirm_data.schedule_id,
            operator_info=operator_info
        )
        return ManualCheckinConfirmResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
