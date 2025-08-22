"""
认证相关的Pydantic模型
"""

from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime


class UserLogin(BaseModel):
    """用户登录请求模型"""
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "password": "admin123"
            }
        }


class UserRegister(BaseModel):
    """用户注册请求模型"""
    username: str
    email: EmailStr
    password: str
    full_name: str  # 与API文档保持一致
    phone: Optional[str] = None

    @validator('username')
    def username_must_be_valid(cls, v):
        if len(v) < 3:
            raise ValueError('用户名长度至少3个字符')
        return v

    @validator('password')
    def password_must_be_valid(cls, v):
        if len(v) < 6:
            raise ValueError('密码长度至少6个字符')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123",
                "full_name": "测试用户",
                "phone": "13800138000"
            }
        }


class TokenResponse(BaseModel):
    """令牌响应模型"""
    access_token: str
    token_type: str
    expires_in: int
    user: dict

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 691200,
                "user": {
                    "id": 1,
                    "username": "admin",
                    "email": "admin@example.com",
                    "role": "admin",
                    "full_name": "管理员"
                }
            }
        }


class RefreshTokenRequest(BaseModel):
    """刷新令牌请求模型"""
    refresh_token: str

    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


class UserInfo(BaseModel):
    """用户信息响应模型"""
    id: int
    username: str
    email: Optional[str]
    phone: Optional[str]
    full_name: Optional[str]
    role: str
    is_active: bool
    is_verified: bool
    institution_id: Optional[int]
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "admin",
                "email": "admin@example.com",
                "phone": "13800138000",
                "full_name": "管理员",
                "role": "admin",
                "is_active": True,
                "is_verified": True,
                "institution_id": None,
                "created_at": "2024-01-01T00:00:00",
                "last_login": "2024-01-01T12:00:00"
            }
        }


class RegisterResponse(BaseModel):
    """注册响应模型"""
    message: str
    user_id: int
    username: str

    class Config:
        json_schema_extra = {
            "example": {
                "message": "注册成功",
                "user_id": 1,
                "username": "testuser"
            }
        }


class LogoutResponse(BaseModel):
    """登出响应模型"""
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "message": "登出成功"
            }
        }
