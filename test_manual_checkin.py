"""
手动签到接口测试脚本
使用方法：python test_manual_checkin.py
"""

import requests
import json
from datetime import datetime

# 配置
BASE_URL = "http://localhost:8000"  # 根据实际后端地址修改
API_BASE = f"{BASE_URL}/api/v1/wechat"

# 测试用户凭据 - 需要是考务人员角色
TEST_USERNAME = "admin"  # 超级管理员
TEST_PASSWORD = "admin123"  # 实际密码
"""
手动签到接口测试脚本
使用方法：python test_manual_checkin.py
"""

import requests
import json
from datetime import datetime

# 配置
BASE_URL = "http://localhost:8000"  # 根据实际后端地址修改
API_BASE = f"{BASE_URL}/api/v1/wechat"

"""
手动签到接口测试脚本
使用方法：python test_manual_checkin.py
"""

import requests
import json
from datetime import datetime

# 配置
BASE_URL = "http://localhost:8000"  # 根据实际后端地址修改
API_BASE = f"{BASE_URL}/api/v1/wechat"

# 测试用户凭据 - 需要是考务人员角色
TEST_USERNAME = "admin"  # 修改为实际的考务人员用户名
TEST_PASSWORD = "password"  # 修改为实际密码

class ManualCheckinTester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        
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
                print(f"❌ 登录失败: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ 登录异常: {e}")
            return False
    
    def test_query_candidate(self, real_name: str, id_card: str):
        """测试查询考生信息接口"""
        print(f"\n📋 测试查询考生信息...")
        print(f"   姓名: {real_name}")
        print(f"   身份证: {id_card}")
        
        query_data = {
            "real_name": real_name,
            "id_card": id_card
        }
        
        try:
            response = self.session.post(f"{API_BASE}/manual-checkin/query", json=query_data)
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ 查询成功")
                print(f"   考生信息: {json.dumps(result.get('candidate_info', {}), ensure_ascii=False, indent=2)}")
                print(f"   考试安排数量: {len(result.get('exam_schedules', []))}")
                
                # 显示考试安排详情
                for i, schedule in enumerate(result.get('exam_schedules', []), 1):
                    print(f"   考试安排 {i}:")
                    print(f"     - 日程ID: {schedule.get('schedule_id')}")
                    print(f"     - 考试名称: {schedule.get('exam_name')}")
                    print(f"     - 考场: {schedule.get('venue_name')}")
                    print(f"     - 时间: {schedule.get('exam_date')} {schedule.get('start_time')}-{schedule.get('end_time')}")
                    print(f"     - 可签到: {schedule.get('can_checkin')}")
                    print(f"     - 签到状态: {schedule.get('checkin_status')}")
                
                return result
            else:
                print(f"❌ 查询失败: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ 查询异常: {e}")
            return None
    
    def test_confirm_checkin(self, candidate_id: int, schedule_id: int, operator_info: str = None):
        """测试确认签到接口"""
        print(f"\n✅ 测试确认签到...")
        print(f"   考生ID: {candidate_id}")
        print(f"   日程ID: {schedule_id}")
        print(f"   操作员: {operator_info or '默认'}")
        
        confirm_data = {
            "candidate_id": candidate_id,
            "schedule_id": schedule_id
        }
        
        if operator_info:
            confirm_data["operator_info"] = operator_info
        
        try:
            response = self.session.post(f"{API_BASE}/manual-checkin/confirm", json=confirm_data)
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ 签到成功")
                print(f"   成功状态: {result.get('success')}")
                print(f"   消息: {result.get('message')}")
                print(f"   签到详情: {json.dumps(result.get('checkin_info', {}), ensure_ascii=False, indent=2)}")
                return result
            else:
                print(f"❌ 签到失败: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ 签到异常: {e}")
            return None
    
    def run_complete_test(self, real_name: str, id_card: str, operator_info: str = None):
        """运行完整的两步测试流程"""
        print("🚀 开始手动签到完整测试流程")
        print("=" * 50)
        
        # 第一步：查询考生信息
        query_result = self.test_query_candidate(real_name, id_card)
        if not query_result:
            print("❌ 查询失败，测试终止")
            return False
        
        # 获取考生ID和可签到的日程
        candidate_info = query_result.get('candidate_info', {})
        candidate_id = candidate_info.get('id')
        exam_schedules = query_result.get('exam_schedules', [])
        
        if not candidate_id:
            print("❌ 未获取到考生ID，测试终止")
            return False
        
        # 找到可签到的日程
        available_schedules = [s for s in exam_schedules if s.get('can_checkin')]
        if not available_schedules:
            print("❌ 没有可签到的考试安排，测试终止")
            return False
        
        # 选择第一个可签到的日程进行测试
        selected_schedule = available_schedules[0]
        schedule_id = selected_schedule.get('schedule_id')
        
        print(f"\n📌 选择签到的考试安排:")
        print(f"   考试: {selected_schedule.get('exam_name')}")
        print(f"   考场: {selected_schedule.get('venue_name')}")
        print(f"   时间: {selected_schedule.get('exam_date')} {selected_schedule.get('start_time')}")
        
        # 第二步：确认签到
        confirm_result = self.test_confirm_checkin(candidate_id, schedule_id, operator_info)
        if confirm_result:
            print("\n🎉 手动签到完整流程测试成功！")
            return True
        else:
            print("\n❌ 签到确认失败")
            return False

def main():
    """主测试函数"""
    print("🧪 手动签到接口测试脚本")
    print("=" * 50)
    
    tester = ManualCheckinTester()
    
    # 登录
    if not tester.login():
        print("❌ 登录失败，无法继续测试")
        return
    
    print("\n请选择测试模式:")
    print("1. 完整流程测试（推荐）")
    print("2. 仅测试查询接口")
    print("3. 仅测试确认接口（需要先知道candidate_id和schedule_id）")
    
    choice = input("请输入选择 (1-3): ").strip()
    
    if choice == "1":
        # 完整流程测试
        print("\n请输入考生信息:")
        real_name = input("考生姓名: ").strip()
        id_card = input("身份证号: ").strip()
        operator_info = input("操作员信息 (可选，直接回车跳过): ").strip() or None
        
        tester.run_complete_test(real_name, id_card, operator_info)
        
    elif choice == "2":
        # 仅测试查询
        print("\n请输入考生信息:")
        real_name = input("考生姓名: ").strip()
        id_card = input("身份证号: ").strip()
        
        tester.test_query_candidate(real_name, id_card)
        
    elif choice == "3":
        # 仅测试确认
        print("\n请输入签到信息:")
        try:
            candidate_id = int(input("考生ID: ").strip())
            schedule_id = int(input("日程ID: ").strip())
            operator_info = input("操作员信息 (可选，直接回车跳过): ").strip() or None
            
            tester.test_confirm_checkin(candidate_id, schedule_id, operator_info)
        except ValueError:
            print("❌ 请输入有效的数字ID")
    
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main()