"""
测试新增的4个微信小程序API接口
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

class WeChatAPITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.candidate_token = None
    
    def test_candidate_info_by_idcard(self):
        """测试根据身份证获取考生信息"""
        print("\n🔍 测试接口1: 根据身份证获取考生信息")
        print("-" * 50)
        
        # 测试有效身份证号
        test_id_cards = [
            "110101199001011234",  # 张三的身份证
            "110101199002022345",  # 李四的身份证
            "999999999999999999",  # 无效身份证号
            "12345"                # 格式错误的身份证号
        ]
        
        for id_card in test_id_cards:
            try:
                url = f"{self.base_url}/wechat/candidate/info-by-idcard"
                params = {"id_card": id_card}
                
                response = self.session.get(url, params=params, timeout=10)
                
                print(f"身份证号: {id_card}")
                print(f"状态码: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        candidate_info = data.get("data", {})
                        print(f"✅ 考生姓名: {candidate_info.get('name')}")
                        print(f"✅ 机构: {candidate_info.get('institution', {}).get('name')}")
                        print(f"✅ 有待考试: {candidate_info.get('has_pending_exams')}")
                    else:
                        print(f"❌ 错误: {data.get('message')}")
                else:
                    error_data = response.json()
                    print(f"❌ 请求失败: {error_data}")
                
                print()
                
            except Exception as e:
                print(f"❌ 请求异常: {e}")
                print()
    
    def login_as_candidate(self, id_card="110101199001011234"):
        """以考生身份登录获取token"""
        try:
            url = f"{self.base_url}/wechat/login"
            data = {
                "id_card": id_card,
                "openid": "test_openid_123"
            }
            
            response = self.session.post(url, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                self.candidate_token = result.get("access_token")
                print(f"✅ 考生登录成功，获取token")
                return True
            else:
                print(f"❌ 考生登录失败: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 登录异常: {e}")
            return False
    
    def test_qrcode_refresh(self):
        """测试二维码刷新接口"""
        print("\n🔄 测试接口2: 二维码刷新")
        print("-" * 50)
        
        if not self.candidate_token:
            print("❌ 需要先登录获取token")
            return
        
        try:
            url = f"{self.base_url}/wechat/candidate/qrcode/refresh"
            headers = {"Authorization": f"Bearer {self.candidate_token}"}
            data = {
                "reason": "expired",
                "current_location": {
                    "latitude": 39.9042,
                    "longitude": 116.4074
                }
            }
            
            response = self.session.post(url, json=data, headers=headers, timeout=10)
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    qr_data = result.get("data", {})
                    print(f"✅ 二维码刷新成功")
                    print(f"✅ 过期时间: {qr_data.get('expires_at')}")
                    print(f"✅ 刷新次数: {qr_data.get('refresh_count')}")
                else:
                    print(f"❌ 刷新失败: {result.get('message')}")
            else:
                error_data = response.json()
                print(f"❌ 请求失败: {error_data}")
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")
    
    def test_checkin_history(self):
        """测试签到历史接口"""
        print("\n📋 测试接口3: 考生签到历史")
        print("-" * 50)
        
        if not self.candidate_token:
            print("❌ 需要先登录获取token")
            return
        
        try:
            url = f"{self.base_url}/wechat/candidate/checkin-history"
            headers = {"Authorization": f"Bearer {self.candidate_token}"}
            params = {
                "page": 1,
                "size": 10,
                "status": "all"
            }
            
            response = self.session.get(url, params=params, headers=headers, timeout=10)
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    data = result.get("data", {})
                    items = data.get("items", [])
                    stats = data.get("statistics", {})
                    
                    print(f"✅ 签到历史获取成功")
                    print(f"✅ 历史记录数: {len(items)}")
                    print(f"✅ 总签到次数: {stats.get('total_checkins')}")
                    print(f"✅ 成功签到: {stats.get('successful_checkins')}")
                    
                    if items:
                        print("最近签到记录:")
                        for item in items[:3]:  # 显示前3条
                            print(f"  - {item.get('checkin_time')} | {item.get('venue', {}).get('name')} | {item.get('status')}")
                else:
                    print(f"❌ 获取失败: {result.get('message')}")
            else:
                error_data = response.json()
                print(f"❌ 请求失败: {error_data}")
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")
    
    def test_exam_results(self):
        """测试考试结果接口"""
        print("\n🎯 测试接口4: 考生考试结果")
        print("-" * 50)
        
        if not self.candidate_token:
            print("❌ 需要先登录获取token")
            return
        
        try:
            url = f"{self.base_url}/wechat/candidate/exam-results"
            headers = {"Authorization": f"Bearer {self.candidate_token}"}
            params = {
                "page": 1,
                "size": 10,
                "status": "all"
            }
            
            response = self.session.get(url, params=params, headers=headers, timeout=10)
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    data = result.get("data", {})
                    items = data.get("items", [])
                    summary = data.get("summary", {})
                    
                    print(f"✅ 考试结果获取成功")
                    print(f"✅ 考试记录数: {len(items)}")
                    print(f"✅ 总考试次数: {summary.get('total_exams')}")
                    print(f"✅ 通过次数: {summary.get('passed_exams')}")
                    print(f"✅ 通过率: {summary.get('pass_rate')}%")
                    print(f"✅ 平均分: {summary.get('average_score')}")
                    
                    if items:
                        print("考试记录:")
                        for item in items[:3]:  # 显示前3条
                            exam_product = item.get('exam_product', {})
                            print(f"  - {item.get('exam_date')} | {exam_product.get('name')} | {item.get('result')} | 分数: {item.get('score')}")
                else:
                    print(f"✅ {result.get('message')}")  # "暂无考试结果"也是正常情况
            else:
                error_data = response.json()
                print(f"❌ 请求失败: {error_data}")
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始测试新增的4个微信小程序API接口")
        print("=" * 60)
        
        # 测试1: 根据身份证获取考生信息（公开接口）
        self.test_candidate_info_by_idcard()
        
        # 登录获取token
        print("\n🔑 考生登录获取认证token")
        print("-" * 50)
        if not self.login_as_candidate():
            print("❌ 无法获取认证token，跳过需要认证的接口测试")
            return
        
        # 测试2: 二维码刷新
        self.test_qrcode_refresh()
        
        # 测试3: 签到历史
        self.test_checkin_history()
        
        # 测试4: 考试结果
        self.test_exam_results()
        
        print("\n" + "=" * 60)
        print("🎉 所有接口测试完成")

if __name__ == "__main__":
    tester = WeChatAPITester()
    tester.run_all_tests()