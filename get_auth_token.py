#!/usr/bin/env python3
"""
获取认证令牌用于Swagger UI测试
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def register_and_login():
    """注册用户并登录获取令牌"""
    
    # 生成唯一的用户名和邮箱
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    username = f"testuser_{timestamp}"
    email = f"testuser_{timestamp}@example.com"
    password = "testpass123"
    
    print("🔧 正在注册测试用户...")
    print(f"用户名: {username}")
    print(f"邮箱: {email}")
    print(f"密码: {password}")
    
    # 1. 注册用户
    register_data = {
        "email": email,
        "password": password,
        "username": username,
        "role_id": 1
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code == 201:
            print("✅ 用户注册成功")
        else:
            print(f"⚠️ 注册状态: {response.status_code}")
            print(f"响应: {response.text}")
    except Exception as e:
        print(f"❌ 注册失败: {e}")
        return None
    
    # 2. 登录获取令牌
    print("\n🔧 正在登录获取令牌...")
    login_data = {
        "username": email,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/jwt/login", data=login_data)
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get("access_token")
            print("✅ 登录成功，获取到令牌")
            return token
        else:
            print(f"❌ 登录失败: {response.status_code}")
            print(f"响应: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 登录失败: {e}")
        return None

def main():
    print("🔐 Swagger UI 认证令牌获取工具")
    print("=" * 50)
    
    token = register_and_login()
    
    if token:
        print("\n" + "=" * 50)
        print("🎉 认证配置完成！")
        print("\n📋 在Swagger UI中的配置步骤：")
        print("1. 点击右上角的 'Authorize' 按钮")
        print("2. 在 'Value' 字段中输入以下令牌：")
        print(f"   Bearer {token}")
        print("3. 点击 'Authorize' 按钮")
        print("4. 关闭对话框")
        print("\n💡 现在您可以测试需要认证的API了！")
        print("\n⚠️ 注意：这个令牌会在一段时间后过期，需要重新获取")
    else:
        print("\n❌ 无法获取认证令牌，请检查服务器状态")

if __name__ == "__main__":
    main() 