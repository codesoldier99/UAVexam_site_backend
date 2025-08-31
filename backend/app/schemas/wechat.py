from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# 现有的模型保持不变...
class CandidateInfoByIdCardRequest(BaseModel):
    id_card: str = Field(..., description="身份证号")

class CandidateInfoResponse(BaseModel):
    id: int
    name: str
    id_card: str
    phone: Optional[str] = None
    email: Optional[str] = None
    status: str
    # 新增考试安排信息
    current_schedule_id: Optional[int] = None
    current_venue_id: Optional[int] = None
    exam_time: Optional[datetime] = None
    exam_end_time: Optional[datetime] = None
    venue_name: Optional[str] = None
    venue_address: Optional[str] = None
    exam_name: Optional[str] = None
    exam_type: Optional[str] = None
    exam_status: Optional[str] = None

class QRCodeRefreshRequest(BaseModel):
    """二维码刷新请求 - 不再需要candidate_id，从token获取"""
    pass  # 空请求体，用户ID从token中获取

class QRCodeRefreshResponse(BaseModel):
    qr_code: str = Field(..., description="新的二维码数据")
    expires_at: datetime = Field(..., description="过期时间")
    refresh_token: str = Field(..., description="刷新令牌")

class CheckinHistoryResponse(BaseModel):
    id: int
    schedule_id: int
    candidate_id: int
    venue_id: int
    venue_name: str
    venue_address: Optional[str] = None
    checkin_time: datetime
    exam_time: datetime
    exam_end_time: Optional[datetime] = None
    exam_type: Optional[str] = None
    exam_name: Optional[str] = None
    exam_result: Optional[str] = None
    status: str

class ExamResultResponse(BaseModel):
    schedule_id: int
    candidate_id: int
    exam_name: str
    exam_time: datetime
    exam_result: Optional[str] = None
    score: Optional[int] = None
    status: str
    venue_name: str

class VenueStatusResponse(BaseModel):
    id: int
    name: str
    address: Optional[str] = None
    capacity: int
    current_occupancy: int = 0
    status: str
    utilization_rate: float = 0.0

# 新增的模型

class ExamScheduleItem(BaseModel):
    """单个考试安排项"""
    schedule_id: int
    exam_name: str
    exam_time: datetime
    exam_end_time: Optional[datetime] = None
    exam_type: Optional[str] = None
    venue: Dict[str, Any]
    status: str  # scheduled, checked_in, in_progress, completed
    can_checkin: bool = False
    checkin_start_time: Optional[datetime] = None
    exam_result: Optional[str] = None
    score: Optional[int] = None

class CandidateScheduleResponse(BaseModel):
    """考生日程查询响应"""
    upcoming_exams: List[ExamScheduleItem]
    completed_exams: List[ExamScheduleItem]
    summary: Dict[str, Any]

class QRCodeGenerationResponse(BaseModel):
    """二维码生成响应"""
    qr_code: str = Field(..., description="Base64编码的二维码图片")
    backup_code: str = Field(..., description="6位数字备用码")
    expires_at: datetime = Field(..., description="过期时间")
    refresh_interval: int = Field(default=30, description="建议刷新间隔(秒)")
    qr_data: Dict[str, Any] = Field(..., description="二维码包含的数据")

class DashboardStatistics(BaseModel):
    """看板统计数据"""
    total_scheduled: int = 0
    checked_in: int = 0
    in_progress: int = 0
    completed: int = 0

class DashboardVenue(BaseModel):
    """看板考场信息"""
    id: int
    name: str
    address: Optional[str] = None
    capacity: int
    current_occupied: int = 0
    utilization_rate: float = 0.0
    status: str  # available, occupied, maintenance

class DashboardAnnouncement(BaseModel):
    """看板公告"""
    id: str
    title: str
    content: str
    type: str  # notice, maintenance, update
    priority: str  # high, medium, low
    created_at: datetime

class DashboardResponse(BaseModel):
    """公共看板响应"""
    statistics: DashboardStatistics
    venues: List[DashboardVenue]
    announcements: List[DashboardAnnouncement]
    system_status: Dict[str, Any]
    current_user: Optional[Dict[str, Any]] = None

# 缺失的登录相关类
class WeChatLoginRequest(BaseModel):
    """微信登录请求"""
    id_card: str = Field(..., description="身份证号")
    openid: Optional[str] = Field(None, description="微信openid")

class ExamScheduleInfo(BaseModel):
    """考试安排信息"""
    schedule_id: int
    venue_id: int
    exam_date: str
    exam_session: str  # morning/afternoon/evening
    start_time: str
    end_time: str
    venue_name: str
    venue_address: str
    exam_name: str
    exam_type: str
    registration_number: str
    status: str

class QRCodeData(BaseModel):
    """二维码数据结构"""
    candidate_id: int
    name: str
    id_card: str
    username: str
    schedule_id: int
    venue_id: int
    exam_session: str
    exam_date: str
    timestamp: int
    type: str = "candidate_checkin"

class WeChatLoginResponse(BaseModel):
    """微信登录响应"""
    access_token: str
    token_type: str = "bearer"
    user_info: Dict[str, Any]
    current_exam: Optional[ExamScheduleInfo] = None
    upcoming_exams: List[ExamScheduleInfo] = []
    has_valid_schedule: bool = False

# 缺失的签到相关类
class CheckInRequest(BaseModel):
    """签到请求 - 新格式，直接包含完整的考生和考试信息"""
    qr_code_data: str = Field(..., description="包含完整信息的二维码JSON字符串")

class CheckInResponse(BaseModel):
    """签到响应"""
    success: bool
    message: str
    checkin_time: datetime
    schedule_info: Dict[str, Any]

# 新增：手动签到相关模型

class ManualCheckinQueryRequest(BaseModel):
    """手动签到查询请求"""
    real_name: str = Field(..., description="考生姓名")
    id_card: str = Field(..., description="身份证号")

class ExamScheduleDetail(BaseModel):
    """考试安排详情"""
    schedule_id: int = Field(..., description="日程ID")
    exam_name: str = Field(..., description="考试名称")
    exam_type: str = Field(..., description="考试类型")
    venue_id: int = Field(..., description="考场ID")
    venue_name: str = Field(..., description="考场名称")
    venue_address: str = Field(..., description="考场地址")
    exam_date: str = Field(..., description="考试日期")
    start_time: str = Field(..., description="开始时间")
    end_time: str = Field(..., description="结束时间")
    status: str = Field(..., description="日程状态")
    registration_number: str = Field(..., description="报名号")
    can_checkin: bool = Field(..., description="是否可以签到")
    checkin_status: str = Field(..., description="签到状态")

class ManualCheckinQueryResponse(BaseModel):
    """手动签到查询响应"""
    candidate_info: Dict[str, Any] = Field(..., description="考生基本信息")
    exam_schedules: List[ExamScheduleDetail] = Field(..., description="考试安排列表")
    message: Optional[str] = Field(None, description="提示信息")

class ManualCheckinConfirmRequest(BaseModel):
    """手动签到确认请求"""
    candidate_id: int = Field(..., description="考生ID")
    schedule_id: int = Field(..., description="日程ID")
    operator_info: Optional[str] = Field(None, description="操作员信息")

class ManualCheckinConfirmResponse(BaseModel):
    """手动签到确认响应"""
    success: bool = Field(..., description="签到是否成功")
    message: str = Field(..., description="签到结果信息")
    checkin_info: Dict[str, Any] = Field(..., description="签到详情")
