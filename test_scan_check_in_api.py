#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扫码签到API测试脚本
"""

import requests
import json
import time
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"
ADMIN_EMAIL = "admin@exam.com"
ADMIN_PASSWORD = "admin123"

class ScanCheckInTester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.test_schedule_id = None
    
    def login(self):
        """登录获取token"""
        login_data = {
            "username": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        }
        
        response = self.session.post(
            f"{BASE_URL}/auth/jwt/login",
            data=login_data
        )
        
        if response.status_code == 200:
            result = response.json()
            self.token = result.get("access_token")
            self.session.headers.update({
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            })
            print("✅ 登录成功")
            return True
        else:
            print(f"❌ 登录失败: {response.status_code}")
            return False
    
    def find_existing_schedule(self):
        """查找现有的排期用于测试"""
        print("🔍 查找现有排期...")
        
        # 获取排期列表
        response = self.session.get(f"{BASE_URL}/schedules?page=1&size=10")
        if response.status_code == 200:
            result = response.json()
            schedules = result.get("items", [])
            if schedules:
                self.test_schedule_id = schedules[0]["id"]
                print(f"✅ 找到排期: {self.test_schedule_id}")
                return True
        
        print("❌ 没有找到可用的排期")
        return False
    
    def create_test_schedule_simple(self):
        """使用简化的方法创建测试排期"""
        print("🔍 尝试创建测试排期...")
        
        # 先查找现有考生
        response = self.session.get(f"{BASE_URL}/candidates?page=1&size=5")
        if response.status_code != 200:
            print("❌ 无法获取考生列表")
            return False
        
        candidates = response.json().get("items", [])
        if not candidates:
            print("❌ 没有找到考生")
            return False
        
        candidate_id = candidates[0]["id"]
        print(f"✅ 使用考生ID: {candidate_id}")
        
        # 创建排期
        schedule_data = {
            "candidate_id": candidate_id,
            "exam_product_id": 1,
            "schedule_type": "理论考试",
            "scheduled_date": datetime.now().date().isoformat(),
            "start_time": (datetime.now() + timedelta(hours=1)).isoformat(),
            "end_time": (datetime.now() + timedelta(hours=2)).isoformat(),
            "venue_id": 1
        }
        
        response = self.session.post(f"{BASE_URL}/schedules", json=schedule_data)
        if response.status_code == 201:
            self.test_schedule_id = response.json()["id"]
            print(f"✅ 创建测试排期成功: {self.test_schedule_id}")
            return True
        else:
            print(f"❌ 创建排期失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
    
    def generate_qr_code(self, schedule_id):
        """生成测试二维码"""
        import hashlib
        timestamp = int(time.time())
        content = f"SCHEDULE_{schedule_id}_{timestamp}"
        hash_value = hashlib.md5(content.encode()).hexdigest()[:8]
        return f"{content}_{hash_value}"
    
    def test_scan_check_in(self):
        """测试扫码签到"""
        print("\n🔍 测试扫码签到...")
        
        if not self.test_schedule_id:
            print("❌ 没有可用的排期ID")
            return False
        
        qr_code = self.generate_qr_code(self.test_schedule_id)
        print(f"📱 二维码: {qr_code}")
        
        check_in_data = {
            "qr_code": qr_code,
            "check_in_time": datetime.now().isoformat(),
            "notes": "测试扫码签到"
        }
        
        response = self.session.post(
            f"{BASE_URL}/schedules/scan-check-in",
            json=check_in_data
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 扫码签到成功")
            print(f"   考生: {result['data']['candidate_name']}")
            print(f"   状态: {result['data']['check_in_status']}")
            return True
        else:
            print(f"❌ 扫码签到失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
    
    def test_batch_check_in(self):
        """测试批量签到"""
        print("\n🔍 测试批量签到...")
        
        # 创建多个排期
        qr_codes = []
        for i in range(2):
            # 获取考生列表
            response = self.session.get(f"{BASE_URL}/candidates?page=1&size=5")
            if response.status_code != 200:
                continue
            
            candidates = response.json().get("items", [])
            if not candidates:
                continue
            
            candidate_id = candidates[i % len(candidates)]["id"]
            
            schedule_data = {
                "candidate_id": candidate_id,
                "exam_product_id": 1,
                "schedule_type": "理论考试",
                "scheduled_date": datetime.now().date().isoformat(),
                "start_time": (datetime.now() + timedelta(hours=i+1)).isoformat(),
                "end_time": (datetime.now() + timedelta(hours=i+2)).isoformat(),
                "venue_id": 1
            }
            
            response = self.session.post(f"{BASE_URL}/schedules", json=schedule_data)
            if response.status_code == 201:
                schedule_id = response.json()["id"]
                qr_code = self.generate_qr_code(schedule_id)
                qr_codes.append(qr_code)
        
        if not qr_codes:
            print("❌ 无法创建测试排期")
            return False
        
        # 批量签到
        batch_data = {
            "qr_codes": qr_codes,
            "check_in_time": datetime.now().isoformat()
        }
        
        response = self.session.post(
            f"{BASE_URL}/schedules/batch-scan-check-in",
            json=batch_data
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 批量签到成功: {result['summary']['success_count']}/{result['summary']['total']}")
            return True
        else:
            print(f"❌ 批量签到失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
    
    def test_stats(self):
        """测试统计功能"""
        print("\n🔍 测试签到统计...")
        
        response = self.session.get(f"{BASE_URL}/schedules/check-in-stats")
        
        if response.status_code == 200:
            result = response.json()
            stats = result['data']
            print(f"✅ 统计获取成功")
            print(f"   总排期: {stats['total_schedules']}")
            print(f"   已签到: {stats['checked_in_count']}")
            print(f"   签到率: {stats['check_in_rate']}%")
            return True
        else:
            print(f"❌ 统计获取失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
    
    def run_tests(self):
        """运行所有测试"""
        print("🚀 开始扫码签到API测试")
        
        if not self.login():
            return False
        
        # 尝试查找现有排期或创建新排期
        if not self.find_existing_schedule():
            if not self.create_test_schedule_simple():
                print("❌ 无法创建测试数据")
                return False
        
        tests = [
            ("单个扫码签到", self.test_scan_check_in),
            ("批量扫码签到", self.test_batch_check_in),
            ("签到统计", self.test_stats)
        ]
        
        passed = 0
        for name, test in tests:
            print(f"\n📋 测试: {name}")
            if test():
                passed += 1
        
        print(f"\n📊 测试结果: {passed}/{len(tests)} 通过")
        return passed == len(tests)

if __name__ == "__main__":
    tester = ScanCheckInTester()
    success = tester.run_tests()
    
    if success:
        print("🎉 扫码签到API测试通过！")
    else:
        print("❌ 扫码签到API测试失败") 