#!/usr/bin/env python3
"""
PC端接口完整测试脚本
测试所有新创建的PC端专用接口功能
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

class PCInterfaceTest:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.pc_base_url = f"{base_url}/api/v1/pc"
        self.token = None
        self.user_info = None
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, message: str = "", data: Any = None):
        """记录测试结果"""
        result = {
            "test_name": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if data and not success:
            print(f"   详细信息: {data}")
    
    def make_request(self, method: str, endpoint: str, data: Dict = None, headers: Dict = None) -> tuple:
        """发送HTTP请求"""
        url = f"{self.pc_base_url}{endpoint}"
        
        # 默认headers
        default_headers = {"Content-Type": "application/json"}
        if self.token:
            default_headers["Authorization"] = f"Bearer {self.token}"
        
        if headers:
            default_headers.update(headers)
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=default_headers, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=default_headers, timeout=10)
            elif method.upper() == "PUT":
                response = requests.put(url, json=data, headers=default_headers, timeout=10)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=default_headers, timeout=10)
            else:
                return False, {"error": f"不支持的HTTP方法: {method}"}
            
            return True, {
                "status_code": response.status_code,
                "data": response.json() if response.content else {},
                "headers": dict(response.headers)
            }
            
        except requests.exceptions.RequestException as e:
            return False, {"error": str(e)}
        except json.JSONDecodeError as e:
            return False, {"error": f"JSON解析错误: {str(e)}"}
    
    def test_server_health(self):
        """测试服务器健康状态"""
        print("\n🏥 测试服务器健康状态...")
        
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                self.log_test("服务器健康检查", True, "服务器运行正常")
                return True
            else:
                self.log_test("服务器健康检查", False, f"服务器响应异常: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("服务器健康检查", False, f"无法连接到服务器: {str(e)}")
            return False
    
    def test_pc_auth_login(self):
        """测试PC端登录接口"""
        print("\n🔐 测试PC端认证接口...")
        
        # 测试管理员登录
        login_data = {
            "username": "beijing_admin",
            "password": "123456"
        }
        
        success, result = self.make_request("POST", "/auth/login", login_data)
        
        if success and result["status_code"] == 200:
            self.token = result["data"].get("access_token")
            self.user_info = result["data"].get("user_info")
            self.log_test("PC端管理员登录", True, f"登录成功，用户: {self.user_info.get('real_name', 'Unknown')}")
        else:
            self.log_test("PC端管理员登录", False, "登录失败", result)
            return False
        
        # 测试考生登录（应该失败）
        candidate_login_data = {
            "username": "candidate_011234",
            "password": "011234"
        }
        
        success, result = self.make_request("POST", "/auth/login", candidate_login_data)
        
        if success and result["status_code"] == 403:
            self.log_test("PC端考生登录限制", True, "正确拒绝了考生登录")
        else:
            self.log_test("PC端考生登录限制", False, "应该拒绝考生登录", result)
        
        return True
    
    def test_pc_auth_profile(self):
        """测试获取用户信息接口"""
        if not self.token:
            self.log_test("获取用户信息", False, "未登录，跳过测试")
            return False
        
        success, result = self.make_request("GET", "/auth/profile")
        
        if success and result["status_code"] == 200:
            user_data = result["data"]
            self.log_test("获取用户信息", True, f"获取成功，角色: {user_data.get('role')}")
        else:
            self.log_test("获取用户信息", False, "获取失败", result)
            return False
        
        return True
    
    def test_pc_dashboard(self):
        """测试PC端仪表板接口"""
        print("\n📊 测试PC端仪表板接口...")
        
        if not self.token:
            self.log_test("仪表板测试", False, "未登录，跳过测试")
            return False
        
        # 测试统计数据
        success, result = self.make_request("GET", "/dashboard/stats")
        
        if success and result["status_code"] == 200:
            stats = result["data"]
            self.log_test("仪表板统计数据", True, f"获取成功，今日考试: {stats.get('exam_stats', {}).get('today_total', 0)}")
        else:
            self.log_test("仪表板统计数据", False, "获取失败", result)
        
        # 测试最近考试
        success, result = self.make_request("GET", "/dashboard/recent-exams?limit=5")
        
        if success and result["status_code"] == 200:
            exams = result["data"]
            self.log_test("最近考试列表", True, f"获取成功，考试数量: {len(exams)}")
        else:
            self.log_test("最近考试列表", False, "获取失败", result)
        
        # 测试系统活动
        success, result = self.make_request("GET", "/dashboard/activities?limit=10")
        
        if success and result["status_code"] == 200:
            activities = result["data"]
            self.log_test("系统活动日志", True, f"获取成功，活动数量: {len(activities)}")
        else:
            self.log_test("系统活动日志", False, "获取失败", result)
        
        return True
    
    def test_pc_candidates(self):
        """测试PC端考生管理接口"""
        print("\n👥 测试PC端考生管理接口...")
        
        if not self.token:
            self.log_test("考生管理测试", False, "未登录，跳过测试")
            return False
        
        # 测试获取考生列表
        success, result = self.make_request("GET", "/candidates/?page=1&size=10")
        
        if success and result["status_code"] == 200:
            candidates_data = result["data"]
            total = candidates_data.get("total", 0)
            self.log_test("获取考生列表", True, f"获取成功，总数: {total}")
        else:
            self.log_test("获取考生列表", False, "获取失败", result)
        
        # 测试搜索考生
        success, result = self.make_request("GET", "/candidates/?search=张三")
        
        if success and result["status_code"] == 200:
            self.log_test("搜索考生功能", True, "搜索功能正常")
        else:
            self.log_test("搜索考生功能", False, "搜索失败", result)
        
        # 测试考生统计
        success, result = self.make_request("GET", "/candidates/statistics")
        
        if success and result["status_code"] == 200:
            stats = result["data"]
            self.log_test("考生统计数据", True, f"统计获取成功")
        else:
            self.log_test("考生统计数据", False, "统计获取失败", result)
        
        # 测试创建考生
        new_candidate = {
            "real_name": "测试考生",
            "id_card": "110101199901010001",
            "phone": "13800000001",
            "email": "test@example.com",
            "institution_id": 1,
            "exam_product_id": 1  # 添加必需的考试产品ID
        }
        
        success, result = self.make_request("POST", "/candidates/", new_candidate)
        
        if success and result["status_code"] in [200, 201]:
            candidate_id = result["data"].get("id")
            self.log_test("创建考生", True, f"创建成功，ID: {candidate_id}")
            
            # 测试更新考生
            if candidate_id:
                update_data = {"real_name": "测试考生更新"}
                success, result = self.make_request("PUT", f"/candidates/{candidate_id}", update_data)
                
                if success and result["status_code"] == 200:
                    self.log_test("更新考生信息", True, "更新成功")
                else:
                    self.log_test("更新考生信息", False, "更新失败", result)
        else:
            self.log_test("创建考生", False, "创建失败", result)
        
        return True
    
    def test_pc_checkins(self):
        """测试PC端签到管理接口"""
        print("\n📝 测试PC端签到管理接口...")
        
        if not self.token:
            self.log_test("签到管理测试", False, "未登录，跳过测试")
            return False
        
        # 测试获取签到记录
        success, result = self.make_request("GET", "/checkins/?page=1&size=10")
        
        if success and result["status_code"] == 200:
            checkins_data = result["data"]
            total = checkins_data.get("total", 0)
            self.log_test("获取签到记录", True, f"获取成功，总数: {total}")
        else:
            self.log_test("获取签到记录", False, "获取失败", result)
        
        # 测试手动签到查询
        success, result = self.make_request("GET", "/checkins/manual-query?real_name=张三&id_card=110101199001011234")
        
        if success and result["status_code"] in [200, 400]:  # 400也是正常的，可能考生不存在
            self.log_test("手动签到查询", True, "查询接口正常响应")
        else:
            self.log_test("手动签到查询", False, "查询失败", result)
        
        # 测试签到统计
        success, result = self.make_request("GET", "/checkins/statistics")
        
        if success and result["status_code"] == 200:
            stats = result["data"]
            self.log_test("签到统计数据", True, f"统计获取成功，总签到数: {stats.get('total', 0)}")
        else:
            self.log_test("签到统计数据", False, "统计获取失败", result)
        
        return True
    
    def test_pc_auth_logout(self):
        """测试PC端登出接口"""
        if not self.token:
            self.log_test("用户登出", False, "未登录，跳过测试")
            return False
        
        success, result = self.make_request("POST", "/auth/logout")
        
        if success and result["status_code"] == 200:
            self.log_test("用户登出", True, "登出成功")
            self.token = None
            self.user_info = None
        else:
            self.log_test("用户登出", False, "登出失败", result)
        
        return True
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始PC端接口完整测试...")
        print("=" * 60)
        
        start_time = time.time()
        
        # 测试顺序
        tests = [
            ("服务器健康检查", self.test_server_health),
            ("PC端认证功能", self.test_pc_auth_login),
            ("用户信息获取", self.test_pc_auth_profile),
            ("仪表板功能", self.test_pc_dashboard),
            ("考生管理功能", self.test_pc_candidates),
            ("签到管理功能", self.test_pc_checkins),
            ("用户登出功能", self.test_pc_auth_logout),
        ]
        
        for test_name, test_func in tests:
            try:
                test_func()
            except Exception as e:
                self.log_test(test_name, False, f"测试异常: {str(e)}")
            
            time.sleep(0.5)  # 避免请求过快
        
        # 生成测试报告
        self.generate_test_report(time.time() - start_time)
    
    def generate_test_report(self, duration: float):
        """生成测试报告"""
        print("\n" + "=" * 60)
        print("📋 PC端接口测试报告")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["success"]])
        failed_tests = total_tests - passed_tests
        
        print(f"📊 测试统计:")
        print(f"   总测试数: {total_tests}")
        print(f"   通过数量: {passed_tests} ✅")
        print(f"   失败数量: {failed_tests} ❌")
        print(f"   成功率: {(passed_tests/total_tests*100):.1f}%")
        print(f"   测试耗时: {duration:.2f}秒")
        
        if failed_tests > 0:
            print(f"\n❌ 失败的测试:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"   - {result['test_name']}: {result['message']}")
        
        print(f"\n🎯 测试的PC端接口:")
        print(f"   - /api/v1/pc/auth/*        # 认证相关")
        print(f"   - /api/v1/pc/dashboard/*   # 仪表板")
        print(f"   - /api/v1/pc/candidates/*  # 考生管理")
        print(f"   - /api/v1/pc/checkins/*    # 签到管理")
        
        # 保存详细报告到文件
        report_file = f"pc_interface_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                "summary": {
                    "total_tests": total_tests,
                    "passed_tests": passed_tests,
                    "failed_tests": failed_tests,
                    "success_rate": passed_tests/total_tests*100,
                    "duration": duration,
                    "timestamp": datetime.now().isoformat()
                },
                "test_results": self.test_results
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 详细报告已保存到: {report_file}")
        
        if passed_tests == total_tests:
            print(f"\n🎉 所有测试通过！PC端接口实现完美！")
        else:
            print(f"\n⚠️  部分测试失败，请检查服务器状态和接口实现")

def main():
    """主函数"""
    print("🛩️  UAV考点运营管理系统 - PC端接口测试")
    print("=" * 60)
    
    # 可以通过命令行参数指定服务器地址
    import sys
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    print(f"🌐 测试服务器: {base_url}")
    print(f"🎯 测试目标: PC端专用接口 (/api/v1/pc/*)")
    
    # 创建测试实例并运行
    tester = PCInterfaceTest(base_url)
    tester.run_all_tests()

if __name__ == "__main__":
    main()