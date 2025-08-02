#!/usr/bin/env python3
"""
快速启动测试环境脚本
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_server_status():
    """检查服务器状态"""
    try:
        response = requests.get("http://localhost:8000/docs", timeout=5)
        return response.status_code == 200
    except:
        return False

def run_command(command, description):
    """运行命令并显示描述"""
    print(f"\n🔄 {description}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {description} 成功")
        if result.stdout:
            print(result.stdout)
        return True
    else:
        print(f"❌ {description} 失败")
        if result.stderr:
            print(result.stderr)
        return False

def main():
    """主函数"""
    print("🚀 快速启动 Exam Site Backend 测试环境")
    print("=" * 50)
    
    # 检查当前目录
    if not Path("start_dev.py").exists():
        print("❌ 请在 exam_site_backend 目录下运行此脚本")
        return
    
    # 检查服务器是否已运行
    if check_server_status():
        print("✅ 服务器已在运行")
        print("📱 API文档地址: http://localhost:8000/docs")
        print("🔧 管理界面: http://localhost:8000/redoc")
        return
    
    # 启动服务器
    print("🚀 启动服务器...")
    if not run_command("python start_dev.py", "启动开发服务器"):
        print("❌ 服务器启动失败")
        return
    
    # 等待服务器启动
    print("⏳ 等待服务器启动...")
    for i in range(30):  # 最多等待30秒
        if check_server_status():
            print("✅ 服务器启动成功!")
            print("📱 API文档地址: http://localhost:8000/docs")
            print("🔧 管理界面: http://localhost:8000/redoc")
            print("\n📋 Postman测试准备:")
            print("1. 导入 exam_site_backend.postman_collection.json")
            print("2. 导入 exam_site_backend.postman_environment.json")
            print("3. 选择 'Exam Site Backend Environment' 环境")
            print("4. 开始测试!")
            return
        time.sleep(1)
        print(f"⏳ 等待中... ({i+1}/30)")
    
    print("❌ 服务器启动超时，请检查日志")

if __name__ == "__main__":
    main() 