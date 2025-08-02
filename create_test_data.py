#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建测试数据
"""

import requests
import json
from datetime import datetime, timedelta

# API基础URL
BASE_URL = "http://localhost:8000"

def create_test_data():
    """创建测试数据"""
    print("🔧 开始创建测试数据...")
    
    # 1. 登录
    print("\n1. 登录...")
    login_data = {
        "username": "admin@exam.com",
        "password": "admin123"
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/auth/jwt/login", data=login_data)
        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data.get("access_token")
            print(f"✅ 登录成功")
        else:
            print(f"❌ 登录失败: {login_response.status_code}")
            return
    except Exception as e:
        print(f"❌ 登录异常: {e}")
        return
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # 2. 创建考试产品
    print("\n2. 创建考试产品...")
    exam_products = [
        {
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
        },
        {
            "name": "超视距固定翼无人机驾驶员考试",
            "code": "BVLOS-FIXED-001",
            "description": "超视距操控固定翼无人机，适用于长距离巡检、测绘等专业作业",
            "category": "BVLOS",
            "exam_type": "FIXED_WING",
            "exam_class": "POWER_INSPECTION",
            "exam_level": "CAPTAIN",
            "theory_pass_score": 80,
            "practical_pass_score": 85,
            "duration_minutes": 180,
            "training_hours": 60,
            "price": 12000.0,
            "training_price": 10000.0,
            "theory_content": "高级飞行原理、导航系统、通信技术、应急处理",
            "practical_content": "长距离飞行、复杂气象条件飞行、应急返航",
            "requirements": "年满18周岁，高中以上学历，无犯罪记录，矫正视力≥1.0，有基础飞行经验",
            "is_active": True
        },
        {
            "name": "农业植保无人机驾驶员考试",
            "code": "AGRI-MULTI-001",
            "description": "专门针对农业植保作业的无人机驾驶员考试",
            "category": "VLOS",
            "exam_type": "MULTIROTOR",
            "exam_class": "AGRICULTURE",
            "exam_level": "PILOT",
            "theory_pass_score": 75,
            "practical_pass_score": 80,
            "duration_minutes": 90,
            "training_hours": 36,
            "price": 6000.0,
            "training_price": 5000.0,
            "theory_content": "农业植保知识、农药使用安全、飞行规划",
            "practical_content": "植保飞行路径规划、农药喷洒操作、安全返航",
            "requirements": "年满16周岁，初中以上学历，无犯罪记录，矫正视力≥1.0",
            "is_active": True
        }
    ]
    
    created_products = []
    for product in exam_products:
        try:
            response = requests.post(
                f"{BASE_URL}/exam-products/",
                json=product,
                headers=headers
            )
            
            if response.status_code == 200:
                created_product = response.json()
                created_products.append(created_product)
                print(f"✅ 创建考试产品: {created_product.get('name')} (ID: {created_product.get('id')})")
            else:
                print(f"❌ 创建考试产品失败: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"❌ 创建考试产品异常: {e}")
    
    # 3. 创建考场
    print("\n3. 创建考场...")
    venues = [
        {
            "name": "无人机考试中心A",
            "address": "北京市朝阳区无人机考试中心",
            "capacity": 50,
            "description": "专业无人机考试场地，配备完善的考试设备",
            "is_active": True
        },
        {
            "name": "无人机考试中心B",
            "address": "上海市浦东新区无人机考试中心",
            "capacity": 30,
            "description": "现代化无人机考试场地，环境优良",
            "is_active": True
        }
    ]
    
    created_venues = []
    for venue in venues:
        try:
            response = requests.post(
                f"{BASE_URL}/venues/",
                json=venue,
                headers=headers
            )
            
            if response.status_code == 200:
                created_venue = response.json()
                created_venues.append(created_venue)
                print(f"✅ 创建考场: {created_venue.get('name')} (ID: {created_venue.get('id')})")
            else:
                print(f"❌ 创建考场失败: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"❌ 创建考场异常: {e}")
    
    # 4. 创建机构
    print("\n4. 创建机构...")
    institutions = [
        {
            "name": "中国民航大学",
            "code": "CAUC001",
            "contact_person": "张主任",
            "phone": "010-12345678",
            "email": "contact@cauc.edu.cn",
            "address": "天津市东丽区津北公路2898号",
            "description": "中国民航局直属高校，无人机培训专业机构",
            "status": "active",
            "license_number": "CAAC001",
            "business_scope": "无人机驾驶员培训、考试"
        },
        {
            "name": "北京航空航天大学",
            "code": "BUAA001",
            "contact_person": "李教授",
            "phone": "010-87654321",
            "email": "contact@buaa.edu.cn",
            "address": "北京市海淀区学院路37号",
            "description": "航空航天领域顶尖高校，无人机技术领先",
            "status": "active",
            "license_number": "CAAC002",
            "business_scope": "无人机技术研发、驾驶员培训"
        }
    ]
    
    created_institutions = []
    for institution in institutions:
        try:
            response = requests.post(
                f"{BASE_URL}/institutions/",
                json=institution,
                headers=headers
            )
            
            if response.status_code == 200:
                created_institution = response.json()
                created_institutions.append(created_institution)
                print(f"✅ 创建机构: {created_institution.get('name')} (ID: {created_institution.get('id')})")
            else:
                print(f"❌ 创建机构失败: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"❌ 创建机构异常: {e}")
    
    print(f"\n🎯 测试数据创建完成!")
    print(f"   创建了 {len(created_products)} 个考试产品")
    print(f"   创建了 {len(created_venues)} 个考场")
    print(f"   创建了 {len(created_institutions)} 个机构")
    
    # 5. 显示可用的考试产品ID
    if created_products:
        print(f"\n📋 可用的考试产品ID:")
        for product in created_products:
            print(f"   - ID: {product.get('id')}, 名称: {product.get('name')}")
    
    if created_venues:
        print(f"\n📋 可用的考场ID:")
        for venue in created_venues:
            print(f"   - ID: {venue.get('id')}, 名称: {venue.get('name')}")

if __name__ == "__main__":
    create_test_data() 