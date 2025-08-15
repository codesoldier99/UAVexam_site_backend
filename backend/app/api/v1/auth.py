from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_async_db, get_current_user
from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.schemas.user import Token, LoginRequest, LoginResponse, User as UserSchema

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db)
):
    """用户登录"""
    # 查找用户
    result = await db.execute(
        select(User).where(User.username == form_data.username)
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserSchema.from_orm(user)
    )

@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return current_user

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """用户登出"""
    # 在实际应用中，这里可以将token加入黑名单
    return {"message": "Successfully logged out"}