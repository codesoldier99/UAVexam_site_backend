"""
PC前端专用API路由模块
"""

from .auth import router as pc_auth_router
from .dashboard import router as pc_dashboard_router
from .candidates import router as pc_candidates_router
from .checkins import router as pc_checkins_router

__all__ = [
    "pc_auth_router",
    "pc_dashboard_router", 
    "pc_candidates_router",
    "pc_checkins_router"
]
