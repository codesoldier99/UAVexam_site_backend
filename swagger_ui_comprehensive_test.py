import requests
import json
import time
from datetime import datetime

class SwaggerUITestSuite:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.session = requests.Session()
        self.access_token = None
        self.test_results = []
        
    def log_test(self, test_name, status, response=None, error=None):
        """记录测试结果"""
        result = {
            "test_name": test_name,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "response_status": response.status_code if response else None,
            "response_text": response.text[:500] if response else None,
            "error": error
        }
        self.test_results.append(result)
        
        status_icon = "✅" if status == "PASS" else "❌"
        print(f"{status_icon} {test_name}")
        if error:
            print(f"   错误: {error}")
        if response and response.status_code != 200:
            print(f"   响应: {response.status_code} - {response.text[:200]}...")
    
    def test_health_check(self):
        """测试健康检查端点"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                self.log_test("健康检查", "PASS", response)
            else:
                self.log_test("健康检查", "FAIL", response, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("健康检查", "FAIL", error=str(e))
    
    def test_root_endpoint(self):
        """测试根端点"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                self.log_test("根端点", "PASS", response)
            else:
                self.log_test("根端点", "FAIL", response, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("根端点", "FAIL", error=str(e))
    
    def test_user_registration(self):
        """测试用户注册"""
        test_user = {
            "username": f"testuser_{int(time.time())}",
            "email": f"test{int(time.time())}@example.com",
            "password": "testpassword123",
            "role_id": 1,
            "institution_id": 1
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/auth/register",
                json=test_user,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code in [200, 201]:
                self.log_test("用户注册", "PASS", response)
                # 保存测试用户信息用于后续测试
                self.test_user = test_user
            else:
                self.log_test("用户注册", "FAIL", response, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("用户注册", "FAIL", error=str(e))
    
    def test_user_login(self):
        """测试用户登录"""
        if not hasattr(self, 'test_user'):
            self.log_test("用户登录", "SKIP", error="没有测试用户数据")
            return
            
        try:
            response = self.session.post(
                f"{self.base_url}/auth/jwt/login",
                data={
                    "username": self.test_user["email"],
                    "password": self.test_user["password"]
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access_token")
                self.log_test("用户登录", "PASS", response)
            else:
                self.log_test("用户登录", "FAIL", response, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("用户登录", "FAIL", error=str(e))
    
    def test_institutions_api(self):
        """测试机构管理 API"""
        # 设置认证头
        headers = {"Content-Type": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        
        # 测试获取机构列表
        try:
            response = self.session.get(f"{self.base_url}/institutions", headers=headers)
            if response.status_code == 200:
                self.log_test("获取机构列表", "PASS", response)
            else:
                self.log_test("获取机构列表", "FAIL", response, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("获取机构列表", "FAIL", error=str(e))
        
        # 测试创建机构
        test_institution = {
            "name": f"测试机构_{int(time.time())}",
            "code": f"TEST_{int(time.time())}",
            "contact_person": "张三",
            "phone": "13800138000",
            "email": f"contact{int(time.time())}@example.com",
            "address": "北京市朝阳区",
            "description": "测试机构",
            "status": "active"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/institutions",
                json=test_institution,
                headers=headers
            )
            
            if response.status_code in [200, 201]:
                self.log_test("创建机构", "PASS", response)
                # 保存机构ID用于后续测试
                institution_data = response.json()
                self.test_institution_id = institution_data.get("id")
            else:
                self.log_test("创建机构", "FAIL", response, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("创建机构", "FAIL", error=str(e))
    
    def test_exam_products_api(self):
        """测试考试产品 API"""
        # 设置认证头
        headers = {"Content-Type": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        
        # 测试获取考试产品列表
        try:
            response = self.session.get(f"{self.base_url}/exam-products", headers=headers)
            if response.status_code == 200:
                self.log_test("获取考试产品列表", "PASS", response)
            else:
                self.log_test("获取考试产品列表", "FAIL", response, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("获取考试产品列表", "FAIL", error=str(e))
        
        # 测试创建考试产品
        test_product = {
            "name": f"测试考试产品_{int(time.time())}",
            "description": "这是一个测试考试产品",
            "duration_minutes": 120,
            "status": "active"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/exam-products",
                json=test_product,
                headers=headers
            )
            
            if response.status_code in [200, 201]:
                self.log_test("创建考试产品", "PASS", response)
            else:
                self.log_test("创建考试产品", "FAIL", response, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("创建考试产品", "FAIL", error=str(e))
    
    def test_venues_api(self):
        """测试场地管理 API"""
        # 设置认证头
        headers = {"Content-Type": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        
        # 测试获取场地列表
        try:
            response = self.session.get(f"{self.base_url}/venues", headers=headers)
            if response.status_code == 200:
                self.log_test("获取场地列表", "PASS", response)
            else:
                self.log_test("获取场地列表", "FAIL", response, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("获取场地列表", "FAIL", error=str(e))
        
        # 测试创建场地
        test_venue = {
            "name": f"测试场地_{int(time.time())}",
            "type": "室内",
            "capacity": 50,
            "status": "active"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/venues",
                json=test_venue,
                headers=headers
            )
            
            if response.status_code in [200, 201]:
                self.log_test("创建场地", "PASS", response)
            else:
                self.log_test("创建场地", "FAIL", response, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("创建场地", "FAIL", error=str(e))
    
    def test_candidates_api(self):
        """测试考生管理 API"""
        # 设置认证头
        headers = {"Content-Type": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        
        # 测试获取考生列表
        try:
            response = self.session.get(f"{self.base_url}/candidates", headers=headers)
            if response.status_code == 200:
                self.log_test("获取考生列表", "PASS", response)
            else:
                self.log_test("获取考生列表", "FAIL", response, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("获取考生列表", "FAIL", error=str(e))
        
        # 测试创建考生
        test_candidate = {
            "name": f"测试考生_{int(time.time())}",
            "id_card": f"123456789{int(time.time())}",
            "phone": "13900139000",
            "institution_id": 1,
            "exam_product_id": 1,
            "status": "pending"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/candidates",
                json=test_candidate,
                headers=headers
            )
            
            if response.status_code in [200, 201]:
                self.log_test("创建考生", "PASS", response)
            else:
                self.log_test("创建考生", "FAIL", response, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("创建考生", "FAIL", error=str(e))
    
    def test_schedules_api(self):
        """测试考试安排 API"""
        # 设置认证头
        headers = {"Content-Type": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        
        # 测试获取考试安排列表
        try:
            response = self.session.get(f"{self.base_url}/schedules", headers=headers)
            if response.status_code == 200:
                self.log_test("获取考试安排列表", "PASS", response)
            else:
                self.log_test("获取考试安排列表", "FAIL", response, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("获取考试安排列表", "FAIL", error=str(e))
        
        # 测试创建考试安排
        test_schedule = {
            "candidate_id": 1,
            "venue_id": 1,
            "exam_date": "2024-12-25",
            "start_time": "09:00",
            "end_time": "11:00",
            "activity_name": "无人机理论考试",
            "status": "pending"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/schedules",
                json=test_schedule,
                headers=headers
            )
            
            if response.status_code in [200, 201]:
                self.log_test("创建考试安排", "PASS", response)
            else:
                self.log_test("创建考试安排", "FAIL", response, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("创建考试安排", "FAIL", error=str(e))
    
    def test_simple_endpoints(self):
        """测试简化端点"""
        # 测试简化机构端点
        try:
            response = self.session.get(f"{self.base_url}/simple-institutions")
            if response.status_code == 200:
                self.log_test("获取简化机构列表", "PASS", response)
            else:
                self.log_test("获取简化机构列表", "FAIL", response, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("获取简化机构列表", "FAIL", error=str(e))
        
        # 测试简化机构统计
        try:
            response = self.session.get(f"{self.base_url}/simple-institutions/stats")
            if response.status_code == 200:
                self.log_test("获取简化机构统计", "PASS", response)
            else:
                self.log_test("获取简化机构统计", "FAIL", response, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("获取简化机构统计", "FAIL", error=str(e))
    
    def test_documentation_endpoints(self):
        """测试文档端点"""
        # 测试 Swagger UI
        try:
            response = self.session.get(f"{self.base_url}/docs")
            if response.status_code == 200:
                self.log_test("Swagger UI 文档", "PASS", response)
            else:
                self.log_test("Swagger UI 文档", "FAIL", response, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("Swagger UI 文档", "FAIL", error=str(e))
        
        # 测试 OpenAPI JSON
        try:
            response = self.session.get(f"{self.base_url}/openapi.json")
            if response.status_code == 200:
                self.log_test("OpenAPI JSON", "PASS", response)
            else:
                self.log_test("OpenAPI JSON", "FAIL", response, f"状态码: {response.status_code}")
        except Exception as e:
            self.log_test("OpenAPI JSON", "FAIL", error=str(e))
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 60)
        print("🚀 开始 Swagger UI 全面测试")
        print("=" * 60)
        
        # 基础端点测试
        print("\n📋 基础端点测试:")
        self.test_health_check()
        self.test_root_endpoint()
        
        # 认证测试
        print("\n🔐 认证测试:")
        self.test_user_registration()
        self.test_user_login()
        
        # 核心 API 测试
        print("\n🏢 机构管理 API 测试:")
        self.test_institutions_api()
        
        print("\n📚 考试产品 API 测试:")
        self.test_exam_products_api()
        
        print("\n🏟️ 场地管理 API 测试:")
        self.test_venues_api()
        
        print("\n👥 考生管理 API 测试:")
        self.test_candidates_api()
        
        print("\n📅 考试安排 API 测试:")
        self.test_schedules_api()
        
        # 简化端点测试
        print("\n⚡ 简化端点测试:")
        self.test_simple_endpoints()
        
        # 文档端点测试
        print("\n📖 文档端点测试:")
        self.test_documentation_endpoints()
        
        # 生成测试报告
        self.generate_report()
    
    def generate_report(self):
        """生成测试报告"""
        print("\n" + "=" * 60)
        print("📊 测试报告")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        skipped_tests = len([r for r in self.test_results if r["status"] == "SKIP"])
        
        print(f"总测试数: {total_tests}")
        print(f"通过: {passed_tests} ✅")
        print(f"失败: {failed_tests} ❌")
        print(f"跳过: {skipped_tests} ⏭️")
        print(f"成功率: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print("\n❌ 失败的测试:")
            for result in self.test_results:
                if result["status"] == "FAIL":
                    print(f"  - {result['test_name']}: {result.get('error', '未知错误')}")
        
        # 保存详细报告到文件
        report_file = f"swagger_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        print(f"\n📄 详细报告已保存到: {report_file}")

if __name__ == "__main__":
    test_suite = SwaggerUITestSuite()
    test_suite.run_all_tests() 