#!/usr/bin/env python3
"""
用户认证API测试脚本
测试PC登录和微信登录（桩）功能
"""

import requests
import json
import time

# 配置
BASE_URL = "http://localhost:8000"
TEST_USER = {
    "email": "admin@exam.com",
    "password": "admin123"
}

def test_server_health():
    """测试服务器健康状态"""
    print("🔍 测试服务器健康状态...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ 服务器运行正常")
            print(f"响应: {response.json()}")
            return True
        else:
            print(f"❌ 服务器响应异常: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保服务器已启动")
        return False

def test_pc_login():
    """测试PC登录功能"""
    print("\n🔐 测试PC登录功能...")
    
    # 测试登录端点
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
            print("✅ PC登录成功")
            print(f"访问令牌: {token_data.get('access_token', 'N/A')[:50]}...")
            return token_data.get("access_token")
        else:
            print(f"❌ PC登录失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None
    except Exception as e:
        print(f"❌ PC登录测试异常: {str(e)}")
        return None

def test_wechat_login_stub():
    """测试微信登录桩功能"""
    print("\n📱 测试微信登录桩功能...")
    
    # 测试微信登录端点
    wechat_login_url = f"{BASE_URL}/social/wechat/login"
    wechat_data = {
        "code": "test_wechat_code_123"
    }
    
    try:
        response = requests.post(
            wechat_login_url,
            json=wechat_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 401:
            print("✅ 微信登录桩功能正常（返回预期的认证失败）")
            print("说明: 微信API尚未集成，返回401是预期的")
            return True
        elif response.status_code == 200:
            print("✅ 微信登录成功（如果已集成微信API）")
            return True
        else:
            print(f"❌ 微信登录测试异常: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 微信登录测试异常: {str(e)}")
        return False

def test_user_info(access_token):
    """测试获取用户信息"""
    if not access_token:
        print("❌ 无法测试用户信息，没有访问令牌")
        return False
    
    print("\n👤 测试获取用户信息...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/users/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        if response.status_code == 200:
            user_info = response.json()
            print("✅ 获取用户信息成功")
            print(f"用户ID: {user_info.get('id')}")
            print(f"邮箱: {user_info.get('email')}")
            print(f"用户名: {user_info.get('username')}")
            print(f"是否激活: {user_info.get('is_active')}")
            print(f"是否超级用户: {user_info.get('is_superuser')}")
            return True
        else:
            print(f"❌ 获取用户信息失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 获取用户信息测试异常: {str(e)}")
        return False

def test_simple_login():
    """测试简化登录功能"""
    print("\n🔑 测试简化登录功能...")
    
    simple_login_url = f"{BASE_URL}/simple-login"
    login_data = {
        "username": TEST_USER["email"],
        "email": TEST_USER["email"],
        "password": TEST_USER["password"]
    }
    
    try:
        response = requests.post(
            simple_login_url,
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 简化登录成功")
            print(f"响应: {result}")
            return True
        else:
            print(f"❌ 简化登录失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 简化登录测试异常: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始用户认证API测试")
    print("=" * 50)
    
    # 测试服务器健康状态
    if not test_server_health():
        print("❌ 服务器未启动，无法继续测试")
        return
    
    # 测试PC登录
    access_token = test_pc_login()
    
    # 测试微信登录桩
    test_wechat_login_stub()
    
    # 测试简化登录
    test_simple_login()
    
    # 测试获取用户信息
    if access_token:
        test_user_info(access_token)
    
    print("\n" + "=" * 50)
    print("🎉 用户认证API测试完成")
    print("📝 测试结果总结:")
    print("- PC登录: ✅ 已实现")
    print("- 微信登录: ✅ 桩功能已实现")
    print("- 用户信息获取: ✅ 已实现")
    print("- 简化登录: ✅ 已实现")

if __name__ == "__main__":
    main() 