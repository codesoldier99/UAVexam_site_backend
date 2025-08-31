#!/usr/bin/env python3
"""
模拟前端请求测试修改密码接口
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_frontend_request():
    """模拟前端的具体请求"""
    
    # 1. 登录
    print("1. 登录...")
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
    
    # 2. 模拟前端的修改密码请求
    print("\n2. 测试修改密码...")
    
    # 这是一个标准的修改密码请求
    password_data = {
        "current_password": "admin123",
        "new_password": "newpass123", 
        "confirm_password": "newpass123"
    }
    
    print(f"请求数据: {json.dumps(password_data, indent=2, ensure_ascii=False)}")
    print(f"请求头: {json.dumps(headers, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/pc/auth/change-password",
            json=password_data,
            headers=headers,
            timeout=30
        )
        
        print(f"\n状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 422:
            print("❌ 422错误详情:")
            try:
                error_detail = response.json()
                print(json.dumps(error_detail, indent=2, ensure_ascii=False))
            except:
                print(f"响应文本: {response.text}")
        elif response.status_code == 200:
            print("✅ 修改密码成功")
            response_data = response.json()
            print(f"响应: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
            
            # 恢复密码
            print("\n3. 恢复密码...")
            restore_response = requests.post(
                f"{BASE_URL}/api/v1/pc/auth/change-password",
                json={
                    "current_password": "newpass123",
                    "new_password": "admin123",
                    "confirm_password": "admin123"
                },
                headers=headers
            )
            if restore_response.status_code == 200:
                print("✅ 密码已恢复")
            else:
                print(f"❌ 密码恢复失败: {restore_response.text}")
        else:
            print(f"❌ 其他错误: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")

if __name__ == "__main__":
    test_frontend_request()