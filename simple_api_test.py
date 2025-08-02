#!/usr/bin/env python3
"""
简单API测试工具
可以逐个测试API接口
"""

import requests
import json
import time
from datetime import datetime

class SimpleAPITester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.admin_token = None
        self.user_token = None
        
    def print_request(self, method, url, headers=None, data=None):
        """打印请求信息"""
        print(f"\n🔍 {method} {url}")
        if headers:
            print("📋 Headers:")
            for key, value in headers.items():
                if key.lower() == 'authorization':
                    print(f"  {key}: Bearer ***")
                else:
                    print(f"  {key}: {value}")
        if data:
            print("📦 Data:")
            print(f"  {json.dumps(data, ensure_ascii=False, indent=2)}")
    
    def print_response(self, response, response_time):
        """打印响应信息"""
        print(f"⏱️  响应时间: {response_time}ms")
        print(f"📊 状态码: {response.status_code}")
        print("📄 响应内容:")
        try:
            response_json = response.json()
            print(json.dumps(response_json, ensure_ascii=False, indent=2))
        except:
            print(response.text)
    
    def make_request(self, method, endpoint, data=None, headers=None, description=""):
        """发送HTTP请求"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        # 打印请求信息
        self.print_request(method, url, headers, data)
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method.upper() == "POST":
                # 检查是否是表单数据
                if isinstance(data, str) and "Content-Type" in headers and "application/x-www-form-urlencoded" in headers["Content-Type"]:
                    response = requests.post(url, data=data, headers=headers, timeout=10)
                else:
                    response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method.upper() == "PUT":
                response = requests.put(url, json=data, headers=headers, timeout=10)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")
            
            response_time = int((time.time() - start_time) * 1000)
            
            # 打印响应信息
            self.print_response(response, response_time)
            
            return response, response_time
            
        except requests.exceptions.ConnectionError:
            print("❌ 连接错误: 无法连接到服务器")
            return None, 0
        except Exception as e:
            print(f"❌ 请求错误: {str(e)}")
            return None, 0
    
    def test_admin_login(self):
        """测试管理员登录"""
        print("\n" + "="*50)
        print("🔐 测试管理员登录")
        print("="*50)
        
        # 首先尝试JWT登录
        print("🔄 尝试JWT登录...")
        data = "username=admin@exam.com&password=admin123"
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        response, response_time = self.make_request("POST", "/auth/jwt/login", data=data, headers=headers)
        
        if response and response.status_code == 200:
            try:
                token_data = response.json()
                if "access_token" in token_data:
                    self.admin_token = token_data["access_token"]
                    print("✅ JWT管理员登录成功，Token已保存")
                    return True
                else:
                    print("❌ JWT响应中缺少access_token")
            except json.JSONDecodeError:
                print("❌ JWT响应格式错误")
        
        # 如果JWT登录失败，尝试简化登录
        print("🔄 尝试简化登录...")
        data = {
            "username": "admin@exam.com",
            "email": "admin@exam.com",
            "password": "admin123"
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        response, response_time = self.make_request("POST", "/simple-login", data=data, headers=headers)
        
        if response and response.status_code == 200:
            try:
                token_data = response.json()
                if "access_token" in token_data:
                    self.admin_token = token_data["access_token"]
                    print("✅ 简化登录成功，Token已保存")
                    return True
                else:
                    print("❌ 简化登录响应中缺少access_token")
                    return False
            except json.JSONDecodeError:
                print("❌ 简化登录响应格式错误")
                return False
        else:
            print("❌ 所有登录方式都失败")
            return False
    
    def test_create_institution(self):
        """测试创建机构"""
        if not self.admin_token:
            print("❌ 需要先登录获取Token")
            return False
        
        print("\n" + "="*50)
        print("🏢 测试创建机构")
        print("="*50)
        
        # 首先尝试使用简化端点
        print("🔄 尝试使用简化端点创建机构...")
        data = {
            "name": "测试机构",
            "code": "TEST001",
            "contact_person": "张三",
            "phone": "13800138000",
            "email": "contact@test.com",
            "address": "北京市朝阳区",
            "description": "测试机构描述",
            "status": "active",
            "license_number": "LIC001",
            "business_scope": "考试服务"
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        response, response_time = self.make_request("POST", "/simple-institutions", data=data, headers=headers)
        
        if response and response.status_code in [200, 201]:
            print("✅ 简化机构创建成功")
            return True
        
        # 如果简化端点失败，尝试完整端点
        print("🔄 尝试使用完整端点创建机构...")
        data = {
            "name": "测试机构",
            "code": "TEST001",
            "contact_person": "张三",
            "phone": "13800138000",
            "email": "contact@test.com",
            "address": "北京市朝阳区",
            "description": "测试机构描述",
            "status": "active",
            "license_number": "LIC001",
            "business_scope": "考试服务",
            "admin_username": "admin_test",
            "admin_email": "admin@test.com",
            "admin_password": "password123"
        }
        
        headers = {
            "Authorization": f"Bearer {self.admin_token}",
            "Content-Type": "application/json"
        }
        
        response, response_time = self.make_request("POST", "/institutions", data=data, headers=headers)
        
        if response and response.status_code in [200, 201]:
            print("✅ 完整机构创建成功")
            return True
        else:
            print("❌ 机构创建失败")
            return False
    
    def test_get_institutions(self):
        """测试获取机构列表"""
        print("\n" + "="*50)
        print("📋 测试获取机构列表")
        print("="*50)
        
        # 首先尝试使用简化端点
        print("🔄 尝试使用简化端点获取机构列表...")
        response, response_time = self.make_request("GET", "/simple-institutions")
        
        if response and response.status_code == 200:
            print("✅ 简化机构列表获取成功")
            return True
        
        # 如果简化端点失败，尝试完整端点
        if not self.admin_token:
            print("❌ 需要先登录获取Token")
            return False
        
        print("🔄 尝试使用完整端点获取机构列表...")
        headers = {
            "Authorization": f"Bearer {self.admin_token}"
        }
        
        response, response_time = self.make_request("GET", "/institutions?page=1&size=10", headers=headers)
        
        if response and response.status_code == 200:
            print("✅ 完整机构列表获取成功")
            return True
        else:
            print("❌ 获取机构列表失败")
            return False
    
    def test_create_exam_product(self):
        """测试创建考试产品"""
        if not self.admin_token:
            print("❌ 需要先登录获取Token")
            return False
        
        print("\n" + "="*50)
        print("📚 测试创建考试产品")
        print("="*50)
        
        data = {
            "name": "无人机驾驶员考试",
            "description": "无人机驾驶员理论考试",
            "category": "无人机",
            "duration": 120,
            "pass_score": 80,
            "status": "active"
        }
        
        headers = {
            "Authorization": f"Bearer {self.admin_token}",
            "Content-Type": "application/json"
        }
        
        response, response_time = self.make_request("POST", "/exam-products", data=data, headers=headers)
        
        if response and response.status_code in [200, 201]:
            print("✅ 考试产品创建成功")
            return True
        else:
            print("❌ 考试产品创建失败")
            return False
    
    def test_create_venue(self):
        """测试创建考场资源"""
        if not self.admin_token:
            print("❌ 需要先登录获取Token")
            return False
        
        print("\n" + "="*50)
        print("🏫 测试创建考场资源")
        print("="*50)
        
        data = {
            "name": "考场A",
            "location": "北京市朝阳区",
            "address": "朝阳区某某街道123号",
            "capacity": 50,
            "equipment": "电脑、投影仪",
            "status": "active",
            "description": "标准考场"
        }
        
        headers = {
            "Authorization": f"Bearer {self.admin_token}",
            "Content-Type": "application/json"
        }
        
        response, response_time = self.make_request("POST", "/venues", data=data, headers=headers)
        
        if response and response.status_code in [200, 201]:
            print("✅ 考场资源创建成功")
            return True
        else:
            print("❌ 考场资源创建失败")
            return False
    
    def test_unauthorized_access(self):
        """测试无权限访问"""
        print("\n" + "="*50)
        print("🔒 测试无权限访问")
        print("="*50)
        
        headers = {
            "Authorization": "Bearer invalid_token"
        }
        
        response, response_time = self.make_request("GET", "/institutions", headers=headers)
        
        if response and response.status_code == 401:
            print("✅ 无权限访问测试通过")
            return True
        else:
            print("❌ 无权限访问测试失败")
            return False
    
    def test_simple_endpoints(self):
        """测试简化端点"""
        print("\n" + "="*50)
        print("🧪 测试简化端点")
        print("="*50)
        
        # 测试根端点
        print("\n🔍 测试根端点...")
        response, response_time = self.make_request("GET", "/")
        if response and response.status_code == 200:
            print("✅ 根端点测试通过")
        else:
            print("❌ 根端点测试失败")
        
        # 测试测试端点
        print("\n🔍 测试测试端点...")
        response, response_time = self.make_request("GET", "/test")
        if response and response.status_code == 200:
            print("✅ 测试端点测试通过")
        else:
            print("❌ 测试端点测试失败")
        
        # 测试简化机构列表
        print("\n🔍 测试简化机构列表...")
        response, response_time = self.make_request("GET", "/simple-institutions")
        if response and response.status_code == 200:
            print("✅ 简化机构列表测试通过")
        else:
            print("❌ 简化机构列表测试失败")
        
        # 测试简化登录
        print("\n🔍 测试简化登录...")
        data = {
            "username": "admin@exam.com",
            "email": "admin@exam.com",
            "password": "admin123"
        }
        headers = {
            "Content-Type": "application/json"
        }
        response, response_time = self.make_request("POST", "/simple-login", data=data, headers=headers)
        if response and response.status_code == 200:
            print("✅ 简化登录测试通过")
        else:
            print("❌ 简化登录测试失败")
    
    def interactive_test(self):
        """交互式测试"""
        print("🚀 简单API测试工具")
        print("="*50)
        
        while True:
            print("\n📋 请选择要测试的接口:")
            print("1. 管理员登录")
            print("2. 创建机构")
            print("3. 获取机构列表")
            print("4. 创建考试产品")
            print("5. 创建考场资源")
            print("6. 无权限访问测试")
            print("7. 测试简化端点")
            print("0. 退出")
            
            choice = input("\n请输入选择 (0-7): ").strip()
            
            if choice == "0":
                print("👋 再见!")
                break
            elif choice == "1":
                self.test_admin_login()
            elif choice == "2":
                self.test_create_institution()
            elif choice == "3":
                self.test_get_institutions()
            elif choice == "4":
                self.test_create_exam_product()
            elif choice == "5":
                self.test_create_venue()
            elif choice == "6":
                self.test_unauthorized_access()
            elif choice == "7":
                self.test_simple_endpoints()
            else:
                print("❌ 无效选择，请重新输入")

def main():
    """主函数"""
    tester = SimpleAPITester()
    tester.interactive_test()

if __name__ == "__main__":
    main() 