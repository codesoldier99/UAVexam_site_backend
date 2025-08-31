#!/usr/bin/env python3
"""
测试报名相关接口
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_registrations_api():
    """测试报名相关接口"""
    
    print("=== 测试报名相关接口 ===")
    
    # 1. 登录获取token
    login_response = requests.post(f"{BASE_URL}/api/v1/pc/auth/login", 
                                  json={"username": "admin", "password": "admin123"})
    
    if login_response.status_code != 200:
        print(f"❌ 登录失败: {login_response.text}")
        return
    
    token = login_response.json()["access_token"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("✅ 登录成功")
    
    # 2. 测试获取报名列表
    print("\n=== 测试获取报名列表 ===")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/pc/registrations",
            headers=headers,
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 获取报名列表成功")
            response_data = response.json()
            print(f"响应: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ 获取报名列表失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")

if __name__ == "__main__":
    test_registrations_api()