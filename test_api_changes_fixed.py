#!/usr/bin/env python3
"""
API接口修改测试脚本
测试所有修改后的接口功能
"""

import requests
import json
from datetime import datetime

# 配置
BASE_URL = "http://localhost:8000/api/v1"

def test_candidate_info_by_idcard():
    """测试身份证验证接口增强"""
    print("\n=== 测试身份证验证接口 ===")
    
    id_card = "110101199001011234"
    response = requests.get(f"{BASE_URL}/wechat/candidate/info-by-idcard?id_card={id_card}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ 身份证验证接口响应成功")
        print(f"考生信息: {data.get('name')}")
        print(f"当前考试安排ID: {data.get('current_schedule_id')}")
        print(f"当前考场ID: {data.get('current_venue_id')}")
        print(f"考试时间: {data.get('exam_time')}")
        print(f"考场地址: {data.get('venue_address')}")
    else:
        print(f"❌ 身份证验证失败: {response.status_code}")
        print(response.text)

def test_candidate_login():
    """测试考生登录接口增强（两步验证流程）"""
    print("\n=== 测试考生登录接口 ===")
    
    # 使用测试数据中的身份证号
    id_card = "110101199001011234"
    
    # 第一步：身份证验证
    print("第一步：验证身份证号...")
    id_card_response = requests.get(f"{BASE_URL}/wechat/candidate/info-by-idcard?id_card={id_card}")
    
    if id_card_response.status_code != 200:
        print(f"❌ 身份证验证失败: {id_card_response.status_code}")
        print(id_card_response.text)
        return None
    
    candidate_info = id_card_response.json()
    print(f"✅ 身份证验证成功，考生: {candidate_info.get('name')}")
    
    # 第二步：实际登录
    print("第二步：执行登录...")
    # 根据规则生成用户名和密码：candidate_ + 身份证后6位
    last_6_digits = id_card[-6:]
    login_data = {
        "username": f"candidate_{last_6_digits}",  # candidate_011234
        "password": last_6_digits  # 011234
    }
    
    print(f"使用用户名: {login_data['username']}")
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ 考生登录成功")
        print(f"用户角色: {data.get('user', {}).get('role')}")
        print(f"当前考试: {data.get('current_exam')}")
        print(f"有效考试安排: {data.get('has_valid_schedule')}")
        
        # 第三步：获取用户详细信息
        print("第三步：获取用户详细信息...")
        token = data.get('access_token')
        headers = {"Authorization": f"Bearer {token}"}
        me_response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        
        if me_response.status_code == 200:
            user_info = me_response.json()
            print(f"✅ 获取用户信息成功: {user_info.get('real_name', user_info.get('username'))}")
        else:
            print(f"⚠️ 获取用户信息失败: {me_response.status_code}")
        
        return token
    else:
        print(f"❌ 考生登录失败: {response.status_code}")
        print(response.text)
        print(f"提示: 请确保数据库中存在用户名为 '{login_data['username']}' 的考生账号")
        return None

def test_wechat_login():
    """测试微信登录接口"""
    print("\n=== 测试微信登录接口 ===")
    
    login_data = {
        "id_card": "110101199001011234",
        "openid": "test_openid_123456"
    }
    
    response = requests.post(f"{BASE_URL}/wechat/login", json=login_data)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ 微信登录成功")
        print(f"用户信息: {data.get('user_info', {}).get('name')}")
        print(f"当前考试: {data.get('current_exam')}")
        print(f"即将到来的考试数量: {len(data.get('upcoming_exams', []))}")
        return data.get('access_token')
    else:
        print(f"❌ 微信登录失败: {response.status_code}")
        print(response.text)
        return None

