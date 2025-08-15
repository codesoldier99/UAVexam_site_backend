from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

# 检测数据库类型
is_sqlite = settings.DATABASE_URL.startswith('sqlite')

# Async engine for main operations
if is_sqlite:
    async_engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        connect_args={"check_same_thread": False}
    )
else:
    async_engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        pool_size=20,
        max_overflow=40
    )

# Sync engine for migrations and initial setup
if is_sqlite:
    sync_engine = create_engine(
        settings.SYNC_DATABASE_URL,
        echo=settings.DEBUG,
        connect_args={"check_same_thread": False}
    )
else:
    sync_engine = create_engine(
        settings.SYNC_DATABASE_URL,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        pool_size=20,
        max_overflow=40
    )

# Async session
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Sync session
SessionLocal = sessionmaker(
    sync_engine,
    autocommit=False,
    autoflush=False
)

# Dependency
async def get_async_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()