#!/usr/bin/env python3
"""
机构管理API测试脚本
"""

import requests
import json

def test_institutions():
    base_url = "http://localhost:8000"
    
    print("🏢 机构管理API测试")
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
    
    # 2. 创建机构
    print("\n2. 创建机构")
    import time
    timestamp = int(time.time())
    institution_data = {
        "name": f"测试机构A_{timestamp}",
        "code": f"TEST001_{timestamp}",
        "contact_person": "张三",
        "phone": "13800138001",
        "email": f"test_{timestamp}@example.com",
        "address": "北京市朝阳区测试街道123号",
        "description": "这是一个测试机构",
        "status": "active",
        "admin_username": f"admin001_{timestamp}",
        "admin_email": f"admin001_{timestamp}@test.com",
        "admin_password": "admin123"
    }
    
    try:
        response = requests.post(f"{base_url}/institutions", json=institution_data, headers=auth_headers)
        print(f"创建机构状态码: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            institution_id = result.get("id")
            print(f"✅ 机构创建成功，ID: {institution_id}")
        else:
            print(f"❌ 创建失败: {response.text}")
            return
    except Exception as e:
        print(f"❌ 创建机构错误: {e}")
        return
    
    # 3. 获取机构列表
    print("\n3. 获取机构列表")
    try:
        response = requests.get(f"{base_url}/institutions?page=1&size=10", headers=auth_headers)
        print(f"获取列表状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 获取成功，共 {result.get('total', 0)} 条记录")
        else:
            print(f"❌ 获取失败: {response.text}")
    except Exception as e:
        print(f"❌ 获取列表错误: {e}")
    
    # 4. 获取机构详情
    print(f"\n4. 获取机构详情 (ID: {institution_id})")
    try:
        response = requests.get(f"{base_url}/institutions/{institution_id}", headers=auth_headers)
        print(f"获取详情状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 获取成功，机构名称: {result.get('name')}")
        else:
            print(f"❌ 获取失败: {response.text}")
    except Exception as e:
        print(f"❌ 获取详情错误: {e}")
    
    # 5. 更新机构信息
    print(f"\n5. 更新机构信息 (ID: {institution_id})")
    update_data = {
        "name": "测试机构A-已更新",
        "contact_person": "李四",
        "phone": "13800138002",
        "description": "这是更新后的测试机构"
    }
    
    try:
        response = requests.put(f"{base_url}/institutions/{institution_id}", json=update_data, headers=auth_headers)
        print(f"更新机构状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 更新成功，新名称: {result.get('name')}")
        else:
            print(f"❌ 更新失败: {response.text}")
    except Exception as e:
        print(f"❌ 更新机构错误: {e}")
    
    # 6. 获取机构统计
    print("\n6. 获取机构统计")
    try:
        response = requests.get(f"{base_url}/institutions/stats", headers=auth_headers)
        print(f"获取统计状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 统计信息: {result}")
        else:
            print(f"❌ 获取统计失败: {response.text}")
    except Exception as e:
        print(f"❌ 获取统计错误: {e}")
    
    # 7. 删除机构
    print(f"\n7. 删除机构 (ID: {institution_id})")
    try:
        response = requests.delete(f"{base_url}/institutions/{institution_id}", headers=auth_headers)
        print(f"删除机构状态码: {response.status_code}")
        
        if response.status_code == 204:
            print("✅ 删除成功")
        else:
            print(f"❌ 删除失败: {response.text}")
    except Exception as e:
        print(f"❌ 删除机构错误: {e}")
    
    print("\n" + "="*50)
    print("🏢 机构管理测试完成")

if __name__ == "__main__":
    test_institutions() 