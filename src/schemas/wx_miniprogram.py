from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time

class WxLoginRequest(BaseModel):
    """微信小程序登录请求"""
    code: str = Field(..., description="微信小程序wx.login()返回的code")
    id_card: str = Field(..., description="考生身份证号", min_length=18, max_length=18)

class WxLoginResponse(BaseModel):
    """微信小程序登录响应"""
    access_token: str = Field(..., description="JWT访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")
    candidate_id: int = Field(..., description="考生ID")
    candidate_name: str = Field(..., description="考生姓名")
    phone: Optional[str] = Field(None, description="考生手机号")
    status: str = Field(..., description="考生状态")

class QrCodeResponse(BaseModel):
    """二维码内容响应"""
    schedule_id: int = Field(..., description="日程ID")
    exam_date: date = Field(..., description="考试日期")
    start_time: time = Field(..., description="开始时间")
    end_time: time = Field(..., description="结束时间")
    venue_name: Optional[str] = Field(None, description="考场名称")
    exam_product_name: Optional[str] = Field(None, description="考试产品名称")

class VenueStatusResponse(BaseModel):
    """考场状态响应"""
    venue_id: int = Field(..., description="考场ID")
    venue_name: str = Field(..., description="考场名称")
    venue_address: Optional[str] = Field(None, description="考场地址")
    status: str = Field(..., description="状态：空闲/使用中")
    current_occupancy: int = Field(..., description="当前占用人数")
    total_capacity: int = Field(..., description="总容量")
    occupancy_rate: float = Field(..., description="占用率百分比")

class PublicVenuesStatusResponse(BaseModel):
    """公共看板考场状态响应"""
    timestamp: str = Field(..., description="时间戳")
    venues: list[VenueStatusResponse] = Field(..., description="考场状态列表") 