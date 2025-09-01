#!/usr/bin/env python3
"""
路由修复验证脚本
专门测试带斜杠路径的422错误是否修复
"""

import requests
import json

# 配置
BASE_URL = "http://localhost:8000"
USERNAME = "admin"  # 请根据实际情况修改
PASSWORD = "admin123"  # 请根据实际情况修改

def test_route_fix():
    """测试路由修复"""
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
    
    print("✅ 登录成功\n")
    
    # 测试之前出现422错误的路径
    print("🔧 测试修复前出现422错误的路径")
    
    problem_urls = [
        ("/api/v1/pc/exam-products/", "考试产品列表（带斜杠）"),
        ("/api/v1/pc/exam-products/?skip=0&limit=10", "考试产品列表（带斜杠+参数）"),
        ("/api/v1/pc/exam-products/statistics/", "考试产品统计（带斜杠）"),
    ]
    
    for url, desc in problem_urls:
        print(f"\n  测试 {desc}")
        print(f"  URL: {url}")
        response = session.get(f"{BASE_URL}{url}", headers=headers)
        print(f"  状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "items" in data:
                print(f"  ✅ 成功 - 返回 {len(data['items'])} 条记录")
            elif "total_products" in data:
                print(f"  ✅ 成功 - 统计数据: {data['total_products']} 个产品")
            else:
                print(f"  ✅ 成功 - 返回数据: {type(data)}")
        elif response.status_code == 422:
            error_detail = response.json()
            print(f"  ❌ 仍有422错误:")
            print(f"    {error_detail}")
        else:
            print(f"  ⚠️  其他状态码: {response.text}")
    
    # 对比测试：无斜杠路径应该正常工作
    print(f"\n🔧 对比测试：无斜杠路径")
    
    working_urls = [
        ("/api/v1/pc/exam-products", "考试产品列表（无斜杠）"),
        ("/api/v1/pc/exam-products?skip=0&limit=10", "考试产品列表（无斜杠+参数）"),
        ("/api/v1/pc/exam-products/statistics", "考试产品统计（无斜杠）"),
    ]
    
    for url, desc in working_urls:
        print(f"\n  测试 {desc}")
        print(f"  URL: {url}")
        response = session.get(f"{BASE_URL}{url}", headers=headers)
        print(f"  状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "items" in data:
                print(f"  ✅ 成功 - 返回 {len(data['items'])} 条记录")
            elif "total_products" in data:
                print(f"  ✅ 成功 - 统计数据: {data['total_products']} 个产品")
            else:
                print(f"  ✅ 成功")
        else:
            print(f"  ❌ 失败: {response.text}")
    
    print(f"\n🏁 路由修复测试完成")

if __name__ == "__main__":
    print("路由修复验证脚本")
    print("=" * 40)
    test_route_fix()