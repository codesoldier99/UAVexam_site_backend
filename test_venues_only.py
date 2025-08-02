#!/usr/bin/env python3
"""
考场资源管理API测试脚本
"""

import requests
import json

def test_venues():
    base_url = "http://localhost:8000"
    
    print("🏫 考场资源管理API测试")
    print("="*50)
    
    # 1. 管理员登录
    print("1. 管理员登录")
    login_data = "username=admin@exam.com&password=admin123"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    try:
        response = requests.post(f"{base_url}/auth/jwt/login", data=login_data, headers=headers)
        print(f"登录状态码: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            admin_token = token_data.get("access_token")
            auth_headers = {"Authorization": f"Bearer {admin_token}"}
            print("✅ 登录成功")
        else:
            print("❌ 登录失败")
            return
    except Exception as e:
        print(f"❌ 连接错误: {e}")
        return
    
    # 2. 创建考场资源
    print("\n2. 创建考场资源")
    venue_data = {
        "name": "北京朝阳考场",
        "code": "BJ001",
        "address": "北京市朝阳区建国路88号",
        "capacity": 100,
        "description": "现代化考场，设备齐全",
        "contact_person": "王五",
        "contact_phone": "010-12345678",
        "status": "active",
        "venue_type": "标准考场",
        "facilities": "电脑、投影仪、音响设备"
    }
    
    try:
        response = requests.post(f"{base_url}/venues", json=venue_data, headers=auth_headers)
        print(f"创建考场状态码: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            venue_id = result.get("id")
            print(f"✅ 考场资源创建成功，ID: {venue_id}")
        else:
            print(f"❌ 创建失败: {response.text}")
            return
    except Exception as e:
        print(f"❌ 创建考场错误: {e}")
        return
    
    # 3. 获取考场资源列表
    print("\n3. 获取考场资源列表")
    try:
        response = requests.get(f"{base_url}/venues?page=1&size=10", headers=auth_headers)
        print(f"获取列表状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 获取成功，共 {result.get('total', 0)} 条记录")
        else:
            print(f"❌ 获取失败: {response.text}")
    except Exception as e:
        print(f"❌ 获取列表错误: {e}")
    
    # 4. 获取考场资源详情
    print(f"\n4. 获取考场资源详情 (ID: {venue_id})")
    try:
        response = requests.get(f"{base_url}/venues/{venue_id}", headers=auth_headers)
        print(f"获取详情状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 获取成功，考场名称: {result.get('name')}")
            print(f"   地址: {result.get('address')}")
            print(f"   容量: {result.get('capacity')} 人")
        else:
            print(f"❌ 获取失败: {response.text}")
    except Exception as e:
        print(f"❌ 获取详情错误: {e}")
    
    # 5. 更新考场资源
    print(f"\n5. 更新考场资源 (ID: {venue_id})")
    update_data = {
        "name": "北京朝阳考场-升级版",
        "capacity": 150,
        "description": "升级后的现代化考场，设备更齐全",
        "facilities": "电脑、投影仪、音响设备、监控系统"
    }
    
    try:
        response = requests.put(f"{base_url}/venues/{venue_id}", json=update_data, headers=auth_headers)
        print(f"更新考场状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 更新成功，新名称: {result.get('name')}")
            print(f"   新容量: {result.get('capacity')} 人")
        else:
            print(f"❌ 更新失败: {response.text}")
    except Exception as e:
        print(f"❌ 更新考场错误: {e}")
    
    # 6. 删除考场资源
    print(f"\n6. 删除考场资源 (ID: {venue_id})")
    try:
        response = requests.delete(f"{base_url}/venues/{venue_id}", headers=auth_headers)
        print(f"删除考场状态码: {response.status_code}")
        
        if response.status_code == 204:
            print("✅ 删除成功")
        else:
            print(f"❌ 删除失败: {response.text}")
    except Exception as e:
        print(f"❌ 删除考场错误: {e}")
    
    print("\n" + "="*50)
    print("🏫 考场资源管理测试完成")

if __name__ == "__main__":
    test_venues() 