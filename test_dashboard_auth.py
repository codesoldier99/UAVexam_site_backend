#!/usr/bin/env python3
"""
Dashboard认证测试脚本
测试dashboard接口的401错误
"""

import requests
import json

# 配置
BASE_URL = "http://localhost:8000"
USERNAME = "admin"  # 请根据实际情况修改
PASSWORD = "admin123"  # 请根据实际情况修改

def test_dashboard_auth():
    """测试dashboard认证"""
    session = requests.Session()
    
    print("🔐 测试Dashboard认证问题")
    print("=" * 40)
    
    # 测试1: 未登录访问dashboard
    print("\n1️⃣ 测试未登录访问dashboard")
    dashboard_urls = [
        "/api/v1/pc/dashboard/activities?limit=20",
        "/api/v1/pc/dashboard/stats?role=super_admin",
        "/api/v1/pc/stats",  # 实际的dashboard路径
        "/api/v1/pc/recent-exams",
        "/api/v1/pc/activities"
    ]
    
    for url in dashboard_urls:
        print(f"\n  测试: {url}")
        response = session.get(f"{BASE_URL}{url}")
        print(f"  状态码: {response.status_code}")
        
        if response.status_code == 401:
            print(f"  ✅ 正确返回401未授权")
        elif response.status_code == 404:
            print(f"  ⚠️  404未找到 - 路径可能不存在")
        else:
            print(f"  ❌ 意外状态码: {response.text}")
    
    # 测试2: 登录后访问dashboard
    print(f"\n2️⃣ 测试登录后访问dashboard")
    
    # 登录
    print("  正在登录...")
    login_response = session.post(
        f"{BASE_URL}/api/v1/pc/auth/login",
        json={"username": USERNAME, "password": PASSWORD}
    )
    
    if login_response.status_code != 200:
        print(f"  ❌ 登录失败: {login_response.status_code}")
        print(f"  错误: {login_response.text}")
        return
    
    token = login_response.json().get("access_token")
    if not token:
        print("  ❌ 未获取到token")
        return
    
    print("  ✅ 登录成功")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 测试带token的dashboard访问
    for url in dashboard_urls:
        print(f"\n  测试（带token）: {url}")
        response = session.get(f"{BASE_URL}{url}", headers=headers)
        print(f"  状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ 成功访问")
            if isinstance(data, dict):
                keys = list(data.keys())[:3]  # 只显示前3个key
                print(f"  返回数据包含: {keys}")
        elif response.status_code == 401:
            print(f"  ❌ 仍然401未授权 - token可能无效")
            print(f"  错误: {response.text}")
        elif response.status_code == 404:
            print(f"  ⚠️  404未找到 - 路径不存在")
        else:
            print(f"  ❌ 其他错误: {response.text}")
    
    # 测试3: 验证token格式
    print(f"\n3️⃣ 验证token信息")
    print(f"  Token长度: {len(token) if token else 0}")
    print(f"  Token前缀: {token[:20] if token else 'None'}...")
    
    # 测试4: 检查用户信息
    print(f"\n4️⃣ 检查用户信息")
    profile_response = session.get(f"{BASE_URL}/api/v1/pc/auth/profile", headers=headers)
    print(f"  用户信息状态码: {profile_response.status_code}")
    
    if profile_response.status_code == 200:
        user_data = profile_response.json()
        print(f"  ✅ 用户: {user_data.get('username', 'N/A')}")
        print(f"  角色: {user_data.get('role', 'N/A')}")
    else:
        print(f"  ❌ 获取用户信息失败: {profile_response.text}")

def test_token_validation():
    """测试token验证"""
    print(f"\n5️⃣ 测试token验证机制")
    
    # 测试无效token
    invalid_tokens = [
        "invalid_token",
        "Bearer invalid_token",
        "",
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.invalid",  # 无效JWT
    ]
    
    for token in invalid_tokens:
        print(f"\n  测试无效token: {token[:20] if token else 'empty'}...")
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        
        response = requests.get(f"{BASE_URL}/api/v1/pc/stats", headers=headers)
        print(f"  状态码: {response.status_code}")
        
        if response.status_code == 401:
            print(f"  ✅ 正确拒绝无效token")
        else:
            print(f"  ❌ 意外结果: {response.text}")

if __name__ == "__main__":
    print("Dashboard认证问题诊断")
    test_dashboard_auth()
    test_token_validation()
    print(f"\n🏁 诊断完成")