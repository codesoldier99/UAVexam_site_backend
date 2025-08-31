"""
数据库迁移脚本 - 为Schedule表添加考试结果字段
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.config.database import engine

def migrate_schedule_table():
    """为Schedule表添加考试结果相关字段"""
    
    migration_sql = """
    -- 添加考试结果相关字段
    ALTER TABLE schedules 
    ADD COLUMN IF NOT EXISTS exam_result VARCHAR(20),
    ADD COLUMN IF NOT EXISTS exam_score INTEGER,
    ADD COLUMN IF NOT EXISTS max_score INTEGER DEFAULT 100,
    ADD COLUMN IF NOT EXISTS pass_score INTEGER DEFAULT 70,
    ADD COLUMN IF NOT EXISTS actual_duration INTEGER,
    ADD COLUMN IF NOT EXISTS result_notes TEXT;
    """
    
    try:
        with engine.connect() as connection:
            connection.execute(text(migration_sql))
            connection.commit()
            print("✅ Schedule表字段迁移成功")
            
            # 验证字段是否添加成功
            verify_sql = """
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'schedules' 
            AND COLUMN_NAME IN ('exam_result', 'exam_score', 'max_score', 'pass_score', 'actual_duration', 'result_notes');
            """
            
            result = connection.execute(text(verify_sql))
            columns = [row[0] for row in result]
            print(f"✅ 已添加字段: {columns}")
            
    except Exception as e:
        print(f"❌ 迁移失败: {e}")

if __name__ == "__main__":
    migrate_schedule_table()