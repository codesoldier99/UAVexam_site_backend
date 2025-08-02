#!/usr/bin/env python3
"""
简单的认证测试工具
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_simple_auth():
    """测试简化认证"""
    
    # 测试用户信息
    username = "testuser_20250802_093145@example.com"
    password = "testpass123"
    
    print("🔧 测试简化认证...")
    print(f"用户名: {username}")
    print(f"密码: {password}")
    
    try:
        # 使用新的简化端点
        response = requests.post(f"{BASE_URL}/simple-auth/login", 
                               params={"username": username, "password": password})
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get("access_token")
            print("✅ 简化认证成功！")
            print(f"令牌: {token}")
            
            # 测试API调用
            headers = {"Authorization": f"Bearer {token}"}
            test_response = requests.get(f"{BASE_URL}/exam-products", headers=headers)
            
            if test_response.status_code == 200:
                print("✅ API调用测试成功！")
            else:
                print(f"⚠️ API调用测试失败: {test_response.status_code}")
                print(f"响应: {test_response.text}")
                
            return token
        else:
            print(f"❌ 简化认证失败: {response.status_code}")
            print(f"响应: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 认证测试失败: {e}")
        return None

def main():
    print("🔐 简化认证测试工具")
    print("=" * 50)
    
    token = test_simple_auth()
    
    if token:
        print("\n" + "=" * 50)
        print("🎉 认证测试成功！")
        print("\n📋 在Swagger UI中的配置：")
        print("1. 点击右上角的 'Authorize' 按钮")
        print("2. 在 'Value' 字段中输入：")
        print(f"   Bearer {token}")
        print("3. 点击 'Authorize' 按钮")
        print("4. 关闭对话框")
        print("\n💡 现在您可以测试API了！")
    else:
        print("\n❌ 认证测试失败")

if __name__ == "__main__":
    main() 