def test_candidate_schedule(token):
    """测试考生日程接口"""
    print("\n=== 测试考生日程接口 ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/wechat/candidate/schedule", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ 获取考生日程成功")
        
        upcoming = data.get('upcoming_exams', [])
        completed = data.get('completed_exams', [])
        summary = data.get('summary', {})
        
        print(f"即将到来的考试: {len(upcoming)}场")
        print(f"已完成的考试: {len(completed)}场")
        print(f"总考试数量: {summary.get('total_count')}")
        
        if upcoming:
            exam = upcoming[0]
            print(f"最近考试:")
            print(f"  - 考试安排ID: {exam.get('schedule_id')}")
            print(f"  - 考试安排ID: {exam.get('schedule_id')}")
            print(f"  - 考场ID: {exam.get('venue', {}).get('id')}")
            print(f"  - 考场ID: {exam.get('venue', {}).get('id')}")
            print(f"  - 考试名称: {exam.get('exam_name')}")
            print(f"  - 考试时间: {exam.get('exam_time')}")
    else:
        print(f"❌ 获取考生日程失败: {response.status_code}")
        print(response.text)

def test_qrcode_generation(token):
    """测试二维码生成接口增强"""
    print("\n=== 测试二维码生成接口 ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/wechat/candidate/qrcode", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ 二维码生成成功")
        print(f"过期时间: {data.get('expires_at')}")
        
        # 解析二维码数据
        qr_code_data = data.get('qr_code_data')
        if qr_code_data:
            try:
                qr_data = json.loads(qr_code_data)
                print("二维码包含的信息:")
                print(f"  - 考生ID: {qr_data.get('candidate_id')}")
                print(f"  - 考生姓名: {qr_data.get('name')}")
                print(f"  - 身份证: {qr_data.get('id_card')}")
                print(f"  - 考试安排ID: {qr_data.get('schedule_id')}")
                print(f"  - 考场ID: {qr_data.get('venue_id')}")
                print(f"  - 考试日期: {qr_data.get('exam_date')}")
            except json.JSONDecodeError:
                print("⚠️ 二维码数据格式错误")
        
        return qr_code_data
    else:
        print(f"❌ 二维码生成失败: {response.status_code}")
        print(response.text)
        return None

def test_qrcode_refresh(token):
    """测试二维码刷新接口增强"""
    print("\n=== 测试二维码刷新接口 ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 不需要传递candidate_id，从token中获取当前用户
    response = requests.post(f"{BASE_URL}/wechat/candidate/qrcode/refresh", 
                           headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ 二维码刷新成功")
        print(f"新的过期时间: {data.get('expires_at')}")
        print(f"刷新时间: {data.get('refreshed_at')}")
    else:
        print(f"❌ 二维码刷新失败: {response.status_code}")
        print(response.text)

def test_checkin(qr_code_data):
    """测试签到接口增强"""
    print("\n=== 测试签到接口 ===")
    
    # 使用管理员token进行签到操作
    admin_login = {
        "username": "admin",
        "password": "admin123"
    }
    
    admin_response = requests.post(f"{BASE_URL}/auth/login", json=admin_login)
    if admin_response.status_code != 200:
        print("❌ 无法获取管理员权限，跳过签到测试")
        return
    
    admin_token = admin_response.json().get('access_token')
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # 新的签到数据格式
    checkin_data = {
        "qr_code_data": qr_code_data
    }
    
    response = requests.post(f"{BASE_URL}/wechat/checkin", 
                           json=checkin_data, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ 签到成功")
        print(f"签到状态: {data.get('success')}")
        print(f"签到消息: {data.get('message')}")
        print(f"签到时间: {data.get('checkin_time')}")
        
        schedule_info = data.get('schedule_info', {})
        print(f"考试安排信息:")
        print(f"  - 考试安排ID: {schedule_info.get('schedule_id')}")
        print(f"  - 考场名称: {schedule_info.get('venue_name')}")
        print(f"  - 考场地址: {schedule_info.get('venue_address')}")
        print(f"  - 考生姓名: {schedule_info.get('candidate_name')}")
    else:
        print(f"❌ 签到失败: {response.status_code}")
        print(response.text)

def main():
    """主测试函数"""
    print("🚀 开始测试API接口修改...")
    
    # 1. 测试身份证验证接口增强
    test_candidate_info_by_idcard()
    
    # 2. 测试考生登录接口增强（两步验证流程）
    candidate_token = test_candidate_login()
    
    # 3. 测试微信登录接口增强
    wechat_token = test_wechat_login()
    
    # 优先使用考生登录的token，如果失败则使用微信登录token
    token = candidate_token or wechat_token
    
    if token:
        print(f"\n📱 使用{'考生登录' if candidate_token else '微信登录'}的token进行后续测试")
        
        # 4. 测试考生日程接口
        test_candidate_schedule(token)
        
        # 5. 测试二维码生成接口
        qr_code_data = test_qrcode_generation(token)
        
        # 6. 测试二维码刷新接口
        test_qrcode_refresh(token)
        
        # 7. 测试签到接口（如果有二维码数据）
        if qr_code_data:
            test_checkin(qr_code_data)
    else:
        print("\n❌ 无法获取有效的访问令牌，跳过需要认证的测试")
    
    print("\n✨ 测试完成！")

if __name__ == "__main__":
    main()