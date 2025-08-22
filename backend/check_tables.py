#!/usr/bin/env python3
"""
检查数据库表结构
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from sqlalchemy import create_engine, text
from app.config.database import Base, engine
from app.config.settings import settings
from app.models import *

def check_tables():
    """检查并创建数据库表"""
    try:
        # 本地测试使用localhost连接
        local_database_url = "mysql+pymysql://dev_user:a_good_password_for_dev@localhost:3307/exam_site_dev_db"
        local_engine = create_engine(local_database_url)
        
        print(f"📊 数据库连接: {local_database_url}")
        
        # 创建所有表
        print("\n🔄 创建数据库表...")
        Base.metadata.create_all(bind=local_engine)
        
        # 检查表是否存在
        print("\n📋 检查数据库表:")
        with local_engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            
            print(f"✅ 数据库中共有 {len(tables)} 张表:")
            for i, table in enumerate(sorted(tables), 1):
                print(f"  {i}. {table}")
        
        # 检查表结构
        print("\n🔍 检查表结构:")
        expected_tables = [
            'users', 'institutions', 'venues', 'exam_products', 
            'exam_registrations', 'schedules', 'checkins'
        ]
        
        for table in expected_tables:
            if table in tables:
                print(f"  ✅ {table} - 存在")
            else:
                print(f"  ❌ {table} - 缺失")
        
        # 显示多余的表
        extra_tables = set(tables) - set(expected_tables)
        if extra_tables:
            print(f"\n⚠️  发现 {len(extra_tables)} 张多余的表:")
            for table in sorted(extra_tables):
                print(f"  - {table}")
        else:
            print("\n✅ 没有多余的表!")
            
        return True
        
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False

if __name__ == "__main__":
    success = check_tables()
    sys.exit(0 if success else 1)
