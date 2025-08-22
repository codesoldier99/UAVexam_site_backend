#!/usr/bin/env python3
"""
本地环境初始化测试数据脚本
使用localhost连接数据库
"""

import sys
import os
import requests
import json
from datetime import datetime

# API基础URL
BASE_URL = "http://localhost:8000/api/v1"

def test_database_connection():
    """测试数据库连接"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API服务连接成功")
            return True
        else:
            print(f"❌ API服务连接失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API服务连接失败: {e}")
        return False

def create_admin_user():
    """创建管理员用户"""
    try:
        # 注册管理员
        register_data = {
            "username": "admin",
            "password": "admin123",
            "email": "admin@example.com",
            "full_name": "系统管理员",
            "phone": "13800138000"
        }
        
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code == 200:
            print("✅ 管理员用户创建成功")
            return True
        else:
            print(f"⚠️ 管理员用户创建响应: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ 管理员用户创建失败: {e}")
        return False

def login_admin():
    """登录管理员获取token"""
    try:
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            print("✅ 管理员登录成功")
            return token_data["access_token"]
        else:
            print(f"❌ 管理员登录失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ 管理员登录失败: {e}")
        return None

def create_institution(token):
    """创建测试机构"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "name": "测试培训机构",
            "code": "TEST001",
            "type": "培训机构",
            "contact_person": "张老师",
            "contact_phone": "13800138000",
            "contact_email": "test@example.com",
            "address": "北京市朝阳区测试路123号"
        }
        
        response = requests.post(f"{BASE_URL}/institutions/", params=params, headers=headers)
        if response.status_code == 200:
            institution = response.json()
            print("✅ 测试机构创建成功")
            return institution["id"]
        else:
            print(f"❌ 测试机构创建失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ 测试机构创建失败: {e}")
        return None

def create_institution_user(token):
    """创建机构用户"""
    try:
        register_data = {
            "username": "institution_user",
            "password": "123456",
            "email": "institution@example.com",
            "full_name": "机构管理员",
            "phone": "13800138001"
        }
        
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code == 200:
            print("✅ 机构用户创建成功")
            return True
        else:
            print(f"⚠️ 机构用户创建响应: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ 机构用户创建失败: {e}")
        return False

def test_institution_endpoints(token):
    """测试机构管理API端点"""
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n🧪 开始测试机构管理API端点...")
    
    # 1. 测试获取机构列表
    try:
        response = requests.get(f"{BASE_URL}/institutions/", headers=headers)
        if response.status_code == 200:
            institutions = response.json()
            print(f"✅ 获取机构列表成功 - 共{institutions.get('total', 0)}个机构")
        else:
            print(f"❌ 获取机构列表失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取机构列表失败: {e}")
    
    # 2. 测试创建机构
    try:
        institution_params = {
            "name": f"API测试机构-{datetime.now().strftime('%H%M%S')}",
            "code": f"API{datetime.now().strftime('%H%M%S')}",
            "type": "培训机构",
            "contact_person": "API测试员",
            "contact_phone": "13900139000",
            "contact_email": "apitest@example.com",
            "address": "API测试地址"
        }
        
        response = requests.post(f"{BASE_URL}/institutions/", params=institution_params, headers=headers)
        if response.status_code == 200:
            institution = response.json()
            institution_id = institution["id"]
            print(f"✅ 创建机构成功 - ID: {institution_id}")
            
            # 3. 测试获取机构详情
            response = requests.get(f"{BASE_URL}/institutions/{institution_id}", headers=headers)
            if response.status_code == 200:
                print(f"✅ 获取机构详情成功")
            else:
                print(f"❌ 获取机构详情失败: {response.status_code}")
            
            # 4. 测试更新机构
            update_params = {
                "name": f"API测试机构-更新-{datetime.now().strftime('%H%M%S')}",
                "contact_person": "更新测试员"
            }
            response = requests.put(f"{BASE_URL}/institutions/{institution_id}", params=update_params, headers=headers)
            if response.status_code == 200:
                print(f"✅ 更新机构成功")
            else:
                print(f"❌ 更新机构失败: {response.status_code}")
                
        else:
            print(f"❌ 创建机构失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ 测试机构API失败: {e}")

def main():
    """主函数"""
    print("🚀 开始本地环境测试数据初始化...")
    
    # 1. 测试数据库连接
    if not test_database_connection():
        print("❌ 请确保API服务正在运行 (docker-compose up -d)")
        return
    
    # 2. 创建管理员用户
    create_admin_user()
    
    # 3. 登录获取token
    token = login_admin()
    if not token:
        print("❌ 无法获取管理员token，停止初始化")
        return
    
    # 4. 创建测试机构
    institution_id = create_institution(token)
    
    # 5. 创建机构用户
    create_institution_user(token)
    
    # 6. 测试机构管理API
    test_institution_endpoints(token)
    
    print("\n🎉 测试数据初始化完成!")
    print("\n📋 测试账号信息:")
    print("管理员: admin / admin123")
    print("机构用户: institution_user / 123456")
    print("\n🔗 API文档: http://localhost:8000/api/v1/docs")
    print("🌐 前端地址: http://localhost:3000")

if __name__ == "__main__":
    main()
