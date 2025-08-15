from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None

# Permission schemas
class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None
    resource: Optional[str] = None
    action: Optional[str] = None

class PermissionCreate(PermissionBase):
    pass

class Permission(PermissionBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Role schemas
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    permission_ids: Optional[List[int]] = []

class Role(RoleBase):
    id: int
    created_at: datetime
    permissions: List[Permission] = []
    
    class Config:
        from_attributes = True

# User schemas
class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = True
    role_id: Optional[int] = None
    institution_id: Optional[int] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None
    role_id: Optional[int] = None
    institution_id: Optional[int] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime]
    role: Optional[Role] = None
    
    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str

# Login schemas
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: User