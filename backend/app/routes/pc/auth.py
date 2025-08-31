"""
PC前端认证API路由
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...config.database import get_db
from ...config.settings import settings
from ...services.auth_service import AuthService
from ...models.user import User, UserRole
from ...schemas.auth import UserLogin, TokenResponse, UserInfo, ChangePasswordRequest
from ...utils.security import create_access_token, verify_password
from datetime import timedelta

router = APIRouter()


@router.post("/login", response_model=TokenResponse, summary="PC端用户登录")
async def pc_login(
    user_login: UserLogin,
    db: Session = Depends(get_db)
):
    """PC端用户登录 - 仅限管理员、操作员、监考员"""
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(user_login.username, user_login.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # PC端允许所有角色用户登录（包括考生）
    # 注释掉角色限制，允许所有用户登录PC端
    # allowed_roles = [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR, UserRole.EXAMINER]
    # if user.role not in allowed_roles:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="该账户无权限访问PC管理端"
    #     )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户账户已被禁用"
        )
    
    # 生成访问令牌 - PC端设置更长的过期时间（8小时）
    access_token_expires = timedelta(hours=8)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id, "role": user.role.value},
        expires_delta=access_token_expires
    )
    
    # 构建响应数据（与原有接口格式保持一致）
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 8 * 60 * 60,  # 8小时，以秒为单位
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "full_name": user.real_name,
            "institution_id": user.institution_id,
            "is_active": user.is_active
        }
    }


@router.get("/profile", summary="获取当前用户信息")
async def get_pc_user_profile(
    current_user: User = Depends(AuthService.get_current_user)
):
    """获取PC端当前登录用户信息"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "real_name": current_user.real_name,
        "role": current_user.role.value,
        "institution_id": current_user.institution_id,
        "is_active": current_user.is_active
    }


@router.put("/profile", summary="更新用户资料")
async def update_pc_user_profile(
    profile_data: dict,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """更新PC端用户资料"""
    # 获取允许更新的字段
    allowed_fields = ['real_name', 'email', 'phone']
    update_data = {k: v for k, v in profile_data.items() if k in allowed_fields and v is not None}
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="没有提供有效的更新数据"
        )
    
    # 检查邮箱是否已被其他用户使用
    if 'email' in update_data:
        existing_user = db.query(User).filter(
            User.email == update_data['email'],
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该邮箱已被其他用户使用"
            )
    
    # 检查手机号是否已被其他用户使用
    if 'phone' in update_data:
        existing_user = db.query(User).filter(
            User.phone == update_data['phone'],
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该手机号已被其他用户使用"
            )
    
    # 更新用户信息
    try:
        for field, value in update_data.items():
            setattr(current_user, field, value)
        
        # 更新时间戳
        from datetime import datetime
        current_user.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(current_user)
        
        return {
            "success": True,
            "message": "用户资料更新成功",
            "data": {
                "id": current_user.id,
                "real_name": current_user.real_name,
                "email": current_user.email,
                "phone": current_user.phone,
                "updated_at": current_user.updated_at.isoformat() if current_user.updated_at else None
            }
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新用户资料失败: {str(e)}"
        )


@router.post("/logout", summary="PC端用户登出")
async def pc_logout():
    """PC端用户登出"""
    return {"message": "登出成功"}


@router.post("/change-password", summary="修改密码")
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """修改当前用户密码"""
    # 验证新密码和确认密码是否匹配
    if password_data.new_password != password_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="新密码和确认密码不匹配"
        )
    
    # 验证新密码长度
    if len(password_data.new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="新密码长度不能少于6位"
        )
    
    auth_service = AuthService(db)
    
    # 验证当前密码
    if not verify_password(password_data.old_password, str(current_user.password_hash)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="当前密码错误"
        )
    
    # 修改密码
    success = auth_service.change_user_password(int(current_user.id), password_data.new_password)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="密码修改失败"
        )
    
    return {
        "success": True,
        "message": "密码修改成功"
    }