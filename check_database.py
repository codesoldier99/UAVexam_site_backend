#!/usr/bin/env python3
"""
数据库状态检查脚本
检查数据库连接和数据内容
"""

import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from src.core.config import settings

def check_database():
    """检查数据库连接和内容"""
    print("=" * 60)
    print("🔍 数据库状态检查")
    print("=" * 60)
    print(f"⏰ 检查时间: {datetime.now()}")
    print(f"🗄️ 数据库URL: {settings.DATABASE_URL}")
    print()
    
    try:
        # 创建数据库引擎
        engine = create_engine(settings.DATABASE_URL)
        
        # 测试连接
        print("📡 测试数据库连接...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ 数据库连接成功")
            
            # 检查数据库版本
            try:
                result = conn.execute(text("SELECT VERSION()"))
                version = result.fetchone()[0]
                print(f"🐬 MySQL版本: {version}")
            except Exception as e:
                print(f"⚠️ 无法获取数据库版本: {e}")
            
            # 检查表是否存在
            print("\n📋 检查数据库表...")
            tables_query = text("SHOW TABLES")
            result = conn.execute(tables_query)
            tables = [row[0] for row in result.fetchall()]
            
            if tables:
                print(f"✅ 发现 {len(tables)} 个表:")
                for table in sorted(tables):
                    print(f"   - {table}")
                
                # 检查每个表的数据量
                print("\n📊 数据统计:")
                for table in sorted(tables):
                    try:
                        count_query = text(f"SELECT COUNT(*) FROM `{table}`")
                        result = conn.execute(count_query)
                        count = result.fetchone()[0]
                        print(f"   - {table}: {count} 条记录")
                        
                        # 如果有数据，显示几条示例
                        if count > 0 and count <= 5:
                            try:
                                sample_query = text(f"SELECT * FROM `{table}` LIMIT 3")
                                result = conn.execute(sample_query)
                                print(f"     示例数据: {result.fetchall()}")
                            except:
                                pass
                                
                    except Exception as e:
                        print(f"   - {table}: 查询失败 ({e})")
                
            else:
                print("❌ 没有找到任何表")
                print("🔧 建议执行数据库迁移:")
                print("   alembic upgrade head")
                
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        print("\n🔧 可能的解决方案:")
        print("1. 检查MySQL服务是否运行")
        print("2. 确认数据库连接参数")
        print("3. 检查防火墙设置")
        print("4. 验证数据库用户权限")
        
        # 提供常见错误的解决方案
        error_str = str(e).lower()
        if "connection refused" in error_str:
            print("\n📌 连接被拒绝错误:")
            print("   - 确保MySQL服务正在运行")
            print("   - 检查端口3307是否正确")
        elif "access denied" in error_str:
            print("\n📌 访问被拒绝错误:")
            print("   - 检查用户名和密码")
            print("   - 确认用户有数据库访问权限")
        elif "unknown database" in error_str:
            print("\n📌 数据库不存在:")
            print("   - 创建数据库: CREATE DATABASE exam_site_db_dev;")
            
    print("\n" + "=" * 60)

def suggest_init_data():
    """建议初始化数据的方法"""
    print("💡 如果数据库为空，建议创建初始数据:")
    print()
    print("🔧 方法1: 手动执行迁移")
    print("   alembic upgrade head")
    print()
    print("🔧 方法2: 创建样例数据")
    print("   python create_sample_data.py")
    print()
    print("🔧 方法3: 导入测试数据")
    print("   python import_test_data.py")

if __name__ == "__main__":
    check_database()
    suggest_init_data()