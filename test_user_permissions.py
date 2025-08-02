#!/usr/bin/env python3
"""
测试用户权限设置
"""

import requests
import json

# 配置
BASE_URL = "http://localhost:8000"
TEST_USER = {
    "email": "institution@test.com",
    "password": "institution123"
}

def get_access_token():
    """获取访问令牌"""
    login_url = f"{BASE_URL}/auth/jwt/login"
    login_data = {
        "username": TEST_USER["email"],
        "password": TEST_USER["password"]
    }
    
    try:
        response = requests.post(
            login_url,
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            token_data = response.json()
            return token_data.get("access_token")
        else:
            print(f"❌ 登录失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 登录异常: {str(e)}")
        return None

def test_user_info():
    """测试获取用户信息"""
    print("🔍 测试获取用户信息...")
    
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取访问令牌")
        return
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/users/me",
            headers=headers
        )
        
        if response.status_code == 200:
            user_info = response.json()
            print("✅ 用户信息获取成功")
            print(f"用户ID: {user_info.get('id')}")
            print(f"邮箱: {user_info.get('email')}")
            print(f"用户名: {user_info.get('username')}")
            print(f"是否超级管理员: {user_info.get('is_superuser')}")
            print(f"机构ID: {user_info.get('institution_id')}")
            print(f"是否激活: {user_info.get('is_active')}")
        else:
            print(f"❌ 获取用户信息失败: {response.status_code}")
            print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"❌ 获取用户信息异常: {str(e)}")

def test_simple_schedule_query():
    """测试简单的排期查询"""
    print("\n📋 测试简单的排期查询...")
    
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取访问令牌")
        return
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/schedules/",
            params={"page": 1, "size": 5},
            headers=headers
        )
        
        print(f"响应状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ 排期查询成功")
            print(f"总数: {data.get('total', 0)}")
        else:
            print(f"❌ 排期查询失败")
            print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"❌ 排期查询异常: {str(e)}")

def main():
    """主测试函数"""
    print("🚀 开始用户权限测试")
    print("=" * 50)
    
    # 测试用户信息
    test_user_info()
    
    # 测试简单排期查询
    test_simple_schedule_query()
    
    print("\n" + "=" * 50)
    print("🎉 用户权限测试完成")

if __name__ == "__main__":
    main() 