#!/usr/bin/env python3
"""
云服务器API测试脚本
部署到云服务器后，运行此脚本测试远程API功能
"""

import requests
import json
import time
from datetime import datetime

# 云服务器配置
CLOUD_SERVER_URL = "http://106.52.214.54"
LOCAL_SERVER_URL = "http://localhost:8000"

def test_cloud_server_api():
    """测试云服务器API功能"""
    print("🌐 测试云服务器API")
    print(f"📍 服务器地址: {CLOUD_SERVER_URL}")
    print("=" * 50)
    
    # 基础连通性测试
    test_endpoints = [
        ("系统欢迎", "/"),
        ("健康检查", "/health"),
        ("测试接口", "/test"),
        ("机构列表", "/institutions"),
        ("用户列表", "/users"),
        ("考生列表", "/candidates"),
        ("考试产品", "/exam-products"),
        ("场地列表", "/venues"),
        ("二维码健康检查", "/qrcode/health"),
        ("生成二维码", "/qrcode/generate-schedule-qr/1"),
    ]
    
    results = []
    
    for name, endpoint in test_endpoints:
        try:
            url = f"{CLOUD_SERVER_URL}{endpoint}"
            print(f"🧪 测试: {name}")
            print(f"   📍 GET {url}")
            
            start_time = time.time()
            response = requests.get(url, timeout=10)
            elapsed_time = time.time() - start_time
            
            if response.status_code == 200:
                print(f"   ✅ 成功 - 状态码: {response.status_code}, 响应时间: {elapsed_time:.3f}s")
                try:
                    data = response.json()
                    if 'message' in data:
                        print(f"   📝 消息: {data['message'][:100]}...")
                except:
                    pass
                results.append({'name': name, 'status': 'SUCCESS', 'time': elapsed_time})
            else:
                print(f"   ❌ 失败 - 状态码: {response.status_code}")
                results.append({'name': name, 'status': 'FAILED', 'time': elapsed_time})
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ 超时")
            results.append({'name': name, 'status': 'TIMEOUT', 'time': 10})
        except requests.exceptions.ConnectionError:
            print(f"   🔌 连接失败")
            results.append({'name': name, 'status': 'CONNECTION_ERROR', 'time': 0})
        except Exception as e:
            print(f"   💥 错误: {e}")
            results.append({'name': name, 'status': 'ERROR', 'time': 0})
        
        print()
    
    # 统计结果
    total = len(results)
    success = sum(1 for r in results if r['status'] == 'SUCCESS')
    print("=" * 50)
    print("📊 测试结果统计:")
    print(f"   总测试数: {total}")
    print(f"   成功数: {success}")
    print(f"   成功率: {success/total*100:.1f}%")
    
    return results

def compare_local_vs_cloud():
    """对比本地和云服务器API响应"""
    print("\n🔄 本地 vs 云服务器API对比测试")
    print("=" * 50)
    
    test_endpoints = ["/", "/health", "/institutions", "/users"]
    
    for endpoint in test_endpoints:
        print(f"🧪 测试端点: {endpoint}")
        
        # 测试本地
        try:
            local_response = requests.get(f"{LOCAL_SERVER_URL}{endpoint}", timeout=5)
            local_status = local_response.status_code
            local_time = local_response.elapsed.total_seconds()
            print(f"   🏠 本地: 状态码 {local_status}, 响应时间 {local_time:.3f}s")
        except:
            print(f"   🏠 本地: 连接失败")
        
        # 测试云服务器
        try:
            cloud_response = requests.get(f"{CLOUD_SERVER_URL}{endpoint}", timeout=10)
            cloud_status = cloud_response.status_code
            cloud_time = cloud_response.elapsed.total_seconds()
            print(f"   ☁️  云端: 状态码 {cloud_status}, 响应时间 {cloud_time:.3f}s")
        except:
            print(f"   ☁️  云端: 连接失败")
        
        print()

def test_api_functionality():
    """测试API具体功能"""
    print("🎯 API功能测试")
    print("=" * 50)
    
    try:
        # 1. 测试机构管理
        print("1️⃣ 测试机构管理功能...")
        response = requests.get(f"{CLOUD_SERVER_URL}/institutions", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 机构列表获取成功，共 {len(data.get('data', []))} 条数据")
        
        # 2. 测试二维码功能
        print("2️⃣ 测试二维码生成功能...")
        response = requests.get(f"{CLOUD_SERVER_URL}/qrcode/generate-schedule-qr/1", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 二维码生成成功: {data.get('message', '')}")
        
        # 3. 测试签到功能
        print("3️⃣ 测试扫码签到功能...")
        response = requests.post(f"{CLOUD_SERVER_URL}/qrcode/scan-checkin", 
                               params={"qr_content": "schedule_1_candidate_1"}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 签到测试成功: {data.get('message', '')}")
        
        # 4. 测试用户管理
        print("4️⃣ 测试用户管理功能...")
        response = requests.get(f"{CLOUD_SERVER_URL}/users", params={"role": "admin"}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 用户筛选成功，管理员用户 {len(data.get('data', []))} 个")
        
    except Exception as e:
        print(f"   ❌ 功能测试出错: {e}")

def main():
    """主函数"""
    print("🚀 云服务器API完整测试")
    print(f"🕐 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 云服务器: {CLOUD_SERVER_URL}")
    print(f"🏠 本地服务器: {LOCAL_SERVER_URL}")
    print()
    
    # 1. 基础连通性测试
    cloud_results = test_cloud_server_api()
    
    # 2. 本地vs云端对比
    compare_local_vs_cloud()
    
    # 3. 功能测试
    test_api_functionality()
    
    # 4. 生成报告
    print("=" * 50)
    print("📋 测试完成!")
    print("💡 提示:")
    print("   - 如果云服务器连接失败，请检查服务是否已部署")
    print("   - 可以使用部署指南中的脚本进行部署")
    print("   - 部署成功后重新运行此测试脚本")

if __name__ == "__main__":
    main()