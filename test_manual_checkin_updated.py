"""
手动签到接口测试脚本 - 基于真实数据库数据
使用方法：python test_manual_checkin_updated.py
"""

import requests
import json
from datetime import datetime
from typing import Optional

# 配置
BASE_URL = "http://localhost:8000"  # 根据实际后端地址修改
API_BASE = f"{BASE_URL}/api/v1/wechat"

# 测试用户凭据 - 基于真实数据库数据
TEST_ACCOUNTS = {
    "admin": {
        "username": "admin",
        "password": "admin123",
        "role": "超级管理员"
    },
    "beijing_admin": {
        "username": "beijing_admin", 
        "password": "123456",
        "role": "北京管理员"
    },
    "shanghai_admin": {
        "username": "shanghai_admin",
        "password": "123456", 
        "role": "上海管理员"
    },
    "shenzhen_admin": {
        "username": "shenzhen_admin",
        "password": "123456",
        "role": "深圳管理员"
    }
}

# 真实测试数据
TEST_CANDIDATES = {
    "张三": {
        "real_name": "张三",
        "id_card": "110101199001011234",
        "phone": "13800138001",
        "institution": "北京航空培训中心"
    },
    "李四": {
        "real_name": "李四", 
        "id_card": "110101199002022345",
        "phone": "13800138002",
        "institution": "北京航空培训中心"
    },
    "王五": {
        "real_name": "王五",
        "id_card": "110101199003033456", 
        "phone": "13800138003",
        "institution": "北京航空培训中心"
    },
    "赵六": {
        "real_name": "赵六",
        "id_card": "310101199004044567",
        "phone": "13800138004", 
        "institution": "上海无人机学院"
    },
    "钱七": {
        "real_name": "钱七",
        "id_card": "310101199005055678",
        "phone": "13800138005",
        "institution": "上海无人机学院"
    },
    "孙八": {
        "real_name": "孙八",
        "id_card": "440301199006066789",
        "phone": "13800138006",
        "institution": "深圳飞行技术学校"
    },
    "周九": {
        "real_name": "周九", 
        "id_card": "440301199007077890",
        "phone": "13800138007",
        "institution": "深圳飞行技术学校"
    },
    "吴十": {
        "real_name": "吴十",
        "id_card": "440301199008088901",
        "phone": "13800138008",
        "institution": "深圳飞行技术学校"
    }
}

class ManualCheckinTester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.current_user = None
        
    def login(self, account_key: str = "admin"):
        """登录获取token"""
        if account_key not in TEST_ACCOUNTS:
            print(f"❌ 无效的账号: {account_key}")
            return False
            
        account = TEST_ACCOUNTS[account_key]
        print(f"🔐 正在登录 {account['role']}...")
        
        login_data = {
            "username": account["username"],
            "password": account["password"]
        }
        
        try:
            response = self.session.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
            if response.status_code == 200:
                result = response.json()
                self.token = result.get("access_token")
                self.current_user = account
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                print(f"✅ 登录成功 - {account['role']}")
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
                
                candidate_info = result.get('candidate_info', {})
                print(f"   考生信息:")
                print(f"     - ID: {candidate_info.get('id')}")
                print(f"     - 姓名: {candidate_info.get('real_name')}")
                print(f"     - 身份证: {candidate_info.get('id_card')}")
                print(f"     - 电话: {candidate_info.get('phone')}")
                
                exam_schedules = result.get('exam_schedules', [])
                print(f"   考试安排数量: {len(exam_schedules)}")
                
                # 显示考试安排详情
                for i, schedule in enumerate(exam_schedules, 1):
                    print(f"   考试安排 {i}:")
                    print(f"     - 日程ID: {schedule.get('schedule_id')}")
                    print(f"     - 考试名称: {schedule.get('exam_name')}")
                    print(f"     - 考场: {schedule.get('venue_name')}")
                    print(f"     - 时间: {schedule.get('exam_date')} {schedule.get('start_time')}-{schedule.get('end_time')}")
                    print(f"     - 可签到: {schedule.get('can_checkin')}")
                    print(f"     - 签到状态: {schedule.get('checkin_status')}")
                
                return result
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {"detail": response.text}
                print(f"❌ 查询失败: {error_data.get('detail', 'Unknown error')}")
                return None
                
        except Exception as e:
            print(f"❌ 查询异常: {e}")
            return None
    
    def test_confirm_checkin(self, candidate_id: int, schedule_id: int, operator_info: Optional[str] = None):
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
                
                checkin_info = result.get('checkin_info', {})
                if checkin_info:
                    print(f"   签到详情:")
                    print(f"     - 签到ID: {checkin_info.get('checkin_id')}")
                    print(f"     - 签到时间: {checkin_info.get('checkin_time')}")
                    print(f"     - 签到方式: {checkin_info.get('method')}")
                    print(f"     - 操作员: {checkin_info.get('operator')}")
                
                return result
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {"detail": response.text}
                print(f"❌ 签到失败: {error_data.get('detail', 'Unknown error')}")
                return None
                
        except Exception as e:
            print(f"❌ 签到异常: {e}")
            return None
    
    def run_complete_test(self, real_name: str, id_card: str, operator_info: Optional[str] = None):
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
            print("   提示：可能的原因：")
            print("   - 不在签到时间窗口内")
            print("   - 考生已经签到过")
            print("   - 考试状态不允许签到")
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

