#!/usr/bin/env python3
"""
开发环境启动脚本
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """运行命令并显示描述"""
    print(f"\n🔄 {description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {description} 成功")
        if result.stdout:
            print(result.stdout)
    else:
        print(f"❌ {description} 失败")
        if result.stderr:
            print(result.stderr)
        return False
    return True

def main():
    """主函数"""
    print("🚀 启动 Exam Site Backend 开发环境")
    print("=" * 50)
    
    # 检查环境变量文件
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 创建 .env 文件...")
        subprocess.run("copy env.example .env", shell=True)
        print("✅ .env 文件已创建，请根据需要修改配置")
    
    # 检查虚拟环境
    venv_path = Path("venv")
    if not venv_path.exists():
        print("📦 创建虚拟环境...")
        if not run_command("python -m venv venv", "创建虚拟环境"):
            return
    
    # 激活虚拟环境并安装依赖
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Linux/Mac
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    # 安装依赖
    if not run_command(f"{pip_cmd} install -r requirements.txt", "安装依赖"):
        return
    
    # 启动数据库（如果使用Docker）
    print("\n🐳 启动数据库...")
    if not run_command("docker-compose up -d db", "启动MySQL数据库"):
        print("⚠️  数据库启动失败，请检查Docker是否运行")
    
    # 等待数据库启动
    print("⏳ 等待数据库启动...")
    import time
    time.sleep(5)
    
    # 运行数据库迁移
    if not run_command("alembic upgrade head", "运行数据库迁移"):
        print("⚠️  数据库迁移失败")
    
    # 初始化数据库
    if not run_command("python init_db.py", "初始化数据库"):
        print("⚠️  数据库初始化失败")
    
    # 启动应用
    print("\n🚀 启动应用服务器...")
    if not run_command("python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000", "启动应用"):
        return
    
    print("\n🎉 应用启动成功!")
    print("📱 API文档地址: http://localhost:8000/docs")
    print("🔧 管理界面: http://localhost:8000/redoc")

if __name__ == "__main__":
    main() 