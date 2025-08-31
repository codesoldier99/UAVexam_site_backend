"""
认证相关API路由
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import JWTError, jwt

from ..config.database import get_db
from ..config.settings import settings
from ..services.auth_service import AuthService
from ..utils.security import verify_password, create_access_token
from ..models.user import User
from ..schemas.auth import (
    UserLogin, UserRegister, TokenResponse, RefreshTokenRequest,
    UserInfo, RegisterResponse, LogoutResponse
)

router = APIRouter(prefix="/auth", tags=["认证"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@router.options("/login", summary="登录接口预检请求")
async def login_options():
    """处理登录接口的OPTIONS预检请求"""
    return {"message": "OK"}


@router.post("/login", response_model=TokenResponse, summary="用户登录")
async def login(
    user_login: UserLogin,
    db: Session = Depends(get_db)
):
    """用户登录获取JWT访问令牌（JSON格式）"""
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(user_login.username, user_login.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户账户已被禁用"
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id, "role": user.role.value},
        expires_delta=access_token_expires
    )
    
    # 构建基本响应
    response_data = {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes * 60,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "full_name": user.real_name
        }
    }
    
    # 如果是考生，添加考试安排信息
    if user.role.value == 'candidate':
        from ..services.wechat_service import WeChatService
        wechat_service = WeChatService(db)
        exam_schedules = wechat_service.get_candidate_exam_schedules(user.id)
        current_exam = exam_schedules[0] if exam_schedules else None
        
        response_data.update({
            "current_exam": current_exam.dict() if current_exam else None,
            "has_valid_schedule": len(exam_schedules) > 0
        })
    
    return response_data


@router.post("/token", summary="用户登录获取访问令牌（OAuth2兼容）")
async def login_oauth2(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """用户登录获取JWT访问令牌（OAuth2 form-data格式，用于兼容）"""
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户账户已被禁用"
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id, "role": user.role.value},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes * 60,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "full_name": user.real_name
        }
    }


@router.post("/register", response_model=RegisterResponse, summary="用户注册")
async def register(
    user_register: UserRegister,
    db: Session = Depends(get_db)
):
    """用户注册"""
    auth_service = AuthService(db)
    
    try:
        user = auth_service.create_user(
            username=user_register.username,
            password=user_register.password,
            email=user_register.email,
            real_name=user_register.full_name,  # 映射 full_name 到 real_name
            phone=user_register.phone
        )
        return {
            "message": "注册成功",
            "user_id": user.id,
            "username": user.username
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/me", response_model=UserInfo, summary="获取当前用户信息")
async def get_current_user_info(
    current_user: User = Depends(AuthService.get_current_user)
):
    """获取当前登录用户的详细信息"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "phone": current_user.phone,
        "full_name": current_user.real_name,  # 映射 real_name 到 full_name
        "role": current_user.role.value,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified,
        "institution_id": current_user.institution_id,
        "created_at": current_user.created_at,
        "last_login": current_user.last_login
    }


@router.post("/logout", response_model=LogoutResponse, summary="用户登出")
async def logout():
    """用户登出（实际上由于JWT无状态，主要在客户端删除token）"""
    return {"message": "登出成功"}


@router.post("/refresh", response_model=TokenResponse, summary="刷新访问令牌")
async def refresh_token(
    refresh_request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """刷新访问令牌"""
    # 验证refresh_token并获取用户信息
    try:
        payload = jwt.decode(refresh_request.refresh_token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的刷新令牌"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新令牌"
        )
    
    # 获取用户信息
    auth_service = AuthService(db)
    user = auth_service.get_user_by_id(user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在或已被禁用"
        )
    
    # 生成新的访问令牌
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id, "role": user.role.value},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes * 60,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "full_name": user.real_name
        }
    }