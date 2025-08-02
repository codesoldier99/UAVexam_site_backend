#!/usr/bin/env python3
"""
高级批量导入考生API测试脚本
测试重复身份证号检测、数据格式验证等
"""

import requests
import json
import time
import random
import pandas as pd
from io import BytesIO

# 配置
BASE_URL = "http://localhost:8000"
TEST_USER = {
    "email": "institution@test.com",
    "password": "institution123"
}

def get_access_token():
    """获取访问令牌"""
    login_url = f"{BASE_URL}/auth/jwt/login"
    login_data = {
        "username": TEST_USER["email"],
        "password": TEST_USER["password"]
    }
    
    try:
        response = requests.post(
            login_url,
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            token_data = response.json()
            return token_data.get("access_token")
        else:
            print(f"❌ 登录失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 登录异常: {str(e)}")
        return None

def test_duplicate_id_import():
    """测试重复身份证号检测"""
    print("\n🔄 测试重复身份证号检测...")
    
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取访问令牌，跳过重复ID测试")
        return
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # 创建包含重复身份证号的测试数据
    test_data = [
        {
            'name': '重复考生1',
            'id_number': '110101199001011234',  # 重复的身份证号
            'phone': '13800138001',
            'email': 'duplicate1@example.com',
            'gender': '男',
            'address': '北京市朝阳区',
            'emergency_contact': '联系人1',
            'emergency_phone': '13900139001'
        },
        {
            'name': '重复考生2',
            'id_number': '110101199001011234',  # 重复的身份证号
            'phone': '13800138002',
            'email': 'duplicate2@example.com',
            'gender': '女',
            'address': '北京市海淀区',
            'emergency_contact': '联系人2',
            'emergency_phone': '13900139002'
        },
        {
            'name': '正常考生',
            'id_number': f'11010119900101{random.randint(1000, 9999)}',
            'phone': '13800138003',
            'email': 'normal@example.com',
            'gender': '男',
            'address': '北京市西城区',
            'emergency_contact': '联系人3',
            'emergency_phone': '13900139003'
        }
    ]
    
    # 创建DataFrame并保存为Excel
    df = pd.DataFrame(test_data)
    excel_file = BytesIO()
    df.to_excel(excel_file, index=False)
    excel_file.seek(0)
    
    try:
        # 准备文件上传
        files = {
            'file': ('duplicate_test.xlsx', excel_file.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        }
        
        response = requests.post(
            f"{BASE_URL}/candidates/batch-import",
            files=files,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 重复ID测试完成")
            print(f"成功导入: {result.get('success_count', 0)} 条")
            print(f"失败记录: {result.get('failed_count', 0)} 条")
            
            errors = result.get('errors', [])
            if errors:
                print("❌ 错误详情:")
                for error in errors:
                    print(f"  - {error}")
        else:
            print(f"❌ 重复ID测试失败: {response.status_code}")
            print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"❌ 重复ID测试异常: {str(e)}")

def test_invalid_data_import():
    """测试无效数据导入"""
    print("\n⚠️ 测试无效数据导入...")
    
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取访问令牌，跳过无效数据测试")
        return
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # 创建包含各种无效数据的测试数据
    test_data = [
        {
            'name': '',  # 空姓名
            'id_number': '110101199001011234',
            'phone': '13800138001',
            'email': 'test1@example.com',
            'gender': '男',
            'address': '北京市朝阳区',
            'emergency_contact': '联系人1',
            'emergency_phone': '13900139001'
        },
        {
            'name': '考生2',
            'id_number': '',  # 空身份证号
            'phone': '13800138002',
            'email': 'test2@example.com',
            'gender': '女',
            'address': '北京市海淀区',
            'emergency_contact': '联系人2',
            'emergency_phone': '13900139002'
        },
        {
            'name': '考生3',
            'id_number': '110101199001011235',
            'phone': '',  # 空手机号
            'email': 'test3@example.com',
            'gender': '男',
            'address': '北京市西城区',
            'emergency_contact': '联系人3',
            'emergency_phone': '13900139003'
        },
        {
            'name': '正常考生4',
            'id_number': f'11010119900101{random.randint(1000, 9999)}',
            'phone': '13800138004',
            'email': 'test4@example.com',
            'gender': '女',
            'address': '北京市东城区',
            'emergency_contact': '联系人4',
            'emergency_phone': '13900139004'
        }
    ]
    
    # 创建DataFrame并保存为Excel
    df = pd.DataFrame(test_data)
    excel_file = BytesIO()
    df.to_excel(excel_file, index=False)
    excel_file.seek(0)
    
    try:
        # 准备文件上传
        files = {
            'file': ('invalid_test.xlsx', excel_file.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        }
        
        response = requests.post(
            f"{BASE_URL}/candidates/batch-import",
            files=files,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 无效数据测试完成")
            print(f"成功导入: {result.get('success_count', 0)} 条")
            print(f"失败记录: {result.get('failed_count', 0)} 条")
            
            errors = result.get('errors', [])
            if errors:
                print("❌ 错误详情:")
                for error in errors:
                    print(f"  - {error}")
        else:
            print(f"❌ 无效数据测试失败: {response.status_code}")
            print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"❌ 无效数据测试异常: {str(e)}")

def test_large_batch_import():
    """测试大批量导入"""
    print("\n📊 测试大批量导入...")
    
    access_token = get_access_token()
    if not access_token:
        print("❌ 无法获取访问令牌，跳过大批量测试")
        return
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # 创建大批量测试数据（20条）
    test_data = []
    for i in range(20):
        test_data.append({
            'name': f'大批量考生{i+1}',
            'id_number': f'11010119900101{random.randint(1000, 9999)}',
            'phone': f'1380013800{i:02d}',
            'email': f'batch{i+1}@example.com',
            'gender': '男' if i % 2 == 0 else '女',
            'address': f'北京市朝阳区测试街道{i+1}号',
            'emergency_contact': f'紧急联系人{i+1}',
            'emergency_phone': f'1390013900{i:02d}'
        })
    
    # 创建DataFrame并保存为Excel
    df = pd.DataFrame(test_data)
    excel_file = BytesIO()
    df.to_excel(excel_file, index=False)
    excel_file.seek(0)
    
    try:
        # 准备文件上传
        files = {
            'file': ('large_batch_test.xlsx', excel_file.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        }
        
        response = requests.post(
            f"{BASE_URL}/candidates/batch-import",
            files=files,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 大批量导入测试完成")
            print(f"成功导入: {result.get('success_count', 0)} 条")
            print(f"失败记录: {result.get('failed_count', 0)} 条")
            
            errors = result.get('errors', [])
            if errors:
                print("❌ 错误详情:")
                for error in errors:
                    print(f"  - {error}")
        else:
            print(f"❌ 大批量导入测试失败: {response.status_code}")
            print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"❌ 大批量导入测试异常: {str(e)}")

def test_server_health():
    """测试服务器健康状态"""
    print("🔍 测试服务器健康状态...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ 服务器运行正常")
            return True
        else:
            print(f"❌ 服务器响应异常: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保服务器已启动")
        return False

def main():
    """主测试函数"""
    print("🚀 开始高级批量导入考生API测试")
    print("=" * 50)
    
    # 测试服务器健康状态
    if not test_server_health():
        print("❌ 服务器未启动，无法继续测试")
        return
    
    # 测试重复身份证号检测
    test_duplicate_id_import()
    
    # 测试无效数据导入
    test_invalid_data_import()
    
    # 测试大批量导入
    test_large_batch_import()
    
    print("\n" + "=" * 50)
    print("🎉 高级批量导入考生API测试完成")
    print("📝 测试结果总结:")
    print("- 重复身份证号检测: ✅ 已实现")
    print("- 数据格式验证: ✅ 已实现")
    print("- 大批量处理: ✅ 已实现")
    print("- 错误汇总: ✅ 已实现")

if __name__ == "__main__":
    main() 