from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

# 导入路由
from src.routers import users, roles, permissions, exam_products, venues, candidates, schedules, public
from src.routers.schedule_enhanced import router as schedule_enhanced_router
from src.routers.qrcode_checkin import router as qrcode_router
from src.routers.wx_miniprogram import router as wx_router
from src.routers.institutions_simple import router as institutions_router
from src.routers.batch_operations import router as batch_router
from src.routers.realtime import router as realtime_router
from src.routers.rbac import router as rbac_router

# 创建FastAPI应用
app = FastAPI(
    title="考试系统后端API",
    description="考试系统后端API - 简化测试版本",
    version="1.0.0-test"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含所有路由 - 移除认证要求
app.include_router(institutions_router)  # 机构管理功能
app.include_router(batch_router)  # 批量操作功能
app.include_router(realtime_router)  # 实时功能
app.include_router(rbac_router)  # RBAC权限控制
app.include_router(venues.router)
app.include_router(exam_products.router)
app.include_router(candidates.router)
app.include_router(schedules.router)
app.include_router(schedule_enhanced_router)  # 增强版排期管理
app.include_router(qrcode_router)  # 二维码和签到功能
app.include_router(wx_router)  # 微信小程序功能
app.include_router(public.router)
app.include_router(roles.router)
app.include_router(permissions.router)
app.include_router(users.router)

@app.get("/")
async def read_root():
    return {"message": "欢迎使用考试系统后端API - 简化测试版本", "version": "1.0.0-test"}

@app.get("/test")
async def test_endpoint():
    return {"message": "测试成功", "status": "ok", "timestamp": datetime.now().isoformat()}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0-test",
        "service": "考试系统后端API - 简化测试版本"
    }
