"""
手动签到接口批量测试脚本 - 基于真实数据库数据
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
TEST_PASSWORD = "admin123"

# 基于真实数据库的测试用例
TEST_CASES = [
    {
        "name": "张三-正常测试",
        "real_name": "张三",
        "id_card": "110101199001011234",
        "expected": "success",
        "description": "北京航空培训中心考生"
    },
    {
        "name": "李四-正常测试", 
        "real_name": "李四",
        "id_card": "110101199002022345",
        "expected": "success",
        "description": "北京航空培训中心考生"
    },
    {
        "name": "赵六-上海考生",
        "real_name": "赵六",
        "id_card": "310101199004044567",
        "expected": "success",
        "description": "上海无人机学院考生"
    },
    {
        "name": "孙八-深圳考生",
        "real_name": "孙八", 
        "id_card": "440301199006066789",
        "expected": "success",
        "description": "深圳飞行技术学校考生"
    },
    {
        "name": "不存在的考生",
        "real_name": "不存在的人",
        "id_card": "999999999999999999",
        "expected": "not_found",
        "description": "测试不存在的考生"
    },
    {
        "name": "姓名不匹配-张三身份证配李四姓名",
        "real_name": "李四",
        "id_card": "110101199001011234",  # 张三的身份证
        "expected": "mismatch",
        "description": "姓名与身份证不匹配"
    },
    {
        "name": "姓名不匹配-李四身份证配张三姓名",
        "real_name": "张三", 
        "id_card": "110101199002022345",  # 李四的身份证
        "expected": "mismatch",
        "description": "姓名与身份证不匹配"
    },
    {
        "name": "空姓名测试",
        "real_name": "",
        "id_card": "110101199001011234",
        "expected": "validation_error",
        "description": "测试空姓名验证"
    },
    {
        "name": "空身份证测试",
        "real_name": "张三",
        "id_card": "",
        "expected": "validation_error", 
        "description": "测试空身份证验证"
    },
    {
        "name": "无效身份证格式",
        "real_name": "张三",
        "id_card": "123456",
        "expected": "validation_error",
        "description": "测试无效身份证格式"
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
        print(f"   描述: {test_case['description']}")
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
                "description": test_case['description'],
                "status_code": status_code,
                "expected": test_case['expected'],
                "success": False,
                "response": None,
                "error": None,
                "candidate_count": 0,
                "schedule_count": 0
            }
            
            if status_code == 200:
                response_data = response.json()
                result["response"] = response_data
                result["success"] = True
                
                candidate_info = response_data.get('candidate_info', {})
                exam_schedules = response_data.get('exam_schedules', [])
                result["candidate_count"] = 1 if candidate_info else 0
                result["schedule_count"] = len(exam_schedules)
                
                print(f"   ✅ 状态码: {status_code}")
                print(f"   📋 考生信息: {candidate_info.get('real_name', 'N/A')} (ID: {candidate_info.get('id', 'N/A')})")
                print(f"   📅 考试安排: {len(exam_schedules)} 个")
                
                # 显示考试安排摘要
                if exam_schedules:
                    available_count = len([s for s in exam_schedules if s.get('can_checkin')])
                    print(f"   🎯 可签到安排: {available_count} 个")
                    
                    for i, schedule in enumerate(exam_schedules[:3], 1):  # 只显示前3个
                        print(f"     {i}. {schedule.get('exam_name')} - {schedule.get('checkin_status')}")
                    
                    if len(exam_schedules) > 3:
                        print(f"     ... 还有 {len(exam_schedules) - 3} 个安排")
                
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
                "description": test_case['description'],
                "status_code": None,
                "expected": test_case['expected'],
                "success": False,
                "response": None,
                "error": str(e),
                "candidate_count": 0,
                "schedule_count": 0
            }
            self.results.append(result)
            return result
    
    def test_permission_scenarios(self):
        """测试权限相关场景"""
        print(f"\n🔒 测试权限相关场景...")
        
        # 测试1: 无token访问
        print(f"\n   测试1: 无认证token访问")
        original_headers = dict(self.session.headers)
        self.session.headers.pop("Authorization", None)
        
        query_data = {
            "real_name": "张三",
            "id_card": "110101199001011234"
        }
        
        try:
            response = self.session.post(f"{API_BASE}/manual-checkin/query", json=query_data)
            print(f"     状态码: {response.status_code}")
            
            if response.status_code == 401:
                print("     ✅ 正确拒绝未认证请求")
            else:
                print(f"     ⚠️  意外状态码: {response.status_code}")
                print(f"     响应: {response.text}")
                
        except Exception as e:
            print(f"     ❌ 请求异常: {e}")
        finally:
            # 恢复headers
            self.session.headers = original_headers
        
        # 测试2: 无效token访问
        print(f"\n   测试2: 无效token访问")
        self.session.headers["Authorization"] = "Bearer invalid_token_12345"
        
        try:
            response = self.session.post(f"{API_BASE}/manual-checkin/query", json=query_data)
            print(f"     状态码: {response.status_code}")
            
            if response.status_code in [401, 403]:
                print("     ✅ 正确拒绝无效token")
            else:
                print(f"     ⚠️  意外状态码: {response.status_code}")
                
        except Exception as e:
            print(f"     ❌ 请求异常: {e}")
        finally:
            # 恢复正确的headers
            self.session.headers = original_headers
    
    def test_edge_cases(self):
        """测试边界情况"""
        print(f"\n🎯 测试边界情况...")
        
        edge_cases = [
            {
                "name": "超长姓名",
                "real_name": "张" * 50,
                "id_card": "110101199001011234"
            },
            {
                "name": "特殊字符姓名",
                "real_name": "张三@#$%",
                "id_card": "110101199001011234"
            },
            {
                "name": "数字姓名",
                "real_name": "123456",
                "id_card": "110101199001011234"
            },
            {
                "name": "超长身份证",
                "real_name": "张三",
                "id_card": "1" * 30
            }
        ]
        
        for case in edge_cases:
            print(f"\n   测试: {case['name']}")
            query_data = {
                "real_name": case['real_name'],
                "id_card": case['id_card']
            }
            
            try:
                response = self.session.post(f"{API_BASE}/manual-checkin/query", json=query_data)
                print(f"     状态码: {response.status_code}")
                
                if response.status_code in [400, 422]:
                    error_detail = response.json().get('detail', 'Unknown error')
                    print(f"     ✅ 正确处理边界情况: {error_detail}")
                elif response.status_code == 200:
                    print(f"     ⚠️  意外成功响应")
                else:
                    print(f"     ❓ 其他状态码: {response.status_code}")
                    
            except Exception as e:
                print(f"     ❌ 请求异常: {e}")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始批量测试")
        print("=" * 70)
        
        # 运行基础测试用例
        print("📋 基础功能测试")
        for test_case in TEST_CASES:
            self.test_single_case(test_case)
        
        # 运行权限测试
        print("\n" + "=" * 70)
        self.test_permission_scenarios()
        
        # 运行边界测试
        print("\n" + "=" * 70)
        self.test_edge_cases()
        
        # 生成测试报告
        self.generate_report()
    
    def generate_report(self):
        """生成测试报告"""
        print("\n" + "=" * 70)
        print("📊 测试报告")
        print("=" * 70)
        
        total_tests = len(self.results)
        successful_requests = len([r for r in self.results if r['status_code'] in [200, 400, 422]])
        failed_requests = len([r for r in self.results if r['status_code'] not in [200, 400, 422] or r['status_code'] is None])
        
        # 统计成功查询到考生的测试
        found_candidates = len([r for r in self.results if r['candidate_count'] > 0])
        total_schedules = sum([r['schedule_count'] for r in self.results])
        
        print(f"📈 总体统计:")
        print(f"  总测试数: {total_tests}")
        print(f"  请求成功: {successful_requests}")
        print(f"  请求失败: {failed_requests}")
        print(f"  成功率: {successful_requests/total_tests*100:.1f}%")
        print(f"  找到考生: {found_candidates} 个")
        print(f"  总考试安排: {total_schedules} 个")
        
        print(f"\n📋 详细结果:")
        
        # 按预期结果分组显示
        success_cases = [r for r in self.results if r['expected'] == 'success']
        error_cases = [r for r in self.results if r['expected'] != 'success']
        
        if success_cases:
            print(f"\n  ✅ 成功场景测试 ({len(success_cases)} 个):")
            for result in success_cases:
                status = "✅" if result['status_code'] == 200 else "❌"
                schedules_info = f"({result['schedule_count']} 个安排)" if result['schedule_count'] > 0 else ""
                print(f"    {status} {result['test_case']}: HTTP {result['status_code']} {schedules_info}")
                if result['error']:
                    print(f"       错误: {result['error']}")
        
        if error_cases:
            print(f"\n  ⚠️  异常场景测试 ({len(error_cases)} 个):")
            for result in error_cases:
                status = "✅" if result['status_code'] in [400, 422] else "❌"
                print(f"    {status} {result['test_case']}: HTTP {result['status_code']}")
                if result['error']:
                    print(f"       错误: {result['error']}")
        
        # 保存详细报告到文件
        report_file = f"manual_checkin_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_tests": total_tests,
                    "successful_requests": successful_requests,
                    "failed_requests": failed_requests,
                    "success_rate": successful_requests/total_tests*100,
                    "found_candidates": found_candidates,
                    "total_schedules": total_schedules
                },
                "results": self.results
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 详细报告已保存到: {report_file}")
        
        # 给出测试建议
        print(f"\n💡 测试建议:")
        if found_candidates > 0:
            print(f"  ✅ 成功找到 {found_candidates} 个考生，可以进行确认签到测试")
        if total_schedules > 0:
            print(f"  ✅ 发现 {total_schedules} 个考试安排，数据完整性良好")
        if failed_requests > 0:
            print(f"  ⚠️  有 {failed_requests} 个请求失败，建议检查网络连接和服务状态")

def main():
    """主函数"""
    print("🧪 手动签到接口批量测试脚本 (基于真实数据)")
    print("=" * 70)
    
    tester = BatchTester()
    
    # 登录
    if not tester.login():
        print("❌ 登录失败，无法继续测试")
        return
    
    print(f"\n📋 测试计划:")
    print(f"  基础功能测试: {len(TEST_CASES)} 个用例")
    print(f"  权限验证测试: 2 个场景")
    print(f"  边界条件测试: 4 个场景")
    print(f"  预计总耗时: 约 30-60 秒")
    
    confirm = input(f"\n是否开始测试? (y/n): ").strip().lower()
    if confirm in ['y', 'yes', '是']:
        # 运行所有测试
        tester.run_all_tests()
    else:
        print("测试已取消")

if __name__ == "__main__":
    main()