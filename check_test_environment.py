#!/usr/bin/env python3
"""
检查测试环境状态脚本
"""

import os
import sys
import requests
import json
from pathlib import Path

def check_file_exists(file_path, description):
    """检查文件是否存在"""
    if Path(file_path).exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} (文件不存在)")
        return False

def check_server_status():
    """检查服务器状态"""
    try:
        response = requests.get("http://localhost:8000/docs", timeout=5)
        if response.status_code == 200:
            print("✅ 服务器状态: 运行中 (http://localhost:8000)")
            return True
        else:
            print(f"❌ 服务器状态: 响应异常 (状态码: {response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 服务器状态: 未运行 (无法连接到 http://localhost:8000)")
        return False
    except Exception as e:
        print(f"❌ 服务器状态: 检查失败 ({str(e)})")
        return False

def check_api_endpoints():
    """检查API端点"""
    endpoints = [
        ("/docs", "API文档"),
        ("/redoc", "管理界面"),
        ("/openapi.json", "OpenAPI规范"),
    ]
    
    print("\n🔍 检查API端点:")
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {description}: http://localhost:8000{endpoint}")
            else:
                print(f"❌ {description}: 状态码 {response.status_code}")
        except:
            print(f"❌ {description}: 无法访问")

def check_postman_files():
    """检查Postman文件"""
    print("\n📋 检查Postman文件:")
    
    files = [
        ("exam_site_backend.postman_collection.json", "Postman集合文件"),
        ("exam_site_backend.postman_environment.json", "Postman环境文件"),
        ("COMPLETE_POSTMAN_TEST_GUIDE.md", "完整测试指南"),
        ("POSTMAN_TEST_GUIDE.md", "基础测试指南"),
    ]
    
    all_exist = True
    for file_path, description in files:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist

def check_environment_files():
    """检查环境配置文件"""
    print("\n🔧 检查环境配置:")
    
    files = [
        (".env", "环境变量文件"),
        ("env.example", "环境变量示例"),
        ("requirements.txt", "依赖文件"),
        ("start_dev.py", "启动脚本"),
        ("init_db.py", "数据库初始化脚本"),
    ]
    
    all_exist = True
    for file_path, description in files:
        if not check_file_exists(file_path, description):
            all_exist = False
    
    return all_exist

def main():
    """主函数"""
    print("🔍 检查 Exam Site Backend 测试环境")
    print("=" * 50)
    
    # 检查当前目录
    if not Path("start_dev.py").exists():
        print("❌ 请在 exam_site_backend 目录下运行此脚本")
        return
    
    # 检查环境文件
    env_ok = check_environment_files()
    
    # 检查Postman文件
    postman_ok = check_postman_files()
    
    # 检查服务器状态
    server_ok = check_server_status()
    
    # 如果服务器运行，检查API端点
    if server_ok:
        check_api_endpoints()
    
    # 总结
    print("\n" + "=" * 50)
    print("📊 环境检查总结:")
    print(f"环境配置: {'✅ 正常' if env_ok else '❌ 异常'}")
    print(f"Postman文件: {'✅ 正常' if postman_ok else '❌ 异常'}")
    print(f"服务器状态: {'✅ 正常' if server_ok else '❌ 异常'}")
    
    if env_ok and postman_ok and server_ok:
        print("\n🎉 测试环境准备就绪!")
        print("📋 下一步:")
        print("1. 打开Postman")
        print("2. 导入集合和环境文件")
        print("3. 开始API测试")
    else:
        print("\n⚠️  环境存在问题，请检查上述错误")
        if not server_ok:
            print("💡 建议运行: python start_dev.py")

if __name__ == "__main__":
    main() 