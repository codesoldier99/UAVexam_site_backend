#!/usr/bin/env python3
"""
API状态检查脚本
检查所有主要API接口的可用性和功能
"""

import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_api_endpoint(method, endpoint, data=None, headers=None, auth=None):
    """测试单个API端点"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, auth=auth)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers, auth=auth)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=headers, auth=auth)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, auth=auth)
        
        return {
            "status_code": response.status_code,
            "success": response.status_code < 400,
            "response": response.json() if response.content else None,
            "error": None
        }
    except Exception as e:
        return {
            "status_code": None,
            "success": False,
            "response": None,
            "error": str(e)
        }

def main():
    print("🔍 API功能状态检查")
    print("=" * 60)
    
    # 测试基础接口
    print("\n📡 基础接口")
    tests = [
        ("GET", "/", "根路径"),
        ("GET", "/health", "健康检查"),
        ("GET", "/test", "测试接口"),
        ("GET", "/docs", "API文档")
    ]
    
    for method, endpoint, description in tests:
        result = test_api_endpoint(method, endpoint)
        status = "✅" if result["success"] else "❌"
        print(f"  {status} {description}: {result['status_code']}")
    
    # 测试数据管理接口（不需要认证的）
    print("\n📊 数据查询接口")
    data_tests = [
        ("GET", "/candidates", "考生列表"),
        ("GET", "/exam-products", "考试产品列表"),
        ("GET", "/venues", "场地列表"),
        ("GET", "/schedules", "排期列表"),
        ("GET", "/institutions", "机构列表"),
    ]
    
    for method, endpoint, description in data_tests:
        result = test_api_endpoint(method, endpoint)
        status = "✅" if result["success"] else "❌"
        if result["success"]:
            # 检查返回数据结构
            resp = result["response"]
            if isinstance(resp, dict) and "data" in resp:
                data_count = len(resp["data"]) if isinstance(resp["data"], list) else "N/A"
                print(f"  {status} {description}: {result['status_code']} (数据: {data_count}条)")
            else:
                print(f"  {status} {description}: {result['status_code']}")
        else:
            error_msg = result["response"].get("detail", "未知错误") if result["response"] else result["error"]
            print(f"  {status} {description}: {result['status_code']} - {error_msg}")
    
    # 测试批量操作接口
    print("\n📦 批量操作接口")
    batch_tests = [
        ("GET", "/batch/candidates/template", "考生导入模板下载"),
        ("GET", "/batch/schedules/candidates-available?exam_date=2025-08-15", "可排期考生查询"),
    ]
    
    for method, endpoint, description in batch_tests:
        result = test_api_endpoint(method, endpoint)
        status = "✅" if result["success"] else "❌"
        print(f"  {status} {description}: {result['status_code']}")
    
    # 测试微信小程序接口
    print("\n📱 微信小程序接口")
    wx_tests = [
        ("GET", "/wx/health", "小程序健康检查"),
        ("POST", "/wx/login-by-idcard?id_card=110101199001011234", "身份证登录"),
        ("GET", "/wx/candidate/1/my-qrcode", "考生二维码"),
        ("GET", "/wx/candidate/1/my-schedules", "考生日程"),
    ]
    
    for method, endpoint, description in wx_tests:
        result = test_api_endpoint(method, endpoint)
        status = "✅" if result["success"] else "❌"
        if not result["success"] and result["response"]:
            error_msg = result["response"].get("detail", "未知错误")
            print(f"  {status} {description}: {result['status_code']} - {error_msg}")
        else:
            print(f"  {status} {description}: {result['status_code']}")
    
    # 测试二维码和签到接口
    print("\n🔲 二维码和签到接口")
    qr_tests = [
        ("GET", "/qrcode/health", "二维码模块健康检查"),
        ("GET", "/qrcode/generate-schedule-qr/1", "生成排期二维码"),
        ("POST", "/qrcode/checkin-by-schedule", "扫码签到"),
    ]
    
    for method, endpoint, description in qr_tests:
        result = test_api_endpoint(method, endpoint)
        status = "✅" if result["success"] else "❌"
        print(f"  {status} {description}: {result['status_code']}")
    
    # 测试实时功能接口
    print("\n⚡ 实时功能接口")
    realtime_tests = [
        ("GET", "/realtime/queue-status/1", "排队状态查询"),
        ("GET", "/realtime/venue-status", "考场状态"),
        ("GET", "/realtime/public-board", "公共看板"),
        ("GET", "/realtime/system-status", "系统状态"),
    ]
    
    for method, endpoint, description in realtime_tests:
        result = test_api_endpoint(method, endpoint)
        status = "✅" if result["success"] else "❌"
        print(f"  {status} {description}: {result['status_code']}")
    
    # 测试权限管理接口
    print("\n🔒 权限管理接口")
    rbac_tests = [
        ("GET", "/rbac/my-permissions", "我的权限"),
        ("GET", "/rbac/roles", "角色列表"),
        ("GET", "/rbac/data-access-check", "数据访问检查"),
    ]
    
    for method, endpoint, description in rbac_tests:
        result = test_api_endpoint(method, endpoint)
        status = "✅" if result["success"] else "❌"
        print(f"  {status} {description}: {result['status_code']}")
    
    print(f"\n🏁 API状态检查完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("📝 详细API文档: http://localhost:8000/docs")

if __name__ == "__main__":
    main()