#!/usr/bin/env python3
"""
测试Swagger UI和请求体界面的脚本
"""
import requests
import json
import time

def test_swagger_ui():
    """测试Swagger UI是否正常工作"""
    base_url = "http://localhost:8000"
    
    print("🔍 测试Swagger UI和请求体界面...")
    
    # 测试1: 检查服务器是否运行
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"✅ 服务器运行正常: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ 服务器未运行，请先启动服务器")
        return False
    
    # 测试2: 检查Swagger UI
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Swagger UI 可访问")
        else:
            print(f"❌ Swagger UI 访问失败: {response.status_code}")
    except Exception as e:
        print(f"❌ Swagger UI 测试失败: {e}")
    
    # 测试3: 测试请求体端点
    test_data = {
        "name": "测试用户",
        "email": "test@example.com",
        "age": 25,
        "is_active": True
    }
    
    try:
        response = requests.post(
            f"{base_url}/test-request-body",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 请求体测试成功")
            print(f"   返回数据: {json.dumps(result, ensure_ascii=False, indent=2)}")
        else:
            print(f"❌ 请求体测试失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
    except Exception as e:
        print(f"❌ 请求体测试异常: {e}")
    
    # 测试4: 测试登录端点
    login_data = {
        "username": "test@example.com",
        "password": "testpassword"
    }
    
    try:
        response = requests.post(
            f"{base_url}/simple-auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        print(f"📝 登录端点测试: {response.status_code}")
        if response.status_code == 401:
            print("   这是预期的，因为测试用户不存在")
        else:
            print(f"   响应: {response.text[:100]}...")
    except Exception as e:
        print(f"❌ 登录测试异常: {e}")
    
    print("\n📋 使用说明:")
    print("1. 访问 http://localhost:8000/docs 查看Swagger UI")
    print("2. 在Swagger UI中，POST端点会显示请求体输入界面")
    print("3. 点击 'Try it out' 按钮来测试API")
    print("4. 填写请求体数据后点击 'Execute' 执行")
    
    return True

if __name__ == "__main__":
    test_swagger_ui() 