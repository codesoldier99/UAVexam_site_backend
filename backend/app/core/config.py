from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "UAV Exam Management System"
    APP_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    
    # Database - Use SQLite for testing if MySQL not available
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
    SYNC_DATABASE_URL: str = os.getenv("SYNC_DATABASE_URL", "sqlite:///./test.db")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173", "http://localhost:8080"]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode='before')
    @classmethod
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, str):
            return eval(v)
        return v
    
    # Redis
    REDIS_URL: Optional[str] = None
    
    # WeChat
    WECHAT_APP_ID: Optional[str] = None
    WECHAT_APP_SECRET: Optional[str] = None
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Super Admin (初始超级管理员)
    FIRST_SUPERUSER: str = "admin"
    FIRST_SUPERUSER_PASSWORD: str = "admin123"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()