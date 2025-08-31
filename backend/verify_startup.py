#!/usr/bin/env python3
"""
验证后端启动脚本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def verify_imports():
    """验证所有导入是否正常"""
    try:
        print("🔍 验证核心模块导入...")
        from app.config.database import get_db
        print("✅ 数据库配置导入成功")
        
        from app.models.user import User, UserRole
        print("✅ 用户模型导入成功")
        
        from app.models.checkin import CheckIn
        print("✅ 签到模型导入成功")
        
        from app.models.schedule import Schedule
        print("✅ 日程模型导入成功")
        
        from app.models.exam import ExamRegistration
        print("✅ 考试模型导入成功")
        
        print("\n🔍 验证PC端路由导入...")
        from app.routes.pc.system import router as pc_system_router
        print("✅ 系统管理路由导入成功")
        
        from app.routes.pc.reports import router as pc_reports_router
        print("✅ 报表分析路由导入成功")
        
        from app.routes.pc.notifications import router as pc_notifications_router
        print("✅ 通知管理路由导入成功")
        
        print("\n🔍 验证主应用导入...")
        from app.main import app
        print("✅ 主应用导入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def main():
    print("=" * 60)
    print("🚀 UAV考点运营管理系统 - 后端启动验证")
    print("=" * 60)
    
    if verify_imports():
        print("\n" + "=" * 60)
        print("🎉 所有验证通过！后端可以正常启动")
        print("💡 可以运行以下命令启动后端:")
        print("   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
        print("=" * 60)
        return True
    else:
        print("\n" + "=" * 60)
        print("❌ 验证失败！请检查导入错误")
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)