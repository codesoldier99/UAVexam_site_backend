from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models here for Alembic
# This will be imported later to avoid circular imports