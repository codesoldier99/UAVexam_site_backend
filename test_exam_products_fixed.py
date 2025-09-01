#!/usr/bin/env python3
"""
考试产品接口修复测试脚本
专门测试修复后的路由问题
"""

import requests
import json

# 配置
BASE_URL = "http://localhost:8000"
USERNAME = "admin"  # 请根据实际情况修改
PASSWORD = "admin123"  # 请根据实际情况修改

def test_fixed_issues():
    """测试修复的问题"""
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
    
    # 测试1: 带斜杠的路径问题
    print("🔧 测试1: 修复带斜杠路径的422错误")
    test_urls = [
        ("/api/v1/pc/exam-products", "无斜杠路径"),
        ("/api/v1/pc/exam-products/", "带斜杠路径"),
    ]
    
    for url, desc in test_urls:
        print(f"  测试 {desc}: {url}")
        response = session.get(f"{BASE_URL}{url}", headers=headers)
        print(f"    状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and "items" in data:
                print(f"    ✅ 成功 - 返回 {len(data['items'])} 条记录")
            else:
                print(f"    ⚠️  返回格式异常")
        elif response.status_code == 422:
            print(f"    ❌ 仍有422错误: {response.json()}")
        else:
            print(f"    ❌ 其他错误: {response.text}")
    
    # 测试2: 统计接口路径冲突问题
    print(f"\n🔧 测试2: 修复统计接口路径冲突")
    stats_urls = [
        ("/api/v1/pc/exam-products/statistics", "统计接口无斜杠"),
        ("/api/v1/pc/exam-products/statistics/", "统计接口带斜杠"),
    ]
    
    for url, desc in stats_urls:
        print(f"  测试 {desc}: {url}")
        response = session.get(f"{BASE_URL}{url}", headers=headers)
        print(f"    状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "total_products" in data:
                print(f"    ✅ 成功 - 总产品数: {data['total_products']}")
                print(f"      活跃产品: {data.get('active_products', 'N/A')}")
                print(f"      非活跃产品: {data.get('inactive_products', 'N/A')}")
            else:
                print(f"    ⚠️  返回格式异常: {data}")
        elif response.status_code == 422:
            error_detail = response.json()
            print(f"    ❌ 仍有422错误: {error_detail}")
        else:
            print(f"    ❌ 其他错误: {response.text}")
    
    # 测试3: 详情接口是否正常
    print(f"\n🔧 测试3: 验证详情接口正常工作")
    
    # 先获取一个产品ID
    list_response = session.get(f"{BASE_URL}/api/v1/pc/exam-products?limit=1", headers=headers)
    if list_response.status_code == 200:
        data = list_response.json()
        if isinstance(data, dict) and "items" in data and data["items"]:
            product_id = data["items"][0]["id"]
            print(f"  使用产品ID: {product_id}")
            
            # 测试详情接口（无斜杠）
            detail_url = f"/api/v1/pc/exam-products/{product_id}"
            print(f"  测试详情接口: {detail_url}")
            detail_response = session.get(f"{BASE_URL}{detail_url}", headers=headers)
            
            print(f"    状态码: {detail_response.status_code}")
            if detail_response.status_code == 200:
                detail_data = detail_response.json()
                print(f"    ✅ 获取详情成功")
                print(f"      名称: {detail_data.get('name', 'N/A')}")
                print(f"      代码: {detail_data.get('code', 'N/A')}")
            else:
                print(f"    ❌ 获取详情失败: {detail_response.text}")
        else:
            print("    ⚠️  没有找到可用的产品ID")
    else:
        print(f"    ❌ 获取产品列表失败: {list_response.text}")
    
    # 测试4: 验证路由优先级
    print(f"\n🔧 测试4: 验证路由优先级（statistics vs 动态参数）")
    
    # 这个应该匹配统计接口，而不是详情接口
    stats_test_url = "/api/v1/pc/exam-products/statistics"
    print(f"  测试路由: {stats_test_url}")
    response = session.get(f"{BASE_URL}{stats_test_url}", headers=headers)
    
    print(f"    状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if "total_products" in data:
            print(f"    ✅ 正确匹配统计接口")
        else:
            print(f"    ❌ 错误匹配为详情接口: {data}")
    else:
        print(f"    ❌ 接口调用失败: {response.text}")
    
    print(f"\n🏁 修复测试完成")

if __name__ == "__main__":
    print("考试产品接口修复验证")
    print("=" * 40)
    test_fixed_issues()