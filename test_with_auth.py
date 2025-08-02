#!/usr/bin/env python3
"""
带认证的API测试脚本
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def get_auth_token():
    """获取认证令牌"""
    try:
        # 先注册一个测试用户
        register_data = {
            "email": f"testuser_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
            "password": "testpass123",
            "username": f"testuser_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "role_id": 1  # 添加必需的role_id字段
        }
        
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print(f"注册状态: {response.status_code}")
        if response.status_code != 201:
            print(f"注册响应: {response.text}")
        
        # 登录获取令牌
        login_data = {
            "username": register_data["email"],
            "password": register_data["password"]
        }
        
        response = requests.post(f"{BASE_URL}/auth/jwt/login", data=login_data)
        if response.status_code == 200:
            token_data = response.json()
            return token_data.get("access_token")
        else:
            print(f"登录失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"获取令牌失败: {e}")
        return None

def test_endpoint_with_auth(endpoint, method="GET", data=None, token=None):
    """带认证测试单个端点"""
    url = f"{BASE_URL}{endpoint}"
    headers = {}
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=10)
        
        print(f"✅ {method} {endpoint}")
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.text[:200]}...")
        
        if response.status_code >= 400:
            print(f"   ❌ 错误: {response.text}")
        
        return response.status_code < 400
        
    except requests.exceptions.ConnectionError as e:
        print(f"❌ {method} {endpoint} - 连接错误: {e}")
        return False
    except requests.exceptions.Timeout as e:
        print(f"❌ {method} {endpoint} - 超时: {e}")
        return False
    except Exception as e:
        print(f"❌ {method} {endpoint} - 未知错误: {e}")
        return False

def main():
    print("🔍 带认证的API测试开始...")
    print(f"测试时间: {datetime.now()}")
    print(f"基础URL: {BASE_URL}")
    print("=" * 50)
    
    # 获取认证令牌
    print("\n📋 1. 获取认证令牌")
    token = get_auth_token()
    if not token:
        print("❌ 无法获取认证令牌，测试终止")
        return
    
    print(f"✅ 获取到令牌: {token[:20]}...")
    
    # 2. 测试需要认证的端点
    print("\n📋 2. 测试需要认证的端点")
    
    # 考试产品API
    print("\n--- 考试产品API ---")
    test_endpoint_with_auth("/exam-products", token=token)
    test_endpoint_with_auth("/exam-products", method="POST", data={
        "name": "测试考试产品",
        "description": "这是一个测试产品"
    }, token=token)
    
    # 场地API
    print("\n--- 场地API ---")
    test_endpoint_with_auth("/venues", token=token)
    test_endpoint_with_auth("/venues", method="POST", data={
        "name": "测试考场",
        "type": "理论"
    }, token=token)
    
    # 考生API
    print("\n--- 考生API ---")
    test_endpoint_with_auth("/candidates", token=token)
    test_endpoint_with_auth("/candidates", method="POST", data={
        "name": "测试考生",
        "id_card": "110101199001011234",
        "institution_id": 1,
        "exam_product_id": 1,
        "status": "待排期"
    }, token=token)
    
    # 考试安排API
    print("\n--- 考试安排API ---")
    test_endpoint_with_auth("/schedules", token=token)
    test_endpoint_with_auth("/schedules", method="POST", data={
        "candidate_id": 1,
        "venue_id": 1,
        "exam_date": "2025-08-03",
        "start_time": "09:00:00",
        "end_time": "10:00:00",
        "activity_name": "理论考试",
        "status": "待签到"
    }, token=token)
    
    print("\n" + "=" * 50)
    print("🏁 带认证的API测试完成")

if __name__ == "__main__":
    main() 