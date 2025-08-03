#!/usr/bin/env python3
"""
考试系统后端API完整功能测试
测试本地API的所有主要接口，模拟实际使用场景
"""

import requests
import json
import time
from datetime import datetime
import sys

# 配置
BASE_URL = "http://localhost:8000"  # 本地测试
# BASE_URL = "http://106.52.214.54"  # 云服务器测试 (部署后使用)

class APITester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
    def test_api(self, name, method, endpoint, data=None, params=None):
        """测试API接口的通用方法"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            print(f"\n🧪 测试: {name}")
            print(f"   📍 {method} {url}")
            
            start_time = time.time()
            
            if method.upper() == 'GET':
                response = self.session.get(url, params=params, timeout=10)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, params=params, timeout=10)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, params=params, timeout=10)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, timeout=10)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")
            
            elapsed_time = time.time() - start_time
            
            # 记录结果
            result = {
                'name': name,
                'method': method,
                'endpoint': endpoint,
                'status_code': response.status_code,
                'response_time': f"{elapsed_time:.3f}s",
                'success': 200 <= response.status_code < 300
            }
            
            if result['success']:
                print(f"   ✅ 成功 - 状态码: {response.status_code}, 响应时间: {result['response_time']}")
                try:
                    response_data = response.json()
                    if 'message' in response_data:
                        print(f"   📝 消息: {response_data['message']}")
                    if 'data' in response_data and isinstance(response_data['data'], list):
                        print(f"   📊 数据量: {len(response_data['data'])} 条")
                    elif 'data' in response_data:
                        print(f"   📄 返回数据: {type(response_data['data']).__name__}")
                except:
                    print(f"   📄 响应长度: {len(response.text)} 字符")
            else:
                print(f"   ❌ 失败 - 状态码: {response.status_code}")
                print(f"   📄 错误信息: {response.text[:200]}...")
            
            self.test_results.append(result)
            return response
            
        except requests.exceptions.Timeout:
            print(f"   ⏰ 超时 - 请求超过10秒")
            self.test_results.append({
                'name': name,
                'method': method,
                'endpoint': endpoint,
                'status_code': 'TIMEOUT',
                'response_time': '>10s',
                'success': False
            })
            return None
            
        except requests.exceptions.ConnectionError:
            print(f"   🔌 连接失败 - 服务器可能未运行")
            self.test_results.append({
                'name': name,
                'method': method,
                'endpoint': endpoint,
                'status_code': 'CONNECTION_ERROR',
                'response_time': 'N/A',
                'success': False
            })
            return None
            
        except Exception as e:
            print(f"   💥 异常 - {str(e)}")
            self.test_results.append({
                'name': name,
                'method': method,
                'endpoint': endpoint,
                'status_code': 'ERROR',
                'response_time': 'N/A',
                'success': False
            })
            return None

    def run_basic_tests(self):
        """运行基础功能测试"""
        print("=" * 60)
        print("🚀 开始基础功能测试")
        print("=" * 60)
        
        # 1. 系统基础接口
        self.test_api("系统欢迎页面", "GET", "/")
        self.test_api("健康检查", "GET", "/health")
        self.test_api("测试接口", "GET", "/test")
        
        # 2. 机构管理
        self.test_api("获取机构列表", "GET", "/institutions")
        self.test_api("获取机构列表(分页)", "GET", "/institutions", params={"page": 1, "size": 5})
        self.test_api("获取机构详情", "GET", "/institutions/1")
        
        # 3. 用户管理
        self.test_api("获取用户列表", "GET", "/users")
        self.test_api("用户角色筛选", "GET", "/users", params={"role": "admin"})
        self.test_api("获取用户详情", "GET", "/users/1")
        
        # 4. 考生管理
        self.test_api("获取考生列表", "GET", "/candidates")
        self.test_api("考生状态筛选", "GET", "/candidates", params={"status": "待排期"})
        self.test_api("获取考生详情", "GET", "/candidates/1")
        
        # 5. 考试产品
        self.test_api("获取考试产品列表", "GET", "/exam-products")
        self.test_api("产品类别筛选", "GET", "/exam-products", params={"category": "理论+实操"})
        self.test_api("获取考试产品详情", "GET", "/exam-products/1")
        
        # 6. 场地管理
        self.test_api("获取场地列表", "GET", "/venues")
        
        # 7. 排期管理
        self.test_api("获取排期列表", "GET", "/schedules")

    def run_advanced_tests(self):
        """运行高级功能测试"""
        print("\n" + "=" * 60)
        print("🔧 开始高级功能测试")
        print("=" * 60)
        
        # 1. 二维码和签到功能
        self.test_api("二维码模块健康检查", "GET", "/qrcode/health")
        self.test_api("生成考试二维码", "GET", "/qrcode/generate-schedule-qr/1")
        self.test_api("扫码签到测试", "POST", "/qrcode/scan-checkin", 
                     params={"qr_content": "schedule_1_candidate_1"})
        
        # 2. 批量操作功能
        self.test_api("下载考生导入模板", "GET", "/batch/candidates/template")
        self.test_api("批量导出考生数据", "GET", "/batch/export/candidates")
        
        # 3. 微信小程序接口
        self.test_api("小程序健康检查", "GET", "/wx-miniprogram/health")
        self.test_api("考生信息查询", "GET", "/wx-miniprogram/candidate-info", 
                     params={"id_number": "110101199001011234"})
        
        # 4. 权限管理
        self.test_api("获取角色列表", "GET", "/roles")
        self.test_api("获取权限列表", "GET", "/permissions")
        
        # 5. 实时功能
        self.test_api("实时状态查询", "GET", "/realtime/status")

    def run_data_operations_tests(self):
        """运行数据操作测试"""
        print("\n" + "=" * 60)
        print("📊 开始数据操作测试")
        print("=" * 60)
        
        # 测试创建操作 (如果API支持的话)
        # 注意: 这些是简化版测试API，可能不支持真实的数据创建
        
        # 1. 创建机构
        new_institution = {
            "name": "测试培训机构",
            "contact_person": "测试联系人", 
            "phone": "13800000000"
        }
        self.test_api("创建新机构", "POST", "/institutions", data=new_institution)
        
        # 2. 测试搜索功能
        self.test_api("机构搜索", "GET", "/institutions", params={"search": "北京"})
        self.test_api("用户状态筛选", "GET", "/users", params={"status": "active"})
        self.test_api("考生性别筛选", "GET", "/candidates", params={"gender": "男"})

    def generate_report(self):
        """生成测试报告"""
        print("\n" + "=" * 60)
        print("📊 测试报告")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - successful_tests
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📋 总测试数: {total_tests}")
        print(f"✅ 成功数: {successful_tests}")
        print(f"❌ 失败数: {failed_tests}")
        print(f"📈 成功率: {success_rate:.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ 失败的测试:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   - {result['name']}: {result['status_code']}")
        
        # 保存详细报告
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'base_url': self.base_url,
            'summary': {
                'total_tests': total_tests,
                'successful_tests': successful_tests,
                'failed_tests': failed_tests,
                'success_rate': success_rate
            },
            'test_results': self.test_results
        }
        
        report_file = f"api_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 详细报告已保存: {report_file}")

def main():
    """主函数"""
    print("🎯 考试系统后端API完整功能测试")
    print(f"📅 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 测试地址: {BASE_URL}")
    
    tester = APITester(BASE_URL)
    
    try:
        # 运行所有测试
        tester.run_basic_tests()
        tester.run_advanced_tests()
        tester.run_data_operations_tests()
        
        # 生成报告
        tester.generate_report()
        
        print(f"\n🎉 测试完成!")
        
    except KeyboardInterrupt:
        print(f"\n⏹️ 测试被用户中断")
        tester.generate_report()
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 测试过程中发生错误: {e}")
        tester.generate_report()
        sys.exit(1)

if __name__ == "__main__":
    main()