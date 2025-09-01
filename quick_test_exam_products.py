#!/usr/bin/env python3
"""
考试产品接口快速测试脚本
"""

import requests
import json

# 配置
BASE_URL = "http://localhost:8000"
USERNAME = "admin"  # 请根据实际情况修改
PASSWORD = "admin123"  # 请根据实际情况修改

def quick_test():
    """快速测试主要接口"""
    session = requests.Session()
    
    print("🔐 登录中...")
    # 登录
    login_response = session.post(
        f"{BASE_URL}/api/v1/pc/auth/login",
        json={"username": USERNAME, "password": PASSWORD}
    )
    
    if login_response.status_code != 200:
        print(f"❌ 登录失败: {login_response.status_code}")
        print(login_response.text)
        return
    
    token = login_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    print("✅ 登录成功")
    
    # 测试考试产品列表接口
    print("\n📋 测试考试产品列表...")
    
    test_urls = [
        "/api/v1/pc/exam-products",
        "/api/v1/pc/exam-products/",
        "/api/v1/pc/exam-products?skip=0&limit=10"
    ]
    
    for url in test_urls:
        print(f"\n测试: {url}")
        response = session.get(f"{BASE_URL}{url}", headers=headers)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and "items" in data:
                print(f"✅ 成功 - 返回 {len(data['items'])} 条记录")
                print(f"总数: {data.get('total')}, 页数: {data.get('pages')}")
            elif isinstance(data, list):
                print(f"✅ 成功 - 返回 {len(data)} 条记录（旧格式）")
        elif response.status_code == 307:
            print(f"🔄 重定向: {response.headers.get('Location')}")
        else:
            print(f"❌ 失败: {response.text}")
    
    print("\n🏁 快速测试完成")

if __name__ == "__main__":
    quick_test()