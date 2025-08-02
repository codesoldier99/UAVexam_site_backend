#!/usr/bin/env python3
"""
简化API测试工具 - 不依赖数据库
只测试简化端点，用于验证服务器基本功能
"""

import requests
import json
import time
from datetime import datetime

class SimpleAPITesterNoDB:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        
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
            if isinstance(data, str):
                print(f"  {data}")
            else:
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
    
    def test_root_endpoint(self):
        """测试根端点"""
        print("\n" + "="*50)
        print("🏠 测试根端点")
        print("="*50)
        
        response, response_time = self.make_request("GET", "/")
        
        if response and response.status_code == 200:
            print("✅ 根端点测试通过")
            return True
        else:
            print("❌ 根端点测试失败")
            return False
    
    def test_test_endpoint(self):
        """测试测试端点"""
        print("\n" + "="*50)
        print("🧪 测试测试端点")
        print("="*50)
        
        response, response_time = self.make_request("GET", "/test")
        
        if response and response.status_code == 200:
            print("✅ 测试端点测试通过")
            return True
        else:
            print("❌ 测试端点测试失败")
            return False
    
    def test_simple_login(self):
        """测试简化登录"""
        print("\n" + "="*50)
        print("🔐 测试简化登录")
        print("="*50)
        
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
            return True
        else:
            print("❌ 简化登录测试失败")
            return False
    
    def test_simple_institutions(self):
        """测试简化机构端点"""
        print("\n" + "="*50)
        print("🏢 测试简化机构端点")
        print("="*50)
        
        # 测试获取机构列表
        print("\n🔍 测试获取机构列表...")
        response, response_time = self.make_request("GET", "/simple-institutions")
        
        if response and response.status_code == 200:
            print("✅ 获取机构列表测试通过")
        else:
            print("❌ 获取机构列表测试失败")
        
        # 测试创建机构
        print("\n🔍 测试创建机构...")
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
            print("✅ 创建机构测试通过")
            return True
        else:
            print("❌ 创建机构测试失败")
            return False
    
    def test_all_simple_endpoints(self):
        """测试所有简化端点"""
        print("\n" + "="*50)
        print("🧪 测试所有简化端点")
        print("="*50)
        
        tests = [
            ("根端点", self.test_root_endpoint),
            ("测试端点", self.test_test_endpoint),
            ("简化登录", self.test_simple_login),
            ("简化机构", self.test_simple_institutions),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n{'='*20} {test_name} {'='*20}")
            if test_func():
                passed += 1
        
        print(f"\n{'='*50}")
        print(f"📊 测试结果: {passed}/{total} 通过")
        if passed == total:
            print("🎉 所有测试通过！")
        else:
            print("⚠️  部分测试失败")
        print("="*50)
        
        return passed == total
    
    def interactive_test(self):
        """交互式测试"""
        print("🚀 简化API测试工具 (无数据库依赖)")
        print("="*50)
        
        while True:
            print("\n📋 请选择要测试的接口:")
            print("1. 测试根端点")
            print("2. 测试测试端点")
            print("3. 测试简化登录")
            print("4. 测试简化机构端点")
            print("5. 测试所有简化端点")
            print("0. 退出")
            
            choice = input("\n请输入选择 (0-5): ").strip()
            
            if choice == "0":
                print("👋 再见!")
                break
            elif choice == "1":
                self.test_root_endpoint()
            elif choice == "2":
                self.test_test_endpoint()
            elif choice == "3":
                self.test_simple_login()
            elif choice == "4":
                self.test_simple_institutions()
            elif choice == "5":
                self.test_all_simple_endpoints()
            else:
                print("❌ 无效选择，请重新输入")

def main():
    """主函数"""
    tester = SimpleAPITesterNoDB()
    tester.interactive_test()

if __name__ == "__main__":
    main() 