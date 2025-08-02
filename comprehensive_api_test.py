#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面API测试脚本
测试所有主要功能模块
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

class ComprehensiveAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.test_data = {}
    
    def test_basic_endpoints(self):
        """测试基础端点"""
        print("🏠 测试基础端点...")
        
        # 测试根端点
        response = self.session.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ 根端点正常")
        else:
            print(f"❌ 根端点异常: {response.status_code}")
            return False
        
        # 测试健康检查
        response = self.session.get(f"{BASE_URL}/test")
        if response.status_code == 200:
            print("✅ 健康检查正常")
        else:
            print(f"❌ 健康检查异常: {response.status_code}")
            return False
        
        return True
    
    def test_authentication(self):
        """测试认证系统"""
        print("\n🔐 测试认证系统...")
        
        # 测试JWT登录
        login_data = {
            "username": "admin@exam.com",
            "password": "admin123"
        }
        
        response = self.session.post(
            f"{BASE_URL}/auth/jwt/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            result = response.json()
            self.token = result.get("access_token")
            self.session.headers.update({
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            })
            print("✅ JWT登录成功")
        else:
            print(f"❌ JWT登录失败: {response.status_code}")
            print(f"响应: {response.text}")
            return False
        
        # 测试用户信息获取
        response = self.session.get(f"{BASE_URL}/users/me")
        if response.status_code == 200:
            user_info = response.json()
            print(f"✅ 用户信息获取成功: {user_info.get('username')}")
        else:
            print(f"❌ 用户信息获取失败: {response.status_code}")
            return False
        
        return True
    
    def test_institution_apis(self):
        """测试机构管理API"""
        print("\n🏢 测试机构管理API...")
        
        # 创建机构
        institution_data = {
            "name": f"测试机构_{int(time.time())}",
            "code": f"TEST_{int(time.time())}",
            "contact_person": "张三",
            "phone": "13800138000",
            "email": "test@example.com",
            "address": "北京市朝阳区",
            "description": "测试机构",
            "status": "active"
        }
        
        response = self.session.post(
            f"{BASE_URL}/simple-institutions",
            json=institution_data
        )
        
        if response.status_code == 200:
            result = response.json()
            self.test_data['institution_id'] = result['institution']['id']
            print("✅ 机构创建成功")
        else:
            print(f"❌ 机构创建失败: {response.status_code}")
            return False
        
        # 获取机构列表
        response = self.session.get(f"{BASE_URL}/simple-institutions")
        if response.status_code == 200:
            print("✅ 机构列表获取成功")
        else:
            print(f"❌ 机构列表获取失败: {response.status_code}")
            return False
        
        return True
    
    def test_venue_apis(self):
        """测试考场管理API"""
        print("\n🏫 测试考场管理API...")
        
        # 创建考场
        venue_data = {
            "name": f"测试考场_{int(time.time())}",
            "type": "理论",
            "status": "active"
        }
        
        response = self.session.post(
            f"{BASE_URL}/venues/",
            json=venue_data
        )
        
        if response.status_code == 200:
            result = response.json()
            self.test_data['venue_id'] = result['venue']['id']
            print("✅ 考场创建成功")
        else:
            print(f"❌ 考场创建失败: {response.status_code}")
            return False
        
        # 获取考场列表
        response = self.session.get(f"{BASE_URL}/venues/")
        if response.status_code == 200:
            print("✅ 考场列表获取成功")
        else:
            print(f"❌ 考场列表获取失败: {response.status_code}")
            return False
        
        return True
    
    def test_exam_product_apis(self):
        """测试考试产品API"""
        print("\n📚 测试考试产品API...")
        
        # 创建考试产品
        product_data = {
            "name": f"测试产品_{int(time.time())}",
            "description": "测试考试产品",
            "status": "active"
        }
        
        response = self.session.post(
            f"{BASE_URL}/exam-products/",
            json=product_data
        )
        
        if response.status_code == 200:
            result = response.json()
            self.test_data['exam_product_id'] = result['exam_product']['id']
            print("✅ 考试产品创建成功")
        else:
            print(f"❌ 考试产品创建失败: {response.status_code}")
            return False
        
        # 获取考试产品列表
        response = self.session.get(f"{BASE_URL}/exam-products/")
        if response.status_code == 200:
            print("✅ 考试产品列表获取成功")
        else:
            print(f"❌ 考试产品列表获取失败: {response.status_code}")
            return False
        
        return True
    
    def test_candidate_apis(self):
        """测试考生管理API"""
        print("\n👤 测试考生管理API...")
        
        # 创建考生
        candidate_data = {
            "name": "张三",
            "id_card": f"110101{int(time.time())}",
            "institution_id": self.test_data.get('institution_id', 1),
            "exam_product_id": self.test_data.get('exam_product_id', 1),
            "status": "待排期"
        }
        
        response = self.session.post(
            f"{BASE_URL}/candidates/",
            json=candidate_data
        )
        
        if response.status_code == 200:
            result = response.json()
            self.test_data['candidate_id'] = result['candidate']['id']
            print("✅ 考生创建成功")
        else:
            print(f"❌ 考生创建失败: {response.status_code}")
            return False
        
        # 获取考生列表
        response = self.session.get(f"{BASE_URL}/candidates/")
        if response.status_code == 200:
            print("✅ 考生列表获取成功")
        else:
            print(f"❌ 考生列表获取失败: {response.status_code}")
            return False
        
        return True
    
    def test_schedule_apis(self):
        """测试排期管理API"""
        print("\n📅 测试排期管理API...")
        
        # 获取待排期考生
        response = self.session.get(f"{BASE_URL}/schedules/candidates-to-schedule")
        if response.status_code == 200:
            print("✅ 待排期考生获取成功")
        else:
            print(f"❌ 待排期考生获取失败: {response.status_code}")
            return False
        
        # 创建排期
        schedule_data = {
            "candidate_id": self.test_data.get('candidate_id', 1),
            "venue_id": self.test_data.get('venue_id', 1),
            "exam_date": "2025-08-15",
            "start_time": "09:00:00",
            "end_time": "10:00:00",
            "activity_name": "理论考试"
        }
        
        response = self.session.post(
            f"{BASE_URL}/schedules/batch-create",
            json={"schedules": [schedule_data]}
        )
        
        if response.status_code == 200:
            print("✅ 排期创建成功")
        else:
            print(f"❌ 排期创建失败: {response.status_code}")
            return False
        
        return True
    
    def test_public_apis(self):
        """测试公共API"""
        print("\n🌐 测试公共API...")
        
        # 获取考场状态
        response = self.session.get(f"{BASE_URL}/public/venues/status")
        if response.status_code == 200:
            print("✅ 考场状态获取成功")
        else:
            print(f"❌ 考场状态获取失败: {response.status_code}")
            return False
        
        return True
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始全面API测试...")
        print("=" * 60)
        
        tests = [
            ("基础端点", self.test_basic_endpoints),
            ("认证系统", self.test_authentication),
            ("机构管理", self.test_institution_apis),
            ("考场管理", self.test_venue_apis),
            ("考试产品", self.test_exam_product_apis),
            ("考生管理", self.test_candidate_apis),
            ("排期管理", self.test_schedule_apis),
            ("公共API", self.test_public_apis),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    print(f"✅ {test_name}测试通过")
                    passed += 1
                else:
                    print(f"❌ {test_name}测试失败")
            except Exception as e:
                print(f"❌ {test_name}测试异常: {str(e)}")
        
        print("\n" + "=" * 60)
        print(f"📊 测试结果: {passed}/{total} 通过")
        
        if passed == total:
            print("🎉 所有测试通过！系统运行正常！")
        else:
            print("⚠️ 部分测试失败，请检查相关功能")
        
        return passed == total

if __name__ == "__main__":
    tester = ComprehensiveAPITester()
    tester.run_all_tests() 