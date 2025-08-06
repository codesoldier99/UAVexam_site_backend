from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class VenueStatus(str, Enum):
    active = "active"
    inactive = "inactive"

class VenueType(str, Enum):
    theory = "理论考场"
    practical = "实操考场"
    waiting = "候考区"

class VenueBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="考场名称")
    type: str = Field(..., description="考场类型")
    address: Optional[str] = Field(None, max_length=255, description="考场地址")
    description: Optional[str] = Field(None, description="考场描述")
    capacity: int = Field(..., ge=0, le=1000, description="容纳人数")
    contact_person: Optional[str] = Field(None, max_length=50, description="联系人")
    contact_phone: Optional[str] = Field(None, max_length=20, description="联系电话")
    equipment_info: Optional[str] = Field(None, description="设备信息")

class VenueCreate(VenueBase):
    is_active: bool = Field(True, description="是否激活")

class VenueRead(VenueBase):
    id: int
    is_active: bool
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class VenueUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="考场名称")
    type: Optional[str] = Field(None, description="考场类型")
    address: Optional[str] = Field(None, max_length=255, description="考场地址")
    description: Optional[str] = Field(None, description="考场描述")
    capacity: Optional[int] = Field(None, ge=0, le=1000, description="容纳人数")
    is_active: Optional[bool] = Field(None, description="是否激活")
    status: Optional[VenueStatus] = Field(None, description="状态")
    contact_person: Optional[str] = Field(None, max_length=50, description="联系人")
    contact_phone: Optional[str] = Field(None, max_length=20, description="联系电话")
    equipment_info: Optional[str] = Field(None, description="设备信息")

class VenueListResponse(BaseModel):
    items: List[VenueRead]
    total: int
    page: int
    size: int
    pages: int

class VenueResponse(BaseModel):
    """标准响应格式"""
    code: int = Field(200, description="状态码")
    message: str = Field("success", description="响应信息")
    data: Optional[VenueRead] = Field(None, description="响应数据")

class VenueListResponseWrapper(BaseModel):
    """列表响应格式"""
    code: int = Field(200, description="状态码")
    message: str = Field("success", description="响应信息")
    data: VenueListResponse = Field(..., description="响应数据")

class VenueBatchStatusUpdate(BaseModel):
    """批量状态更新请求"""
    venue_ids: List[int] = Field(..., description="考场ID列表", min_items=1)
    new_status: VenueStatus = Field(..., description="新状态") 