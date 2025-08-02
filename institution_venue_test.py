#!/usr/bin/env python3
"""
机构与资源管理API测试工具
测试机构管理、考试产品管理、考场资源管理的所有CRUD操作
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

class InstitutionVenueTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.admin_token = None
        self.headers = {}
        
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
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method.upper() == "PUT":
                response = requests.put(url, json=data, headers=headers, timeout=10)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers, timeout=10)
            elif method.upper() == "PATCH":
                response = requests.patch(url, json=data, headers=headers, timeout=10)
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
    
    def login_admin(self):
        """管理员登录获取token"""
        print("\n" + "="*50)
        print("🔐 管理员登录")
        print("="*50)
        
        data = "username=admin@exam.com&password=admin123"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        response, _ = self.make_request("POST", "/auth/jwt/login", data=data, headers=headers)
        
        if response and response.status_code == 200:
            try:
                token_data = response.json()
                if "access_token" in token_data:
                    self.admin_token = token_data["access_token"]
                    self.headers = {"Authorization": f"Bearer {self.admin_token}"}
                    print("✅ 管理员登录成功")
                    return True
                else:
                    print("❌ 登录响应中没有access_token")
                    return False
            except Exception as e:
                print(f"❌ 解析登录响应失败: {str(e)}")
                return False
        else:
            print("❌ 管理员登录失败")
            return False
    
    def test_institutions_crud(self):
        """测试机构管理的CRUD操作"""
        print("\n" + "="*60)
        print("🏢 机构管理CRUD测试")
        print("="*60)
        
        # 1. 创建机构
        print("\n📝 1. 创建机构")
        institution_data = {
            "name": "测试机构A",
            "code": "TEST001",
            "contact_person": "张三",
            "phone": "13800138001",
            "email": "test@example.com",
            "address": "北京市朝阳区测试街道123号",
            "description": "这是一个测试机构",
            "status": "active",
            "license_number": "LIC001",
            "business_scope": "考试服务"
        }
        
        response, _ = self.make_request("POST", "/institutions", data=institution_data, headers=self.headers)
        institution_id = None
        if response and response.status_code == 201:
            try:
                result = response.json()
                institution_id = result.get("id")
                print(f"✅ 机构创建成功，ID: {institution_id}")
            except:
                print("❌ 无法获取机构ID")
        
        # 2. 获取机构列表
        print("\n📋 2. 获取机构列表")
        response, _ = self.make_request("GET", "/institutions?page=1&size=10", headers=self.headers)
        
        # 3. 获取机构统计
        print("\n📊 3. 获取机构统计")
        response, _ = self.make_request("GET", "/institutions/stats", headers=self.headers)
        
        # 4. 获取机构详情
        if institution_id:
            print(f"\n🔍 4. 获取机构详情 (ID: {institution_id})")
            response, _ = self.make_request("GET", f"/institutions/{institution_id}", headers=self.headers)
            
            # 5. 更新机构信息
            print(f"\n✏️  5. 更新机构信息 (ID: {institution_id})")
            update_data = {
                "name": "测试机构A-已更新",
                "contact_person": "李四",
                "phone": "13800138002",
                "description": "这是更新后的测试机构"
            }
            response, _ = self.make_request("PUT", f"/institutions/{institution_id}", data=update_data, headers=self.headers)
            
            # 6. 更新机构状态
            print(f"\n🔄 6. 更新机构状态 (ID: {institution_id})")
            response, _ = self.make_request("PATCH", f"/institutions/{institution_id}/status?status=inactive", headers=self.headers)
            
            # 7. 删除机构
            print(f"\n🗑️  7. 删除机构 (ID: {institution_id})")
            response, _ = self.make_request("DELETE", f"/institutions/{institution_id}", headers=self.headers)
    
    def test_exam_products_crud(self):
        """测试考试产品管理的CRUD操作"""
        print("\n" + "="*60)
        print("📚 考试产品管理CRUD测试")
        print("="*60)
        
        # 1. 创建考试产品
        print("\n📝 1. 创建考试产品")
        exam_product_data = {
            "name": "Python编程基础考试",
            "code": "PYTHON001",
            "description": "Python编程基础知识和技能测试",
            "duration_minutes": 120,
            "pass_score": 60,
            "max_score": 100,
            "price": 299.00,
            "status": "active",
            "category": "编程语言",
            "difficulty_level": "初级"
        }
        
        response, _ = self.make_request("POST", "/exam-products", data=exam_product_data, headers=self.headers)
        exam_product_id = None
        if response and response.status_code == 201:
            try:
                result = response.json()
                exam_product_id = result.get("id")
                print(f"✅ 考试产品创建成功，ID: {exam_product_id}")
            except:
                print("❌ 无法获取考试产品ID")
        
        # 2. 获取考试产品列表
        print("\n📋 2. 获取考试产品列表")
        response, _ = self.make_request("GET", "/exam-products?page=1&size=10", headers=self.headers)
        
        # 3. 获取考试产品详情
        if exam_product_id:
            print(f"\n🔍 3. 获取考试产品详情 (ID: {exam_product_id})")
            response, _ = self.make_request("GET", f"/exam-products/{exam_product_id}", headers=self.headers)
            
            # 4. 更新考试产品
            print(f"\n✏️  4. 更新考试产品 (ID: {exam_product_id})")
            update_data = {
                "name": "Python编程基础考试-高级版",
                "description": "更新后的Python编程基础知识和技能测试",
                "duration_minutes": 150,
                "price": 399.00
            }
            response, _ = self.make_request("PUT", f"/exam-products/{exam_product_id}", data=update_data, headers=self.headers)
            
            # 5. 删除考试产品
            print(f"\n🗑️  5. 删除考试产品 (ID: {exam_product_id})")
            response, _ = self.make_request("DELETE", f"/exam-products/{exam_product_id}", headers=self.headers)
    
    def test_venues_crud(self):
        """测试考场资源管理的CRUD操作"""
        print("\n" + "="*60)
        print("🏫 考场资源管理CRUD测试")
        print("="*60)
        
        # 1. 创建考场资源
        print("\n📝 1. 创建考场资源")
        venue_data = {
            "name": "北京朝阳考场",
            "code": "BJ001",
            "address": "北京市朝阳区建国路88号",
            "capacity": 100,
            "description": "现代化考场，设备齐全",
            "contact_person": "王五",
            "contact_phone": "010-12345678",
            "status": "active",
            "venue_type": "标准考场",
            "facilities": "电脑、投影仪、音响设备"
        }
        
        response, _ = self.make_request("POST", "/venues", data=venue_data, headers=self.headers)
        venue_id = None
        if response and response.status_code == 201:
            try:
                result = response.json()
                venue_id = result.get("id")
                print(f"✅ 考场资源创建成功，ID: {venue_id}")
            except:
                print("❌ 无法获取考场资源ID")
        
        # 2. 获取考场资源列表
        print("\n📋 2. 获取考场资源列表")
        response, _ = self.make_request("GET", "/venues?page=1&size=10", headers=self.headers)
        
        # 3. 获取考场资源详情
        if venue_id:
            print(f"\n🔍 3. 获取考场资源详情 (ID: {venue_id})")
            response, _ = self.make_request("GET", f"/venues/{venue_id}", headers=self.headers)
            
            # 4. 更新考场资源
            print(f"\n✏️  4. 更新考场资源 (ID: {venue_id})")
            update_data = {
                "name": "北京朝阳考场-升级版",
                "capacity": 150,
                "description": "升级后的现代化考场，设备更齐全",
                "facilities": "电脑、投影仪、音响设备、监控系统"
            }
            response, _ = self.make_request("PUT", f"/venues/{venue_id}", data=update_data, headers=self.headers)
            
            # 5. 删除考场资源
            print(f"\n🗑️  5. 删除考场资源 (ID: {venue_id})")
            response, _ = self.make_request("DELETE", f"/venues/{venue_id}", headers=self.headers)
    
    def test_unauthorized_access(self):
        """测试未授权访问"""
        print("\n" + "="*60)
        print("🚫 未授权访问测试")
        print("="*60)
        
        # 测试不带token访问
        print("\n🔒 测试不带token访问机构列表")
        response, _ = self.make_request("GET", "/institutions")
        
        print("\n🔒 测试不带token访问考试产品列表")
        response, _ = self.make_request("GET", "/exam-products")
        
        print("\n🔒 测试不带token访问考场资源列表")
        response, _ = self.make_request("GET", "/venues")
    
    def test_pagination_and_search(self):
        """测试分页和搜索功能"""
        print("\n" + "="*60)
        print("🔍 分页和搜索功能测试")
        print("="*60)
        
        # 测试分页
        print("\n📄 测试机构列表分页")
        response, _ = self.make_request("GET", "/institutions?page=1&size=5", headers=self.headers)
        
        # 测试搜索
        print("\n🔍 测试机构搜索")
        response, _ = self.make_request("GET", "/institutions?search=测试", headers=self.headers)
        
        # 测试状态过滤
        print("\n🔍 测试机构状态过滤")
        response, _ = self.make_request("GET", "/institutions?status_filter=active", headers=self.headers)
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始机构与资源管理API测试")
        print("="*60)
        
        # 1. 登录
        if not self.login_admin():
            print("❌ 登录失败，无法继续测试")
            return
        
        # 2. 测试机构管理
        self.test_institutions_crud()
        
        # 3. 测试考试产品管理
        self.test_exam_products_crud()
        
        # 4. 测试考场资源管理
        self.test_venues_crud()
        
        # 5. 测试未授权访问
        self.test_unauthorized_access()
        
        # 6. 测试分页和搜索
        self.test_pagination_and_search()
        
        print("\n" + "="*60)
        print("✅ 所有测试完成")
        print("="*60)

def main():
    """主函数"""
    tester = InstitutionVenueTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 