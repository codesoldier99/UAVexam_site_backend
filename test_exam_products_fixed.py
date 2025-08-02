#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复后的考试产品API测试脚本
使用正确的CAAC体系字段
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"
ADMIN_EMAIL = "admin@exam.com"
ADMIN_PASSWORD = "admin123"

class ExamProductTester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
    
    def login(self):
        """登录获取token"""
        login_data = {
            "username": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        }
        
        response = self.session.post(
            f"{BASE_URL}/auth/jwt/login",
            data=login_data
        )
        
        if response.status_code == 200:
            result = response.json()
            self.token = result.get("access_token")
            self.session.headers.update({
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            })
            print("✅ 登录成功")
            return True
        else:
            print(f"❌ 登录失败: {response.status_code}")
            return False
    
    def test_create_exam_product(self):
        """测试创建考试产品"""
        print("\n📚 测试创建考试产品...")
        
        # 使用正确的CAAC体系字段
        exam_product_data = {
            "name": "CAAC多旋翼无人机驾驶员理论考试",
            "code": "CAAC_MULTIROTOR_VLOS_PILOT",
            "description": "中国民航局多旋翼无人机视距内驾驶员理论考试",
            "category": "VLOS",  # 视距内
            "exam_type": "MULTIROTOR",  # 多旋翼
            "exam_class": "AGRICULTURE",  # 农业应用
            "exam_level": "PILOT",  # 驾驶员级别
            "theory_pass_score": 80,  # 理论考试及格分数
            "practical_pass_score": 70,  # 实践考试及格分数
            "duration_minutes": 120,  # 考试时长（分钟）
            "training_hours": 40,  # 培训时长（小时）
            "price": 1500.0,  # 考试费用
            "training_price": 3000.0,  # 培训费用
            "theory_content": "无人机法规、飞行原理、气象知识、应急处置等",
            "practical_content": "无人机操控、航线规划、应急处置等",
            "requirements": "年满16周岁，身体健康，无色盲色弱",
            "is_active": True
        }
        
        response = self.session.post(
            f"{BASE_URL}/exam-products",
            json=exam_product_data
        )
        
        if response.status_code == 201:
            result = response.json()
            print("✅ 考试产品创建成功")
            print(f"   ID: {result['id']}")
            print(f"   名称: {result['name']}")
            print(f"   代码: {result['code']}")
            print(f"   类别: {result['category']}")
            print(f"   类型: {result['exam_type']}")
            return True
        else:
            print(f"❌ 考试产品创建失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
    
    def test_get_exam_products(self):
        """测试获取考试产品列表"""
        print("\n📋 测试获取考试产品列表...")
        
        response = self.session.get(f"{BASE_URL}/exam-products?page=1&size=10")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 获取考试产品列表成功")
            print(f"   总数: {result['total']}")
            print(f"   当前页: {result['page']}")
            print(f"   每页大小: {result['size']}")
            print(f"   总页数: {result['pages']}")
            
            if result['items']:
                print("   产品列表:")
                for item in result['items'][:3]:  # 只显示前3个
                    print(f"     - {item['name']} ({item['code']})")
            return True
        else:
            print(f"❌ 获取考试产品列表失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
    
    def test_create_multiple_products(self):
        """测试创建多个CAAC考试产品"""
        print("\n🔄 测试创建多个CAAC考试产品...")
        
        # CAAC考试产品列表
        exam_products = [
            {
                "name": "CAAC固定翼无人机驾驶员理论考试",
                "code": "CAAC_FIXED_WING_VLOS_PILOT",
                "description": "中国民航局固定翼无人机视距内驾驶员理论考试",
                "category": "VLOS",
                "exam_type": "FIXED_WING",
                "exam_class": "POWER_INSPECTION",
                "exam_level": "PILOT",
                "theory_pass_score": 80,
                "practical_pass_score": 70,
                "duration_minutes": 120,
                "training_hours": 45,
                "price": 1800.0,
                "training_price": 3500.0,
                "theory_content": "固定翼飞行原理、航空气象、导航系统等",
                "practical_content": "固定翼操控、航线规划、应急处理等",
                "requirements": "年满18周岁，身体健康，无色盲色弱",
                "is_active": True
            },
            {
                "name": "CAAC垂直起降无人机驾驶员理论考试",
                "code": "CAAC_VTOL_VLOS_PILOT",
                "description": "中国民航局垂直起降无人机视距内驾驶员理论考试",
                "category": "VLOS",
                "exam_type": "VTOL",
                "exam_class": "FILM_PHOTOGRAPHY",
                "exam_level": "PILOT",
                "theory_pass_score": 80,
                "practical_pass_score": 70,
                "duration_minutes": 120,
                "training_hours": 50,
                "price": 2000.0,
                "training_price": 4000.0,
                "theory_content": "VTOL飞行原理、摄影技术、影视制作等",
                "practical_content": "VTOL操控、摄影技巧、影视拍摄等",
                "requirements": "年满18周岁，身体健康，无色盲色弱",
                "is_active": True
            },
            {
                "name": "CAAC超视距无人机驾驶员理论考试",
                "code": "CAAC_MULTIROTOR_BVLOS_PILOT",
                "description": "中国民航局多旋翼无人机超视距驾驶员理论考试",
                "category": "BVLOS",
                "exam_type": "MULTIROTOR",
                "exam_class": "LOGISTICS",
                "exam_level": "PILOT",
                "theory_pass_score": 85,
                "practical_pass_score": 75,
                "duration_minutes": 150,
                "training_hours": 60,
                "price": 2500.0,
                "training_price": 5000.0,
                "theory_content": "超视距飞行原理、通信系统、导航技术等",
                "practical_content": "超视距操控、航线规划、应急处理等",
                "requirements": "年满18周岁，身体健康，无色盲色弱，有VLOS经验",
                "is_active": True
            }
        ]
        
        success_count = 0
        for i, product_data in enumerate(exam_products, 1):
            print(f"   创建产品 {i}: {product_data['name']}")
            
            response = self.session.post(
                f"{BASE_URL}/exam-products",
                json=product_data
            )
            
            if response.status_code == 201:
                result = response.json()
                print(f"   ✅ 成功创建: {result['code']}")
                success_count += 1
            else:
                print(f"   ❌ 创建失败: {response.status_code}")
                print(f"   错误信息: {response.text}")
        
        print(f"\n📊 批量创建结果: {success_count}/{len(exam_products)} 成功")
        return success_count == len(exam_products)
    
    def run_tests(self):
        """运行所有测试"""
        print("🚀 开始修复后的考试产品API测试")
        
        if not self.login():
            return False
        
        tests = [
            ("创建考试产品", self.test_create_exam_product),
            ("获取考试产品列表", self.test_get_exam_products),
            ("创建多个CAAC产品", self.test_create_multiple_products)
        ]
        
        passed = 0
        for name, test in tests:
            print(f"\n📋 测试: {name}")
            if test():
                passed += 1
        
        print(f"\n📊 测试结果: {passed}/{len(tests)} 通过")
        return passed == len(tests)

if __name__ == "__main__":
    tester = ExamProductTester()
    success = tester.run_tests()
    
    if success:
        print("🎉 考试产品API测试完全成功！")
    else:
        print("❌ 考试产品API测试失败") 