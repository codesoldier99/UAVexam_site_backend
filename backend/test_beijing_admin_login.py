#!/usr/bin/env python3
"""
测试beijing_admin登录
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_beijing_admin_login():
    """测试beijing_admin登录"""
    
    print("=== 测试beijing_admin登录 ===")
    
    # 测试登录
    login_data = {
        "username": "beijing_admin",
        "password": "beijing123"
    }
    
    print(f"登录数据: {json.dumps(login_data, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/pc/auth/login",
            json=login_data,
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 登录成功")
            response_data = response.json()
            print(f"响应: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
            
            # 测试修改密码
            token = response_data["access_token"]
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            print("\n=== 测试修改密码 ===")
            password_data = {
                "old_password": "beijing123",
                "new_password": "newpass123",
                "confirm_password": "newpass123"
            }
            
            change_response = requests.post(
                f"{BASE_URL}/api/v1/pc/auth/change-password",
                json=password_data,
                headers=headers
            )
            
            print(f"修改密码状态码: {change_response.status_code}")
            if change_response.status_code == 200:
                print("✅ 修改密码成功")
                print(f"响应: {change_response.json()}")
                
                # 恢复密码
                restore_data = {
                    "old_password": "newpass123",
                    "new_password": "beijing123",
                    "confirm_password": "beijing123"
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
                print(f"❌ 修改密码失败: {change_response.text}")
                
        else:
            print(f"❌ 登录失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")

if __name__ == "__main__":
    test_beijing_admin_login()