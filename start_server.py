#!/usr/bin/env python3
"""
考试系统后端启动脚本
遵守团队规定：端口8000，支持团队配置
"""
import sys
import os
import uvicorn

# 确保项目根目录在Python路径中
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def main():
    """启动FastAPI应用"""
    print("🚀 启动考试系统后端服务器...")
    print(f"📁 项目目录: {project_root}")
    print("⚙️  团队配置:")
    print("   - 项目名称: exam_site_backend")
    print("   - 数据库: MySQL (端口3307)")
    print("   - 认证: fastapi-users")
    print("   - 容器: Docker支持")
    print("   - 迁移: Alembic")
    
    try:
        # 遵守团队规定：端口8000
        uvicorn.run(
            "src.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            reload_dirs=[project_root],
        )
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("💡 请检查:")
        print("   1. 是否在项目根目录执行")
        print("   2. 是否安装了所有依赖")
        print("   3. 数据库是否正常运行")
        sys.exit(1)

if __name__ == "__main__":
    main()