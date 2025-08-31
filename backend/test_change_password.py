#!/usr/bin/env python3
"""
测试修改密码接口
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_change_password():
    """测试修改密码接口"""
    
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
            
            # 2. 测试修改密码接口
            print("\n2. 测试修改密码接口...")
            headers = {"Authorization": f"Bearer {token}"}
            
            change_password_data = {
                "current_password": "123456",
                "new_password": "newpass123",
                "confirm_password": "newpass123"
            }
            
            change_response = requests.post(
                f"{BASE_URL}/api/v1/pc/auth/change-password", 
                json=change_password_data,
                headers=headers
            )
            
            print(f"修改密码状态码: {change_response.status_code}")
            print(f"修改密码响应: {change_response.text}")
            
            if change_response.status_code == 200:
                print("✅ 修改密码接口测试成功")
                
                # 3. 用新密码重新登录验证
                print("\n3. 用新密码重新登录验证...")
                new_login_data = {
                    "username": "beijing_admin", 
                    "password": "newpass123"
                }
                
                new_login_response = requests.post(f"{BASE_URL}/api/v1/pc/auth/login", json=new_login_data)
                print(f"新密码登录状态码: {new_login_response.status_code}")
                
                if new_login_response.status_code == 200:
                    print("✅ 新密码登录成功，密码修改验证通过")
                    
                    # 4. 恢复原密码
                    print("\n4. 恢复原密码...")
                    new_token = new_login_response.json().get("access_token")
                    new_headers = {"Authorization": f"Bearer {new_token}"}
                    
                    restore_password_data = {
                        "current_password": "newpass123",
                        "new_password": "123456", 
                        "confirm_password": "123456"
                    }
                    
                    restore_response = requests.post(
                        f"{BASE_URL}/api/v1/pc/auth/change-password",
                        json=restore_password_data,
                        headers=new_headers
                    )
                    
                    if restore_response.status_code == 200:
                        print("✅ 密码已恢复为原密码")
                    else:
                        print(f"❌ 密码恢复失败: {restore_response.text}")
                        
                else:
                    print(f"❌ 新密码登录失败: {new_login_response.text}")
            else:
                print(f"❌ 修改密码失败: {change_response.text}")
        else:
            print(f"❌ 登录失败: {login_response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败，请确保后端服务正在运行")
    except Exception as e:
        print(f"❌ 测试出错: {str(e)}")

if __name__ == "__main__":
    test_change_password()