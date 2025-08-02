#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速API测试脚本
只测试核心功能，确保系统基本运行正常
"""

import requests
import time

BASE_URL = "http://localhost:8000"

def test_basic_functionality():
    """测试基本功能"""
    print("🚀 开始快速API测试...")
    print("=" * 40)
    
    # 等待服务器启动
    print("⏳ 等待服务器启动...")
    time.sleep(3)
    
    # 测试根端点
    print("🏠 测试根端点...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ 根端点正常")
        else:
            print(f"❌ 根端点异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 根端点连接失败: {e}")
        return False
    
    # 测试健康检查
    print("🏥 测试健康检查...")
    try:
        response = requests.get(f"{BASE_URL}/test", timeout=5)
        if response.status_code == 200:
            print("✅ 健康检查正常")
        else:
            print(f"❌ 健康检查异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查连接失败: {e}")
        return False
    
    # 测试Swagger UI
    print("📚 测试Swagger UI...")
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Swagger UI正常")
        else:
            print(f"❌ Swagger UI异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Swagger UI连接失败: {e}")
        return False
    
    # 测试JWT登录
    print("🔐 测试JWT登录...")
    try:
        login_data = {
            "username": "admin@exam.com",
            "password": "admin123"
        }
        
        response = requests.post(
            f"{BASE_URL}/auth/jwt/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            token = result.get("access_token")
            print("✅ JWT登录成功")
            
            # 测试用户信息
            print("👤 测试用户信息...")
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(f"{BASE_URL}/users/me", headers=headers, timeout=5)
            if response.status_code == 200:
                user_info = response.json()
                print(f"✅ 用户信息获取成功: {user_info.get('username')}")
            else:
                print(f"❌ 用户信息获取失败: {response.status_code}")
                return False
        else:
            print(f"❌ JWT登录失败: {response.status_code}")
            print(f"响应: {response.text}")
            return False
    except Exception as e:
        print(f"❌ JWT登录连接失败: {e}")
        return False
    
    print("\n" + "=" * 40)
    print("🎉 核心功能测试通过！")
    print("✅ 服务器运行正常")
    print("✅ 数据库连接正常")
    print("✅ 认证系统正常")
    print("✅ API文档可访问")
    
    return True

def main():
    """主函数"""
    if test_basic_functionality():
        print("\n📋 系统状态总结:")
        print("✅ 基础功能: 正常")
        print("✅ 认证系统: 正常")
        print("✅ 数据库: 正常")
        print("✅ API文档: 正常")
        print("\n🚀 系统已准备好使用！")
        print("📖 访问API文档: http://localhost:8000/docs")
        print("🔧 可以开始前端开发或进行完整测试")
    else:
        print("\n❌ 系统存在问题，需要检查")

if __name__ == "__main__":
    main() 