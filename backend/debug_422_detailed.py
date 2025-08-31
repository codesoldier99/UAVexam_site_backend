#!/usr/bin/env python3
"""
详细调试修改密码接口的422错误
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def debug_detailed_422():
    """详细调试422错误"""
    
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
    
    # 2. 测试各种请求格式
    test_cases = [
        {
            "name": "完整请求",
            "data": {
                "current_password": "admin123",
                "new_password": "newpass123",
                "confirm_password": "newpass123"
            }
        },
        {
            "name": "空字符串字段",
            "data": {
                "current_password": "",
                "new_password": "newpass123",
                "confirm_password": "newpass123"
            }
        },
        {
            "name": "None值字段",
            "data": {
                "current_password": None,
                "new_password": "newpass123",
                "confirm_password": "newpass123"
            }
        },
        {
            "name": "额外字段",
            "data": {
                "current_password": "admin123",
                "new_password": "newpass123",
                "confirm_password": "newpass123",
                "extra_field": "should_be_ignored"
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n--- 测试 {i+1}: {test_case['name']} ---")
        print(f"请求数据: {json.dumps(test_case['data'], indent=2, ensure_ascii=False)}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/v1/pc/auth/change-password",
                json=test_case['data'],
                headers=headers,
                timeout=10
            )
            
            print(f"状态码: {response.status_code}")
            print(f"响应头: {dict(response.headers)}")
            
            try:
                response_data = response.json()
                print(f"响应JSON: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"响应文本: {response.text}")
                
            # 如果成功，恢复密码
            if response.status_code == 200 and test_case['name'] == "完整请求":
                print("\n--- 恢复密码 ---")
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
                    
        except requests.exceptions.Timeout:
            print("❌ 请求超时")
        except Exception as e:
            print(f"❌ 请求异常: {e}")

if __name__ == "__main__":
    debug_detailed_422()