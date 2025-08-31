#!/usr/bin/env python3
"""
测试新实现的三个缺失API接口
"""

import requests
import json
from datetime import datetime

# 配置
BASE_URL = "http://localhost:8000"
TEST_CREDENTIALS = {
    "username": "candidate_011234",
    "password": "011234"
}

def get_auth_token():
    """获取认证token"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            json=TEST_CREDENTIALS,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("access_token")
        else:
            print(f"❌ 登录失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ 登录请求失败: {e}")
        return None

def test_candidate_schedule(token):
    """测试考生日程查询接口"""
    print("\n🔍 测试考生日程查询接口...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/wechat/candidate/schedule",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 考生日程查询成功!")
            print(f"即将到来的考试: {len(data.get('upcoming_exams', []))}")
            print(f"已完成的考试: {len(data.get('completed_exams', []))}")
            print(f"总计: {data.get('summary', {}).get('total_count', 0)}")
            return True
        else:
            print(f"❌ 考生日程查询失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False

def test_qrcode_generation(token):
    """测试二维码生成接口"""
    print("\n📱 测试二维码生成接口...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/wechat/candidate/qrcode",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 二维码生成成功!")
            print(f"备用码: {data.get('backup_code')}")
            print(f"过期时间: {data.get('expires_at')}")
            print(f"刷新间隔: {data.get('refresh_interval')}秒")
            print(f"二维码长度: {len(data.get('qr_code', ''))}")
            return True
        else:
            print(f"❌ 二维码生成失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False

def test_dashboard_data():
    """测试公共看板接口"""
    print("\n📊 测试公共看板接口...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/wechat/dashboard",
            timeout=10
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 看板数据获取成功!")
            
            stats = data.get('statistics', {})
            print(f"今日统计:")
            print(f"  - 总安排: {stats.get('total_scheduled', 0)}")
            print(f"  - 已签到: {stats.get('checked_in', 0)}")
            print(f"  - 进行中: {stats.get('in_progress', 0)}")
            print(f"  - 已完成: {stats.get('completed', 0)}")
            
            venues = data.get('venues', [])
            print(f"考场数量: {len(venues)}")
            
            announcements = data.get('announcements', [])
            print(f"公告数量: {len(announcements)}")
            
            return True
        else:
            print(f"❌ 看板数据获取失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False

def test_existing_apis(token):
    """测试现有的API是否仍然正常工作"""
    print("\n🔄 测试现有API兼容性...")
    
    # 测试身份证查询
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/wechat/candidate/info-by-idcard",
            params={"id_card": "110101199001011234"},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ 身份证查询接口正常")
        else:
            print(f"⚠️ 身份证查询接口异常: {response.status_code}")
    except Exception as e:
        print(f"❌ 身份证查询请求失败: {e}")
    
    # 测试签到历史
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/wechat/candidate/checkin-history",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 签到历史接口正常 (记录数: {len(data)})")
        else:
            print(f"⚠️ 签到历史接口异常: {response.status_code}")
    except Exception as e:
        print(f"❌ 签到历史请求失败: {e}")

def main():
    """主测试函数"""
    print("🚀 开始测试新实现的三个缺失API接口")
    print("=" * 50)
    
    # 1. 获取认证token
    print("🔐 获取认证token...")
    token = get_auth_token()
    
    if not token:
        print("❌ 无法获取认证token，测试终止")
        return
    
    print("✅ 认证token获取成功")
    
    # 2. 测试三个新接口
    results = []
    
    results.append(test_candidate_schedule(token))
    results.append(test_qrcode_generation(token))
    results.append(test_dashboard_data())
    
    # 3. 测试现有API兼容性
    test_existing_apis(token)
    
    # 4. 总结测试结果
    print("\n" + "=" * 50)
    print("📋 测试结果总结:")
    
    success_count = sum(results)
    total_count = len(results)
    
    print(f"✅ 成功: {success_count}/{total_count}")
    print(f"❌ 失败: {total_count - success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 所有新接口测试通过！")
    else:
        print("⚠️ 部分接口需要进一步调试")
    
    print("\n💡 提示:")
    print("- 确保后端服务正在运行 (python -m uvicorn app.main:app --reload)")
    print("- 确保数据库连接正常")
    print("- 确保测试用户数据存在")

if __name__ == "__main__":
    main()