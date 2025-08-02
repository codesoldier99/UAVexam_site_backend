#!/usr/bin/env python3
"""
考生管理和排期管理综合测试脚本
"""

import requests
import json
from datetime import datetime, timedelta

def test_candidates_and_schedules():
    base_url = "http://localhost:8000"
    
    print("👥 考生管理和排期管理综合测试")
    print("="*60)
    
    # 1. 管理员登录
    print("1. 管理员登录")
    login_data = "username=admin@exam.com&password=admin123"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    try:
        response = requests.post(f"{base_url}/auth/jwt/login", data=login_data, headers=headers)
        print(f"登录状态码: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            admin_token = token_data.get("access_token")
            auth_headers = {"Authorization": f"Bearer {admin_token}"}
            print("✅ 登录成功")
        else:
            print("❌ 登录失败")
            return
    except Exception as e:
        print(f"❌ 连接错误: {e}")
        return
    
    # 2. 创建考生
    print("\n2. 创建考生")
    candidate_data = {
        "name": "张三",
        "id_number": "110101199001011234",
        "phone": "13800138001",
        "email": "zhangsan@example.com",
        "gender": "男",
        "address": "北京市朝阳区",
        "emergency_contact": "张父",
        "emergency_phone": "13900139001",
        "target_exam_product_id": 3,  # 使用之前创建的考试产品
        "institution_id": 1,
        "status": "待审核",
        "notes": "测试考生"
    }
    
    try:
        response = requests.post(f"{base_url}/candidates", json=candidate_data, headers=auth_headers)
        print(f"创建考生状态码: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            candidate_id = result.get("id")
            print(f"✅ 考生创建成功，ID: {candidate_id}")
        else:
            print(f"❌ 创建失败: {response.text}")
            return
    except Exception as e:
        print(f"❌ 创建考生错误: {e}")
        return
    
    # 3. 获取考生列表
    print("\n3. 获取考生列表")
    try:
        response = requests.get(f"{base_url}/candidates?page=1&size=10", headers=auth_headers)
        print(f"获取考生列表状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 获取成功，共 {result.get('total', 0)} 条记录")
        else:
            print(f"❌ 获取失败: {response.text}")
    except Exception as e:
        print(f"❌ 获取考生列表错误: {e}")
    
    # 4. 获取待排期考生
    print("\n4. 获取待排期考生")
    tomorrow = datetime.now() + timedelta(days=1)
    try:
        response = requests.get(
            f"{base_url}/schedules/candidates-to-schedule?scheduled_date={tomorrow.isoformat()}",
            headers=auth_headers
        )
        print(f"获取待排期考生状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            candidates = result.get('candidates', [])
            print(f"✅ 获取成功，共 {len(candidates)} 个待排期考生")
            for candidate in candidates:
                print(f"  - {candidate.get('name')} ({candidate.get('phone')})")
        else:
            print(f"❌ 获取失败: {response.text}")
    except Exception as e:
        print(f"❌ 获取待排期考生错误: {e}")
    
    # 5. 批量创建排期
    print("\n5. 批量创建排期")
    schedule_data = {
        "candidate_ids": [candidate_id],
        "exam_product_id": 3,
        "schedule_type": "理论考试",
        "scheduled_date": tomorrow.isoformat(),
        "start_time": (tomorrow + timedelta(hours=9)).isoformat(),
        "end_time": (tomorrow + timedelta(hours=11)).isoformat(),
        "venue_id": 1,
        "notes": "理论考试排期"
    }
    
    try:
        response = requests.post(f"{base_url}/schedules/batch-create", json=schedule_data, headers=auth_headers)
        print(f"批量创建排期状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 批量创建成功: {result.get('message')}")
            schedules = result.get('schedules', [])
            for schedule in schedules:
                print(f"  - {schedule.get('candidate_name')} - {schedule.get('schedule_type')}")
        else:
            print(f"❌ 创建失败: {response.text}")
    except Exception as e:
        print(f"❌ 批量创建排期错误: {e}")
    
    # 6. 获取考生排期
    print(f"\n6. 获取考生排期 (考生ID: {candidate_id})")
    try:
        response = requests.get(f"{base_url}/schedules/{candidate_id}/schedules", headers=auth_headers)
        print(f"获取考生排期状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 获取成功，共 {result.get('total', 0)} 条排期")
        else:
            print(f"❌ 获取失败: {response.text}")
    except Exception as e:
        print(f"❌ 获取考生排期错误: {e}")
    
    # 7. 获取排队位置
    print("\n7. 获取排队位置")
    try:
        # 先获取排期列表
        response = requests.get(f"{base_url}/schedules", headers=auth_headers)
        if response.status_code == 200:
            result = response.json()
            schedules = result.get('items', [])
            if schedules:
                schedule_id = schedules[0].get('id')
                
                response = requests.get(f"{base_url}/schedules/{schedule_id}/queue-position", headers=auth_headers)
                print(f"获取排队位置状态码: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ 排队位置: 第{result.get('queue_position')}位")
                    print(f"   预估等待时间: {result.get('estimated_wait_time')} 分钟")
                    print(f"   总排队人数: {result.get('total_in_queue')} 人")
                else:
                    print(f"❌ 获取失败: {response.text}")
            else:
                print("❌ 没有找到排期")
        else:
            print(f"❌ 获取排期列表失败: {response.text}")
    except Exception as e:
        print(f"❌ 获取排队位置错误: {e}")
    
    # 8. 签到测试
    print("\n8. 签到测试")
    try:
        # 先获取排期列表
        response = requests.get(f"{base_url}/schedules", headers=auth_headers)
        if response.status_code == 200:
            result = response.json()
            schedules = result.get('items', [])
            if schedules:
                schedule_id = schedules[0].get('id')
                
                check_in_data = {
                    "check_in_time": datetime.now().isoformat(),
                    "notes": "测试签到"
                }
                
                response = requests.post(f"{base_url}/schedules/{schedule_id}/check-in", json=check_in_data, headers=auth_headers)
                print(f"签到状态码: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ 签到成功，状态: {result.get('check_in_status')}")
                else:
                    print(f"❌ 签到失败: {response.text}")
            else:
                print("❌ 没有找到排期")
        else:
            print(f"❌ 获取排期列表失败: {response.text}")
    except Exception as e:
        print(f"❌ 签到错误: {e}")
    
    print("\n" + "="*60)
    print("👥 考生管理和排期管理测试完成")

if __name__ == "__main__":
    test_candidates_and_schedules() 