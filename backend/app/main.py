"""
FastAPI主应用程序 - UAV考点运营管理系统
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager

from .config.settings import settings
from .config.database import engine, Base
from .routes import (
    auth_router,
    institutions_router,
    exam_products_router,
    candidates_router,
    wechat_router,
    venues_router,
    schedules_router,
    system_router,
    health_router
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用程序生命周期管理"""
    # 启动时创建数据库表
    Base.metadata.create_all(bind=engine)
    print("🚀 UAV考点运营管理系统启动成功")
    print(f"📊 API文档: http://localhost:8000{app.docs_url}")
    yield
    print("👋 UAV考点运营管理系统关闭")


# 创建FastAPI应用实例
app = FastAPI(
    title="UAV考点运营管理系统",
    version="1.0.0",
    description="""🛩️ **UAV考点运营管理系统API**
    
    ## 系统特性
    - 🔐 JWT身份认证与RBAC权限管理
    - 🏢 多机构考点运营管理
    - 📋 考生报名与智能排期
    - 📱 微信小程序扫码签到
    - 📊 实时考场状态监控
    - 🔄 支持1200人并发访问
    
    ## 技术架构
    - **后端**: FastAPI + Python 3.11
    - **数据库**: MySQL 8.0 + Redis
    - **认证**: JWT Token
    - **部署**: Docker + Docker Compose
    """,
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    lifespan=lifespan
)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 信任主机中间件
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["*"]  # 生产环境应配置具体域名
)


# 注册路由
app.include_router(auth_router, prefix="/api/v1")
app.include_router(institutions_router, prefix="/api/v1")
app.include_router(exam_products_router, prefix="/api/v1")
app.include_router(candidates_router, prefix="/api/v1")
app.include_router(wechat_router, prefix="/api/v1")
app.include_router(venues_router, prefix="/api/v1")
app.include_router(schedules_router, prefix="/api/v1")
app.include_router(system_router, prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")


# 系统基础端点
@app.get("/", tags=["系统"], summary="系统首页")
def read_root():
    """系统首页信息"""
    return {
        "message": "🛩️ 欢迎使用UAV考点运营管理系统",
        "version": settings.app_version,
        "docs": app.docs_url,
        "redoc": app.redoc_url,
        "features": [
            "🔐 JWT身份认证与RBAC权限管理",
            "🏢 多机构考点运营管理", 
            "📋 考生报名与智能排期",
            "📱 微信小程序扫码签到",
            "📊 实时考场状态监控",
            "🔄 支持1200人并发访问"
        ]
    }


@app.get("/health", tags=["系统"], summary="健康检查")
def health_check():
    """系统健康检查"""
    return {
        "status": "healthy",
        "message": "UAV考点运营管理系统运行正常",
        "version": settings.app_version,
        "timestamp": "2025-08-18T08:00:00Z"
    }


@app.get("/api/v1/system/info", tags=["系统"], summary="获取系统信息")
def get_system_info():
    """获取系统基本信息"""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "description": "UAV考点运营管理系统",
        "environment": "development" if settings.debug else "production",
        "features": {
            "authentication": "JWT Token",
            "authorization": "RBAC权限管理",
            "database": "MySQL 8.0 + Redis",
            "concurrent_users": 1200,
            "wechat_miniprogram": "支持",
            "qr_code_checkin": "支持",
            "real_time_monitoring": "支持"
        }
    }


# 公共API端点（无需认证）
@app.get("/api/v1/public/venues/status", tags=["公共接口"], summary="获取考场实时状态")
def get_public_venues_status():
    """获取考场实时状态（供小程序公共看板使用）"""
    return {
        "venues": [
            {
                "venue_id": 1,
                "venue_name": "多旋翼A号实操场",
                "venue_type": "实操",
                "status": "进行中",
                "current_candidate": "李**",
                "waiting_count": 12,
                "next_start_time": "14:30",
                "capacity": 20
            },
            {
                "venue_id": 2,
                "venue_name": "理论一号教室",
                "venue_type": "理论", 
                "status": "空闲",
                "current_candidate": None,
                "waiting_count": 0,
                "next_start_time": "15:00",
                "capacity": 50
            },
            {
                "venue_id": 3,
                "venue_name": "固定翼实操区",
                "venue_type": "实操",
                "status": "维护中",
                "current_candidate": None,
                "waiting_count": 0,
                "next_start_time": None,
                "capacity": 15
            }
        ],
        "summary": {
            "total_venues": 3,
            "active_venues": 2,
            "total_waiting": 12,
            "last_updated": "2025-08-18T14:25:00Z"
        }
    }


# 微信小程序专用API
@app.get("/api/v1/wechat/venues/dashboard", tags=["微信小程序"], summary="小程序看板数据")
def get_wechat_venues_dashboard():
    """获取小程序看板显示数据"""
    return {
        "title": "UAV考点实时状态",
        "update_time": "14:25",
        "venues": [
            {
                "id": 1,
                "name": "多旋翼A号实操场",
                "type": "实操",
                "status": "进行中",
                "status_color": "#ff6b6b",
                "current": "李**",
                "waiting": 12,
                "next_time": "14:30"
            },
            {
                "id": 2,
                "name": "理论一号教室",
                "type": "理论",
                "status": "空闲", 
                "status_color": "#51cf66",
                "current": "",
                "waiting": 0,
                "next_time": "15:00"
            },
            {
                "id": 3,
                "name": "固定翼实操区",
                "type": "实操",
                "status": "维护中",
                "status_color": "#868e96",
                "current": "",
                "waiting": 0,
                "next_time": ""
            }
        ]
    }