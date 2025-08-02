# 导入所有模型，确保 Alembic 能够检测到
from src.models.user import User
from src.institutions.models import Institution
from src.models.exam_product import ExamProduct
from src.models.venue import Venue
from src.models.candidate import Candidate
from src.models.schedule import Schedule
from src.models.role import Role
from src.models.permission import Permission, RolePermission

__all__ = [
    "User", 
    "Institution", 
    "ExamProduct", 
    "Venue", 
    "Candidate", 
    "Schedule",
    "Role",
    "Permission", 
    "RolePermission"
] 