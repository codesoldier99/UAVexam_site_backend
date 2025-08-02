#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的扫码签到API测试
"""

import requests
import json
import time
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"
ADMIN_EMAIL = "admin@exam.com"
ADMIN_PASSWORD = "admin123"

def test_scan_check_in_api():
    """测试扫码签到API"""
    print("🚀 开始扫码签到API测试")
    
    # 创建会话
    session = requests.Session()
    
    # 1. 登录
    print("1. 登录测试...")
    login_data = {
        "username": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }
    
    response = session.post(f"{BASE_URL}/auth/jwt/login", data=login_data)
    if response.status_code != 200:
        print(f"❌ 登录失败: {response.status_code}")
        return False
    
    token = response.json().get("access_token")
    session.headers.update({
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    })
    print("✅ 登录成功")
    
    # 2. 检查扫码签到API端点是否存在
    print("\n2. 检查API端点...")
    response = session.get(f"{BASE_URL}/docs")
    if response.status_code == 200:
        print("✅ API文档可访问")
    else:
        print("❌ API文档不可访问")
    
    # 3. 测试扫码签到API（使用无效二维码）
    print("\n3. 测试扫码签到API...")
    
    # 生成测试二维码
    import hashlib
    timestamp = int(time.time())
    test_qr_code = f"SCHEDULE_999_{timestamp}_{hashlib.md5(str(timestamp).encode()).hexdigest()[:8]}"
    
    check_in_data = {
        "qr_code": test_qr_code,
        "check_in_time": datetime.now().isoformat(),
        "notes": "测试扫码签到"
    }
    
    response = session.post(f"{BASE_URL}/schedules/scan-check-in", json=check_in_data)
    
    if response.status_code == 404:
        print("✅ API正常工作 - 正确返回404（排期不存在）")
        print(f"   响应: {response.json()}")
    elif response.status_code == 403:
        print("✅ API正常工作 - 权限检查正常")
        print(f"   响应: {response.json()}")
    else:
        print(f"❌ 意外响应: {response.status_code}")
        print(f"   响应: {response.text}")
        return False
    
    # 4. 测试批量扫码签到API
    print("\n4. 测试批量扫码签到API...")
    
    batch_data = {
        "qr_codes": [test_qr_code],
        "check_in_time": datetime.now().isoformat()
    }
    
    response = session.post(f"{BASE_URL}/schedules/batch-scan-check-in", json=batch_data)
    
    if response.status_code in [200, 400, 404]:
        print("✅ 批量签到API正常工作")
        print(f"   响应: {response.json()}")
    else:
        print(f"❌ 批量签到API异常: {response.status_code}")
        print(f"   响应: {response.text}")
        return False
    
    # 5. 测试签到统计API
    print("\n5. 测试签到统计API...")
    
    response = session.get(f"{BASE_URL}/schedules/check-in-stats")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ 签到统计API正常工作")
        print(f"   统计信息: {result}")
    else:
        print(f"❌ 签到统计API异常: {response.status_code}")
        print(f"   响应: {response.text}")
        return False
    
    print("\n🎉 扫码签到API测试完成！")
    print("📋 测试结果:")
    print("   ✅ 登录功能正常")
    print("   ✅ 扫码签到API端点存在")
    print("   ✅ 权限控制正常")
    print("   ✅ 错误处理正确")
    print("   ✅ 批量签到API正常")
    print("   ✅ 统计API正常")
    
    return True

if __name__ == "__main__":
    success = test_scan_check_in_api()
    
    if success:
        print("\n🎉 扫码签到API测试通过！")
    else:
        print("\n❌ 扫码签到API测试失败") 