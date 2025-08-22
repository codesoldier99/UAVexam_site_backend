"""
数据库模型模块 - 简化版本
"""

from .user import User, UserRole
from .institution import Institution
from .venue import Venue, VenueStatus
from .exam import ExamRegistration, ExamProduct
from .checkin import CheckIn
from .schedule import Schedule, ScheduleStatus

__all__ = [
    "User", "UserRole",
    "Institution", 
    "Venue", "VenueStatus",
    "ExamRegistration", "ExamProduct",
    "CheckIn",
    "Schedule", "ScheduleStatus"
]