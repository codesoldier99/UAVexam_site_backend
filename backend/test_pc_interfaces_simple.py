#!/usr/bin/env python3
"""
PC端接口简化测试脚本 - 只测试核心功能
"""

import requests
import json
from datetime import datetime

class SimplePCTest:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.pc_base_url = f"{base_url}/api/v1/pc"
        self.token = None
        
    def test_health(self):
        """测试服务器健康状态"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            print(f"✅ 健康检查: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ 健康检查失败: {e}")
            return False
    
    def test_pc_login(self):
        """测试PC端登录"""
        try:
            login_data = {
                "username": "beijing_admin",
                "password": "123456"
            }
            
            response = requests.post(
                f"{self.pc_base_url}/auth/login",
                json=login_data,
                timeout=10
            )
            
            print(f"✅ PC端登录: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                user = data.get("user", {})
                print(f"   用户: {user.get('full_name', 'Unknown')} ({user.get('role', 'Unknown')})")
                return True
            else:
                print(f"   错误: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ PC端登录失败: {e}")
            return False
    
    def test_pc_profile(self):
        """测试获取用户信息"""
        if not self.token:
            print("❌ 获取用户信息: 未登录")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(
                f"{self.pc_base_url}/auth/profile",
                headers=headers,
                timeout=10
            )
            
            print(f"✅ 获取用户信息: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   用户: {data.get('real_name', 'Unknown')} ({data.get('role', 'Unknown')})")
                return True
            else:
                print(f"   错误: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 获取用户信息失败: {e}")
            return False
    
    def test_pc_dashboard_activities(self):
        """测试系统活动日志"""
        if not self.token:
            print("❌ 系统活动日志: 未登录")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(
                f"{self.pc_base_url}/dashboard/activities",
                headers=headers,
                timeout=10
            )
            
            print(f"✅ 系统活动日志: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   活动数量: {len(data)}")
                return True
            else:
                print(f"   错误: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 系统活动日志失败: {e}")
            return False
    
    def test_pc_candidate_stats(self):
        """测试考生统计"""
        if not self.token:
            print("❌ 考生统计: 未登录")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(
                f"{self.pc_base_url}/candidates/statistics",
                headers=headers,
                timeout=10
            )
            
            print(f"✅ 考生统计: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   统计数据获取成功")
                return True
            else:
                print(f"   错误: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 考生统计失败: {e}")
            return False
    
    def test_pc_logout(self):
        """测试登出"""
        if not self.token:
            print("❌ 用户登出: 未登录")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(
                f"{self.pc_base_url}/auth/logout",
                headers=headers,
                timeout=10
            )
            
            print(f"✅ 用户登出: {response.status_code}")
            if response.status_code == 200:
                self.token = None
                return True
            else:
                print(f"   错误: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 用户登出失败: {e}")
            return False
    
    def run_tests(self):
        """运行所有测试"""
        print("🚀 PC端接口简化测试")
        print("=" * 40)
        
        tests = [
            ("服务器健康检查", self.test_health),
            ("PC端登录", self.test_pc_login),
            ("获取用户信息", self.test_pc_profile),
            ("系统活动日志", self.test_pc_dashboard_activities),
            ("考生统计", self.test_pc_candidate_stats),
            ("用户登出", self.test_pc_logout),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n📋 {test_name}:")
            if test_func():
                passed += 1
        
        print("\n" + "=" * 40)
        print(f"📊 测试结果: {passed}/{total} 通过")
        print(f"🎯 成功率: {(passed/total*100):.1f}%")
        
        if passed == total:
            print("🎉 所有核心功能测试通过！")
        else:
            print("⚠️  部分功能需要进一步调试")

def main():
    tester = SimplePCTest()
    tester.run_tests()

if __name__ == "__main__":
    main()