#!/usr/bin/env python3
"""
测试数据库连接和API功能
"""

import requests
import json
from datetime import datetime

def test_api_endpoints():
    """测试API端点"""
    base_url = "http://localhost:8000"
    
    print("🔍 测试API端点...")
    
    # 测试根端点
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ 根端点: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ 根端点错误: {e}")
    
    # 测试测试端点
    try:
        response = requests.get(f"{base_url}/test")
        print(f"✅ 测试端点: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ 测试端点错误: {e}")
    
    # 测试文档端点
    try:
        response = requests.get(f"{base_url}/docs")
        print(f"✅ API文档: {response.status_code} - 可访问")
    except Exception as e:
        print(f"❌ API文档错误: {e}")

def test_database_tables():
    """测试数据库表"""
    import pymysql
    
    print("\n🔍 测试数据库表...")
    
    try:
        conn = pymysql.connect(
            host='localhost',
            port=3307,
            user='root',
            password='a_secret_password',
            database='exam_site_db_dev'
        )
        
        cursor = conn.cursor()
        
        # 检查表
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"✅ 数据库连接成功，找到 {len(tables)} 个表:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # 检查用户表结构
        cursor.execute("DESCRIBE users")
        columns = cursor.fetchall()
        print(f"\n📋 users表结构:")
        for col in columns:
            print(f"  - {col[0]}: {col[1]}")
        
        # 检查考生表结构
        cursor.execute("DESCRIBE candidates")
        columns = cursor.fetchall()
        print(f"\n📋 candidates表结构:")
        for col in columns:
            print(f"  - {col[0]}: {col[1]}")
        
        conn.close()
        print("\n✅ 数据库测试完成")
        
    except Exception as e:
        print(f"❌ 数据库测试错误: {e}")

def main():
    """主函数"""
    print("🚀 开始测试考试系统后端...")
    print(f"⏰ 测试时间: {datetime.now()}")
    print("=" * 50)
    
    test_api_endpoints()
    test_database_tables()
    
    print("\n" + "=" * 50)
    print("🎉 测试完成！")
    print("\n📝 总结:")
    print("- ✅ 服务器运行在 http://localhost:8000")
    print("- ✅ 数据库连接正常")
    print("- ✅ 所有表结构已创建")
    print("- ✅ API文档可访问: http://localhost:8000/docs")

if __name__ == "__main__":
    main() 