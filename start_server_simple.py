#!/usr/bin/env python3
"""
简单服务器启动脚本
"""

import os
import sys
import subprocess
import time
from pathlib import Path

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
    print("🚀 启动 Exam Site Backend 服务器")
    print("=" * 50)
    
    # 检查当前目录
    if not Path("start_dev.py").exists():
        print("❌ 请在 exam_site_backend 目录下运行此脚本")
        return
    
    # 检查环境变量文件
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 创建 .env 文件...")
        subprocess.run("copy env.example .env", shell=True)
        print("✅ .env 文件已创建")
    
    # 启动服务器
    print("🚀 启动服务器...")
    print("📱 API文档地址: http://localhost:8000/docs")
    print("🔧 管理界面: http://localhost:8000/redoc")
    print("\n💡 测试工具:")
    print("1. 使用 simple_api_test.py 进行交互式测试")
    print("2. 参考 SIMPLE_API_TEST_GUIDE.md 进行手动测试")
    print("3. 使用 auto_test.py 进行自动测试")
    
    # 启动应用
    if not run_command("python start_dev.py", "启动应用"):
        print("❌ 服务器启动失败")
        return
    
    print("\n🎉 服务器启动成功!")

if __name__ == "__main__":
    main() 