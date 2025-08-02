from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum
from fastapi_users import schemas

class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(schemas.BaseUserCreate):
    username: str
    role_id: int
    institution_id: Optional[int] = None

class UserRead(schemas.BaseUser[int]):
    username: str
    status: UserStatus
    role_id: int
    institution_id: Optional[int] = None
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None
    role_id: Optional[int] = None
    institution_id: Optional[int] = None
    status: Optional[UserStatus] = None

class UserLogin(BaseModel):
    username: str
    password: str
