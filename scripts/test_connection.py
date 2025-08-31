#!/usr/bin/env python3
"""
数据库连接测试脚本
"""

import sys
import os

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from sqlalchemy import create_engine, text
    from app.config.settings import settings
    
    print("🔍 测试数据库连接...")
    print(f"数据库URL: {settings.database_url}")
    
    # 创建引擎
    engine = create_engine(settings.database_url)
    
    # 测试连接
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ 数据库连接成功！")
        
        # 检查表是否存在
        tables = conn.execute(text("SHOW TABLES")).fetchall()
        print(f"📋 数据库中有 {len(tables)} 个表:")
        for table in tables:
            print(f"   - {table[0]}")
            
except Exception as e:
    print(f"❌ 数据库连接失败: {e}")
    sys.exit(1)