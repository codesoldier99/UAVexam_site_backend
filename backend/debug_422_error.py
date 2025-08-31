#!/usr/bin/env python3
"""
调试修改密码接口的422错误
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def debug_change_password_422():
    """调试修改密码接口的422错误"""
    
    # 1. 先登录获取token
    print("1. 登录获取token...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/api/v1/pc/auth/login", json=login_data)
        print(f"登录状态码: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data.get("access_token")
            print("✅ 登录成功")
            
            # 2. 测试修改密码接口 - 获取详细错误信息
            print("\n2. 测试修改密码接口...")
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # 测试不同的请求数据格式
            test_cases = [
                {
                    "name": "标准格式",
                    "data": {
                        "current_password": "admin123",
                        "new_password": "newpass123",
                        "confirm_password": "newpass123"
                    }
                },
                {
                    "name": "缺少confirm_password",
                    "data": {
                        "current_password": "admin123",
                        "new_password": "newpass123"
                    }
                },
                {
                    "name": "密码不匹配",
                    "data": {
                        "current_password": "admin123",
                        "new_password": "newpass123",
                        "confirm_password": "different123"
                    }
                },
                {
                    "name": "密码太短",
                    "data": {
                        "current_password": "admin123",
                        "new_password": "123",
                        "confirm_password": "123"
                    }
                }
            ]
            
            for test_case in test_cases:
                print(f"\n--- 测试用例: {test_case['name']} ---")
                print(f"请求数据: {json.dumps(test_case['data'], indent=2, ensure_ascii=False)}")
                
                change_response = requests.post(
                    f"{BASE_URL}/api/v1/pc/auth/change-password", 
                    json=test_case['data'],
                    headers=headers
                )
                
                print(f"状态码: {change_response.status_code}")
                
                try:
                    response_json = change_response.json()
                    print(f"响应内容: {json.dumps(response_json, indent=2, ensure_ascii=False)}")
                except:
                    print(f"响应文本: {change_response.text}")
                
                # 如果是标准格式且成功，恢复密码
                if test_case['name'] == "标准格式" and change_response.status_code == 200:
                    print("\n--- 恢复原密码 ---")
                    restore_data = {
                        "current_password": "newpass123",
                        "new_password": "admin123",
                        "confirm_password": "admin123"
                    }
                    
                    restore_response = requests.post(
                        f"{BASE_URL}/api/v1/pc/auth/change-password",
                        json=restore_data,
                        headers=headers
                    )
                    
                    if restore_response.status_code == 200:
                        print("✅ 密码已恢复")
                    else:
                        print(f"❌ 密码恢复失败: {restore_response.text}")
                        
        else:
            print(f"❌ 登录失败: {login_response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败，请确保后端服务正在运行")
    except Exception as e:
        print(f"❌ 测试出错: {str(e)}")

if __name__ == "__main__":
    debug_change_password_422()