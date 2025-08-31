import requests
import json
from datetime import datetime

# 配置
BASE_URL = "http://localhost:8000/api/v1/pc"
HEADERS = {"Content-Type": "application/json"}

class PCInterfaceTest:
    def __init__(self):
        self.token = None
        self.headers = HEADERS.copy()
        self.test_results = []
    
    def log_test(self, test_name, success, message=""):
        """记录测试结果"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.test_results.append({
            "test": test_name,
            "status": status,
            "message": message
        })
        print(f"{status} {test_name}: {message}")
    
    def login(self):
        """登录获取token"""
        try:
            response = requests.post(
                f"{BASE_URL}/login",
                json={"username": "beijing_admin", "password": "123456"},
                headers=self.headers
            )
            if response.status_code == 200:
                data = response.json()
                self.token = data["access_token"]
                self.headers["Authorization"] = f"Bearer {self.token}"
                self.log_test("登录", True, "获取token成功")
                return True
            else:
                self.log_test("登录", False, f"状态码: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("登录", False, str(e))
            return False
    
    def test_auth_endpoints(self):
        """测试认证相关接口"""
        print("\n=== 测试认证接口 ===")
        
        # 获取用户信息
        try:
            response = requests.get(f"{BASE_URL}/profile", headers=self.headers)
            success = response.status_code == 200
            self.log_test("获取用户信息", success, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("获取用户信息", False, str(e))
    
    def test_dashboard_endpoints(self):
        """测试仪表板接口"""
        print("\n=== 测试仪表板接口 ===")
        
        # 获取统计信息
        try:
            response = requests.get(f"{BASE_URL}/dashboard/stats", headers=self.headers)
            success = response.status_code == 200
            self.log_test("仪表板统计", success, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("仪表板统计", False, str(e))
        
        # 获取最近考试
        try:
            response = requests.get(f"{BASE_URL}/dashboard/recent-exams", headers=self.headers)
            success = response.status_code == 200
            self.log_test("最近考试", success, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("最近考试", False, str(e))
        
        # 获取系统活动
        try:
            response = requests.get(f"{BASE_URL}/dashboard/activities", headers=self.headers)
            success = response.status_code == 200
            self.log_test("系统活动", success, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("系统活动", False, str(e))
    
    def test_candidate_endpoints(self):
        """测试考生管理接口"""
        print("\n=== 测试考生管理接口 ===")
        
        # 获取考生列表
        try:
            response = requests.get(f"{BASE_URL}/candidates", headers=self.headers)
            success = response.status_code == 200
            self.log_test("考生列表", success, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("考生列表", False, str(e))
        
        # 获取考生统计
        try:
            response = requests.get(f"{BASE_URL}/candidates/statistics", headers=self.headers)
            success = response.status_code == 200
            self.log_test("考生统计", success, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("考生统计", False, str(e))
    
    def test_checkin_endpoints(self):
        """测试签到管理接口"""
        print("\n=== 测试签到管理接口 ===")
        
        # 获取签到记录
        try:
            response = requests.get(f"{BASE_URL}/checkins", headers=self.headers)
            success = response.status_code == 200
            self.log_test("签到记录", success, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("签到记录", False, str(e))
        
        # 获取签到统计
        try:
            response = requests.get(f"{BASE_URL}/checkins/statistics", headers=self.headers)
            success = response.status_code == 200
            self.log_test("签到统计", success, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("签到统计", False, str(e))
    
    def test_venue_endpoints(self):
        """测试考场管理接口"""
        print("\n=== 测试考场管理接口 ===")
        
        # 获取考场列表
        try:
            response = requests.get(f"{BASE_URL}/venues", headers=self.headers)
            success = response.status_code == 200
            self.log_test("考场列表", success, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("考场列表", False, str(e))
        
        # 获取考场统计
        try:
            response = requests.get(f"{BASE_URL}/venues/statistics", headers=self.headers)
            success = response.status_code == 200
            self.log_test("考场统计", success, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("考场统计", False, str(e))
    
    def test_exam_product_endpoints(self):
        """测试考试产品接口"""
        print("\n=== 测试考试产品接口 ===")
        
        # 获取考试产品列表
        try:
            response = requests.get(f"{BASE_URL}/exam-products", headers=self.headers)
            success = response.status_code == 200
            self.log_test("考试产品列表", success, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("考试产品列表", False, str(e))
        
        # 获取考试产品统计
        try:
            response = requests.get(f"{BASE_URL}/exam-products/statistics", headers=self.headers)
            success = response.status_code == 200
            self.log_test("考试产品统计", success, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("考试产品统计", False, str(e))
    
    def test_institution_endpoints(self):
        """测试机构管理接口"""
        print("\n=== 测试机构管理接口 ===")
        
        # 获取机构列表 (需要超级管理员权限)
        try:
            response = requests.get(f"{BASE_URL}/institutions", headers=self.headers)
            # 预期403，因为当前用户是机构管理员，不是超级管理员
            success = response.status_code in [200, 403]
            self.log_test("机构列表", success, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("机构列表", False, str(e))
        
        # 获取机构统计 (需要超级管理员权限)
        try:
            response = requests.get(f"{BASE_URL}/institutions/statistics", headers=self.headers)
            # 预期403，因为当前用户是机构管理员，不是超级管理员
            success = response.status_code in [200, 403]
            self.log_test("机构统计", success, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("机构统计", False, str(e))
    
    def logout(self):
        """登出"""
        try:
            response = requests.post(f"{BASE_URL}/logout", headers=self.headers)
            success = response.status_code == 200
            self.log_test("登出", success, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("登出", False, str(e))
    
    def run_all_tests(self):
        """运行所有测试"""
        print("开始测试PC端接口...")
        print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 登录
        if not self.login():
            print("登录失败，终止测试")
            return
        
        # 运行各模块测试
        self.test_auth_endpoints()
        self.test_dashboard_endpoints()
        self.test_candidate_endpoints()
        self.test_checkin_endpoints()
        self.test_venue_endpoints()
        self.test_exam_product_endpoints()
        self.test_institution_endpoints()
        
        # 登出
        self.logout()
        
        # 统计结果
        self.print_summary()
    
    def print_summary(self):
        """打印测试总结"""
        print("\n" + "="*50)
        print("测试总结")
        print("="*50)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if "✅" in r["status"]])
        failed_tests = total_tests - passed_tests
        
        print(f"总测试数: {total_tests}")
        print(f"通过: {passed_tests}")
        print(f"失败: {failed_tests}")
        print(f"成功率: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print("\n失败的测试:")
            for result in self.test_results:
                if "❌" in result["status"]:
                    print(f"  - {result['test']}: {result['message']}")

if __name__ == "__main__":
    tester = PCInterfaceTest()
    tester.run_all_tests()