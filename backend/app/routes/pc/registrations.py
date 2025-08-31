from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime

from ...config.database import get_db
from ...models.user import User, UserRole
from ...models.exam import ExamRegistration, ExamProduct
from ...models.schedule import Schedule
from ...models.venue import Venue
from ...services.auth_service import AuthService

router = APIRouter()

@router.get("/registrations")
async def get_registrations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),

    candidate_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取考试报名列表"""
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR]:
        raise HTTPException(status_code=403, detail="权限不足")
    
    try:
        query = db.query(ExamRegistration)
        
        # 根据用户角色过滤
        if current_user.role == UserRole.ADMIN and current_user.institution_id:
            # 通过用户的机构过滤
            query = query.join(User).filter(User.institution_id == current_user.institution_id)
        

        
        # 按考生过滤
        if candidate_id:
            query = query.filter(ExamRegistration.user_id == candidate_id)
        
        # 按状态过滤
        if status:
            query = query.filter(ExamRegistration.status == status)
        
        total = query.count()
        registrations = query.offset(skip).limit(limit).all()
        
        # 手动序列化，包含关联信息
        result = []
        for registration in registrations:
            registration_dict = {
                "id": registration.id,
                "user_id": registration.user_id,
                "exam_product_id": registration.exam_product_id,
                "registration_number": registration.registration_number,
                "registration_time": registration.created_at.isoformat() if registration.created_at else None,
                "status": registration.status.value if registration.status else None,
                "notes": registration.notes,
                "created_at": registration.created_at.isoformat() if registration.created_at else None,
                "updated_at": registration.updated_at.isoformat() if registration.updated_at else None,
                # 关联信息
                "candidate_name": registration.user.real_name if registration.user else None,
                "candidate_phone": registration.user.phone if registration.user else None,
                "exam_product_name": registration.exam_product.name if registration.exam_product else None,
                "exam_date": None,  # 需要通过Schedule表查询
                "venue_name": None  # 需要通过Schedule表查询
            }
            result.append(registration_dict)
        
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

@router.get("/registrations/statistics")
async def get_registration_statistics(
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取考试报名统计信息"""
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR]:
        raise HTTPException(status_code=403, detail="权限不足")
    
    try:
        query = db.query(ExamRegistration)
        
        # 根据用户角色过滤
        if current_user.role == UserRole.ADMIN and current_user.institution_id:
            query = query.join(User).filter(User.institution_id == current_user.institution_id)
        
        # 基础统计
        total_registrations = query.count()
        confirmed_registrations = query.filter(ExamRegistration.status == "confirmed").count()
        pending_registrations = query.filter(ExamRegistration.status == "pending").count()
        cancelled_registrations = query.filter(ExamRegistration.status == "cancelled").count()
        completed_registrations = query.filter(ExamRegistration.status == "completed").count()
        approved_registrations = query.filter(ExamRegistration.status == "approved").count()
        rejected_registrations = query.filter(ExamRegistration.status == "rejected").count()
        
        # 支付统计 - 由于数据库中没有支付状态字段，暂时返回0
        paid_registrations = 0
        unpaid_registrations = 0
        
        return {
            "total_registrations": total_registrations,
            "confirmed_registrations": confirmed_registrations,
            "pending_registrations": pending_registrations,
            "approved_registrations": approved_registrations,
            "rejected_registrations": rejected_registrations,
            "cancelled_registrations": cancelled_registrations,
            "completed_registrations": completed_registrations,
            "paid_registrations": paid_registrations,
            "unpaid_registrations": unpaid_registrations
        }
    except Exception as e:
        # 如果查询失败，返回默认统计
        return {
            "total_registrations": 0,
            "confirmed_registrations": 0,
            "pending_registrations": 0,
            "approved_registrations": 0,
            "rejected_registrations": 0,
            "cancelled_registrations": 0,
            "completed_registrations": 0,
            "paid_registrations": 0,
            "unpaid_registrations": 0
        }

