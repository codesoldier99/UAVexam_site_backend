#!/usr/bin/env python3
"""
测试注册功能的脚本
"""
import requests
import json
import time

def test_register():
    """测试注册功能"""
    base_url = "http://localhost:8000"
    
    print("📝 测试注册功能...")
    
    # 生成唯一的邮箱和用户名
    timestamp = int(time.time())
    email = f"testuser{timestamp}@example.com"
    username = f"testuser{timestamp}"
    
    # 测试数据
    register_data = {
        "username": username,
        "email": email,
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(
            f"{base_url}/simple-register",
            json=register_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📝 注册响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 注册成功!")
            print(f"   用户ID: {result['user']['id']}")
            print(f"   邮箱: {result['user']['email']}")
            print(f"   用户名: {result['user']['username']}")
            print(f"   角色ID: {result['user']['role_id']}")
            print(f"   机构ID: {result['user']['institution_id']}")
            
            # 测试登录
            login_data = {
                "username": email,
                "password": "testpassword123"
            }
            
            login_response = requests.post(
                f"{base_url}/simple-auth/login",
                json=login_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            print(f"🔐 登录测试状态码: {login_response.status_code}")
            if login_response.status_code == 200:
                print("✅ 新注册用户登录成功!")
            else:
                print(f"❌ 登录失败: {login_response.text}")
            
            return True
        else:
            print(f"❌ 注册失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 注册测试异常: {e}")
        return False

if __name__ == "__main__":
    test_register() 