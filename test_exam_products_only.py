#!/usr/bin/env python3
"""
考试产品管理API测试脚本
"""

import requests
import json

def test_exam_products():
    base_url = "http://localhost:8000"
    
    print("📚 考试产品管理API测试")
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
    
    # 2. 创建考试产品
    print("\n2. 创建考试产品")
    exam_product_data = {
        "name": "Python编程基础考试",
        "description": "Python编程基础知识和技能测试",
        "duration_minutes": 120,
        "is_active": True
    }
    
    try:
        response = requests.post(f"{base_url}/exam-products", json=exam_product_data, headers=auth_headers)
        print(f"创建产品状态码: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            product_id = result.get("id")
            print(f"✅ 考试产品创建成功，ID: {product_id}")
        else:
            print(f"❌ 创建失败: {response.text}")
            return
    except Exception as e:
        print(f"❌ 创建产品错误: {e}")
        return
    
    # 3. 获取考试产品列表
    print("\n3. 获取考试产品列表")
    try:
        response = requests.get(f"{base_url}/exam-products?page=1&size=10", headers=auth_headers)
        print(f"获取列表状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 获取成功，共 {result.get('total', 0)} 条记录")
        else:
            print(f"❌ 获取失败: {response.text}")
    except Exception as e:
        print(f"❌ 获取列表错误: {e}")
    
    # 4. 获取考试产品详情
    print(f"\n4. 获取考试产品详情 (ID: {product_id})")
    try:
        response = requests.get(f"{base_url}/exam-products/{product_id}", headers=auth_headers)
        print(f"获取详情状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 获取成功，产品名称: {result.get('name')}")
            print(f"   描述: {result.get('description')}")
            print(f"   时长: {result.get('duration_minutes')} 分钟")
            print(f"   状态: {'启用' if result.get('is_active') else '禁用'}")
        else:
            print(f"❌ 获取失败: {response.text}")
    except Exception as e:
        print(f"❌ 获取详情错误: {e}")
    
    # 5. 更新考试产品
    print(f"\n5. 更新考试产品 (ID: {product_id})")
    update_data = {
        "name": "Python编程基础考试-高级版",
        "description": "更新后的Python编程基础知识和技能测试",
        "duration_minutes": 150,
        "is_active": True
    }
    
    try:
        response = requests.put(f"{base_url}/exam-products/{product_id}", json=update_data, headers=auth_headers)
        print(f"更新产品状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 更新成功，新名称: {result.get('name')}")
            print(f"   新描述: {result.get('description')}")
            print(f"   新时长: {result.get('duration_minutes')} 分钟")
        else:
            print(f"❌ 更新失败: {response.text}")
    except Exception as e:
        print(f"❌ 更新产品错误: {e}")
    
    # 6. 删除考试产品
    print(f"\n6. 删除考试产品 (ID: {product_id})")
    try:
        response = requests.delete(f"{base_url}/exam-products/{product_id}", headers=auth_headers)
        print(f"删除产品状态码: {response.status_code}")
        
        if response.status_code == 204:
            print("✅ 删除成功")
        else:
            print(f"❌ 删除失败: {response.text}")
    except Exception as e:
        print(f"❌ 删除产品错误: {e}")
    
    print("\n" + "="*50)
    print("📚 考试产品管理测试完成")

if __name__ == "__main__":
    test_exam_products() 