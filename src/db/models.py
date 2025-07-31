# 导入所有模型，确保 Alembic 能够检测到
from src.models.user import User
from src.institutions.models import Institution

__all__ = ["User", "Institution"] 