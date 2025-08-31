import requests
import json
import time

# 配置
BASE_URL = "http://127.0.0.1:8000"
API_V1 = f"{BASE_URL}/api/v1"

def test_login_by_id_card():
    """测试身份证登录功能"""
    print("=== 测试身份证登录功能 ===")
    
    # 测试数据 - 请根据你的数据库中的实际数据修改
    test_id_cards = [
        "110101199001011234",  # 替换为你数据库中的真实身份证号
        "110101199001011235",  # 替换为你数据库中的真实身份证号
    ]
    
    for id_card in test_id_cards:
        print(f"\n测试身份证: {id_card}")
        
        response = requests.post(
            f"{API_V1}/wechat/login",
            json={
                "id_card": id_card,
                "openid": "test_openid_123"  # 测试用的openid
            }
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("登录成功!")
            print(f"考生信息: {data.get('candidate_info', {})}")
            print(f"考试安排数量: {len(data.get('exam_schedules', []))}")
            
            # 打印考试安排详情
            for i, schedule in enumerate(data.get('exam_schedules', []), 1):
                print(f"  考试安排 {i}:")
                print(f"    考试ID: {schedule.get('schedule_id')}")
                print(f"    考试日期: {schedule.get('exam_date')}")
                print(f"    考试时间: {schedule.get('exam_time')}")
                print(f"    考场: {schedule.get('venue_name')}")
                print(f"    考场地址: {schedule.get('venue_address')}")
                print(f"    二维码数据: {schedule.get('qr_code_data', '')[:50]}...")
        else:
            print(f"登录失败: {response.text}")

def test_checkin_process():
    """测试签到流程"""
    print("\n=== 测试签到流程 ===")
    
    # 首先获取一个有效的考生登录信息
    test_id_card = "110101199001011234"  # 替换为你数据库中的真实身份证号
    
    login_response = requests.post(
        f"{API_V1}/wechat/login",
        json={
            "id_card": test_id_card,
            "openid": "test_openid_123"
        }
    )
    
    if login_response.status_code != 200:
        print("无法获取登录信息，跳过签到测试")
        return
    
    login_data = login_response.json()
    exam_schedules = login_data.get('exam_schedules', [])
    
    if not exam_schedules:
        print("没有找到考试安排，跳过签到测试")
        return
    
    # 使用第一个考试安排进行签到测试
    schedule = exam_schedules[0]
    schedule_id = schedule.get('schedule_id')
    qr_code_data = schedule.get('qr_code_data')
    
    print(f"使用考试安排ID: {schedule_id}")
    print(f"二维码数据: {qr_code_data[:50]}...")
    
    # 测试签到
    checkin_response = requests.post(
        f"{API_V1}/wechat/checkin",
        json={
            "schedule_id": schedule_id,
            "examiner_id": 1,  # 替换为你数据库中的真实考务人员ID
            "venue_id": schedule.get('venue_id'),
            "qr_code_data": qr_code_data
        }
    )
    
    print(f"签到状态码: {checkin_response.status_code}")
    
    if checkin_response.status_code == 200:
        checkin_data = checkin_response.json()
        print("签到成功!")
        print(f"签到结果: {json.dumps(checkin_data, indent=2, ensure_ascii=False)}")
    else:
        print(f"签到失败: {checkin_response.text}")

def test_candidate_info():
    """测试考生信息查询"""
    print("\n=== 测试考生信息查询 ===")
    
    test_id_card = "110101199001011234"  # 替换为你数据库中的真实身份证号
    
    response = requests.get(
        f"{API_V1}/wechat/candidate/info-by-idcard?id_card={test_id_card}"
    )
    
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("查询成功!")
        print(f"考生信息: {json.dumps(data, indent=2, ensure_ascii=False)}")
    else:
        print(f"查询失败: {response.text}")

def test_qr_code_refresh():
    """测试二维码刷新"""
    print("\n=== 测试二维码刷新 ===")
    
    candidate_id = 5  # 替换为你数据库中的真实考生ID
    
    response = requests.post(
        f"{API_V1}/wechat/candidate/qrcode/refresh",
        json={"candidate_id": candidate_id}
    )
    
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("刷新成功!")
        print(f"新二维码数据: {data.get('qr_code_data', '')[:100]}...")
        print(f"过期时间: {data.get('expires_at')}")
    else:
        print(f"刷新失败: {response.text}")

def test_candidate_schedule():
    """测试考生考试安排查询"""
    print("\n=== 测试考生考试安排查询 ===")
    
    response = requests.get(f"{API_V1}/wechat/candidate/schedule")
    
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("查询成功!")
        print(f"考试安排: {json.dumps(data, indent=2, ensure_ascii=False)}")
    else:
        print(f"查询失败: {response.text}")

def test_dashboard():
    """测试公共看板数据"""
    print("\n=== 测试公共看板数据 ===")
    
    response = requests.get(f"{API_V1}/wechat/dashboard")
    
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("查询成功!")
        print(f"看板数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
    else:
        print(f"查询失败: {response.text}")

def test_venue_status():
    """测试考场状态查询"""
    print("\n=== 测试考场状态查询 ===")
    
    response = requests.get(f"{API_V1}/wechat/venues/status")
    
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("查询成功!")
        print(f"考场状态: {json.dumps(data, indent=2, ensure_ascii=False)}")
    else:
        print(f"查询失败: {response.text}")

def main():
    """主测试函数"""
    print("开始测试微信API功能...")
    print(f"后端地址: {BASE_URL}")
    
    try:
        # 测试后端连接
        health_response = requests.get(f"{BASE_URL}/health", timeout=5)
        if health_response.status_code == 200:
            print("✓ 后端连接正常")
        else:
            print("✗ 后端连接异常")
            return
    except requests.exceptions.RequestException as e:
        print(f"✗ 无法连接到后端: {e}")
        return
    
    # 执行各项测试
    test_candidate_info()
    test_login_by_id_card()
    test_candidate_schedule()
    test_qr_code_refresh()
    test_dashboard()
    test_venue_status()
    test_checkin_process()
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    main()