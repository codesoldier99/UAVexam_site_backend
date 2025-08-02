#!/usr/bin/env python3
"""
简洁的机构与资源管理API测试工具
"""

import requests
import json
import time

class QuickInstitutionTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.admin_token = None
        self.headers = {}
    
    def login_admin(self):
        """管理员登录"""
        print("🔐 管理员登录...")
        data = "username=admin@exam.com&password=admin123"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        response = requests.post(f"{self.base_url}/auth/jwt/login", data=data, headers=headers)
        
        if response.status_code == 200:
            token_data = response.json()
            self.admin_token = token_data.get("access_token")
            self.headers = {"Authorization": f"Bearer {self.admin_token}"}
            print("✅ 登录成功")
            return True
        else:
            print("❌ 登录失败")
            return False
    
    def test_institutions(self):
        """测试机构管理"""
        print("\n🏢 测试机构管理")
        
        # 创建机构
        data = {
            "name": "测试机构",
            "code": "TEST001",
            "contact_person": "张三",
            "phone": "13800138001",
            "email": "test@example.com"
        }
        
        response = requests.post(f"{self.base_url}/institutions", json=data, headers=self.headers)
        print(f"创建机构: {response.status_code}")
        
        if response.status_code == 201:
            institution_id = response.json().get("id")
            
            # 获取列表
            response = requests.get(f"{self.base_url}/institutions?page=1&size=10", headers=self.headers)
            print(f"获取列表: {response.status_code}")
            
            # 获取详情
            response = requests.get(f"{self.base_url}/institutions/{institution_id}", headers=self.headers)
            print(f"获取详情: {response.status_code}")
            
            # 更新机构
            update_data = {"name": "测试机构-已更新"}
            response = requests.put(f"{self.base_url}/institutions/{institution_id}", json=update_data, headers=self.headers)
            print(f"更新机构: {response.status_code}")
            
            # 删除机构
            response = requests.delete(f"{self.base_url}/institutions/{institution_id}", headers=self.headers)
            print(f"删除机构: {response.status_code}")
    
    def test_exam_products(self):
        """测试考试产品管理"""
        print("\n📚 测试考试产品管理")
        
        data = {
            "name": "Python编程考试",
            "code": "PYTHON001",
            "description": "Python编程基础测试",
            "duration_minutes": 120,
            "pass_score": 60,
            "max_score": 100,
            "price": 299.00
        }
        
        response = requests.post(f"{self.base_url}/exam-products", json=data, headers=self.headers)
        print(f"创建产品: {response.status_code}")
        
        if response.status_code == 201:
            product_id = response.json().get("id")
            
            # 获取列表
            response = requests.get(f"{self.base_url}/exam-products?page=1&size=10", headers=self.headers)
            print(f"获取列表: {response.status_code}")
            
            # 删除产品
            response = requests.delete(f"{self.base_url}/exam-products/{product_id}", headers=self.headers)
            print(f"删除产品: {response.status_code}")
    
    def test_venues(self):
        """测试考场资源管理"""
        print("\n🏫 测试考场资源管理")
        
        data = {
            "name": "北京朝阳考场",
            "code": "BJ001",
            "address": "北京市朝阳区建国路88号",
            "capacity": 100,
            "contact_person": "王五",
            "contact_phone": "010-12345678"
        }
        
        response = requests.post(f"{self.base_url}/venues", json=data, headers=self.headers)
        print(f"创建考场: {response.status_code}")
        
        if response.status_code == 201:
            venue_id = response.json().get("id")
            
            # 获取列表
            response = requests.get(f"{self.base_url}/venues?page=1&size=10", headers=self.headers)
            print(f"获取列表: {response.status_code}")
            
            # 删除考场
            response = requests.delete(f"{self.base_url}/venues/{venue_id}", headers=self.headers)
            print(f"删除考场: {response.status_code}")
    
    def test_unauthorized(self):
        """测试未授权访问"""
        print("\n🚫 测试未授权访问")
        
        response = requests.get(f"{self.base_url}/institutions")
        print(f"未授权访问机构: {response.status_code}")
        
        response = requests.get(f"{self.base_url}/exam-products")
        print(f"未授权访问产品: {response.status_code}")
        
        response = requests.get(f"{self.base_url}/venues")
        print(f"未授权访问考场: {response.status_code}")
    
    def run_tests(self):
        """运行所有测试"""
        print("🚀 开始机构与资源管理API测试")
        
        if not self.login_admin():
            return
        
        self.test_institutions()
        self.test_exam_products()
        self.test_venues()
        self.test_unauthorized()
        
        print("\n✅ 测试完成")

if __name__ == "__main__":
    tester = QuickInstitutionTester()
    tester.run_tests() 