from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base

# 使用SQLite进行测试
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_test_db():
    """初始化测试数据库"""
    Base.metadata.create_all(bind=engine)
    print("Test database created successfully!")