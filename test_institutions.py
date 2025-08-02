import requests
import json
from typing import Dict, Any

# 测试配置
BASE_URL = "http://localhost:8000"

def test_simple_institutions():
    """测试简化的机构管理API"""
    print("开始测试机构管理API...")
    
    # 测试1: 创建机构
    print("\n1. 测试创建机构")
    create_data = {
        "name": "测试培训机构",
        "code": "TEST_001",
        "contact_person": "测试联系人",
        "phone": "13800138000",
        "email": "test@example.com",
        "address": "测试地址",
        "description": "测试机构描述",
        "status": "active",
        "license_number": "TEST_LIC001",
        "business_scope": "测试经营范围"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/simple-institutions", json=create_data)
        print(f"创建机构响应状态码: {response.status_code}")
        if response.status_code == 200:
            print("✓ 创建机构成功")
            print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        else:
            print(f"✗ 创建机构失败: {response.text}")
    except Exception as e:
        print(f"✗ 创建机构请求异常: {e}")
    
    # 测试2: 获取机构列表
    print("\n2. 测试获取机构列表")
    try:
        response = requests.get(f"{BASE_URL}/simple-institutions")
        print(f"获取机构列表响应状态码: {response.status_code}")
        if response.status_code == 200:
            print("✓ 获取机构列表成功")
            data = response.json()
            print(f"机构总数: {data.get('total', 0)}")
            print(f"机构列表: {json.dumps(data.get('items', []), indent=2, ensure_ascii=False)}")
        else:
            print(f"✗ 获取机构列表失败: {response.text}")
    except Exception as e:
        print(f"✗ 获取机构列表请求异常: {e}")
    
    # 测试3: 获取机构详情
    print("\n3. 测试获取机构详情")
    try:
        response = requests.get(f"{BASE_URL}/simple-institutions/1")
        print(f"获取机构详情响应状态码: {response.status_code}")
        if response.status_code == 200:
            print("✓ 获取机构详情成功")
            print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        else:
            print(f"✗ 获取机构详情失败: {response.text}")
    except Exception as e:
        print(f"✗ 获取机构详情请求异常: {e}")
    
    # 测试4: 更新机构
    print("\n4. 测试更新机构")
    update_data = {
        "name": "更新后的机构名称",
        "contact_person": "更新后的联系人",
        "phone": "13900139000",
        "email": "updated@example.com",
        "description": "更新后的描述"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/simple-institutions/1", json=update_data)
        print(f"更新机构响应状态码: {response.status_code}")
        if response.status_code == 200:
            print("✓ 更新机构成功")
            print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        else:
            print(f"✗ 更新机构失败: {response.text}")
    except Exception as e:
        print(f"✗ 更新机构请求异常: {e}")
    
    # 测试5: 更新机构状态
    print("\n5. 测试更新机构状态")
    try:
        response = requests.patch(f"{BASE_URL}/simple-institutions/1/status?status=inactive")
        print(f"更新机构状态响应状态码: {response.status_code}")
        if response.status_code == 200:
            print("✓ 更新机构状态成功")
            print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        else:
            print(f"✗ 更新机构状态失败: {response.text}")
    except Exception as e:
        print(f"✗ 更新机构状态请求异常: {e}")
    
    # 测试6: 批量更新机构状态
    print("\n6. 测试批量更新机构状态")
    bulk_data = {
        "institution_ids": [1, 2],
        "status": "active"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/simple-institutions/bulk-status", json=bulk_data)
        print(f"批量更新机构状态响应状态码: {response.status_code}")
        if response.status_code == 200:
            print("✓ 批量更新机构状态成功")
            print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        else:
            print(f"✗ 批量更新机构状态失败: {response.text}")
    except Exception as e:
        print(f"✗ 批量更新机构状态请求异常: {e}")
    
    # 测试7: 复制机构
    print("\n7. 测试复制机构")
    try:
        response = requests.post(f"{BASE_URL}/simple-institutions/1/duplicate?new_name=复制的机构")
        print(f"复制机构响应状态码: {response.status_code}")
        if response.status_code == 200:
            print("✓ 复制机构成功")
            print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        else:
            print(f"✗ 复制机构失败: {response.text}")
    except Exception as e:
        print(f"✗ 复制机构请求异常: {e}")
    
    # 测试8: 获取机构统计信息
    print("\n8. 测试获取机构统计信息")
    try:
        response = requests.get(f"{BASE_URL}/simple-institutions/stats")
        print(f"获取机构统计信息响应状态码: {response.status_code}")
        if response.status_code == 200:
            print("✓ 获取机构统计信息成功")
            print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        else:
            print(f"✗ 获取机构统计信息失败: {response.text}")
    except Exception as e:
        print(f"✗ 获取机构统计信息请求异常: {e}")
    
    # 测试9: 删除机构
    print("\n9. 测试删除机构")
    try:
        response = requests.delete(f"{BASE_URL}/simple-institutions/999")
        print(f"删除机构响应状态码: {response.status_code}")
        if response.status_code == 200:
            print("✓ 删除机构成功")
            print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        else:
            print(f"✗ 删除机构失败: {response.text}")
    except Exception as e:
        print(f"✗ 删除机构请求异常: {e}")
    
    print("\n机构管理API测试完成！")

def test_health_endpoints():
    """测试健康检查端点"""
    print("\n开始测试健康检查端点...")
    
    # 测试根端点
    print("\n1. 测试根端点")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"根端点响应状态码: {response.status_code}")
        if response.status_code == 200:
            print("✓ 根端点正常")
            print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        else:
            print(f"✗ 根端点异常: {response.text}")
    except Exception as e:
        print(f"✗ 根端点请求异常: {e}")
    
    # 测试测试端点
    print("\n2. 测试测试端点")
    try:
        response = requests.get(f"{BASE_URL}/test")
        print(f"测试端点响应状态码: {response.status_code}")
        if response.status_code == 200:
            print("✓ 测试端点正常")
            print(f"响应内容: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        else:
            print(f"✗ 测试端点异常: {response.text}")
    except Exception as e:
        print(f"✗ 测试端点请求异常: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("机构管理模块API测试")
    print("=" * 50)
    
    # 测试健康检查端点
    test_health_endpoints()
    
    # 测试机构管理API
    test_simple_institutions()
    
    print("\n" + "=" * 50)
    print("所有测试完成！")
    print("=" * 50) 