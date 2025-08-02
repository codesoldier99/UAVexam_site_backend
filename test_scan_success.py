#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
成功的扫码签到测试
"""

import requests
import json
import time
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"
ADMIN_EMAIL = "admin@exam.com"
ADMIN_PASSWORD = "admin123"

def login():
    """登录获取token"""
    session = requests.Session()
    
    login_data = {
        "username": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }
    
    response = session.post(
        f"{BASE_URL}/auth/jwt/login",
        data=login_data
    )
    
    if response.status_code == 200:
        result = response.json()
        token = result.get("access_token")
        session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })
        print("✅ 登录成功")
        return session
    else:
        print(f"❌ 登录失败: {response.status_code}")
        return None

def generate_qr_code(schedule_id):
    """生成测试二维码"""
    import hashlib
    timestamp = int(time.time())
    content = f"SCHEDULE_{schedule_id}_{timestamp}"
    hash_value = hashlib.md5(content.encode()).hexdigest()[:8]
    return f"{content}_{hash_value}"

def test_scan_check_in():
    """测试扫码签到"""
    print("🚀 开始扫码签到API测试")
    
    # 登录
    session = login()
    if not session:
        return False
    
    # 获取现有排期
    response = session.get(f"{BASE_URL}/schedules")
    if response.status_code != 200:
        print("❌ 获取排期失败")
        return False
    
    schedules = response.json()
    if not schedules.get("items"):
        print("❌ 没有找到排期数据")
        return False
    
    # 找到未签到的排期
    available_schedule = None
    for schedule in schedules["items"]:
        if schedule.get("check_in_status") == "未签到":
            available_schedule = schedule
            break
    
    if not available_schedule:
        print("❌ 没有找到未签到的排期")
        return False
    
    schedule_id = available_schedule["id"]
    print(f"📋 使用排期ID: {schedule_id}")
    print(f"📋 考生: {available_schedule.get('candidate_name', '未知')}")
    
    # 生成二维码
    qr_code = generate_qr_code(schedule_id)
    print(f"📱 生成二维码: {qr_code}")
    
    # 测试扫码签到
    check_in_data = {
        "qr_code": qr_code,
        "check_in_time": datetime.now().isoformat(),
        "notes": "测试扫码签到"
    }
    
    response = session.post(
        f"{BASE_URL}/schedules/scan-check-in",
        json=check_in_data
    )
    
    print(f"📊 响应状态: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ 扫码签到成功")
        print(f"   考生: {result['data']['candidate_name']}")
        print(f"   考试: {result['data']['exam_product_name']}")
        print(f"   状态: {result['data']['check_in_status']}")
        print(f"   是否迟到: {result['data']['is_late']}")
        print(f"   签到时间: {result['data']['check_in_time']}")
        return True
    else:
        print(f"❌ 扫码签到失败: {response.status_code}")
        print(f"📄 响应内容: {response.text}")
        return False

def test_batch_check_in():
    """测试批量签到"""
    print("\n🔍 测试批量签到...")
    
    session = login()
    if not session:
        return False
    
    # 获取多个未签到的排期
    response = session.get(f"{BASE_URL}/schedules")
    if response.status_code != 200:
        return False
    
    schedules = response.json()
    available_schedules = []
    
    for schedule in schedules["items"]:
        if schedule.get("check_in_status") == "未签到" and len(available_schedules) < 2:
            available_schedules.append(schedule)
    
    if len(available_schedules) < 2:
        print("❌ 没有足够的未签到排期进行批量测试")
        return False
    
    # 生成二维码列表
    qr_codes = []
    for schedule in available_schedules:
        qr_code = generate_qr_code(schedule["id"])
        qr_codes.append(qr_code)
        print(f"📱 排期 {schedule['id']}: {qr_code}")
    
    # 批量签到
    batch_data = {
        "qr_codes": qr_codes,
        "check_in_time": datetime.now().isoformat(),
        "notes": "批量签到测试"
    }
    
    response = session.post(
        f"{BASE_URL}/schedules/batch-scan-check-in",
        json=batch_data
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ 批量签到成功")
        print(f"   总数: {result['summary']['total']}")
        print(f"   成功: {result['summary']['success_count']}")
        print(f"   失败: {result['summary']['error_count']}")
        return True
    else:
        print(f"❌ 批量签到失败: {response.status_code}")
        return False

def test_stats():
    """测试统计功能"""
    print("\n🔍 测试签到统计...")
    
    session = login()
    if not session:
        return False
    
    response = session.get(f"{BASE_URL}/schedules/check-in-stats")
    
    if response.status_code == 200:
        result = response.json()
        stats = result['data']
        print(f"✅ 统计获取成功")
        print(f"   总排期: {stats['total_schedules']}")
        print(f"   已签到: {stats['checked_in_count']}")
        print(f"   迟到: {stats['late_count']}")
        print(f"   未签到: {stats['not_checked_in_count']}")
        print(f"   签到率: {stats['check_in_rate']}%")
        
        today_stats = stats.get('today_stats', {})
        if today_stats:
            print(f"   今日统计:")
            print(f"     总数: {today_stats.get('total', 0)}")
            print(f"     已签到: {today_stats.get('checked_in', 0)}")
            print(f"     迟到: {today_stats.get('late', 0)}")
            print(f"     未签到: {today_stats.get('not_checked_in', 0)}")
        
        return True
    else:
        print(f"❌ 统计获取失败: {response.status_code}")
        return False

if __name__ == "__main__":
    print("🎉 扫码签到API成功测试")
    print("=" * 40)
    
    # 测试扫码签到
    success1 = test_scan_check_in()
    
    # 测试批量签到
    success2 = test_batch_check_in()
    
    # 测试统计功能
    success3 = test_stats()
    
    print("\n" + "=" * 40)
    if success1 and success2 and success3:
        print("🎉 扫码签到API测试完全成功！")
    else:
        print("⚠️  部分测试失败") 