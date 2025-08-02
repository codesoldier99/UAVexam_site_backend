#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
登录诊断脚本
测试不同的登录参数，找出问题所在
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_login_with_correct_credentials():
    """测试正确的登录凭据"""
    print("🔐 测试正确的登录凭据...")
    
    login_data = {
        "username": "admin@exam.com",
        "password": "admin123"
    }
    
    response = requests.post(
        f"{BASE_URL}/auth/jwt/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    print(f"状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    print(f"响应内容: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ 登录成功!")
        print(f"访问令牌: {result.get('access_token', 'N/A')[:50]}...")
        return result.get('access_token')
    else:
        print("❌ 登录失败")
        return None

def test_login_with_wrong_credentials():
    """测试错误的登录凭据"""
    print("\n🔐 测试错误的登录凭据...")
    
    login_data = {
        "username": "wrong@email.com",
        "password": "wrongpassword"
    }
    
    response = requests.post(
        f"{BASE_URL}/auth/jwt/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")

def test_simple_login():
    """测试简化登录端点"""
    print("\n🔐 测试简化登录端点...")
    
    login_data = {
        "username": "admin@exam.com",
        "password": "admin123"
    }
    
    response = requests.post(
        f"{BASE_URL}/simple-login",
        json=login_data
    )
    
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")

def test_user_info_with_token(token):
    """使用令牌测试用户信息"""
    if not token:
        print("❌ 没有令牌，跳过用户信息测试")
        return
    
    print("\n👤 测试用户信息获取...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(
        f"{BASE_URL}/users/me",
        headers=headers
    )
    
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")

def test_swagger_ui():
    """测试Swagger UI"""
    print("\n📚 测试Swagger UI...")
    
    response = requests.get(f"{BASE_URL}/docs")
    print(f"状态码: {response.status_code}")
    
    response = requests.get(f"{BASE_URL}/openapi.json")
    print(f"OpenAPI状态码: {response.status_code}")

def main():
    """主函数"""
    print("🚀 开始登录诊断测试...")
    print("=" * 50)
    
    # 测试Swagger UI
    test_swagger_ui()
    
    # 测试简化登录
    test_simple_login()
    
    # 测试JWT登录
    token = test_login_with_correct_credentials()
    
    # 测试错误凭据
    test_login_with_wrong_credentials()
    
    # 测试用户信息
    test_user_info_with_token(token)
    
    print("\n" + "=" * 50)
    print("🏁 诊断测试完成!")

if __name__ == "__main__":
    main() 