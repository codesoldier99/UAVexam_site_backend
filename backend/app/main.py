from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, candidates, schedules
from app.db.session import async_engine
from app.db.base_class import Base
import asyncio

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# 配置CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# 注册路由
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(candidates.router, prefix=f"{settings.API_V1_STR}/candidates", tags=["candidates"])
app.include_router(schedules.router, prefix=f"{settings.API_V1_STR}/schedules", tags=["schedules"])

@app.on_event("startup")
async def startup_event():
    """启动时创建数据库表"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}