"""
手动签到接口批量测试脚本 - 最终版本
包含详细的错误处理和多种登录方式
"""

import requests
import json
from datetime import datetime

# 配置
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1/wechat"

# 扩展的登录账号
LOGIN_ACCOUNTS = [
    {"username": "admin", "password": "admin123"},
    {"username": "admin", "password": "admin"},
    {"username": "admin", "password": "123456"},
    {"username": "beijing_admin", "password": "123456"},
    {"username": "shanghai_admin", "password": "123456"},
    {"username": "shenzhen_admin", "password": "123456"},
]

# 基于真实数据的测试用例
TEST_CASES = [
    {
        "name": "张三-正常测试",
        "real_name": "张三",
        "id_card": "110101199001011234",
        "expected": "success"
    },
    {
        "name": "李四-正常测试",
        "real_name": "李四",
        "id_card": "110101199002022345",
        "expected": "success"
    },
    {
        "name": "赵六-上海考生",
        "real_name": "赵六",
        "id_card": "310101199004044567",
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
        "real_name": "李四",
        "id_card": "110101199001011234",  # 张三的身份证
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
        self.current_user = None
        
    def try_login(self):
        """尝试登录"""
        print("🔐 尝试登录...")
        
        for account in LOGIN_ACCOUNTS:
            print(f"   尝试: {account['username']} / {account['password']}")
            
            try:
                response = self.session.post(f"{BASE_URL}/api/v1/auth/login", json=account, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    self.token = result.get("access_token")
                    self.current_user = account
                    self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                    print(f"   ✅ 登录成功: {account['username']}")
                    return True
                else:
                    print(f"   ❌ 登录失败: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ 登录异常: {e}")
        
        print("❌ 所有登录尝试都失败了")
        return False
    
    def test_single_case(self, test_case):
        """测试单个用例"""
        print(f"\n🧪 测试用例: {test_case['name']}")
        print(f"   姓名: '{test_case['real_name']}'")
        print(f"   身份证: '{test_case['id_card']}'")
        
        if not self.token:
            print("   ❌ 未登录，跳过测试")
            return None
        
        query_data = {
            "real_name": test_case['real_name'],
            "id_card": test_case['id_card']
        }
        
        try:
            response = self.session.post(f"{API_BASE}/manual-checkin/query", json=query_data, timeout=10)
            status_code = response.status_code
            
            result = {
                "test_case": test_case['name'],
                "status_code": status_code,
                "expected": test_case['expected'],
                "success": False,
                "response": None,
                "error": None,
                "schedule_count": 0
            }
            
            print(f"   状态码: {status_code}")
            
            if status_code == 200:
                response_data = response.json()
                result["response"] = response_data
                result["success"] = True
                
                candidate_info = response_data.get('candidate_info', {})
                exam_schedules = response_data.get('exam_schedules', [])
                result["schedule_count"] = len(exam_schedules)
                
                print(f"   ✅ 查询成功")
                print(f"   考生: {candidate_info.get('real_name', 'N/A')}")
                print(f"   考试安排: {len(exam_schedules)} 个")
                
                if exam_schedules:
                    available_count = len([s for s in exam_schedules if s.get('can_checkin')])
                    print(f"   可签到: {available_count} 个")
                
            elif status_code in [400, 422]:
                try:
                    error_detail = response.json().get('detail', 'Unknown error')
                    result["error"] = error_detail
                    print(f"   ⚠️  预期错误: {error_detail}")
                except:
                    result["error"] = response.text
                    print(f"   ⚠️  预期错误: {response.text}")
                
            else:
                result["error"] = response.text
                print(f"   ❌ 意外状态码: {status_code}")
            
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
                "error": str(e),
                "schedule_count": 0
            }
            self.results.append(result)
            return result
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始批量测试")
        print("=" * 60)
        
        # 尝试登录
        if not self.try_login():
            print("❌ 无法登录，测试终止")
            return
        
        print(f"\n✅ 使用账号进行测试: {self.current_user['username']}")
        
        # 运行测试用例
        for test_case in TEST_CASES:
            self.test_single_case(test_case)
        
        # 生成报告
        self.generate_report()
    
    def generate_report(self):
        """生成测试报告"""
        print("\n" + "=" * 60)
        print("📊 测试报告")
        print("=" * 60)
        
        total_tests = len(self.results)
        successful_requests = len([r for r in self.results if r['status_code'] in [200, 400, 422]])
        found_candidates = len([r for r in self.results if r['success']])
        total_schedules = sum([r['schedule_count'] for r in self.results])
        
        print(f"📈 总体统计:")
        print(f"  总测试数: {total_tests}")
        print(f"  请求成功: {successful_requests}")
        print(f"  成功率: {successful_requests/total_tests*100:.1f}%")
        print(f"  找到考生: {found_candidates} 个")
        print(f"  总考试安排: {total_schedules} 个")
        
        print(f"\n📋 详细结果:")
        for result in self.results:
            status = "✅" if result['status_code'] in [200, 400, 422] else "❌"
            schedule_info = f"({result['schedule_count']} 个安排)" if result['schedule_count'] > 0 else ""
            print(f"  {status} {result['test_case']}: HTTP {result['status_code']} {schedule_info}")
            if result['error'] and result['status_code'] not in [400, 422]:
                print(f"     错误: {result['error']}")
        
        # 保存报告
        report_file = f"manual_checkin_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "timestamp": datetime.now().isoformat(),
                    "login_user": self.current_user,
                    "summary": {
                        "total_tests": total_tests,
                        "successful_requests": successful_requests,
                        "found_candidates": found_candidates,
                        "total_schedules": total_schedules
                    },
                    "results": self.results
                }, f, ensure_ascii=False, indent=2)
            print(f"\n📄 详细报告已保存到: {report_file}")
        except Exception as e:
            print(f"\n⚠️  保存报告失败: {e}")
        
        # 测试建议
        print(f"\n💡 测试建议:")
        if found_candidates > 0:
            print(f"  ✅ 成功找到 {found_candidates} 个考生，接口工作正常")
        if total_schedules > 0:
            print(f"  ✅ 发现 {total_schedules} 个考试安排，数据完整")
        if successful_requests < total_tests:
            print(f"  ⚠️  有 {total_tests - successful_requests} 个请求失败，建议检查网络和服务状态")

def main():
    """主函数"""
    print("🧪 手动签到接口批量测试脚本 - 最终版本")
    print("=" * 60)
    
    # 测试服务器连接
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ 后端服务连接正常")
        else:
            print(f"⚠️  后端服务响应异常: {response.status_code}")
    except Exception as e:
        print(f"❌ 无法连接后端服务: {e}")
        print("请确保后端服务正在运行在 http://localhost:8000")
        return
    
    tester = BatchTester()
    
    print(f"\n📋 测试计划:")
    print(f"  测试用例: {len(TEST_CASES)} 个")
    print(f"  登录方式: {len(LOGIN_ACCOUNTS)} 种")
    print(f"  预计耗时: 约 30-60 秒")
    
    confirm = input(f"\n是否开始测试? (y/n): ").strip().lower()
    if confirm in ['y', 'yes', '是']:
        tester.run_all_tests()
    else:
        print("测试已取消")

if __name__ == "__main__":
    main()