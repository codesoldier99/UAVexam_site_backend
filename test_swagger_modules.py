#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Swagger UI 业务模块测试
测试Swagger UI中的主要业务API模块
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"
ADMIN_EMAIL = "admin@exam.com"
ADMIN_PASSWORD = "admin123"

class SwaggerModuleTester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
    
    def login(self):
        """登录获取token"""
        print("🔐 登录获取token...")
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
    
    def test_authentication_module(self):
        """测试认证模块"""
        print("\n🔐 测试认证模块...")
        
        # 测试登录
        login_data = {
            "username": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        }
        
        response = self.session.post(
            f"{BASE_URL}/auth/jwt/login",
            data=login_data
        )
        
        if response.status_code == 200:
            print("✅ JWT登录正常")
        else:
            print(f"❌ JWT登录失败: {response.status_code}")
            return False
        
        # 测试用户信息
        response = self.session.get(f"{BASE_URL}/users/me")
        if response.status_code == 200:
            print("✅ 获取用户信息正常")
        else:
            print(f"❌ 获取用户信息失败: {response.status_code}")
            return False
        
        return True
    
    def test_exam_products_module(self):
        """测试考试产品模块"""
        print("\n📚 测试考试产品模块...")
        
        # 获取考试产品列表
        response = self.session.get(f"{BASE_URL}/exam-products?page=1&size=10")
        if response.status_code == 200:
            print("✅ 获取考试产品列表正常")
        else:
            print(f"❌ 获取考试产品列表失败: {response.status_code}")
            return False
        
        # 创建考试产品
        timestamp = int(time.time())
        exam_product_data = {
            "name": f"Swagger测试考试_{timestamp}",
            "code": f"SWAGGER_TEST_{timestamp}",
            "description": "Swagger UI测试考试产品",
            "category": "VLOS",
            "exam_type": "MULTIROTOR",
            "exam_class": "AGRICULTURE",
            "exam_level": "PILOT",
            "theory_pass_score": 80,
            "practical_pass_score": 70,
            "duration_minutes": 120,
            "training_hours": 40,
            "price": 1500.0,
            "training_price": 3000.0,
            "theory_content": "Swagger测试理论内容",
            "practical_content": "Swagger测试实践内容",
            "requirements": "Swagger测试要求",
            "is_active": True
        }
        
        response = self.session.post(
            f"{BASE_URL}/exam-products",
            json=exam_product_data
        )
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ 创建考试产品正常，ID: {result['id']}")
        else:
            print(f"❌ 创建考试产品失败: {response.status_code}")
            return False
        
        return True
    
    def test_venues_module(self):
        """测试考场模块"""
        print("\n🏫 测试考场模块...")
        
        # 获取考场列表
        response = self.session.get(f"{BASE_URL}/venues?page=1&size=10")
        if response.status_code == 200:
            print("✅ 获取考场列表正常")
        else:
            print(f"❌ 获取考场列表失败: {response.status_code}")
            return False
        
        # 创建考场
        timestamp = int(time.time())
        venue_data = {
            "name": f"Swagger测试考场_{timestamp}",
            "description": "Swagger UI测试考场",
            "capacity": 50,
            "is_active": True
        }
        
        response = self.session.post(
            f"{BASE_URL}/venues",
            json=venue_data
        )
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ 创建考场正常，ID: {result['id']}")
        else:
            print(f"❌ 创建考场失败: {response.status_code}")
            return False
        
        return True
    
    def test_candidates_module(self):
        """测试考生模块"""
        print("\n👥 测试考生模块...")
        
        # 获取考生列表
        response = self.session.get(f"{BASE_URL}/candidates?page=1&size=10")
        if response.status_code == 200:
            print("✅ 获取考生列表正常")
        else:
            print(f"❌ 获取考生列表失败: {response.status_code}")
            return False
        
        # 创建考生
        timestamp = int(time.time())
        candidate_data = {
            "name": f"Swagger测试考生_{timestamp}",
            "id_number": f"110101{timestamp}",
            "phone": "13800138000",
            "email": "swagger@example.com",
            "gender": "男",
            "birth_date": "1990-01-01",
            "address": "北京市朝阳区",
            "emergency_contact": "紧急联系人",
            "emergency_phone": "13900139000",
            "target_exam_product_id": 1,
            "institution_id": 1,
            "status": "PENDING",
            "notes": "Swagger测试考生"
        }
        
        response = self.session.post(
            f"{BASE_URL}/candidates",
            json=candidate_data
        )
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ 创建考生正常，ID: {result['id']}")
        else:
            print(f"❌ 创建考生失败: {response.status_code}")
            return False
        
        return True
    
    def test_schedules_module(self):
        """测试排期模块"""
        print("\n📅 测试排期模块...")
        
        # 获取排期列表
        response = self.session.get(f"{BASE_URL}/schedules?page=1&size=10")
        if response.status_code == 200:
            print("✅ 获取排期列表正常")
        else:
            print(f"❌ 获取排期列表失败: {response.status_code}")
            return False
        
        # 获取待排期考生
        response = self.session.get(
            f"{BASE_URL}/schedules/candidates-to-schedule?scheduled_date=2025-08-01"
        )
        if response.status_code == 200:
            print("✅ 获取待排期考生正常")
        else:
            print(f"❌ 获取待排期考生失败: {response.status_code}")
            return False
        
        return True
    
    def run_swagger_tests(self):
        """运行Swagger模块测试"""
        print("🚀 开始Swagger UI业务模块测试")
        print("=" * 50)
        
        if not self.login():
            return False
        
        tests = [
            ("认证模块", self.test_authentication_module),
            ("考试产品模块", self.test_exam_products_module),
            ("考场模块", self.test_venues_module),
            ("考生模块", self.test_candidates_module),
            ("排期模块", self.test_schedules_module)
        ]
        
        passed = 0
        total = len(tests)
        
        for name, test in tests:
            print(f"\n📋 测试模块: {name}")
            if test():
                passed += 1
                print(f"✅ {name} 测试通过")
            else:
                print(f"❌ {name} 测试失败")
        
        print("\n" + "=" * 50)
        print(f"📊 测试结果: {passed}/{total} 模块通过")
        
        if passed == total:
            print("🎉 所有Swagger UI业务模块测试通过！")
            return True
        else:
            print("⚠️ 部分模块测试失败，需要检查")
            return False

if __name__ == "__main__":
    tester = SwaggerModuleTester()
    success = tester.run_swagger_tests()
    
    if success:
        print("\n🎉 Swagger UI业务模块测试完全成功！")
    else:
        print("\n❌ Swagger UI业务模块测试失败") 