#!/usr/bin/env python3
"""
本地端到端测试脚本
用于测试运行在Docker容器中的UAV考试系统API
在本地Windows机器上运行此脚本，访问Docker容器中的服务
"""

import requests
import json
import time
from datetime import datetime, timedelta

# API基础URL - 从本地访问Docker容器
BASE_URL = "http://localhost:8000/api/v1"

class UAVExamTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.tokens = {}
        
    def log(self, message):
        """打印带时间戳的日志"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        
    def test_api_health(self):
        """测试API健康状态"""
        self.log("🔍 测试API健康状态")
        
        try:
            response = self.session.get(f"{self.base_url.replace('/api/v1', '')}/health")
            if response.status_code == 200:
                self.log("✅ API服务正常运行")
                return True
            else:
                self.log(f"❌ API健康检查失败: {response.status_code}")
                return False
        except Exception as e:
            self.log(f"❌ 无法连接到API服务: {str(e)}")
            self.log("   请确认Docker容器正在运行且端口8000已映射")
            return False
        
    def test_institution_user_login(self):
        """测试机构用户登录"""
        self.log("🔍 测试机构用户登录")
        
        login_data = {
            "username": "institution_user",
            "password": "123456"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/auth/login",
                json=login_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.tokens['institution'] = data['access_token']
                user_info = data['user']
                self.log(f"✅ 机构用户登录成功")
                self.log(f"   用户名: {user_info['username']}")
                self.log(f"   角色: {user_info['role']}")
                self.log(f"   机构ID: {user_info.get('institution_id', 'N/A')}")
                return True
            else:
                self.log(f"❌ 机构用户登录失败: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            self.log(f"❌ 机构用户登录异常: {str(e)}")
            return False

    def run_all_tests(self):
        """运行所有测试"""
        self.log("🚀 开始本地端到端测试（测试Docker容器中的API）")
        self.log("="*60)
        
        tests = [
            ("API健康检查", self.test_api_health),
            ("机构用户登录", self.test_institution_user_login),
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            self.log(f"\n{'='*60}")
            try:
                if test_func():
                    passed += 1
                    self.log(f"✅ {test_name} - 通过")
                else:
                    failed += 1
                    self.log(f"❌ {test_name} - 失败")
                    # 如果API健康检查失败，就不继续其他测试了
                    if test_name == "API健康检查":
                        self.log("⚠️  API服务不可用，停止后续测试")
                        break
            except Exception as e:
                failed += 1
                self.log(f"❌ {test_name} - 异常: {str(e)}")
            
            time.sleep(1)  # 避免请求过快
        
        self.log(f"\n{'='*60}")
        self.log(f"🏁 测试完成")
        self.log(f"   通过: {passed}")
        self.log(f"   失败: {failed}")
        self.log(f"   总计: {passed + failed}")
        
        if failed == 0:
            self.log("🎉 所有测试都通过了！")
        else:
            self.log(f"⚠️  有 {failed} 个测试失败")

if __name__ == "__main__":
    print("="*60)
    print("UAV考试系统 - 本地端到端测试")
    print("测试目标: Docker容器中的API服务")
    print("运行环境: Windows本地")
    print("="*60)
    
    tester = UAVExamTester()
    tester.run_all_tests()
