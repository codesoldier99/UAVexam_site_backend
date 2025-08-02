#!/usr/bin/env python3
"""
快速启动脚本 - 一键启动考试系统后端
"""

import subprocess
import time
import sys
import os

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} 成功")
            return True
        else:
            print(f"❌ {description} 失败")
            print(f"错误: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} 异常: {e}")
        return False

def check_docker():
    """检查Docker是否运行"""
    print("🔍 检查Docker状态...")
    result = subprocess.run("docker --version", shell=True, capture_output=True)
    if result.returncode == 0:
        print("✅ Docker 已安装")
        return True
    else:
        print("❌ Docker 未安装或未运行")
        return False

def start_database():
    """启动数据库"""
    return run_command("docker-compose up -d db", "启动数据库容器")

def wait_for_database():
    """等待数据库启动"""
    print("\n⏳ 等待数据库启动 (15秒)...")
    time.sleep(15)
    print("✅ 数据库启动等待完成")

def run_migrations():
    """运行数据库迁移"""
    return run_command("alembic upgrade head", "运行数据库迁移")

def create_test_user():
    """创建测试用户"""
    return run_command("python create_test_user.py", "创建测试用户")

def start_server():
    """启动API服务器"""
    print("\n🚀 启动API服务器...")
    print("📝 服务器将在 http://localhost:8000 启动")
    print("📝 API文档将在 http://localhost:8000/docs 可用")
    print("⏹️  按 Ctrl+C 停止服务器")
    
    try:
        subprocess.run([
            "python", "-m", "uvicorn", 
            "src.main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")

def main():
    """主函数"""
    print("🚀 考试系统后端 - 快速启动")
    print("=" * 50)
    
    # 检查Docker
    if not check_docker():
        print("❌ 请先安装并启动Docker")
        return
    
    # 启动数据库
    if not start_database():
        print("❌ 数据库启动失败")
        return
    
    # 等待数据库
    wait_for_database()
    
    # 运行迁移
    if not run_migrations():
        print("❌ 数据库迁移失败")
        return
    
    # 创建测试用户
    create_test_user()
    
    # 启动服务器
    start_server()

if __name__ == "__main__":
    main() 