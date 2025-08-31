#!/usr/bin/env python3
"""
测试签到时间逻辑修复
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def test_checkin_with_fixed_time_logic():
    """测试修复后的签到时间逻辑"""
    
    print("🧪 测试签到时间逻辑修复")
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 测试数据 - 使用数据库中的真实数据
    test_qr_data = {
        "candidate_id": 5,
        "name": "张三",
        "id_card": "110101199001011234",
        "username": "candidate_011234",
        "schedule_id": 1,
        "venue_id": 1,
        "exam_session": "上午",
        "exam_date": "2025-01-26",
        "timestamp": int(datetime.now().timestamp()),
        "type": "candidate_checkin"
    }
    
    # 签到请求
    checkin_request = {
        "qr_code_data": json.dumps(test_qr_data)
    }
    
    try:
        print("\n📱 发送签到请求...")
        response = requests.post(
            f"{BASE_URL}/api/v1/wechat/checkin",
            json=checkin_request,
            timeout=10
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 签到成功!")
            print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        else:
            try:
                error_data = response.json()
                print(f"❌ 签到失败: {error_data.get('detail', '未知错误')}")
            except:
                print(f"❌ 签到失败: {response.text}")
                
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")

def test_health_check():
    """测试健康检查"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health", timeout=5)
        if response.status_code == 200:
            print("✅ 后端服务正常")
            return True
        else:
            print("❌ 后端服务异常")
            return False
    except Exception as e:
        print(f"❌ 无法连接后端服务: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("签到时间逻辑修复测试")
    print("=" * 50)
    
    # 1. 检查后端服务
    if not test_health_check():
        print("\n请先启动后端服务")
        exit(1)
    
    # 2. 测试签到逻辑
    test_checkin_with_fixed_time_logic()
    
    print("\n" + "=" * 50)
    print("测试完成")