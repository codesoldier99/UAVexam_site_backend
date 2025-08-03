#!/usr/bin/env python3
"""
快速API测试脚本
验证修复后的API功能
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_api(endpoint, description):
    """测试单个API端点"""
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
        if response.status_code == 200:
            print(f"✅ {description}: {response.status_code}")
            return True
        else:
            print(f"❌ {description}: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {description}: 连接失败 - {str(e)}")
        return False

def main():
    print("🔧 快速API修复验证")
    print("=" * 40)
    
    tests = [
        ("/", "基础接口"),
        ("/health", "健康检查"),
        ("/batch/candidates/template", "批量操作-考生模板"),
        ("/wx/health", "微信小程序模块"),
        ("/qrcode/health", "二维码模块"),
        ("/realtime/system-status", "实时功能模块"),
        ("/rbac/roles", "权限管理模块"),
        ("/candidates", "考生管理"),
        ("/venues", "场地管理"),
        ("/exam-products", "考试产品"),
        ("/schedules", "排期管理"),
    ]
    
    passed = 0
    for endpoint, description in tests:
        if test_api(endpoint, description):
            passed += 1
    
    print(f"\n📊 测试结果: {passed}/{len(tests)} 通过")
    
    if passed == len(tests):
        print("🎉 所有API功能正常工作！")
    else:
        print("⚠️ 部分API仍有问题，需要进一步检查")

if __name__ == "__main__":
    main()