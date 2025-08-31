"""
机构数据模式
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime


class InstitutionBase(BaseModel):
    """机构基础模式"""
    name: str = Field(..., description="机构名称", max_length=100)
    code: str = Field(..., description="机构代码", max_length=50)
    description: Optional[str] = Field(None, description="机构描述")
    contact_person: Optional[str] = Field(None, description="联系人", max_length=50)
    contact_phone: Optional[str] = Field(None, description="联系电话", max_length=20)
    contact_email: Optional[str] = Field(None, description="联系邮箱", max_length=100)
    address: Optional[str] = Field(None, description="地址")
    is_active: Optional[bool] = Field(True, description="是否启用")


class InstitutionCreate(InstitutionBase):
    """创建机构模式"""
    pass


class InstitutionUpdate(BaseModel):
    """更新机构模式"""
    name: Optional[str] = Field(None, description="机构名称", max_length=100)
    code: Optional[str] = Field(None, description="机构代码", max_length=50)
    description: Optional[str] = Field(None, description="机构描述")
    contact_person: Optional[str] = Field(None, description="联系人", max_length=50)
    contact_phone: Optional[str] = Field(None, description="联系电话", max_length=20)
    contact_email: Optional[str] = Field(None, description="联系邮箱", max_length=100)
    address: Optional[str] = Field(None, description="地址")
    is_active: Optional[bool] = Field(None, description="是否启用")


class InstitutionResponse(InstitutionBase):
    """机构响应模式"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class InstitutionList(BaseModel):
    """机构列表响应模式"""
    items: List[InstitutionResponse]
    total: int
    page: int
    size: int
    pages: int


class InstitutionStatistics(BaseModel):
    """机构统计信息模式"""
    total_institutions: int
    active_institutions: int
    inactive_institutions: int