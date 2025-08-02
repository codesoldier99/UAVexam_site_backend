#!/usr/bin/env python3
"""
直接测试登录功能
"""

import requests
import json

def test_jwt_login():
    """测试JWT登录"""
    print("🔐 测试JWT登录...")
    
    url = "http://localhost:8000/auth/jwt/login"
    data = "username=admin@exam.com&password=admin123"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        response = requests.post(url, data=data, headers=headers, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        if response.status_code == 200:
            print("✅ JWT登录成功!")
            return True
        else:
            print("❌ JWT登录失败")
            return False
    except Exception as e:
        print(f"❌ 请求错误: {e}")
        return False

def test_simple_login():
    """测试简化登录"""
    print("\n🔐 测试简化登录...")
    
    url = "http://localhost:8000/simple-login"
    data = {
        "username": "admin@exam.com",
        "email": "admin@exam.com",
        "password": "admin123"
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        if response.status_code == 200:
            print("✅ 简化登录成功!")
            return True
        else:
            print("❌ 简化登录失败")
            return False
    except Exception as e:
        print(f"❌ 请求错误: {e}")
        return False

if __name__ == "__main__":
    print("🚀 直接测试登录功能")
    print("="*50)
    
    # 测试JWT登录
    jwt_success = test_jwt_login()
    
    # 测试简化登录
    simple_success = test_simple_login()
    
    print("\n" + "="*50)
    print("📊 测试结果:")
    print(f"JWT登录: {'✅ 成功' if jwt_success else '❌ 失败'}")
    print(f"简化登录: {'✅ 成功' if simple_success else '❌ 失败'}")
    print("="*50) 