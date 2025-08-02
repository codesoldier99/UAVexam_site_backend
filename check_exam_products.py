#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据库中的考试产品数据
"""

import requests
import json
from datetime import datetime, timedelta

# API基础URL
BASE_URL = "http://localhost:8000"

def check_exam_products():
    """检查考试产品数据"""
    print("🔍 检查数据库中的考试产品数据...")
    
    # 1. 登录
    print("\n1. 登录...")
    login_data = {
        "username": "admin@exam.com",
        "password": "admin123"
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/auth/jwt/login", data=login_data)
        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data.get("access_token")
            print(f"✅ 登录成功")
        else:
            print(f"❌ 登录失败: {login_response.status_code}")
            return
    except Exception as e:
        print(f"❌ 登录异常: {e}")
        return
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # 2. 检查考试产品列表
    print("\n2. 检查考试产品列表...")
    try:
        products_response = requests.get(
            f"{BASE_URL}/exam-products/",
            headers=headers
        )
        
        if products_response.status_code == 200:
            products_data = products_response.json()
            products = products_data.get('items', [])
            print(f"✅ 找到 {len(products)} 个考试产品")
            
            for i, product in enumerate(products):
                print(f"   产品{i+1}: ID={product.get('id')}, 名称={product.get('name')}, 代码={product.get('code')}")
        else:
            print(f"❌ 获取考试产品失败: {products_response.status_code}")
            print(products_response.text)
    except Exception as e:
        print(f"❌ 获取考试产品异常: {e}")
    
    # 3. 检查机构列表
    print("\n3. 检查机构列表...")
    try:
        institutions_response = requests.get(
            f"{BASE_URL}/institutions/",
            headers=headers
        )
        
        if institutions_response.status_code == 200:
            institutions_data = institutions_response.json()
            institutions = institutions_data.get('items', [])
            print(f"✅ 找到 {len(institutions)} 个机构")
            
            for i, institution in enumerate(institutions[:5]):
                print(f"   机构{i+1}: ID={institution.get('id')}, 名称={institution.get('name')}")
        else:
            print(f"❌ 获取机构失败: {institutions_response.status_code}")
    except Exception as e:
        print(f"❌ 获取机构异常: {e}")
    
    # 4. 检查考场列表
    print("\n4. 检查考场列表...")
    try:
        venues_response = requests.get(
            f"{BASE_URL}/venues/",
            headers=headers
        )
        
        if venues_response.status_code == 200:
            venues_data = venues_response.json()
            venues = venues_data.get('items', [])
            print(f"✅ 找到 {len(venues)} 个考场")
            
            for i, venue in enumerate(venues[:5]):
                print(f"   考场{i+1}: ID={venue.get('id')}, 名称={venue.get('name')}")
        else:
            print(f"❌ 获取考场失败: {venues_response.status_code}")
    except Exception as e:
        print(f"❌ 获取考场异常: {e}")
    
    print("\n🎯 检查完成!")

if __name__ == "__main__":
    check_exam_products() 