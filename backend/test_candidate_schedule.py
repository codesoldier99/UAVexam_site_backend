#!/usr/bin/env python3
"""
测试考生安排查询
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_candidate_schedule():
    """测试考生安排查询"""
    
    print("=== 测试考生安排查询 ===")
    
    # 首先需要一个考生用户的token
    # 这里我们先用admin登录获取token，然后测试接口
    
    # 1. 登录获取token
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
    
    # 2. 测试考生安排查询接口
    print("\n=== 测试考生安排查询接口 ===")
    
    try:
        # 注意：这个接口路径是 /api/v1/wechat/candidate/schedule
        # 但我们用PC端的token来测试，看看是否还有数据库字段问题
        response = requests.get(
            f"{BASE_URL}/api/v1/wechat/candidate/schedule",
            headers=headers,
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 考生安排查询成功")
            response_data = response.json()
            print(f"响应: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ 考生安排查询失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")

if __name__ == "__main__":
    test_candidate_schedule()