def show_test_data():
    """显示可用的测试数据"""
    print("📊 可用的测试数据:")
    print("\n🔐 测试账号:")
    for key, account in TEST_ACCOUNTS.items():
        print(f"  {key}: {account['username']} / {account['password']} ({account['role']})")
    
    print("\n👥 测试考生:")
    for name, candidate in TEST_CANDIDATES.items():
        print(f"  {name}: {candidate['id_card']} ({candidate['institution']})")

def main():
    """主测试函数"""
    print("🧪 手动签到接口测试脚本 (基于真实数据)")
    print("=" * 60)
    
    # 显示测试数据
    show_test_data()
    
    tester = ManualCheckinTester()
    
    print("\n请选择登录账号:")
    print("1. admin (超级管理员)")
    print("2. beijing_admin (北京管理员)")
    print("3. shanghai_admin (上海管理员)")
    print("4. shenzhen_admin (深圳管理员)")
    
    account_choice = input("请输入选择 (1-4): ").strip()
    account_map = {
        "1": "admin",
        "2": "beijing_admin", 
        "3": "shanghai_admin",
        "4": "shenzhen_admin"
    }
    
    account_key = account_map.get(account_choice)
    if not account_key:
        print("❌ 无效选择")
        return
    
    # 登录
    if not tester.login(account_key):
        print("❌ 登录失败，无法继续测试")
        return
    
    print("\n请选择测试模式:")
    print("1. 完整流程测试（推荐）")
    print("2. 仅测试查询接口")
    print("3. 仅测试确认接口（需要先知道candidate_id和schedule_id）")
    print("4. 使用预设考生数据快速测试")
    
    choice = input("请输入选择 (1-4): ").strip()
    
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
    
    elif choice == "4":
        # 快速测试
        print("\n选择测试考生:")
        candidates = list(TEST_CANDIDATES.keys())
        for i, name in enumerate(candidates, 1):
            candidate = TEST_CANDIDATES[name]
            print(f"{i}. {name} ({candidate['institution']})")
        
        try:
            candidate_choice = int(input("请选择考生 (1-8): ").strip())
            if 1 <= candidate_choice <= len(candidates):
                selected_name = candidates[candidate_choice - 1]
                candidate = TEST_CANDIDATES[selected_name]
                
                operator_info = input("操作员信息 (可选，直接回车跳过): ").strip() or None
                
                tester.run_complete_test(
                    candidate['real_name'], 
                    candidate['id_card'], 
                    operator_info
                )
            else:
                print("❌ 无效选择")
        except ValueError:
            print("❌ 请输入有效的数字")
    
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main()