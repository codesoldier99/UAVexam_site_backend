#!/usr/bin/env python3
"""
自动API测试脚本
"""

import requests
import json
import time
from datetime import datetime

class APITester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.admin_token = None
        self.user_token = None
        self.test_results = []
        
    def log_test(self, test_name, status, response_time, status_code, details=""):
        """记录测试结果"""
        result = {
            "test_name": test_name,
            "status": status,
            "response_time": response_time,
            "status_code": status_code,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        # 打印结果
        status_icon = "✅" if status == "PASS" else "❌"
        print(f"{status_icon} {test_name}: {status_code} ({response_time}ms) {details}")
    
    def make_request(self, method, endpoint, data=None, headers=None, description=""):
        """发送HTTP请求"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
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
            return response, response_time
            
        except requests.exceptions.ConnectionError:
            return None, 0
        except Exception as e:
            return None, 0
    
    def test_server_status(self):
        """测试服务器状态"""
        print("\n🔍 测试服务器状态...")
        
        response, response_time = self.make_request("GET", "/docs")
        if response and response.status_code == 200:
            self.log_test("服务器状态", "PASS", response_time, response.status_code, "服务器正常运行")
            return True
        else:
            self.log_test("服务器状态", "FAIL", response_time, 0, "服务器未运行或无法访问")
            return False
    
    def test_admin_login(self):
        """测试管理员登录"""
        print("\n🔐 测试管理员登录...")
        
        data = {
            "username": "admin@exam.com",
            "password": "admin123"
        }
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        response, response_time = self.make_request("POST", "/auth/jwt/login", data=data, headers=headers)
        
        if response and response.status_code == 200:
            try:
                token_data = response.json()
                if "access_token" in token_data:
                    self.admin_token = token_data["access_token"]
                    self.log_test("管理员登录", "PASS", response_time, response.status_code, "登录成功")
                    return True
                else:
                    self.log_test("管理员登录", "FAIL", response_time, response.status_code, "响应中缺少access_token")
                    return False
            except json.JSONDecodeError:
                self.log_test("管理员登录", "FAIL", response_time, response.status_code, "响应格式错误")
                return False
        else:
            status_code = response.status_code if response else 0
            self.log_test("管理员登录", "FAIL", response_time, status_code, "登录失败")
            return False
    
    def test_create_institution(self):
        """测试创建机构"""
        if not self.admin_token:
            self.log_test("创建机构", "SKIP", 0, 0, "需要管理员token")
            return False
        
        print("\n🏢 测试创建机构...")
        
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
            self.log_test("创建机构", "PASS", response_time, response.status_code, "机构创建成功")
            return True
        else:
            status_code = response.status_code if response else 0
            self.log_test("创建机构", "FAIL", response_time, status_code, "机构创建失败")
            return False
    
    def test_get_institutions(self):
        """测试获取机构列表"""
        if not self.admin_token:
            self.log_test("获取机构列表", "SKIP", 0, 0, "需要管理员token")
            return False
        
        print("\n📋 测试获取机构列表...")
        
        headers = {
            "Authorization": f"Bearer {self.admin_token}"
        }
        
        response, response_time = self.make_request("GET", "/institutions?page=1&size=10", headers=headers)
        
        if response and response.status_code == 200:
            self.log_test("获取机构列表", "PASS", response_time, response.status_code, "获取成功")
            return True
        else:
            status_code = response.status_code if response else 0
            self.log_test("获取机构列表", "FAIL", response_time, status_code, "获取失败")
            return False
    
    def test_create_exam_product(self):
        """测试创建考试产品"""
        if not self.admin_token:
            self.log_test("创建考试产品", "SKIP", 0, 0, "需要管理员token")
            return False
        
        print("\n📚 测试创建考试产品...")
        
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
            self.log_test("创建考试产品", "PASS", response_time, response.status_code, "产品创建成功")
            return True
        else:
            status_code = response.status_code if response else 0
            self.log_test("创建考试产品", "FAIL", response_time, status_code, "产品创建失败")
            return False
    
    def test_create_venue(self):
        """测试创建考场资源"""
        if not self.admin_token:
            self.log_test("创建考场资源", "SKIP", 0, 0, "需要管理员token")
            return False
        
        print("\n🏫 测试创建考场资源...")
        
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
            self.log_test("创建考场资源", "PASS", response_time, response.status_code, "资源创建成功")
            return True
        else:
            status_code = response.status_code if response else 0
            self.log_test("创建考场资源", "FAIL", response_time, status_code, "资源创建失败")
            return False
    
    def test_unauthorized_access(self):
        """测试无权限访问"""
        print("\n🔒 测试无权限访问...")
        
        headers = {
            "Authorization": "Bearer invalid_token"
        }
        
        response, response_time = self.make_request("GET", "/institutions", headers=headers)
        
        if response and response.status_code == 401:
            self.log_test("无权限访问", "PASS", response_time, response.status_code, "正确返回401错误")
            return True
        else:
            status_code = response.status_code if response else 0
            self.log_test("无权限访问", "FAIL", response_time, status_code, "权限检查异常")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始自动API测试")
        print("=" * 50)
        
        # 测试服务器状态
        if not self.test_server_status():
            print("❌ 服务器未运行，请先启动服务器")
            return
        
        # 测试认证
        if not self.test_admin_login():
            print("❌ 管理员登录失败，请检查用户凭据")
            return
        
        # 测试功能模块
        self.test_create_institution()
        self.test_get_institutions()
        self.test_create_exam_product()
        self.test_create_venue()
        self.test_unauthorized_access()
        
        # 生成测试报告
        self.generate_report()
    
    def generate_report(self):
        """生成测试报告"""
        print("\n" + "=" * 50)
        print("📊 测试报告")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        skipped_tests = len([r for r in self.test_results if r["status"] == "SKIP"])
        
        print(f"总测试数: {total_tests}")
        print(f"通过: {passed_tests}")
        print(f"失败: {failed_tests}")
        print(f"跳过: {skipped_tests}")
        print(f"成功率: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "成功率: 0%")
        
        # 计算平均响应时间
        response_times = [r["response_time"] for r in self.test_results if r["response_time"] > 0]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            print(f"平均响应时间: {avg_response_time:.0f}ms")
        
        # 保存详细报告
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 详细报告已保存到: {report_file}")

def main():
    """主函数"""
    tester = APITester()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 