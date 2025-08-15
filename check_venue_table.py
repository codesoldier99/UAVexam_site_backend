#!/usr/bin/env python3
"""
检查venues表结构
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from sqlalchemy import text
from src.db.session import SessionLocal

def check_venue_table():
    """检查venues表的当前结构"""
    db = SessionLocal()
    try:
        # 查看表结构
        result = db.execute(text("DESCRIBE venues"))
        print("当前venues表结构:")
        print("=" * 60)
        for row in result:
            print(f"{row[0]:<20} {row[1]:<20} {row[2]:<10} {row[3]:<10} {row[4] or '':<20} {row[5] or ''}")
        
        print("\n" + "=" * 60)
        
        # 查看现有数据
        result = db.execute(text("SELECT * FROM venues LIMIT 5"))
        print("现有数据 (前5条):")
        print("=" * 60)
        for row in result:
            print(row)
            
    except Exception as e:
        print(f"错误: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_venue_table()