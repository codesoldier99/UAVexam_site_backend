from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import decode_token
from app.db.session import get_async_db, get_db
from app.models.user import User
from app.schemas.user import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_current_user(
    db: AsyncSession = Depends(get_async_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")
    user_id: int = payload.get("user_id")
    if username is None or user_id is None:
        raise credentials_exception
    
    # 从数据库获取用户
    from sqlalchemy import select
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    return user

async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """获取当前超级用户"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

async def get_current_exam_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """获取考务管理员"""
    if not current_user.is_superuser and current_user.role_id != 2:  # 2 = 考务管理员
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

async def get_current_institution_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """获取机构用户"""
    if not current_user.institution_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not an institution user"
        )
    return current_user