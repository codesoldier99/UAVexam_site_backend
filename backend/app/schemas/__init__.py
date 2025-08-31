"""
数据模式模块
"""

from .exam_product import ExamProductCreate, ExamProductUpdate, ExamProductResponse, ExamProductList
from .candidate import CandidateCreate, CandidateUpdate, CandidateResponse, CandidateList, BatchImportResult, CandidateStatistics
from .wechat import (
    CandidateInfoByIdCardRequest, CandidateInfoResponse, 
    QRCodeRefreshRequest, QRCodeRefreshResponse,
    CheckinHistoryResponse, ExamResultResponse, VenueStatusResponse,
    ExamScheduleItem, CandidateScheduleResponse, 
    QRCodeGenerationResponse, DashboardStatistics, 
    DashboardVenue, DashboardAnnouncement, DashboardResponse,
    WeChatLoginRequest, WeChatLoginResponse,
    CheckInRequest, CheckInResponse
)

__all__ = [
    "ExamProductCreate", "ExamProductUpdate", "ExamProductResponse", "ExamProductList",
    "CandidateCreate", "CandidateUpdate", "CandidateResponse", "CandidateList", "BatchImportResult", "CandidateStatistics",
    "CandidateInfoByIdCardRequest", "CandidateInfoResponse", 
    "QRCodeRefreshRequest", "QRCodeRefreshResponse",
    "CheckinHistoryResponse", "ExamResultResponse", "VenueStatusResponse",
    "ExamScheduleItem", "CandidateScheduleResponse", 
    "QRCodeGenerationResponse", "DashboardStatistics", 
    "DashboardVenue", "DashboardAnnouncement", "DashboardResponse",
    "WeChatLoginRequest", "WeChatLoginResponse",
    "CheckInRequest", "CheckInResponse"
]
