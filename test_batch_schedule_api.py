#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试批量排队API功能
"""

import requests
import json
from datetime import datetime, timedelta
import time

# API基础URL
BASE_URL = "http://localhost:8000"

def test_batch_schedule_api():
    """测试批量排队API"""
    print("🚀 开始测试批量排队API功能...")
    
    # 1. 测试登录获取token
    print("\n1. 测试登录...")
    login_data = {
        "username": "admin@exam.com",
        "password": "admin123"
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/auth/jwt/login", data=login_data)
        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data.get("access_token")
            print(f"✅ 登录成功，获取到token: {access_token[:20]}...")
        else:
            print(f"❌ 登录失败: {login_response.status_code}")
            print(login_response.text)
            return
    except Exception as e:
        print(f"❌ 登录请求异常: {e}")
        return
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # 2. 测试获取待排期考生
    print("\n2. 测试获取待排期考生...")
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_str = tomorrow.strftime("%Y-%m-%d")
    
    try:
        candidates_response = requests.get(
            f"{BASE_URL}/schedules/candidates-to-schedule",
            params={
                "scheduled_date": tomorrow_str,
                "institution_id": 1
            },
            headers=headers
        )
        
        if candidates_response.status_code == 200:
            candidates_data = candidates_response.json()
            print(f"✅ 获取到 {len(candidates_data.get('candidates', []))} 个待排期考生")
            for candidate in candidates_data.get('candidates', []):
                print(f"   - {candidate.get('name')} ({candidate.get('phone')})")
        else:
            print(f"❌ 获取待排期考生失败: {candidates_response.status_code}")
            print(candidates_response.text)
    except Exception as e:
        print(f"❌ 获取待排期考生异常: {e}")
    
    # 3. 测试批量创建排期
    print("\n3. 测试批量创建排期...")
    
    # 准备测试数据
    batch_request = {
        "candidate_ids": [1, 2, 3],  # 假设这些考生ID存在
        "exam_product_id": 1,
        "schedule_type": "理论考试",
        "scheduled_date": tomorrow_str,
        "start_time": f"{tomorrow_str}T09:00:00",
        "end_time": f"{tomorrow_str}T17:00:00",
        "venue_id": 1,
        "notes": "批量排队测试"
    }
    
    try:
        batch_response = requests.post(
            f"{BASE_URL}/schedules/batch-create",
            json=batch_request,
            headers=headers
        )
        
        if batch_response.status_code == 200:
            batch_data = batch_response.json()
            print(f"✅ 批量创建成功: {batch_data.get('message')}")
            print(f"   创建了 {len(batch_data.get('schedules', []))} 个排期")
            for schedule in batch_data.get('schedules', []):
                print(f"   - {schedule.get('candidate_name')}: {schedule.get('start_time')}")
        else:
            print(f"❌ 批量创建失败: {batch_response.status_code}")
            print(batch_response.text)
    except Exception as e:
        print(f"❌ 批量创建异常: {e}")
    
    # 4. 测试获取排队位置
    print("\n4. 测试获取排队位置...")
    try:
        queue_response = requests.get(
            f"{BASE_URL}/schedules/1/queue-position",
            headers=headers
        )
        
        if queue_response.status_code == 200:
            queue_data = queue_response.json()
            print(f"✅ 排队位置信息:")
            print(f"   - 位置: {queue_data.get('queue_position')}")
            print(f"   - 预估等待时间: {queue_data.get('estimated_wait_time')} 分钟")
            print(f"   - 总排队人数: {queue_data.get('total_in_queue')}")
        else:
            print(f"❌ 获取排队位置失败: {queue_response.status_code}")
            print(queue_response.text)
    except Exception as e:
        print(f"❌ 获取排队位置异常: {e}")
    
    # 5. 测试获取排期列表
    print("\n5. 测试获取排期列表...")
    try:
        schedules_response = requests.get(
            f"{BASE_URL}/schedules/",
            params={
                "page": 1,
                "size": 10,
                "scheduled_date": tomorrow_str
            },
            headers=headers
        )
        
        if schedules_response.status_code == 200:
            schedules_data = schedules_response.json()
            print(f"✅ 获取排期列表成功:")
            print(f"   - 总数: {schedules_data.get('total')}")
            print(f"   - 当前页: {schedules_data.get('page')}")
            print(f"   - 每页大小: {schedules_data.get('size')}")
            print(f"   - 总页数: {schedules_data.get('pages')}")
        else:
            print(f"❌ 获取排期列表失败: {schedules_response.status_code}")
            print(schedules_response.text)
    except Exception as e:
        print(f"❌ 获取排期列表异常: {e}")
    
    print("\n🎯 批量排队API测试完成!")

if __name__ == "__main__":
    test_batch_schedule_api() 