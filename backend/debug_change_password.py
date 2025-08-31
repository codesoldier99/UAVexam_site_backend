#!/usr/bin/env python3
"""
调试修改密码接口的参数验证问题
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def debug_change_password():
    """调试修改密码接口"""
    
    # 1. 先登录获取token
    print("1. 登录获取token...")
    login_data = {
        "username": "beijing_admin",
        "password": "123456"
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/api/v1/pc/auth/login", json=login_data)
        print(f"登录状态码: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data.get("access_token")
            print("✅ 登录成功")
            
            # 2. 测试修改密码接口 - 详细错误信息
            print("\n2. 测试修改密码接口...")
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            change_password_data = {
                "current_password": "123456",
                "new_password": "newpass123",
                "confirm_password": "newpass123"
            }
            
            print(f"请求数据: {json.dumps(change_password_data, indent=2, ensure_ascii=False)}")
            print(f"请求头: {headers}")
            
            change_response = requests.post(
                f"{BASE_URL}/api/v1/pc/auth/change-password", 
                json=change_password_data,
                headers=headers
            )
            
            print(f"\n修改密码状态码: {change_response.status_code}")
            print(f"响应头: {dict(change_response.headers)}")
            
            try:
                response_json = change_response.json()
                print(f"响应内容: {json.dumps(response_json, indent=2, ensure_ascii=False)}")
            except:
                print(f"响应文本: {change_response.text}")
                
        else:
            print(f"❌ 登录失败: {login_response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败，请确保后端服务正在运行")
    except Exception as e:
        print(f"❌ 测试出错: {str(e)}")

if __name__ == "__main__":
    debug_change_password()