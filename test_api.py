#!/usr/bin/env python3
"""
简单的API测试脚本
"""

import requests
import json

def test_health():
    """测试健康检查接口"""
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        print(f"健康检查 - 状态码: {response.status_code}")
        if response.status_code == 200:
            print(f"健康检查 - 响应: {response.json()}")
            return True
        else:
            print(f"健康检查失败: {response.text}")
            return False
    except Exception as e:
        print(f"健康检查异常: {str(e)}")
        return False

def test_api_docs():
    """测试API文档接口"""
    try:
        response = requests.get('http://localhost:8000/api/v1/docs', timeout=5)
        print(f"API文档 - 状态码: {response.status_code}")
        if response.status_code == 200:
            print("API文档可访问")
            return True
        else:
            print("API文档访问失败")
            return False
    except Exception as e:
        print(f"API文档异常: {str(e)}")
        return False

def test_root():
    """测试根路径"""
    try:
        response = requests.get('http://localhost:8000/', timeout=5)
        print(f"根路径 - 状态码: {response.status_code}")
        if response.status_code == 200:
            print(f"根路径 - 响应: {response.json()}")
            return True
        else:
            print(f"根路径失败: {response.text}")
            return False
    except Exception as e:
        print(f"根路径异常: {str(e)}")
        return False

def main():
    print("🚀 开始API测试")
    print("="*50)
    
    tests = [
        ("健康检查", test_health),
        ("API文档", test_api_docs),
        ("根路径", test_root),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n测试: {test_name}")
        print("-" * 30)
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} - 通过")
            else:
                failed += 1
                print(f"❌ {test_name} - 失败")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name} - 异常: {str(e)}")
    
    print(f"\n{'='*50}")
    print(f"测试结果:")
    print(f"  通过: {passed}")
    print(f"  失败: {failed}")
    print(f"  总计: {passed + failed}")
    
    if failed == 0:
        print("🎉 所有测试都通过了！UAV考点管理系统API运行正常！")
    else:
        print(f"⚠️ 有 {failed} 个测试失败")

if __name__ == "__main__":
    main()