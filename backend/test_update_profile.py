#!/usr/bin/env python3
"""
测试更新用户资料接口
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_update_profile():
    """测试更新用户资料接口"""
    
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
            
            # 2. 获取当前用户信息
            print("\n2. 获取当前用户信息...")
            headers = {"Authorization": f"Bearer {token}"}
            
            profile_response = requests.get(f"{BASE_URL}/api/v1/pc/auth/profile", headers=headers)
            print(f"获取资料状态码: {profile_response.status_code}")
            
            if profile_response.status_code == 200:
                current_profile = profile_response.json()
                print(f"当前用户信息: {json.dumps(current_profile, indent=2, ensure_ascii=False)}")
                
                # 3. 更新用户资料
                print("\n3. 更新用户资料...")
                update_data = {
                    "real_name": "更新后的管理员",
                    "email": "updated_admin@example.com",
                    "phone": "13800138999"
                }
                
                update_response = requests.put(
                    f"{BASE_URL}/api/v1/pc/auth/profile",
                    json=update_data,
                    headers=headers
                )
                
                print(f"更新资料状态码: {update_response.status_code}")
                print(f"更新资料响应: {update_response.text}")
                
                if update_response.status_code == 200:
                    print("✅ 用户资料更新成功")
                    
                    # 4. 再次获取用户信息验证更新
                    print("\n4. 验证更新结果...")
                    verify_response = requests.get(f"{BASE_URL}/api/v1/pc/auth/profile", headers=headers)
                    
                    if verify_response.status_code == 200:
                        updated_profile = verify_response.json()
                        print(f"更新后用户信息: {json.dumps(updated_profile, indent=2, ensure_ascii=False)}")
                        print("✅ 用户资料更新验证成功")
                    else:
                        print(f"❌ 验证更新失败: {verify_response.text}")
                        
                else:
                    print(f"❌ 用户资料更新失败: {update_response.text}")
            else:
                print(f"❌ 获取用户信息失败: {profile_response.text}")
        else:
            print(f"❌ 登录失败: {login_response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败，请确保后端服务正在运行")
    except Exception as e:
        print(f"❌ 测试出错: {str(e)}")

if __name__ == "__main__":
    test_update_profile()