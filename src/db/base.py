from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 导入所有模型，确保 Alembic 能够检测到
__all__ = ["Base"]
