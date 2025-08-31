"""
数据库验证脚本 - 检查数据库表结构和数据
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy import text, inspect
from backend.app.config.database import engine
from backend.app.models.schedule import Schedule
from backend.app.models.checkin import CheckIn
from backend.app.models.user import User

def check_database_connection():
    """检查数据库连接"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ 数据库连接正常")
            return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

def check_table_structure():
    """检查表结构"""
    try:
        inspector = inspect(engine)
        
        # 检查schedules表
        if 'schedules' in inspector.get_table_names():
            columns = inspector.get_columns('schedules')
            column_names = [col['name'] for col in columns]
            print(f"✅ schedules表存在，字段: {column_names}")
            
            # 检查新增字段
            required_fields = ['exam_result', 'exam_score', 'max_score', 'pass_score', 'actual_duration', 'result_notes']
            missing_fields = [field for field in required_fields if field not in column_names]
            
            if missing_fields:
                print(f"⚠️  schedules表缺少字段: {missing_fields}")
                return False
            else:
                print("✅ schedules表字段完整")
        else:
            print("❌ schedules表不存在")
            return False
            
        # 检查其他关键表
        required_tables = ['users', 'venues', 'exam_registrations', 'checkins']
        for table in required_tables:
            if table in inspector.get_table_names():
                print(f"✅ {table}表存在")
            else:
                print(f"❌ {table}表不存在")
                return False
                
        return True
        
    except Exception as e:
        print(f"❌ 检查表结构失败: {e}")
        return False

def check_test_data():
    """检查测试数据"""
    try:
        with engine.connect() as connection:
            # 检查用户数据
            result = connection.execute(text("SELECT COUNT(*) FROM users WHERE role = 'candidate'"))
            candidate_count = result.scalar()
            print(f"✅ 考生用户数量: {candidate_count}")
            
            # 检查考场数据
            result = connection.execute(text("SELECT COUNT(*) FROM venues"))
            venue_count = result.scalar()
            print(f"✅ 考场数量: {venue_count}")
            
            # 检查日程数据
            result = connection.execute(text("SELECT COUNT(*) FROM schedules"))
            schedule_count = result.scalar()
            print(f"✅ 日程数量: {schedule_count}")
            
            if candidate_count > 0 and venue_count > 0:
                print("✅ 基础测试数据存在")
                return True
            else:
                print("⚠️  缺少基础测试数据")
                return False
                
    except Exception as e:
        print(f"❌ 检查测试数据失败: {e}")
        return False

def run_migration_if_needed():
    """如果需要，运行数据库迁移"""
    try:
        inspector = inspect(engine)
        columns = inspector.get_columns('schedules')
        column_names = [col['name'] for col in columns]
        
        required_fields = ['exam_result', 'exam_score', 'max_score', 'pass_score', 'actual_duration', 'result_notes']
        missing_fields = [field for field in required_fields if field not in column_names]
        
        if missing_fields:
            print(f"⚠️  需要添加字段: {missing_fields}")
            print("正在运行数据库迁移...")
            
            migration_sql = """
            ALTER TABLE schedules 
            ADD COLUMN IF NOT EXISTS exam_result VARCHAR(20),
            ADD COLUMN IF NOT EXISTS exam_score INTEGER,
            ADD COLUMN IF NOT EXISTS max_score INTEGER DEFAULT 100,
            ADD COLUMN IF NOT EXISTS pass_score INTEGER DEFAULT 70,
            ADD COLUMN IF NOT EXISTS actual_duration INTEGER,
            ADD COLUMN IF NOT EXISTS result_notes TEXT;
            """
            
            with engine.connect() as connection:
                connection.execute(text(migration_sql))
                connection.commit()
                print("✅ 数据库迁移完成")
                return True
        else:
            print("✅ 数据库结构已是最新")
            return True
            
    except Exception as e:
        print(f"❌ 数据库迁移失败: {e}")
        return False

if __name__ == "__main__":
    print("🔍 开始数据库验证")
    print("=" * 50)
    
    if check_database_connection():
        if not check_table_structure():
            print("\n🔧 尝试修复数据库结构...")
            run_migration_if_needed()
            check_table_structure()
        
        check_test_data()
    
    print("\n" + "=" * 50)
    print("🎉 数据库验证完成")