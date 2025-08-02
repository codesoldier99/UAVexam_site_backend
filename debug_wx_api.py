#!/usr/bin/env python3
"""
调试微信小程序API
"""

import requests
import json

def test_wx_login():
    """测试微信小程序登录"""
    print("🔍 测试微信小程序登录...")
    
    url = "http://localhost:8000/wx/login"
    data = {
        "code": "test_wx_code_123456",
        "id_card": "110101199001011234"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ 登录成功")
            print(f"响应: {response.json()}")
        else:
            print(f"❌ 登录失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")

def test_venues_status():
    """测试考场状态"""
    print("\n🔍 测试考场状态...")
    
    url = "http://localhost:8000/public/venues-status"
    
    try:
        response = requests.get(url)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 获取成功")
            data = response.json()
            print(f"考场数量: {len(data.get('venues', []))}")
        else:
            print(f"❌ 获取失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")

def test_server_status():
    """测试服务器状态"""
    print("🔍 测试服务器状态...")
    
    url = "http://localhost:8000/"
    
    try:
        response = requests.get(url)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 服务器运行正常")
        else:
            print(f"❌ 服务器异常: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 服务器连接失败: {e}")

if __name__ == "__main__":
    test_server_status()
    test_wx_login()
    test_venues_status() 