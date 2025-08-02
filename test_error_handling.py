#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
错误处理测试脚本
测试各种异常情况的错误处理
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"
ADMIN_EMAIL = "admin@exam.com"
ADMIN_PASSWORD = "admin123"

class ErrorHandlingTester:
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
    
    def test_authentication_errors(self):
        """测试认证相关错误"""
        print("\n🔐 测试认证错误处理...")
        
        # 测试错误的用户名密码
        wrong_login_data = {
            "username": "wrong@email.com",
            "password": "wrongpassword"
        }
        
        response = self.session.post(
            f"{BASE_URL}/auth/jwt/login",
            data=wrong_login_data
        )
        
        if response.status_code == 400:
            print("✅ 错误用户名密码处理正常")
        else:
            print(f"❌ 错误用户名密码处理异常: {response.status_code}")
            return False
        
        # 测试缺少必填字段
        incomplete_login_data = {
            "username": "test@email.com"
            # 缺少password字段
        }
        
        response = self.session.post(
            f"{BASE_URL}/auth/jwt/login",
            data=incomplete_login_data
        )
        
        if response.status_code == 422:
            print("✅ 缺少必填字段处理正常")
        else:
            print(f"❌ 缺少必填字段处理异常: {response.status_code}")
            return False
        
        return True
    
    def test_authorization_errors(self):
        """测试权限相关错误"""
        print("\n🔒 测试权限错误处理...")
        
        # 测试未授权访问
        unauthorized_session = requests.Session()
        response = unauthorized_session.get(f"{BASE_URL}/candidates")
        
        if response.status_code == 401:
            print("✅ 未授权访问处理正常")
        else:
            print(f"❌ 未授权访问处理异常: {response.status_code}")
            return False
        
        # 测试错误的token
        wrong_token_session = requests.Session()
        wrong_token_session.headers.update({
            "Authorization": "Bearer wrong_token",
            "Content-Type": "application/json"
        })
        
        response = wrong_token_session.get(f"{BASE_URL}/candidates")
        
        if response.status_code == 401:
            print("✅ 错误token处理正常")
        else:
            print(f"❌ 错误token处理异常: {response.status_code}")
            return False
        
        return True
    
    def test_validation_errors(self):
        """测试数据验证错误"""
        print("\n📝 测试数据验证错误处理...")
        
        # 测试考试产品验证错误
        invalid_exam_product = {
            "name": "",  # 空名称
            "code": "TEST_CODE",
            "category": "INVALID_CATEGORY",  # 无效类别
            "exam_type": "INVALID_TYPE",  # 无效类型
            "exam_class": "INVALID_CLASS",  # 无效分类
            "exam_level": "INVALID_LEVEL",  # 无效级别
            "theory_pass_score": -10,  # 负数分数
            "practical_pass_score": 200,  # 超过100分
            "duration_minutes": -60,  # 负数时长
            "training_hours": -10,  # 负数培训时长
            "price": -100,  # 负数价格
            "is_active": True
        }
        
        response = self.session.post(
            f"{BASE_URL}/exam-products",
            json=invalid_exam_product
        )
        
        if response.status_code == 422:
            print("✅ 考试产品验证错误处理正常")
        else:
            print(f"❌ 考试产品验证错误处理异常: {response.status_code}")
            return False
        
        # 测试考生验证错误
        invalid_candidate = {
            "name": "",  # 空名称
            "id_number": "invalid_id",  # 无效身份证号
            "phone": "invalid_phone",  # 无效手机号
            "email": "invalid_email",  # 无效邮箱
            "gender": "INVALID_GENDER",  # 无效性别
            "birth_date": "invalid_date",  # 无效日期
            "target_exam_product_id": 99999,  # 不存在的考试产品ID
            "institution_id": 99999,  # 不存在的机构ID
            "status": "INVALID_STATUS"  # 无效状态
        }
        
        response = self.session.post(
            f"{BASE_URL}/candidates",
            json=invalid_candidate
        )
        
        if response.status_code == 422:
            print("✅ 考生验证错误处理正常")
        else:
            print(f"❌ 考生验证错误处理异常: {response.status_code}")
            return False
        
        return True
    
    def test_not_found_errors(self):
        """测试资源不存在错误"""
        print("\n🔍 测试资源不存在错误处理...")
        
        # 测试不存在的考试产品
        response = self.session.get(f"{BASE_URL}/exam-products/99999")
        
        if response.status_code == 404:
            print("✅ 考试产品不存在处理正常")
        else:
            print(f"❌ 考试产品不存在处理异常: {response.status_code}")
            return False
        
        # 测试不存在的考生
        response = self.session.get(f"{BASE_URL}/candidates/99999")
        
        if response.status_code == 404:
            print("✅ 考生不存在处理正常")
        else:
            print(f"❌ 考生不存在处理异常: {response.status_code}")
            return False
        
        # 测试不存在的排期
        response = self.session.get(f"{BASE_URL}/schedules/99999")
        
        if response.status_code == 404:
            print("✅ 排期不存在处理正常")
        else:
            print(f"❌ 排期不存在处理异常: {response.status_code}")
            return False
        
        return True
    
    def test_business_logic_errors(self):
        """测试业务逻辑错误"""
        print("\n💼 测试业务逻辑错误处理...")
        
        # 测试重复身份证号
        duplicate_candidate = {
            "name": "重复考生",
            "id_number": "110101199001011234",  # 使用已存在的身份证号
            "phone": "13800138000",
            "email": "duplicate@example.com",
            "gender": "男",
            "birth_date": "1990-01-01",
            "address": "北京市朝阳区",
            "emergency_contact": "紧急联系人",
            "emergency_phone": "13900139000",
            "target_exam_product_id": 1,
            "institution_id": 1,
            "status": "PENDING",
            "notes": "重复考生测试"
        }
        
        response = self.session.post(
            f"{BASE_URL}/candidates",
            json=duplicate_candidate
        )
        
        if response.status_code == 400 or response.status_code == 422:
            print("✅ 重复身份证号处理正常")
        else:
            print(f"❌ 重复身份证号处理异常: {response.status_code}")
            return False
        
        # 测试无效的二维码
        invalid_qr_code = {
            "qr_code": "INVALID_QR_CODE",
            "check_in_time": "2025-08-01T10:00:00",
            "notes": "测试无效二维码"
        }
        
        response = self.session.post(
            f"{BASE_URL}/schedules/scan-check-in",
            json=invalid_qr_code
        )
        
        if response.status_code == 400 or response.status_code == 404:
            print("✅ 无效二维码处理正常")
        else:
            print(f"❌ 无效二维码处理异常: {response.status_code}")
            return False
        
        return True
    
    def test_server_errors(self):
        """测试服务器错误"""
        print("\n🖥️ 测试服务器错误处理...")
        
        # 测试无效的JSON数据
        invalid_json = "invalid json string"
        
        response = self.session.post(
            f"{BASE_URL}/candidates",
            data=invalid_json,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 422:
            print("✅ 无效JSON数据处理正常")
        else:
            print(f"❌ 无效JSON数据处理异常: {response.status_code}")
            return False
        
        # 测试缺少Content-Type
        candidate_data = {
            "name": "测试考生",
            "id_number": "110101199001011234",
            "phone": "13800138000",
            "email": "test@example.com",
            "gender": "男",
            "birth_date": "1990-01-01",
            "address": "北京市朝阳区",
            "emergency_contact": "紧急联系人",
            "emergency_phone": "13900139000",
            "target_exam_product_id": 1,
            "institution_id": 1,
            "status": "PENDING",
            "notes": "测试考生"
        }
        
        response = self.session.post(
            f"{BASE_URL}/candidates",
            json=candidate_data,
            headers={}  # 不设置Content-Type
        )
        
        if response.status_code == 422 or response.status_code == 400:
            print("✅ 缺少Content-Type处理正常")
        else:
            print(f"❌ 缺少Content-Type处理异常: {response.status_code}")
            return False
        
        return True
    
    def run_error_tests(self):
        """运行错误处理测试"""
        print("🚀 开始错误处理测试")
        print("=" * 50)
        
        if not self.login():
            return False
        
        tests = [
            ("认证错误", self.test_authentication_errors),
            ("权限错误", self.test_authorization_errors),
            ("数据验证错误", self.test_validation_errors),
            ("资源不存在错误", self.test_not_found_errors),
            ("业务逻辑错误", self.test_business_logic_errors),
            ("服务器错误", self.test_server_errors)
        ]
        
        passed = 0
        total = len(tests)
        
        for name, test in tests:
            print(f"\n📋 测试: {name}")
            if test():
                passed += 1
                print(f"✅ {name} 测试通过")
            else:
                print(f"❌ {name} 测试失败")
        
        print("\n" + "=" * 50)
        print(f"📊 测试结果: {passed}/{total} 错误处理测试通过")
        
        if passed == total:
            print("🎉 所有错误处理测试通过！")
            return True
        else:
            print("⚠️ 部分错误处理测试失败，需要检查")
            return False

if __name__ == "__main__":
    tester = ErrorHandlingTester()
    success = tester.run_error_tests()
    
    if success:
        print("\n🎉 错误处理测试完全成功！")
    else:
        print("\n❌ 错误处理测试失败") 