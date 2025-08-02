#!/usr/bin/env python3
"""
测试登录功能的脚本
"""
import requests
import json

def test_login():
    """测试登录功能"""
    base_url = "http://localhost:8000"
    
    print("🔐 测试登录功能...")
    
    # 测试数据
    login_data = {
        "username": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(
            f"{base_url}/simple-auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📝 登录响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 登录成功!")
            print(f"   用户ID: {result['user']['id']}")
            print(f"   邮箱: {result['user']['email']}")
            print(f"   用户名: {result['user']['username']}")
            print(f"   角色ID: {result['user']['role_id']}")
            print(f"   机构ID: {result['user']['institution_id']}")
            print(f"   访问令牌: {result['access_token'][:50]}...")
            
            # 测试使用令牌访问受保护的端点
            headers = {
                "Authorization": f"Bearer {result['access_token']}"
            }
            
            # 测试健康检查端点
            health_response = requests.get(f"{base_url}/health", headers=headers)
            print(f"🔒 受保护端点测试: {health_response.status_code}")
            
            return True
        else:
            print(f"❌ 登录失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 登录测试异常: {e}")
        return False

if __name__ == "__main__":
    test_login() 