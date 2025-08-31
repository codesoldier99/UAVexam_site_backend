#!/usr/bin/env python3
"""
测试admin用户登录
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_admin_login():
    """测试admin用户登录"""
    
    print("=== 测试admin用户登录 ===")
    
    # 测试登录
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    print(f"登录数据: {json.dumps(login_data, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/pc/auth/login",
            json=login_data,
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ admin登录成功")
            response_data = response.json()
            print(f"响应: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ admin登录失败: {response.text}")
            
        # 同时测试一个考生账户登录
        print("\n=== 测试考生账户登录 ===")
        candidate_login_data = {
            "username": "candidate_011234",
            "password": "123456"  # 通常考生密码是身份证后6位或默认密码
        }
        
        candidate_response = requests.post(
            f"{BASE_URL}/api/v1/pc/auth/login",
            json=candidate_login_data,
            timeout=30
        )
        
        print(f"考生登录状态码: {candidate_response.status_code}")
        if candidate_response.status_code == 200:
            print("✅ 考生登录成功")
            print(f"响应: {candidate_response.json()}")
        else:
            print(f"❌ 考生登录失败: {candidate_response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")

if __name__ == "__main__":
    test_admin_login()