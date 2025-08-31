"""
手动签到接口批量测试脚本
用于测试多种场景和边界条件
"""

import requests
import json
from datetime import datetime

# 配置
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1/wechat"

# 测试用户凭据
TEST_USERNAME = "admin"
TEST_PASSWORD = "password"

# 测试用例数据
TEST_CASES = [
    {
        "name": "正常考生测试",
        "real_name": "张三",
        "id_card": "110101199001011234",
        "expected": "success"
    },
    {
        "name": "不存在的考生",
        "real_name": "不存在的人",
        "id_card": "999999999999999999",
        "expected": "not_found"
    },
    {
        "name": "姓名不匹配",
        "real_name": "错误姓名",
        "id_card": "110101199001011234",
        "expected": "mismatch"
    },
    {
        "name": "空姓名测试",
        "real_name": "",
        "id_card": "110101199001011234",
        "expected": "validation_error"
    },
    {
        "name": "空身份证测试",
        "real_name": "张三",
        "id_card": "",
        "expected": "validation_error"
    }
]

class BatchTester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.results = []
        
    def login(self):
        """登录获取token"""
        print("🔐 正在登录...")
        login_data = {
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD
        }
        
        try:
            response = self.session.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
            if response.status_code == 200:
                result = response.json()
                self.token = result.get("access_token")
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                print("✅ 登录成功")
                return True
            else:
                print(f"❌ 登录失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 登录异常: {e}")
            return False
    
    def test_single_case(self, test_case):
        """测试单个用例"""
        print(f"\n🧪 测试用例: {test_case['name']}")
        print(f"   姓名: '{test_case['real_name']}'")
        print(f"   身份证: '{test_case['id_card']}'")
        print(f"   预期结果: {test_case['expected']}")
        
        query_data = {
            "real_name": test_case['real_name'],
            "id_card": test_case['id_card']
        }
        
        try:
            response = self.session.post(f"{API_BASE}/manual-checkin/query", json=query_data)
            status_code = response.status_code
            
            result = {
                "test_case": test_case['name'],
                "status_code": status_code,
                "expected": test_case['expected'],
                "success": False,
                "response": None,
                "error": None
            }
            
            if status_code == 200:
                response_data = response.json()
                result["response"] = response_data
                result["success"] = True
                print(f"   ✅ 状态码: {status_code}")
                print(f"   📋 考生信息: {response_data.get('candidate_info', {}).get('real_name', 'N/A')}")
                print(f"   📅 考试安排: {len(response_data.get('exam_schedules', []))} 个")
                
            elif status_code == 400:
                error_detail = response.json().get('detail', 'Unknown error')
                result["error"] = error_detail
                print(f"   ⚠️  状态码: {status_code}")
                print(f"   📝 错误信息: {error_detail}")
                
            elif status_code == 422:
                error_detail = response.json().get('detail', 'Validation error')
                result["error"] = error_detail
                print(f"   ⚠️  状态码: {status_code} (验证错误)")
                print(f"   📝 错误信息: {error_detail}")
                
            else:
                error_text = response.text
                result["error"] = error_text
                print(f"   ❌ 状态码: {status_code}")
                print(f"   📝 响应: {error_text}")
            
            self.results.append(result)
            return result
            
        except Exception as e:
            print(f"   ❌ 请求异常: {e}")
            result = {
                "test_case": test_case['name'],
                "status_code": None,
                "expected": test_case['expected'],
                "success": False,
                "response": None,
                "error": str(e)
            }
            self.results.append(result)
            return result
    
    def test_permission_denied(self):
        """测试权限拒绝场景"""
        print(f"\n🔒 测试权限拒绝场景...")
        
        # 临时移除token
        original_headers = dict(self.session.headers)
        self.session.headers.pop("Authorization", None)
        
        query_data = {
            "real_name": "测试用户",
            "id_card": "110101199001011234"
        }
        
        try:
            response = self.session.post(f"{API_BASE}/manual-checkin/query", json=query_data)
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 401:
                print("   ✅ 正确拒绝未认证请求")
            else:
                print(f"   ⚠️  意外状态码: {response.status_code}")
                print(f"   响应: {response.text}")
                
        except Exception as e:
            print(f"   ❌ 请求异常: {e}")
        finally:
            # 恢复headers
            self.session.headers = original_headers
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始批量测试")
        print("=" * 60)
        
        # 运行所有测试用例
        for test_case in TEST_CASES:
            self.test_single_case(test_case)
        
        # 测试权限
        self.test_permission_denied()
        
        # 生成测试报告
        self.generate_report()
    
    def generate_report(self):
        """生成测试报告"""
        print("\n" + "=" * 60)
        print("📊 测试报告")
        print("=" * 60)
        
        total_tests = len(self.results)
        successful_requests = len([r for r in self.results if r['status_code'] in [200, 400, 422]])
        failed_requests = len([r for r in self.results if r['status_code'] not in [200, 400, 422] or r['status_code'] is None])
        
        print(f"总测试数: {total_tests}")
        print(f"请求成功: {successful_requests}")
        print(f"请求失败: {failed_requests}")
        print(f"成功率: {successful_requests/total_tests*100:.1f}%")
        
        print("\n📋 详细结果:")
        for result in self.results:
            status = "✅" if result['status_code'] in [200, 400, 422] else "❌"
            print(f"  {status} {result['test_case']}: HTTP {result['status_code']}")
            if result['error']:
                print(f"     错误: {result['error']}")
        
        # 保存详细报告到文件
        report_file = f"manual_checkin_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_tests": total_tests,
                    "successful_requests": successful_requests,
                    "failed_requests": failed_requests,
                    "success_rate": successful_requests/total_tests*100
                },
                "results": self.results
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 详细报告已保存到: {report_file}")

def main():
    """主函数"""
    print("🧪 手动签到接口批量测试脚本")
    print("=" * 60)
    
    tester = BatchTester()
    
    # 登录
    if not tester.login():
        print("❌ 登录失败，无法继续测试")
        return
    
    # 运行所有测试
    tester.run_all_tests()

if __name__ == "__main__":
    main()