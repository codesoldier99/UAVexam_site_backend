from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    name: Optional[str] = None


class RoleRead(RoleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PermissionBase(BaseModel):
    name: str


class PermissionCreate(PermissionBase):
    pass


class PermissionRead(PermissionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class RolePermissionCreate(BaseModel):
    role_id: int
    permission_id: int


class RoleWithPermissions(RoleRead):
    permissions: List[PermissionRead] = [] 