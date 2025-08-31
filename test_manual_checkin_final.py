"""
手动签到接口测试脚本 - 最终版本
包含多种登录方式和详细的错误处理
"""

import requests
import json
from datetime import datetime
from typing import Optional

# 配置
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1/wechat"

# 扩展的测试账号列表 - 包含多种可能的密码组合
TEST_ACCOUNTS = [
    # 超级管理员可能的密码组合
    {"key": "admin_1", "username": "admin", "password": "admin123", "role": "超级管理员"},
    {"key": "admin_2", "username": "admin", "password": "admin", "role": "超级管理员"},
    {"key": "admin_3", "username": "admin", "password": "123456", "role": "超级管理员"},
    {"key": "admin_4", "username": "admin", "password": "password", "role": "超级管理员"},
    
    # 机构管理员
    {"key": "beijing", "username": "beijing_admin", "password": "123456", "role": "北京管理员"},
    {"key": "shanghai", "username": "shanghai_admin", "password": "123456", "role": "上海管理员"},
    {"key": "shenzhen", "username": "shenzhen_admin", "password": "123456", "role": "深圳管理员"},
    
    # 考生账号（如果有考务权限）
    {"key": "candidate_1", "username": "candidate_011234", "password": "011234", "role": "考生"},
]

# 真实测试数据
TEST_CANDIDATES = {
    "张三": {"real_name": "张三", "id_card": "110101199001011234"},
    "李四": {"real_name": "李四", "id_card": "110101199002022345"},
    "王五": {"real_name": "王五", "id_card": "110101199003033456"},
    "赵六": {"real_name": "赵六", "id_card": "310101199004044567"},
    "钱七": {"real_name": "钱七", "id_card": "310101199005055678"},
    "孙八": {"real_name": "孙八", "id_card": "440301199006066789"},
    "周九": {"real_name": "周九", "id_card": "440301199007077890"},
    "吴十": {"real_name": "吴十", "id_card": "440301199008088901"},
}

