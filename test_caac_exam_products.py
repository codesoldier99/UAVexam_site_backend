#!/usr/bin/env python3
"""
基于CAAC无人机驾驶员考试分类体系的测试脚本
"""

import requests
import json

def test_caac_exam_products():
    base_url = "http://localhost:8000"
    
    print("🚁 CAAC无人机驾驶员考试产品测试")
    print("="*60)
    
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
    
    # 2. 创建视距内多旋翼无人机考试产品
    print("\n2. 创建视距内多旋翼无人机考试产品")
    vlos_multi_data = {
        "name": "视距内多旋翼无人机驾驶员考试",
        "code": "VLOS-MULTI-001",
        "description": "在肉眼可见范围内操控多旋翼无人机，适用于航拍、短距离巡检等基础作业",
        "category": "VLOS",
        "exam_type": "MULTIROTOR",
        "exam_class": "FILM_PHOTOGRAPHY",
        "exam_level": "PILOT",
        "theory_pass_score": 70,
        "practical_pass_score": 80,
        "duration_minutes": 120,
        "training_hours": 44,
        "price": 7500.0,
        "training_price": 6800.0,
        "theory_content": "无人机法规、飞行原理、气象知识、应急处置",
        "practical_content": "GPS模式悬停、水平8字飞行、定点降落",
        "requirements": "年满16周岁，初中以上学历，无犯罪记录，矫正视力≥1.0",
        "is_active": True
    }
    
    try:
        response = requests.post(f"{base_url}/exam-products", json=vlos_multi_data, headers=auth_headers)
        print(f"创建产品状态码: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            product_id = result.get("id")
            print(f"✅ 视距内多旋翼考试产品创建成功，ID: {product_id}")
        else:
            print(f"❌ 创建失败: {response.text}")
            return
    except Exception as e:
        print(f"❌ 创建产品错误: {e}")
        return
    
    # 3. 创建超视距固定翼无人机考试产品
    print("\n3. 创建超视距固定翼无人机考试产品")
    bvlos_fixed_data = {
        "name": "超视距固定翼无人机机长考试",
        "code": "BVLOS-FIXED-001",
        "description": "超出目视范围操控固定翼无人机，需通过地面站规划航线，适用于电力巡检、长距离测绘等复杂任务",
        "category": "BVLOS",
        "exam_type": "FIXED_WING",
        "exam_class": "POWER_INSPECTION",
        "exam_level": "CAPTAIN",
        "theory_pass_score": 80,
        "practical_pass_score": 85,
        "duration_minutes": 180,
        "training_hours": 56,
        "price": 12000.0,
        "training_price": 15000.0,
        "theory_content": "复杂气象分析、航线规划、应急处理、地面站操作",
        "practical_content": "姿态模式精准控制、地面站操作、应急返航",
        "requirements": "大专学历或100小时飞行经验，年满18周岁，无犯罪记录",
        "is_active": True
    }
    
    try:
        response = requests.post(f"{base_url}/exam-products", json=bvlos_fixed_data, headers=auth_headers)
        print(f"创建产品状态码: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            product_id_2 = result.get("id")
            print(f"✅ 超视距固定翼考试产品创建成功，ID: {product_id_2}")
        else:
            print(f"❌ 创建失败: {response.text}")
    except Exception as e:
        print(f"❌ 创建产品错误: {e}")
    
    # 4. 创建农业植保类考试产品
    print("\n4. 创建农业植保类考试产品")
    agriculture_data = {
        "name": "农业植保无人机驾驶员考试",
        "code": "AGRI-MULTI-001",
        "description": "专门针对农业植保作业的无人机驾驶员考试，需掌握农药喷洒、播撒等专业操作",
        "category": "VLOS",
        "exam_type": "MULTIROTOR",
        "exam_class": "AGRICULTURE",
        "exam_level": "PILOT",
        "theory_pass_score": 70,
        "practical_pass_score": 80,
        "duration_minutes": 150,
        "training_hours": 50,
        "price": 8000.0,
        "training_price": 7200.0,
        "theory_content": "农药知识、植保技术、安全操作、环保要求",
        "practical_content": "农药喷洒操作、播撒技术、农田作业规划",
        "requirements": "年满16周岁，初中以上学历，无犯罪记录，身体健康",
        "is_active": True
    }
    
    try:
        response = requests.post(f"{base_url}/exam-products", json=agriculture_data, headers=auth_headers)
        print(f"创建产品状态码: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            product_id_3 = result.get("id")
            print(f"✅ 农业植保考试产品创建成功，ID: {product_id_3}")
        else:
            print(f"❌ 创建失败: {response.text}")
    except Exception as e:
        print(f"❌ 创建产品错误: {e}")
    
    # 5. 获取考试产品列表
    print("\n5. 获取考试产品列表")
    try:
        response = requests.get(f"{base_url}/exam-products?page=1&size=10", headers=auth_headers)
        print(f"获取列表状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 获取成功，共 {result.get('total', 0)} 条记录")
            
            # 显示产品详情
            items = result.get('items', [])
            for item in items:
                print(f"  - {item.get('name')} ({item.get('code')})")
                print(f"    种类: {item.get('category')}")
                print(f"    类型: {item.get('exam_type')}")
                print(f"    类别: {item.get('exam_class')}")
                print(f"    等级: {item.get('exam_level')}")
                print(f"    费用: {item.get('price')} 元")
                print()
        else:
            print(f"❌ 获取失败: {response.text}")
    except Exception as e:
        print(f"❌ 获取列表错误: {e}")
    
    # 6. 按分类筛选考试产品
    print("\n6. 按分类筛选考试产品")
    try:
        # 筛选视距内考试
        response = requests.get(f"{base_url}/exam-products?category=VLOS", headers=auth_headers)
        print(f"视距内考试筛选状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 视距内考试产品: {result.get('total', 0)} 条")
        
        # 筛选多旋翼考试
        response = requests.get(f"{base_url}/exam-products?exam_type=MULTIROTOR", headers=auth_headers)
        print(f"多旋翼考试筛选状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 多旋翼考试产品: {result.get('total', 0)} 条")
            
    except Exception as e:
        print(f"❌ 筛选错误: {e}")
    
    print("\n" + "="*60)
    print("🚁 CAAC无人机驾驶员考试产品测试完成")

if __name__ == "__main__":
    test_caac_exam_products() 