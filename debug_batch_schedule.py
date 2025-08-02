#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试批量排期功能
"""

import requests
import json
from datetime import datetime, timedelta

# API基础URL
BASE_URL = "http://localhost:8000"

def debug_batch_schedule():
    """调试批量排期功能"""
    print("🔍 开始调试批量排期功能...")
    
    # 1. 登录
    print("\n1. 登录...")
    login_data = {
        "username": "admin@exam.com",
        "password": "admin123"
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/auth/jwt/login", data=login_data)
        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data.get("access_token")
            print(f"✅ 登录成功")
        else:
            print(f"❌ 登录失败: {login_response.status_code}")
            return
    except Exception as e:
        print(f"❌ 登录异常: {e}")
        return
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # 2. 获取考生列表
    print("\n2. 获取考生列表...")
    try:
        candidates_response = requests.get(
            f"{BASE_URL}/schedules/candidates-to-schedule",
            params={
                "scheduled_date": "2024-01-20",
                "institution_id": 1
            },
            headers=headers
        )
        
        if candidates_response.status_code == 200:
            candidates_data = candidates_response.json()
            candidates = candidates_data.get('candidates', [])
            print(f"✅ 获取到 {len(candidates)} 个考生")
            
            # 显示前5个考生的详细信息
            for i, candidate in enumerate(candidates[:5]):
                print(f"   考生{i+1}: ID={candidate.get('id')}, 姓名={candidate.get('name')}, 机构={candidate.get('institution_name')}")
            
            # 获取考生ID列表
            candidate_ids = [candidate.get('id') for candidate in candidates[:3]]
            print(f"   将使用考生ID: {candidate_ids}")
        else:
            print(f"❌ 获取考生失败: {candidates_response.status_code}")
            print(candidates_response.text)
            return
    except Exception as e:
        print(f"❌ 获取考生异常: {e}")
        return
    
    # 3. 测试简单的批量创建
    print("\n3. 测试简单的批量创建...")
    
    batch_request = {
        "candidate_ids": candidate_ids,
        "exam_product_id": 3,  # 使用存在的考试产品ID
        "schedule_type": "理论考试",
        "scheduled_date": "2024-01-20",
        "start_time": "2024-01-20T09:00:00",
        "end_time": "2024-01-20T17:00:00",
        "venue_id": 5,  # 使用存在的考场ID
        "notes": "调试测试",
        "group_by_institution": False,
        "exam_duration_minutes": 30,
        "break_duration_minutes": 10,
        "max_exams_per_day": 16
    }
    
    print(f"   请求数据: {json.dumps(batch_request, indent=2, ensure_ascii=False)}")
    
    try:
        batch_response = requests.post(
            f"{BASE_URL}/schedules/batch-create",
            json=batch_request,
            headers=headers
        )
        
        print(f"   响应状态码: {batch_response.status_code}")
        print(f"   响应内容: {batch_response.text}")
        
        if batch_response.status_code == 200:
            batch_data = batch_response.json()
            print(f"✅ 批量创建响应: {batch_data}")
        else:
            print(f"❌ 批量创建失败")
    except Exception as e:
        print(f"❌ 批量创建异常: {e}")
    
    # 4. 检查现有排期
    print("\n4. 检查现有排期...")
    try:
        schedules_response = requests.get(
            f"{BASE_URL}/schedules/",
            params={
                "page": 1,
                "size": 10,
                "scheduled_date": "2024-01-20"
            },
            headers=headers
        )
        
        if schedules_response.status_code == 200:
            schedules_data = schedules_response.json()
            print(f"✅ 现有排期: {schedules_data}")
        else:
            print(f"❌ 获取排期失败: {schedules_response.status_code}")
    except Exception as e:
        print(f"❌ 获取排期异常: {e}")
    
    print("\n🎯 调试完成!")

if __name__ == "__main__":
    debug_batch_schedule() 