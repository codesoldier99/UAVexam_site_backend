from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from src.dependencies.get_db import get_db
from src.auth.fastapi_users_config import current_active_user
from src.models.user import User
from src.schemas.schedule import (
    ScheduleCreate, ScheduleRead, ScheduleUpdate, ScheduleListResponse,
    BatchCreateScheduleRequest, QueuePositionResponse, CheckInRequest
)
from src.services.schedule import ScheduleService
from src.services.candidate import CandidateService

router = APIRouter(prefix="/schedules", tags=["排期管理"])

@router.get("/candidates-to-schedule")
def get_candidates_to_schedule(
    scheduled_date: datetime = Query(...),
    institution_id: Optional[int] = Query(None),
    exam_product_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    """获取待排期考生"""
    # 权限检查：考务管理员或机构用户
    if not current_user.is_superuser and not current_user.institution_id:
        raise HTTPException(status_code=403, detail="只有考务管理员或机构用户可以查看待排期考生")
    
    candidates = ScheduleService.get_candidates_to_schedule(
        db, scheduled_date, institution_id, exam_product_id, status
    )
    
    return {
        "candidates": [
            {
                "id": candidate.id,
                "name": candidate.name,
                "phone": candidate.phone,
                "institution_name": candidate.institution.name if candidate.institution else None,
                "target_exam_product_name": candidate.target_exam_product.name if candidate.target_exam_product else None
            }
            for candidate in candidates
        ]
    }

@router.post("/batch-create")
def batch_create_schedules(
    request: BatchCreateScheduleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    """批量创建排期"""
    # 权限检查：考务管理员或机构用户
    if not current_user.is_superuser and not current_user.institution_id:
        raise HTTPException(status_code=403, detail="只有考务管理员或机构用户可以批量创建排期")
    
    schedules = ScheduleService.batch_create_schedules(db, request, current_user.id)
    
    return {
        "message": f"成功创建 {len(schedules)} 个排期",
        "schedules": [
            {
                "id": schedule.id,
                "candidate_name": schedule.candidate.name,
                "exam_product_name": schedule.exam_product.name,
                "schedule_type": schedule.schedule_type,
                "scheduled_date": schedule.scheduled_date,
                "start_time": schedule.start_time,
                "end_time": schedule.end_time
            }
            for schedule in schedules
        ]
    }

@router.get("/candidates/{candidate_id}/schedules", response_model=ScheduleListResponse)
def get_candidate_schedules(
    candidate_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    """查询某考生的全部日程"""
    # 验证考生是否存在
    candidate = CandidateService.get(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="考生不存在")
    
    # 权限检查：考生本人或考务管理员
    if not current_user.is_superuser and current_user.id != candidate_id:
        raise HTTPException(status_code=403, detail="权限不足")
    
    skip = (page - 1) * size
    
    schedules = ScheduleService.get_multi(
        db, 
        skip=skip, 
        limit=size,
        candidate_id=candidate_id
    )
    
    total = ScheduleService.count(db, candidate_id=candidate_id)
    pages = (total + size - 1) // size
    
    return ScheduleListResponse(
        items=schedules,
        total=total,
        page=page,
        size=size,
        pages=pages
    )

@router.get("/{schedule_id}/queue-position", response_model=QueuePositionResponse)
def get_queue_position(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    """查询某日程的排队位置"""
    try:
        schedule = ScheduleService.get(db, schedule_id)
        if not schedule:
            raise HTTPException(status_code=404, detail="排期不存在")
        
        # 权限检查：考务管理员或机构用户
        if not current_user.is_superuser and not current_user.institution_id:
            raise HTTPException(status_code=403, detail="只有考务管理员或机构用户可以查看排队位置")
        
        queue_position = ScheduleService.get_queue_position(db, schedule_id)
        if not queue_position:
            raise HTTPException(status_code=404, detail="排队信息不存在")
        
        return queue_position
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取排队位置失败: {str(e)}")

@router.post("/{schedule_id}/check-in", response_model=ScheduleRead)
def check_in_schedule(
    schedule_id: int,
    check_in_request: CheckInRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    """考务人员扫码签到"""
    schedule = ScheduleService.get(db, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="排期不存在")
    
    # 权限检查：考务人员（这里简化为考务管理员）
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="只有考务人员可以签到")
    
    updated_schedule = ScheduleService.check_in(
        db, 
        schedule_id, 
        check_in_request.check_in_time
    )
    
    if not updated_schedule:
        raise HTTPException(status_code=404, detail="排期不存在")
    
    return updated_schedule

@router.post("/scan-check-in", response_model=dict)
def scan_check_in(
    qr_code: str = Body(...),
    check_in_time: Optional[datetime] = Body(None),
    notes: Optional[str] = Body(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    """
    扫码签到API - 支持二维码扫描签到
    
    二维码格式: SCHEDULE_{schedule_id}_{timestamp}_{hash}
    例如: SCHEDULE_123_1640995200_a1b2c3d4
    
    参数:
    - qr_code: 二维码内容
    - check_in_time: 签到时间（可选，默认为当前时间）
    - notes: 备注信息（可选）
    
    返回:
    - 签到结果和详细信息
    """
    try:
        # 解析二维码
        if not qr_code.startswith("SCHEDULE_"):
            raise HTTPException(status_code=400, detail="无效的二维码格式")
        
        # 解析二维码内容
        parts = qr_code.split("_")
        if len(parts) < 3:
            raise HTTPException(status_code=400, detail="二维码格式错误")
        
        schedule_id = int(parts[1])
        
        # 获取排期信息
        schedule = ScheduleService.get(db, schedule_id)
        if not schedule:
            raise HTTPException(status_code=404, detail="排期不存在")
        
        # 权限检查：考务人员
        if not current_user.is_superuser:
            raise HTTPException(status_code=403, detail="只有考务人员可以签到")
        
        # 检查排期状态
        if schedule.status == "已完成":
            raise HTTPException(status_code=400, detail="该排期已完成，无法签到")
        
        if schedule.status == "已取消":
            raise HTTPException(status_code=400, detail="该排期已取消，无法签到")
        
        # 检查是否已经签到
        if schedule.check_in_status == "已签到":
            raise HTTPException(status_code=400, detail="该考生已经签到")
        
        if schedule.check_in_status == "迟到":
            raise HTTPException(status_code=400, detail="该考生已标记为迟到")
        
        # 设置签到时间
        if check_in_time is None:
            check_in_time = datetime.now()
        
        # 执行签到（事务安全）
        result = ScheduleService.scan_check_in_with_transaction(
            db=db,
            schedule_id=schedule_id,
            check_in_time=check_in_time,
            notes=notes,
            operator_id=current_user.id
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return {
            "success": True,
            "message": "签到成功",
            "data": {
                "schedule_id": schedule_id,
                "candidate_name": result["candidate_name"],
                "exam_product_name": result["exam_product_name"],
                "check_in_time": check_in_time.isoformat(),
                "check_in_status": result["check_in_status"],
                "is_late": result["is_late"],
                "notes": notes,
                "operator": current_user.email
            }
        }
        
    except ValueError:
        raise HTTPException(status_code=400, detail="二维码中的排期ID格式错误")
    except HTTPException:
        # 重新抛出HTTPException，不包装为500错误
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"签到失败: {str(e)}")

@router.post("/batch-scan-check-in", response_model=dict)
def batch_scan_check_in(
    qr_codes: List[str] = Body(...),
    check_in_time: Optional[datetime] = Body(None),
    notes: Optional[str] = Body(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    """
    批量扫码签到API - 支持多个二维码同时签到
    
    参数:
    - qr_codes: 二维码内容列表
    - check_in_time: 签到时间（可选，默认为当前时间）
    - notes: 备注信息（可选）
    
    返回:
    - 批量签到结果
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="只有考务人员可以批量签到")
    
    if check_in_time is None:
        check_in_time = datetime.now()
    
    results = []
    success_count = 0
    error_count = 0
    
    for qr_code in qr_codes:
        try:
            # 解析二维码
            if not qr_code.startswith("SCHEDULE_"):
                results.append({
                    "qr_code": qr_code,
                    "success": False,
                    "error": "无效的二维码格式"
                })
                error_count += 1
                continue
            
            parts = qr_code.split("_")
            if len(parts) < 3:
                results.append({
                    "qr_code": qr_code,
                    "success": False,
                    "error": "二维码格式错误"
                })
                error_count += 1
                continue
            
            schedule_id = int(parts[1])
            
            # 执行单个签到
            result = ScheduleService.scan_check_in_with_transaction(
                db=db,
                schedule_id=schedule_id,
                check_in_time=check_in_time,
                notes=notes,
                operator_id=current_user.id
            )
            
            if result["success"]:
                results.append({
                    "qr_code": qr_code,
                    "success": True,
                    "data": {
                        "schedule_id": schedule_id,
                        "candidate_name": result["candidate_name"],
                        "exam_product_name": result["exam_product_name"],
                        "check_in_status": result["check_in_status"],
                        "is_late": result["is_late"]
                    }
                })
                success_count += 1
            else:
                results.append({
                    "qr_code": qr_code,
                    "success": False,
                    "error": result["error"]
                })
                error_count += 1
                
        except Exception as e:
            results.append({
                "qr_code": qr_code,
                "success": False,
                "error": str(e)
            })
            error_count += 1
    
    return {
        "success": True,
        "message": f"批量签到完成，成功: {success_count}，失败: {error_count}",
        "summary": {
            "total": len(qr_codes),
            "success_count": success_count,
            "error_count": error_count
        },
        "results": results
    }

@router.get("/check-in-stats", response_model=dict)
def get_check_in_stats(
    scheduled_date: Optional[datetime] = Query(None),
    venue_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    """
    获取签到统计信息
    
    参数:
    - scheduled_date: 排期日期（可选）
    - venue_id: 考场ID（可选）
    
    返回:
    - 签到统计信息
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="只有考务人员可以查看签到统计")
    
    stats = ScheduleService.get_check_in_stats(db, scheduled_date, venue_id)
    
    return {
        "success": True,
        "data": stats
    }

@router.post("/", response_model=ScheduleRead)
def create_schedule(
    schedule: ScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    """创建单个排期"""
    # 权限检查：考务管理员或机构用户
    if not current_user.is_superuser and not current_user.institution_id:
        raise HTTPException(status_code=403, detail="只有考务管理员或机构用户可以创建排期")
    
    created_schedule = ScheduleService.create(db, schedule, current_user.id)
    return created_schedule

@router.get("/", response_model=ScheduleListResponse)
def get_schedules(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    candidate_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    scheduled_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    """查询排期列表"""
    # 权限检查：考务管理员或机构用户
    if not current_user.is_superuser and not current_user.institution_id:
        raise HTTPException(status_code=403, detail="只有考务管理员或机构用户可以查看排期列表")
    
    skip = (page - 1) * size
    
    schedules = ScheduleService.get_multi(
        db, 
        skip=skip, 
        limit=size,
        candidate_id=candidate_id,
        status=status,
        scheduled_date=scheduled_date
    )
    
    total = ScheduleService.count(db, candidate_id=candidate_id)
    pages = (total + size - 1) // size
    
    return ScheduleListResponse(
        items=schedules,
        total=total,
        page=page,
        size=size,
        pages=pages
    )

@router.get("/{schedule_id}", response_model=ScheduleRead)
def get_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    """获取排期详情"""
    schedule = ScheduleService.get(db, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="排期不存在")
    
    # 权限检查：考务管理员或考生本人
    if not current_user.is_superuser and current_user.id != schedule.candidate_id:
        raise HTTPException(status_code=403, detail="权限不足")
    
    return schedule

@router.put("/{schedule_id}", response_model=ScheduleRead)
def update_schedule(
    schedule_id: int,
    schedule: ScheduleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    """更新排期信息"""
    # 权限检查：考务管理员
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="只有考务管理员可以更新排期")
    
    updated_schedule = ScheduleService.update(db, schedule_id, schedule)
    if not updated_schedule:
        raise HTTPException(status_code=404, detail="排期不存在")
    
    return updated_schedule

@router.delete("/{schedule_id}", status_code=204)
def delete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(current_active_user)
):
    """删除排期"""
    # 权限检查：考务管理员
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="只有考务管理员可以删除排期")
    
    success = ScheduleService.delete(db, schedule_id)
    if not success:
        raise HTTPException(status_code=404, detail="排期不存在") 