class ManualCheckinTester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.current_user = None
        
    def test_server_connection(self):
        """测试服务器连接"""
        print("🌐 测试服务器连接...")
        try:
            response = self.session.get(f"{BASE_URL}/docs", timeout=5)
            if response.status_code == 200:
                print("✅ 后端服务连接正常")
                return True
            else:
                print(f"⚠️  后端服务响应异常: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 无法连接后端服务: {e}")
            print("请确保后端服务正在运行在 http://localhost:8000")
            return False
    
    def try_login_all_accounts(self):
        """尝试所有可能的账号登录"""
        print("🔐 尝试所有可能的登录组合...")
        print("=" * 60)
        
        for account in TEST_ACCOUNTS:
            print(f"\n🧪 测试: {account['username']} / {account['password']} ({account['role']})")
            
            login_data = {
                "username": account["username"],
                "password": account["password"]
            }
            
            try:
                response = self.session.post(f"{BASE_URL}/api/v1/auth/login", json=login_data, timeout=10)
                print(f"   状态码: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    self.token = result.get("access_token")
                    self.current_user = account
                    self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                    
                    print("   ✅ 登录成功!")
                    print(f"   Token: {self.token[:50] if self.token else 'N/A'}...")
                    
                    user_info = result.get("user_info", {})
                    if user_info:
                        print(f"   用户信息: {user_info.get('real_name', 'N/A')} ({user_info.get('role', 'N/A')})")
                    
                    return True
                else:
                    try:
                        error = response.json()
                        print(f"   ❌ 登录失败: {error.get('detail', 'Unknown error')}")
                    except:
                        print(f"   ❌ 登录失败: HTTP {response.status_code}")
                        
            except Exception as e:
                print(f"   ❌ 请求异常: {e}")
        
        print("\n❌ 所有登录组合都失败了")
        return False
    
    def test_query_candidate(self, real_name: str, id_card: str):
        """测试查询考生信息接口"""
        print(f"\n📋 测试查询考生信息...")
        print(f"   姓名: {real_name}")
        print(f"   身份证: {id_card}")
        
        if not self.token:
            print("   ❌ 未登录，无法测试")
            return None
        
        query_data = {
            "real_name": real_name,
            "id_card": id_card
        }
        
        try:
            response = self.session.post(f"{API_BASE}/manual-checkin/query", json=query_data, timeout=10)
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("   ✅ 查询成功")
                
                candidate_info = result.get('candidate_info', {})
                print(f"   考生信息:")
                print(f"     - ID: {candidate_info.get('id')}")
                print(f"     - 姓名: {candidate_info.get('real_name')}")
                print(f"     - 身份证: {candidate_info.get('id_card')}")
                
                exam_schedules = result.get('exam_schedules', [])
                print(f"   考试安排: {len(exam_schedules)} 个")
                
                for i, schedule in enumerate(exam_schedules, 1):
                    print(f"     {i}. {schedule.get('exam_name')} - {schedule.get('checkin_status')}")
                    print(f"        考场: {schedule.get('venue_name')}")
                    print(f"        时间: {schedule.get('exam_date')} {schedule.get('start_time')}")
                    print(f"        可签到: {schedule.get('can_checkin')}")
                
                return result
            else:
                try:
                    error = response.json()
                    print(f"   ❌ 查询失败: {error.get('detail', 'Unknown error')}")
                except:
                    print(f"   ❌ 查询失败: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ 查询异常: {e}")
            return None
    
    def test_confirm_checkin(self, candidate_id: int, schedule_id: int, operator_info: Optional[str] = None):
        """测试确认签到接口"""
        print(f"\n✅ 测试确认签到...")
        print(f"   考生ID: {candidate_id}")
        print(f"   日程ID: {schedule_id}")
        
        if not self.token:
            print("   ❌ 未登录，无法测试")
            return None
        
        confirm_data = {
            "candidate_id": candidate_id,
            "schedule_id": schedule_id
        }
        
        if operator_info:
            confirm_data["operator_info"] = operator_info
        
        try:
            response = self.session.post(f"{API_BASE}/manual-checkin/confirm", json=confirm_data, timeout=10)
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("   ✅ 签到成功")
                print(f"   消息: {result.get('message')}")
                
                checkin_info = result.get('checkin_info', {})
                if checkin_info:
                    print(f"   签到详情:")
                    for key, value in checkin_info.items():
                        print(f"     - {key}: {value}")
                
                return result
            else:
                try:
                    error = response.json()
                    print(f"   ❌ 签到失败: {error.get('detail', 'Unknown error')}")
                except:
                    print(f"   ❌ 签到失败: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ 签到异常: {e}")
            return None
    
    def run_complete_test(self, real_name: str, id_card: str):
        """运行完整测试流程"""
        print("🚀 开始手动签到完整测试流程")
        print("=" * 60)
        
        # 查询考生信息
        query_result = self.test_query_candidate(real_name, id_card)
        if not query_result:
            return False
        
        # 获取可签到的安排
        candidate_info = query_result.get('candidate_info', {})
        candidate_id = candidate_info.get('id')
        exam_schedules = query_result.get('exam_schedules', [])
        
        if not candidate_id:
            print("❌ 未获取到考生ID")
            return False
        
        available_schedules = [s for s in exam_schedules if s.get('can_checkin')]
        if not available_schedules:
            print("❌ 没有可签到的考试安排")
            print("   可能原因:")
            print("   - 不在签到时间窗口内")
            print("   - 考生已经签到过")
            print("   - 考试状态不允许签到")
            return False
        
        # 选择第一个可签到的安排
        selected_schedule = available_schedules[0]
        schedule_id = selected_schedule.get('schedule_id')
        
        print(f"\n📌 选择的考试安排:")
        print(f"   考试: {selected_schedule.get('exam_name')}")
        print(f"   考场: {selected_schedule.get('venue_name')}")
        print(f"   时间: {selected_schedule.get('exam_date')} {selected_schedule.get('start_time')}")
        
        # 确认签到
        operator_info = f"测试操作员({self.current_user['role']})" if self.current_user else None
        confirm_result = self.test_confirm_checkin(candidate_id, schedule_id, operator_info)
        
        if confirm_result:
            print("\n🎉 手动签到完整流程测试成功！")
            return True
        else:
            print("\n❌ 签到确认失败")
            return False

def show_manual_solution():
    """显示手动解决方案"""
    print("\n" + "=" * 60)
    print("💡 手动解决方案")
    print("=" * 60)
    print("如果所有自动登录都失败，请尝试以下步骤:")
    print()
    print("1. 检查后端服务状态:")
    print("   cd backend")
    print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    print()
    print("2. 重新初始化数据库:")
    print("   cd backend")
    print("   python init_test_data.py")
    print()
    print("3. 手动重置admin密码:")
    print("   - 进入数据库管理工具")
    print("   - 找到users表中的admin用户")
    print("   - 更新password_hash字段")
    print()
    print("4. 检查数据库连接配置:")
    print("   - 确认backend/app/config/database.py中的数据库配置")
    print("   - 确认数据库服务正在运行")
    print()
    print("5. 查看后端日志:")
    print("   - 检查控制台输出的详细错误信息")
    print("   - 查看是否有数据库连接或其他错误")

def main():
    """主函数"""
    print("🧪 手动签到接口测试脚本 - 最终版本")
    print("=" * 60)
    
    tester = ManualCheckinTester()
    
    # 测试服务器连接
    if not tester.test_server_connection():
        show_manual_solution()
        return
    
    # 尝试登录
    if not tester.try_login_all_accounts():
        print("\n❌ 所有登录尝试都失败了")
        show_manual_solution()
        return
    
    print(f"\n🎉 成功登录: {tester.current_user['username']} ({tester.current_user['role']})")
    
    # 选择测试模式
    print("\n请选择测试模式:")
    print("1. 快速测试 - 使用张三的数据")
    print("2. 选择考生测试")
    print("3. 手动输入考生信息")
    print("4. 仅测试查询接口")
    
    choice = input("请输入选择 (1-4): ").strip()
    
    if choice == "1":
        # 快速测试
        candidate = TEST_CANDIDATES["张三"]
        tester.run_complete_test(candidate['real_name'], candidate['id_card'])
        
    elif choice == "2":
        # 选择考生测试
        print("\n选择测试考生:")
        candidates = list(TEST_CANDIDATES.keys())
        for i, name in enumerate(candidates, 1):
            candidate = TEST_CANDIDATES[name]
            print(f"{i}. {name} ({candidate['id_card']})")
        
        try:
            candidate_choice = int(input("请选择考生 (1-8): ").strip())
            if 1 <= candidate_choice <= len(candidates):
                selected_name = candidates[candidate_choice - 1]
                candidate = TEST_CANDIDATES[selected_name]
                tester.run_complete_test(candidate['real_name'], candidate['id_card'])
            else:
                print("❌ 无效选择")
        except ValueError:
            print("❌ 请输入有效的数字")
    
    elif choice == "3":
        # 手动输入
        real_name = input("请输入考生姓名: ").strip()
        id_card = input("请输入身份证号: ").strip()
        
        if real_name and id_card:
            tester.run_complete_test(real_name, id_card)
        else:
            print("❌ 姓名和身份证号不能为空")
    
    elif choice == "4":
        # 仅测试查询
        candidate = TEST_CANDIDATES["张三"]
        tester.test_query_candidate(candidate['real_name'], candidate['id_card'])
    
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main()