@router.get("/registrations/{registration_id}")
async def get_registration(
    registration_id: int,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """获取考试报名详情"""
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR]:
        raise HTTPException(status_code=403, detail="权限不足")
    
    try:
        registration = db.query(ExamRegistration).filter(ExamRegistration.id == registration_id).first()
        if not registration:
            raise HTTPException(status_code=404, detail="考试报名不存在")
        
        # 权限检查 - 通过用户的机构检查
        if current_user.role == UserRole.ADMIN and current_user.institution_id:
            if registration.user and registration.user.institution_id != current_user.institution_id:
                raise HTTPException(status_code=403, detail="无权访问此考试报名")
        
        # 手动序列化
        return {
            "id": registration.id,
            "user_id": registration.user_id,
            "exam_product_id": registration.exam_product_id,
            "registration_number": registration.registration_number,
            "registration_time": registration.created_at.isoformat() if registration.created_at else None,
            "status": registration.status.value if registration.status else None,
            "notes": registration.notes,
            "created_at": registration.created_at.isoformat() if registration.created_at else None,
            "updated_at": registration.updated_at.isoformat() if registration.updated_at else None,
            # 详细关联信息
            "candidate": {
                "id": registration.user.id,
                "real_name": registration.user.real_name,
                "phone": registration.user.phone,
                "email": registration.user.email,
                "id_card": registration.user.id_card
            } if registration.user else None,
            "schedule": None,  # 需要单独查询Schedule表
            "exam_product": {
                "id": registration.exam_product.id,
                "name": registration.exam_product.name,
                "code": registration.exam_product.code,
                "duration_minutes": registration.exam_product.duration_minutes
            } if registration.exam_product else None
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取考试报名详情失败: {str(e)}")

@router.put("/registrations/{registration_id}/status")
async def update_registration_status(
    registration_id: int,
    status_data: dict,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """更新考试报名状态"""
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR]:
        raise HTTPException(status_code=403, detail="权限不足")
    
    try:
        registration = db.query(ExamRegistration).filter(ExamRegistration.id == registration_id).first()
        if not registration:
            raise HTTPException(status_code=404, detail="考试报名不存在")
        
        # 权限检查
        if current_user.role == UserRole.ADMIN and current_user.institution_id:
            if registration.user and registration.user.institution_id != current_user.institution_id:
                raise HTTPException(status_code=403, detail="无权修改此考试报名")
        
        # 更新状态
        if "status" in status_data:
            registration.status = status_data["status"]

        if "notes" in status_data:
            registration.notes = status_data["notes"]
        
        db.commit()
        
        return {"message": "考试报名状态更新成功"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"更新考试报名状态失败: {str(e)}")

@router.delete("/registrations/{registration_id}")
async def cancel_registration(
    registration_id: int,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """取消考试报名"""
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="权限不足")
    
    try:
        registration = db.query(ExamRegistration).filter(ExamRegistration.id == registration_id).first()
        if not registration:
            raise HTTPException(status_code=404, detail="考试报名不存在")
        
        # 权限检查
        if current_user.role == UserRole.ADMIN and current_user.institution_id:
            if registration.user and registration.user.institution_id != current_user.institution_id:
                raise HTTPException(status_code=403, detail="无权取消此考试报名")
        
        # 检查是否可以取消
        if registration.status == "COMPLETED":
            raise HTTPException(status_code=400, detail="已完成的考试报名无法取消")
        
        # 更新为取消状态
        registration.status = "CANCELLED"
        
        # 注意：如果需要更新考试安排的报名人数，需要单独查询Schedule表
        
        db.commit()
        
        return {"message": "考试报名取消成功"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"取消考试报名失败: {str(e)}")

@router.get("/registrations/statistics")
async def get_registration_statistics(
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取考试报名统计信息"""
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR]:
        raise HTTPException(status_code=403, detail="权限不足")
    
    try:
        query = db.query(ExamRegistration)
        
        # 根据用户角色过滤 - 通过用户的机构ID过滤
        if current_user.role == UserRole.ADMIN and current_user.institution_id:
            query = query.join(User).filter(User.institution_id == current_user.institution_id)
        
        total_registrations = query.count()
        confirmed_registrations = query.filter(ExamRegistration.status == "confirmed").count()
        pending_registrations = query.filter(ExamRegistration.status == "pending").count()
        cancelled_registrations = query.filter(ExamRegistration.status == "cancelled").count()
        completed_registrations = query.filter(ExamRegistration.status == "completed").count()
        approved_registrations = query.filter(ExamRegistration.status == "approved").count()
        rejected_registrations = query.filter(ExamRegistration.status == "rejected").count()
        
        # 支付统计 - 由于数据库中没有支付状态字段，暂时返回0
        paid_registrations = 0
        unpaid_registrations = 0
        
        return {
            "total_registrations": total_registrations,
            "confirmed_registrations": confirmed_registrations,
            "pending_registrations": pending_registrations,
            "approved_registrations": approved_registrations,
            "rejected_registrations": rejected_registrations,
            "cancelled_registrations": cancelled_registrations,
            "completed_registrations": completed_registrations,
            "paid_registrations": paid_registrations,
            "unpaid_registrations": unpaid_registrations
        }
    except Exception as e:
        # 如果查询失败，返回默认统计
        return {
            "total_registrations": 0,
            "confirmed_registrations": 0,
            "pending_registrations": 0,
            "approved_registrations": 0,
            "rejected_registrations": 0,
            "cancelled_registrations": 0,
            "completed_registrations": 0,
            "paid_registrations": 0,
            "unpaid_registrations": 0
        }

@router.post("/registrations/batch-confirm")
async def batch_confirm_registrations(
    registration_ids: List[int],
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """批量确认考试报名"""
    # 权限检查
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="权限不足")
    
    # 参数验证
    if not registration_ids:
        raise HTTPException(status_code=400, detail="报名ID列表不能为空")
    
    try:
        confirmed_count = 0
        failed_count = 0
        
        for registration_id in registration_ids:
            registration = db.query(ExamRegistration).filter(ExamRegistration.id == registration_id).first()
            if registration and registration.status == "PENDING":
                # 权限检查
                if current_user.role == UserRole.ADMIN and current_user.institution_id:
                    if registration.user and registration.user.institution_id != current_user.institution_id:
                        failed_count += 1
                        continue
                
                registration.status = "CONFIRMED"
                confirmed_count += 1
            else:
                failed_count += 1
        
        db.commit()
        
        return {
            "message": f"批量确认完成",
            "confirmed_count": confirmed_count,
            "failed_count": failed_count
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"批量确认考试报名失败: {str(e)}")