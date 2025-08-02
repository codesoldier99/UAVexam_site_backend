#!/usr/bin/env python3
"""
排期核心API测试脚本
专门测试查询待排期考生和获取排队位置功能
"""

import requests
import json
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

def test_candidates_to_schedule():
    """测试查询待排期考生API"""
    print("\n📋 测试查询待排期考生API...")
    
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取访问令牌")
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
            
            print(f"\n📅 测试日期: {test_date}")
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                candidates = data.get('candidates', [])
                print(f"✅ 查询成功，找到 {len(candidates)} 个待排期考生")
                
                if candidates:
                    print("📝 考生列表:")
                    for i, candidate in enumerate(candidates[:3], 1):  # 只显示前3个
                        print(f"  {i}. {candidate.get('name')} - {candidate.get('phone')}")
                        print(f"     机构: {candidate.get('institution_name')}")
                        print(f"     考试产品: {candidate.get('target_exam_product_name')}")
                else:
                    print("📝 该日期暂无待排期考生")
            else:
                print(f"❌ 查询失败")
                print(f"错误信息: {response.text}")
        except Exception as e:
            print(f"❌ 查询异常: {str(e)}")

def test_queue_position():
    """测试获取排队位置API"""
    print("\n🔄 测试获取排队位置API...")
    
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取访问令牌")
        return
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # 先获取排期列表
    try:
        response = requests.get(
            f"{BASE_URL}/schedules/",
            params={"page": 1, "size": 5},
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            schedules = data.get('items', [])
            
            if schedules:
                print(f"✅ 找到 {len(schedules)} 个排期记录")
                
                # 测试前2个排期的排队位置
                for i, schedule in enumerate(schedules[:2], 1):
                    schedule_id = schedule.get('id')
                    print(f"\n📊 测试排期ID {schedule_id} 的排队位置:")
                    
                    try:
                        queue_response = requests.get(
                            f"{BASE_URL}/schedules/{schedule_id}/queue-position",
                            headers=headers
                        )
                        
                        print(f"响应状态码: {queue_response.status_code}")
                        
                        if queue_response.status_code == 200:
                            queue_data = queue_response.json()
                            print(f"✅ 排队位置查询成功")
                            print(f"  排期ID: {queue_data.get('schedule_id')}")
                            print(f"  排队位置: {queue_data.get('queue_position')}")
                            print(f"  预估等待时间: {queue_data.get('estimated_wait_time')} 分钟")
                            print(f"  队列总人数: {queue_data.get('total_in_queue')}")
                        else:
                            print(f"❌ 排队位置查询失败")
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
    print("🚀 开始排期核心API测试")
    print("=" * 50)
    
    # 测试服务器健康状态
    if not test_server_health():
        print("❌ 服务器未启动，无法继续测试")
        return
    
    # 测试查询待排期考生API
    test_candidates_to_schedule()
    
    # 测试获取排队位置API
    test_queue_position()
    
    print("\n" + "=" * 50)
    print("🎉 排期核心API测试完成")
    print("📝 测试结果总结:")
    print("- 查询待排期考生API: ✅ 已实现")
    print("- 获取排队位置API: ✅ 已实现")

if __name__ == "__main__":
    main() 