#!/usr/bin/env python3
"""
API问题诊断脚本
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, method="GET", data=None, headers=None):
    """测试单个端点"""
    url = f"{BASE_URL}{endpoint}"
    
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
        
        return response.status_code == 200
        
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
    print("🔍 API问题诊断开始...")
    print(f"测试时间: {datetime.now()}")
    print(f"基础URL: {BASE_URL}")
    print("=" * 50)
    
    # 1. 测试基础端点
    print("\n📋 1. 测试基础端点")
    test_endpoint("/")
    test_endpoint("/health")
    test_endpoint("/test")
    
    # 2. 测试认证端点
    print("\n📋 2. 测试认证端点")
    test_endpoint("/auth/jwt/login", method="POST", data={
        "username": "testuser",
        "password": "testpass"
    })
    
    # 3. 测试简化端点
    print("\n📋 3. 测试简化端点")
    test_endpoint("/simple-institutions")
    test_endpoint("/simple-institutions/stats")
    
    # 4. 测试需要权限的端点（不带认证）
    print("\n📋 4. 测试需要权限的端点（不带认证）")
    test_endpoint("/exam-products")
    test_endpoint("/venues")
    test_endpoint("/candidates")
    test_endpoint("/schedules")
    
    # 5. 测试Swagger文档
    print("\n📋 5. 测试Swagger文档")
    test_endpoint("/docs")
    test_endpoint("/openapi.json")
    
    print("\n" + "=" * 50)
    print("🏁 诊断完成")

if __name__ == "__main__":
    main() 