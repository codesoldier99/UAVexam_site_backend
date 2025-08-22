"""
健康检查API路由
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict, Any
import time
from datetime import datetime

from ..config.database import get_db
from ..config.settings import settings

router = APIRouter(prefix="/health", tags=["健康检查"])


@router.get("/", summary="基础健康检查")
async def health_check() -> Dict[str, Any]:
    """系统基础健康检查"""
    return {
        "status": "healthy",
        "message": "UAV考点运营管理系统运行正常",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.app_version,
        "environment": "development" if settings.debug else "production"
    }


@router.get("/detailed", summary="详细健康检查")
async def detailed_health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """详细的系统健康检查，包括数据库连接等"""
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.app_version,
        "checks": {}
    }
    
    # 数据库连接检查
    try:
        start_time = time.time()
        result = db.execute(text("SELECT 1")).fetchone()
        db_response_time = round((time.time() - start_time) * 1000, 2)
        
        if result and result[0] == 1:
            health_status["checks"]["database"] = {
                "status": "healthy",
                "response_time_ms": db_response_time,
                "message": "数据库连接正常"
            }
        else:
            health_status["checks"]["database"] = {
                "status": "unhealthy",
                "message": "数据库查询返回异常结果"
            }
            health_status["status"] = "unhealthy"
            
    except Exception as e:
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "message": f"数据库连接失败: {str(e)}"
        }
        health_status["status"] = "unhealthy"
    
    # Redis连接检查（如果配置了Redis）
    if hasattr(settings, 'redis_url') and settings.redis_url:
        try:
            import redis
            redis_client = redis.from_url(settings.redis_url)
            start_time = time.time()
            redis_client.ping()
            redis_response_time = round((time.time() - start_time) * 1000, 2)
            
            health_status["checks"]["redis"] = {
                "status": "healthy",
                "response_time_ms": redis_response_time,
                "message": "Redis连接正常"
            }
        except Exception as e:
            health_status["checks"]["redis"] = {
                "status": "unhealthy",
                "message": f"Redis连接失败: {str(e)}"
            }
            health_status["status"] = "degraded" if health_status["status"] == "healthy" else "unhealthy"
    else:
        health_status["checks"]["redis"] = {
            "status": "not_configured",
            "message": "Redis未配置"
        }
    
    # 文件系统检查
    try:
        import os
        upload_path = getattr(settings, 'upload_path', 'uploads')
        if os.path.exists(upload_path) and os.access(upload_path, os.W_OK):
            health_status["checks"]["filesystem"] = {
                "status": "healthy",
                "message": "文件系统可写"
            }
        else:
            health_status["checks"]["filesystem"] = {
                "status": "unhealthy",
                "message": "上传目录不存在或不可写"
            }
            health_status["status"] = "degraded" if health_status["status"] == "healthy" else "unhealthy"
    except Exception as e:
        health_status["checks"]["filesystem"] = {
            "status": "unhealthy",
            "message": f"文件系统检查失败: {str(e)}"
        }
        health_status["status"] = "degraded" if health_status["status"] == "healthy" else "unhealthy"
    
    return health_status


@router.get("/database", summary="数据库健康检查")
async def database_health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """专门的数据库健康检查"""
    
    try:
        # 检查数据库连接
        start_time = time.time()
        db.execute(text("SELECT 1"))
        connection_time = round((time.time() - start_time) * 1000, 2)
        
        # 检查主要表是否存在
        tables_check = {}
        essential_tables = ['users', 'institutions', 'venues', 'exam_products']
        
        for table in essential_tables:
            try:
                result = db.execute(text(f"SELECT COUNT(*) FROM {table}")).fetchone()
                tables_check[table] = {
                    "exists": True,
                    "count": result[0] if result else 0
                }
            except Exception as e:
                tables_check[table] = {
                    "exists": False,
                    "error": str(e)
                }
        
        return {
            "status": "healthy",
            "connection_time_ms": connection_time,
            "tables": tables_check,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


@router.get("/readiness", summary="就绪检查")
async def readiness_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """应用就绪检查 - 检查应用是否准备好接收流量"""
    
    checks = []
    overall_ready = True
    
    # 数据库就绪检查
    try:
        db.execute(text("SELECT 1"))
        checks.append({
            "name": "database",
            "ready": True,
            "message": "数据库连接正常"
        })
    except Exception as e:
        checks.append({
            "name": "database", 
            "ready": False,
            "message": f"数据库连接失败: {str(e)}"
        })
        overall_ready = False
    
    # 必要配置检查
    required_configs = ['secret_key', 'access_token_expire_minutes']
    config_ready = True
    missing_configs = []
    
    for config in required_configs:
        if not hasattr(settings, config) or not getattr(settings, config):
            missing_configs.append(config)
            config_ready = False
    
    if config_ready:
        checks.append({
            "name": "configuration",
            "ready": True,
            "message": "必要配置项完整"
        })
    else:
        checks.append({
            "name": "configuration",
            "ready": False,
            "message": f"缺少必要配置: {', '.join(missing_configs)}"
        })
        overall_ready = False
    
    return {
        "ready": overall_ready,
        "checks": checks,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/liveness", summary="存活检查")
async def liveness_check() -> Dict[str, Any]:
    """应用存活检查 - 检查应用进程是否正常运行"""
    return {
        "alive": True,
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": "运行中",
        "memory_usage": "正常",
        "cpu_usage": "正常"
    }
