#!/usr/bin/env python3
"""
测试所有报名相关接口
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_login():
    """测试登录"""
    print("=== 测试登录 ===")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/pc/auth/login",
            json=login_data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 登录成功")
            return data.get("access_token")
        else:
            print(f"❌ 登录失败: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 登录异常: {e}")
        return None

def test_get_registrations(token):
    """测试获取报名列表"""
    print("\n=== 测试获取报名列表 ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/pc/registrations",
            headers=headers,
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取报名列表成功，共 {data.get('total', 0)} 条记录")
            return data.get('items', [])
        else:
            print(f"❌ 获取报名列表失败: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ 获取报名列表异常: {e}")
        return []

def test_get_registration_detail(token, registration_id):
    """测试获取报名详情"""
    print(f"\n=== 测试获取报名详情 (ID: {registration_id}) ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/pc/registrations/{registration_id}",
            headers=headers,
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取报名详情成功: {data.get('registration_number', 'N/A')}")
            return data
        else:
            print(f"❌ 获取报名详情失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 获取报名详情异常: {e}")
        return None

def test_update_registration_status(token, registration_id):
    """测试更新报名状态"""
    print(f"\n=== 测试更新报名状态 (ID: {registration_id}) ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    update_data = {
        "status": "approved",
        "notes": "测试更新状态"
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/api/v1/pc/registrations/{registration_id}/status",
            json=update_data,
            headers=headers,
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 更新报名状态成功")
            return data
        else:
            print(f"❌ 更新报名状态失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 更新报名状态异常: {e}")
        return None

def test_get_registration_statistics(token):
    """测试获取报名统计"""
    print(f"\n=== 测试获取报名统计 ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/pc/registrations/statistics",
            headers=headers,
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取报名统计成功")
            print(f"   总报名数: {data.get('total_registrations', 0)}")
            print(f"   待审核: {data.get('pending_registrations', 0)}")
            print(f"   已通过: {data.get('approved_registrations', 0)}")
            print(f"   已拒绝: {data.get('rejected_registrations', 0)}")
            return data
        else:
            print(f"❌ 获取报名统计失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 获取报名统计异常: {e}")
        return None

def main():
    print("开始测试所有报名相关接口...")
    
    # 1. 登录
    token = test_login()
    if not token:
        print("❌ 登录失败，终止测试")
        sys.exit(1)
    
    # 2. 获取报名列表
    registrations = test_get_registrations(token)
    
    # 3. 测试报名详情（如果有数据）
    if registrations:
        first_registration = registrations[0]
        registration_id = first_registration.get('id')
        if registration_id:
            test_get_registration_detail(token, registration_id)
            test_update_registration_status(token, registration_id)
    
    # 4. 测试报名统计
    test_get_registration_statistics(token)
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    main()