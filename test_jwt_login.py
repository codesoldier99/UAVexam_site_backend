#!/usr/bin/env python3
"""
测试JWT登录功能
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_jwt_login():
    """测试JWT登录"""
    
    # 测试用户信息
    username = "swagger_user_20250802_093829@example.com"
    password = "testpass123"
    
    print("🔧 测试JWT登录...")
    print(f"用户名: {username}")
    print(f"密码: {password}")
    
    # 方法1：使用表单数据
    print("\n📋 方法1：使用表单数据")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/jwt/login",
            data={
                "username": username,
                "password": password
            }
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get("access_token")
            print("✅ JWT登录成功！")
            print(f"令牌: {token}")
            return token
        else:
            print("❌ JWT登录失败")
            return None
            
    except Exception as e:
        print(f"❌ 登录失败: {e}")
        return None

def test_api_with_token(token):
    """使用令牌测试API"""
    if not token:
        print("❌ 没有令牌，无法测试API")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n🧪 测试API调用...")
    
    # 测试考试产品API
    try:
        response = requests.get(f"{BASE_URL}/exam-products", headers=headers)
        print(f"考试产品API - 状态码: {response.status_code}")
        if response.status_code == 200:
            print("✅ 考试产品API测试成功")
        else:
            print(f"⚠️ 考试产品API测试失败: {response.text}")
    except Exception as e:
        print(f"❌ 考试产品API测试失败: {e}")
    
    # 测试场地API
    try:
        response = requests.get(f"{BASE_URL}/venues", headers=headers)
        print(f"场地API - 状态码: {response.status_code}")
        if response.status_code == 200:
            print("✅ 场地API测试成功")
        else:
            print(f"⚠️ 场地API测试失败: {response.text}")
    except Exception as e:
        print(f"❌ 场地API测试失败: {e}")

def main():
    print("🔐 JWT登录测试工具")
    print("=" * 50)
    
    token = test_jwt_login()
    
    if token:
        test_api_with_token(token)
        
        print("\n" + "=" * 50)
        print("🎉 JWT登录测试完成！")
        print("\n📋 在Swagger UI中的配置：")
        print("1. 点击右上角的 'Authorize' 按钮")
        print("2. 在 'Value' 字段中输入：")
        print(f"   Bearer {token}")
        print("3. 点击 'Authorize' 按钮")
        print("4. 关闭对话框")
        print("\n💡 现在您可以测试API了！")
    else:
        print("\n❌ JWT登录测试失败")

if __name__ == "__main__":
    main() 