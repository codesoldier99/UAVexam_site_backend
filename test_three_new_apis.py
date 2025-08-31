#!/usr/bin/env python3
"""
测试三个新增的微信API接口
"""

import requests
import json
from datetime import datetime

# API基础URL
BASE_URL = "http://127.0.0.1:8000"

# 测试用户凭据
TEST_CREDENTIALS = {
    "username": "candidate_011234",
    "password": "011234"
}

def get_auth_token():
    """获取认证token"""
    print("🔐 获取认证token...")
    
    login_url = f"{BASE_URL}/auth/token"
    response = requests.post(
        login_url,
        data=TEST_CREDENTIALS,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    if response.status_code == 200:
        token_data = response.json()
        token = token_data.get("access_token")
        print(f"✅ Token获取成功: {token[:20]}...")
        return token
    else:
        print(f"❌ Token获取失败: {response.status_code} - {response.text}")
        return None

def test_candidate_schedule(token):
    """测试考生日程API"""
    print("\n📅 测试考生日程API...")
    
    url = f"{BASE_URL}/api/v1/wechat/candidate/schedule"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("✅ 考生日程获取成功:")
        print(f"  - 即将到来的考试: {len(data.get('upcoming_exams', []))} 场")
        print(f"  - 已完成的考试: {len(data.get('completed_exams', []))} 场")
        print(f"  - 统计信息: {data.get('summary', {})}")
    else:
        print(f"❌ 考生日程获取失败: {response.text}")

def test_candidate_qrcode(token):
    """测试二维码生成API"""
    print("\n🔲 测试二维码生成API...")
    
    url = f"{BASE_URL}/api/v1/wechat/candidate/qrcode"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("✅ 二维码生成成功:")
        print(f"  - 备用码: {data.get('backup_code')}")
        print(f"  - 过期时间: {data.get('expires_at')}")
        print(f"  - 刷新间隔: {data.get('refresh_interval')}秒")
        print(f"  - 二维码数据长度: {len(data.get('qr_code', ''))} 字符")
    else:
        print(f"❌ 二维码生成失败: {response.text}")

def test_dashboard():
    """测试公共看板API"""
    print("\n📊 测试公共看板API...")
    
    url = f"{BASE_URL}/api/v1/wechat/dashboard"
    
    response = requests.get(url)
    
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("✅ 看板数据获取成功:")
        stats = data.get('statistics', {})
        print(f"  - 统计数据: 已安排{stats.get('total_scheduled', 0)}场, 已签到{stats.get('checked_in', 0)}场")
        print(f"  - 考场数量: {len(data.get('venues', []))} 个")
        print(f"  - 公告数量: {len(data.get('announcements', []))} 条")
        print(f"  - 系统状态: {data.get('system_status', {})}")
    else:
        print(f"❌ 看板数据获取失败: {response.text}")

def main():
    """主测试函数"""
    print("🚀 开始测试三个新增的微信API接口")
    print("=" * 50)
    
    # 1. 获取认证token
    token = get_auth_token()
    if not token:
        print("❌ 无法获取认证token，测试终止")
        return
    
    # 2. 测试三个新API
    test_candidate_schedule(token)
    test_candidate_qrcode(token)
    test_dashboard()
    
    print("\n" + "=" * 50)
    print("🎉 测试完成！")

if __name__ == "__main__":
    main()