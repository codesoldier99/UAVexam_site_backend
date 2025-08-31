#!/usr/bin/env python3
"""
本地API测试脚本
用于测试后端API功能，无需ngrok
"""

import requests
import json
from datetime import datetime

# API基础URL
BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    """测试健康检查接口"""
    print("🔍 测试健康检查接口...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False

def test_login():
    """测试登录接口"""
    print("\n🔍 测试登录接口...")
    try:
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200 and "access_token" in result:
            return result["access_token"]
        return None
    except Exception as e:
        print(f"❌ 登录失败: {e}")
        return None

def test_wechat_candidate_info():
    """测试微信考生信息查询接口"""
    print("\n🔍 测试微信考生信息查询接口...")
    try:
        # 测试张三的身份证
        id_card = "110101199001011234"
        response = requests.get(f"{BASE_URL}/wechat/candidate/info-by-idcard?id_card={id_card}")
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 微信考生信息查询失败: {e}")
        return False

def test_wechat_candidate_schedules():
    """测试微信考生日程查询接口"""
    print("\n🔍 测试微信考生日程查询接口...")
    try:
        # 测试微信看板数据接口
        response = requests.get(f"{BASE_URL}/wechat/dashboard")
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 微信看板数据查询失败: {e}")
        return False

def test_venues():
    """测试考场列表接口"""
    print("\n🔍 测试考场列表接口...")
    try:
        response = requests.get(f"{BASE_URL}/venues")
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 考场列表查询失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始本地API测试...")
    print("="*60)
    
    # 测试结果统计
    results = []
    
    # 1. 健康检查
    results.append(("健康检查", test_health()))
    
    # 2. 登录测试
    token = test_login()
    results.append(("管理员登录", token is not None))
    
    # 3. 微信接口测试
    results.append(("微信考生信息", test_wechat_candidate_info()))
    results.append(("微信考生日程", test_wechat_candidate_schedules()))
    
    # 4. 考场接口测试
    results.append(("考场列表", test_venues()))
    
    # 输出测试结果
    print("\n" + "="*60)
    print("📊 测试结果汇总:")
    print("="*60)
    
    success_count = 0
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{test_name:<20} {status}")
        if success:
            success_count += 1
    
    print(f"\n总计: {success_count}/{len(results)} 个接口测试通过")
    
    if success_count == len(results):
        print("🎉 所有API测试通过！后端服务运行正常。")
    else:
        print("⚠️ 部分API测试失败，请检查后端服务状态。")
    
    print("\n💡 提示:")
    print("- 后端服务地址: http://localhost:8000")
    print("- API文档地址: http://localhost:8000/api/v1/docs")
    print("- 如需公网访问，请确保ngrok正常运行")

if __name__ == "__main__":
    main()