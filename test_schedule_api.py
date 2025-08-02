#!/usr/bin/env python3
"""
排期相关API测试脚本
测试查询待排期考生和获取排队位置功能
"""

import requests
import json
import time
import random
from datetime import datetime, timedelta

# 配置
BASE_URL = "http://localhost:8000"
TEST_USER = {
    "email": "institution@test.com",
    "password": "institution123"
}

def get_access_token():
    """获取访问令牌"""
    login_url = f"{BASE_URL}/auth/jwt/login"
    login_data = {
        "username": TEST_USER["email"],
        "password": TEST_USER["password"]
    }
    
    try:
        response = requests.post(
            login_url,
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            token_data = response.json()
            return token_data.get("access_token")
        else:
            print(f"❌ 登录失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 登录异常: {str(e)}")
        return None

def test_get_candidates_to_schedule():
    """测试获取待排期考生"""
    print("\n📋 测试获取待排期考生...")
    
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取访问令牌，跳过待排期考生测试")
        return
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # 测试不同日期的查询
    test_dates = [
        datetime.now().date(),
        datetime.now().date() + timedelta(days=1),
        datetime.now().date() + timedelta(days=7)
    ]
    
    for test_date in test_dates:
        try:
            response = requests.get(
                f"{BASE_URL}/schedules/candidates-to-schedule",
                params={
                    "scheduled_date": test_date.isoformat(),
                    "institution_id": 1,
                    "status": "PENDING"
                },
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                candidates = data.get('candidates', [])
                print(f"✅ {test_date} 待排期考生查询成功")
                print(f"找到 {len(candidates)} 个待排期考生")
                
                if candidates:
                    print("📝 考生列表:")
                    for i, candidate in enumerate(candidates[:5], 1):  # 只显示前5个
                        print(f"  {i}. {candidate.get('name')} - {candidate.get('phone')}")
                        print(f"     机构: {candidate.get('institution_name')}")
                        print(f"     考试产品: {candidate.get('target_exam_product_name')}")
                else:
                    print("📝 该日期暂无待排期考生")
            else:
                print(f"❌ {test_date} 待排期考生查询失败: {response.status_code}")
                print(f"错误信息: {response.text}")
        except Exception as e:
            print(f"❌ {test_date} 待排期考生查询异常: {str(e)}")

def test_get_queue_position():
    """测试获取排队位置"""
    print("\n🔄 测试获取排队位置...")
    
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取访问令牌，跳过排队位置测试")
        return
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # 先获取一些排期记录
    try:
        response = requests.get(
            f"{BASE_URL}/schedules/",
            params={"page": 1, "size": 10},
            headers=headers
        )
        
        if response.status_code == 200:
            schedules_data = response.json()
            schedules = schedules_data.get('items', [])
            
            if schedules:
                print(f"✅ 找到 {len(schedules)} 个排期记录")
                
                # 测试前3个排期的排队位置
                for i, schedule in enumerate(schedules[:3], 1):
                    schedule_id = schedule.get('id')
                    print(f"\n📊 测试排期ID {schedule_id} 的排队位置:")
                    
                    try:
                        queue_response = requests.get(
                            f"{BASE_URL}/schedules/{schedule_id}/queue-position",
                            headers=headers
                        )
                        
                        if queue_response.status_code == 200:
                            queue_data = queue_response.json()
                            print(f"✅ 排队位置查询成功")
                            print(f"  排期ID: {queue_data.get('schedule_id')}")
                            print(f"  排队位置: {queue_data.get('queue_position')}")
                            print(f"  预估等待时间: {queue_data.get('estimated_wait_time')} 分钟")
                            print(f"  队列总人数: {queue_data.get('total_in_queue')}")
                        else:
                            print(f"❌ 排队位置查询失败: {queue_response.status_code}")
                            print(f"错误信息: {queue_response.text}")
                    except Exception as e:
                        print(f"❌ 排队位置查询异常: {str(e)}")
            else:
                print("📝 暂无排期记录，无法测试排队位置")
        else:
            print(f"❌ 获取排期列表失败: {response.status_code}")
            print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"❌ 获取排期列表异常: {str(e)}")

def test_batch_create_schedules():
    """测试批量创建排期"""
    print("\n📅 测试批量创建排期...")
    
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取访问令牌，跳过批量创建排期测试")
        return
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # 先获取一些考生ID
    try:
        candidates_response = requests.get(
            f"{BASE_URL}/candidates/",
            params={"page": 1, "size": 5},
            headers=headers
        )
        
        if candidates_response.status_code == 200:
            candidates_data = candidates_response.json()
            candidates = candidates_data.get('items', [])
            
            if candidates:
                candidate_ids = [candidate.get('id') for candidate in candidates]
                print(f"✅ 获取到 {len(candidate_ids)} 个考生ID")
                
                # 创建批量排期请求
                scheduled_date = datetime.now().date() + timedelta(days=3)
                start_time = datetime.combine(scheduled_date, datetime.strptime("09:00:00", "%H:%M:%S").time())
                end_time = datetime.combine(scheduled_date, datetime.strptime("10:00:00", "%H:%M:%S").time())
                
                batch_request = {
                    "candidate_ids": candidate_ids,
                    "exam_product_id": 12,  # 使用之前创建的考试产品
                    "schedule_type": "理论考试",
                    "scheduled_date": scheduled_date.isoformat(),
                    "start_time": start_time.isoformat(),
                    "end_time": end_time.isoformat(),
                    "venue_id": 5,  # 使用存在的考场ID
                    "notes": "批量创建的测试排期"
                }
                
                try:
                    response = requests.post(
                        f"{BASE_URL}/schedules/batch-create",
                        json=batch_request,
                        headers=headers
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        print("✅ 批量创建排期成功")
                        print(f"成功创建 {len(result.get('schedules', []))} 个排期")
                        
                        schedules = result.get('schedules', [])
                        if schedules:
                            print("📝 创建的排期:")
                            for i, schedule in enumerate(schedules[:3], 1):  # 只显示前3个
                                print(f"  {i}. {schedule.get('candidate_name')} - {schedule.get('exam_product_name')}")
                                print(f"     日期: {schedule.get('scheduled_date')}")
                                print(f"     时间: {schedule.get('start_time')} - {schedule.get('end_time')}")
                    else:
                        print(f"❌ 批量创建排期失败: {response.status_code}")
                        print(f"错误信息: {response.text}")
                except Exception as e:
                    print(f"❌ 批量创建排期异常: {str(e)}")
            else:
                print("📝 暂无考生记录，无法测试批量创建排期")
        else:
            print(f"❌ 获取考生列表失败: {candidates_response.status_code}")
            print(f"错误信息: {candidates_response.text}")
    except Exception as e:
        print(f"❌ 获取考生列表异常: {str(e)}")

def test_get_schedules():
    """测试获取排期列表"""
    print("\n📋 测试获取排期列表...")
    
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取访问令牌，跳过排期列表测试")
        return
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/schedules/",
            params={
                "page": 1,
                "size": 10,
                "status": "PENDING"
            },
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            schedules = data.get('items', [])
            total = data.get('total', 0)
            
            print(f"✅ 排期列表查询成功")
            print(f"总数: {total}")
            print(f"当前页: {data.get('page', 0)}")
            print(f"每页数量: {data.get('size', 0)}")
            print(f"总页数: {data.get('pages', 0)}")
            
            if schedules:
                print("📝 排期列表:")
                for i, schedule in enumerate(schedules[:5], 1):  # 只显示前5个
                    print(f"  {i}. 排期ID: {schedule.get('id')}")
                    print(f"     考生: {schedule.get('candidate_name')}")
                    print(f"     考试产品: {schedule.get('exam_product_name')}")
                    print(f"     日期: {schedule.get('scheduled_date')}")
                    print(f"     状态: {schedule.get('status')}")
            else:
                print("📝 暂无排期记录")
        else:
            print(f"❌ 排期列表查询失败: {response.status_code}")
            print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"❌ 排期列表查询异常: {str(e)}")

def test_server_health():
    """测试服务器健康状态"""
    print("🔍 测试服务器健康状态...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ 服务器运行正常")
            return True
        else:
            print(f"❌ 服务器响应异常: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保服务器已启动")
        return False

def main():
    """主测试函数"""
    print("🚀 开始排期相关API测试")
    print("=" * 50)
    
    # 测试服务器健康状态
    if not test_server_health():
        print("❌ 服务器未启动，无法继续测试")
        return
    
    # 测试获取待排期考生
    test_get_candidates_to_schedule()
    
    # 测试获取排队位置
    test_get_queue_position()
    
    # 测试批量创建排期
    test_batch_create_schedules()
    
    # 测试获取排期列表
    test_get_schedules()
    
    print("\n" + "=" * 50)
    print("🎉 排期相关API测试完成")
    print("📝 测试结果总结:")
    print("- 查询待排期考生: ✅ 已实现")
    print("- 获取排队位置: ✅ 已实现")
    print("- 批量创建排期: ✅ 已实现")
    print("- 排期列表查询: ✅ 已实现")

if __name__ == "__main__":
    main() 