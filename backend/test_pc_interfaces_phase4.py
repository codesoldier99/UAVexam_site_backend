#!/usr/bin/env python3
"""
PC端接口测试脚本 - 第四阶段
测试系统管理、报表分析、通知管理接口
"""

import requests
import json
from datetime import datetime

# 配置
BASE_URL = "http://localhost:8000/api/v1/pc"
LOGIN_URL = f"{BASE_URL}/auth/login"

# 测试账号
TEST_CREDENTIALS = {
    "username": "beijing_admin",
    "password": "123456"
}

class PCInterfacePhase4Tester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.test_results = []
    
    def log_result(self, test_name, success, status_code=None, response_data=None, error=None):
        """记录测试结果"""
        result = {
            "test_name": test_name,
            "success": success,
            "status_code": status_code,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "error": str(error) if error else None
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: 状态码: {status_code}")
        if error:
            print(f"    错误: {error}")
    
    def login(self):
        """登录获取token"""
        try:
            response = self.session.post(LOGIN_URL, json=TEST_CREDENTIALS)
            if response.status_code == 200:
                data = response.json()
                # PC端登录接口返回标准TokenResponse格式
                if "access_token" in data:
                    self.token = data["access_token"]
                    self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                    self.log_result("登录", True, response.status_code)
                    return True
                # 兼容其他格式
                elif data.get("success") and "access_token" in data.get("data", {}):
                    self.token = data["data"]["access_token"]
                    self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                    self.log_result("登录", True, response.status_code)
                    return True
            
            self.log_result("登录", False, response.status_code, error="登录失败")
            return False
        except Exception as e:
            self.log_result("登录", False, error=e)
            return False
    
    def test_system_overview(self):
        """测试系统概览"""
        try:
            response = self.session.get(f"{BASE_URL}/system/overview")
            success = response.status_code == 200
            self.log_result("系统概览", success, response.status_code)
        except Exception as e:
            self.log_result("系统概览", False, error=e)
    
    def test_system_logs(self):
        """测试系统日志"""
        try:
            response = self.session.get(f"{BASE_URL}/system/logs?page=1&size=10")
            success = response.status_code == 200
            self.log_result("系统日志", success, response.status_code)
        except Exception as e:
            self.log_result("系统日志", False, error=e)
    
    def test_system_backup(self):
        """测试数据备份"""
        try:
            response = self.session.post(f"{BASE_URL}/system/backup")
            success = response.status_code == 200
            self.log_result("数据备份", success, response.status_code)
        except Exception as e:
            self.log_result("数据备份", False, error=e)
    
    def test_system_config(self):
        """测试系统配置"""
        try:
            response = self.session.get(f"{BASE_URL}/system/config")
            success = response.status_code == 200
            self.log_result("系统配置", success, response.status_code)
        except Exception as e:
            self.log_result("系统配置", False, error=e)
    
    def test_checkin_trend(self):
        """测试签到趋势分析"""
        try:
            response = self.session.get(f"{BASE_URL}/reports/checkin-trend?days=7")
            success = response.status_code == 200
            self.log_result("签到趋势分析", success, response.status_code)
        except Exception as e:
            self.log_result("签到趋势分析", False, error=e)
    
    def test_venue_analysis(self):
        """测试考场分析报告"""
        try:
            response = self.session.get(f"{BASE_URL}/reports/venue-analysis")
            success = response.status_code == 200
            self.log_result("考场分析报告", success, response.status_code)
        except Exception as e:
            self.log_result("考场分析报告", False, error=e)
    
    def test_exam_statistics(self):
        """测试考试统计报告"""
        try:
            response = self.session.get(f"{BASE_URL}/reports/exam-statistics")
            success = response.status_code == 200
            self.log_result("考试统计报告", success, response.status_code)
        except Exception as e:
            self.log_result("考试统计报告", False, error=e)
    
    def test_export_report(self):
        """测试导出报表"""
        try:
            response = self.session.post(f"{BASE_URL}/reports/export?report_type=checkin&format=excel")
            success = response.status_code == 200
            self.log_result("导出报表", success, response.status_code)
        except Exception as e:
            self.log_result("导出报表", False, error=e)
    
    def test_notifications_list(self):
        """测试通知列表"""
        try:
            response = self.session.get(f"{BASE_URL}/notifications?page=1&size=10")
            success = response.status_code == 200
            self.log_result("通知列表", success, response.status_code)
        except Exception as e:
            self.log_result("通知列表", False, error=e)
    
    def test_create_notification(self):
        """测试创建通知"""
        try:
            notification_data = {
                "title": "测试通知",
                "content": "这是一条测试通知内容",
                "type": "SYSTEM",
                "target_users": "ALL"
            }
            response = self.session.post(f"{BASE_URL}/notifications", json=notification_data)
            success = response.status_code == 200
            self.log_result("创建通知", success, response.status_code)
            
            # 如果创建成功，返回通知ID用于后续测试
            if success:
                data = response.json()
                return data.get("data", {}).get("id", 1)
            return 1
        except Exception as e:
            self.log_result("创建通知", False, error=e)
            return 1
    
    def test_send_notification(self, notification_id):
        """测试发送通知"""
        try:
            response = self.session.post(f"{BASE_URL}/notifications/{notification_id}/send")
            success = response.status_code == 200
            self.log_result("发送通知", success, response.status_code)
        except Exception as e:
            self.log_result("发送通知", False, error=e)
    
    def test_notification_statistics(self):
        """测试通知统计"""
        try:
            response = self.session.get(f"{BASE_URL}/notifications/statistics")
            success = response.status_code == 200
            self.log_result("通知统计", success, response.status_code)
        except Exception as e:
            self.log_result("通知统计", False, error=e)
    
    def logout(self):
        """登出"""
        try:
            response = self.session.post(f"{BASE_URL}/auth/logout")
            success = response.status_code == 200
            self.log_result("登出", success, response.status_code)
        except Exception as e:
            self.log_result("登出", False, error=e)
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 60)
        print("🧪 PC端接口测试 - 第四阶段")
        print("测试范围: 系统管理、报表分析、通知管理")
        print("=" * 60)
        
        # 登录
        if not self.login():
            print("❌ 登录失败，终止测试")
            return
        
        # 系统管理接口测试
        print("\n📊 系统管理接口测试:")
        self.test_system_overview()
        self.test_system_logs()
        self.test_system_backup()
        self.test_system_config()
        
        # 报表分析接口测试
        print("\n📈 报表分析接口测试:")
        self.test_checkin_trend()
        self.test_venue_analysis()
        self.test_exam_statistics()
        self.test_export_report()
        
        # 通知管理接口测试
        print("\n📢 通知管理接口测试:")
        self.test_notifications_list()
        notification_id = self.test_create_notification()
        self.test_send_notification(notification_id)
        self.test_notification_statistics()
        
        # 登出
        self.logout()
        
        # 统计结果
        self.print_summary()
    
    def print_summary(self):
        """打印测试总结"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print("\n" + "=" * 60)
        print("📋 测试结果总结")
        print("=" * 60)
        print(f"总测试数: {total_tests}")
        print(f"通过: {passed_tests}")
        print(f"失败: {failed_tests}")
        print(f"成功率: {success_rate:.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ 失败的测试:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test_name']}: {result['error'] or f'状态码 {result['status_code']}'}")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    tester = PCInterfacePhase4Tester()
    tester.run_all_tests()