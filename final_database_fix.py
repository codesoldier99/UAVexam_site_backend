#!/usr/bin/env python3
"""
最终数据库修复脚本
解决所有剩余的表结构问题
"""

import pymysql
from datetime import datetime

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3307,
    'user': 'root',
    'password': 'a_secret_password',
    'database': 'exam_site_db_dev',
    'charset': 'utf8mb4'
}

def connect_db():
    """连接数据库"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        print("✅ 数据库连接成功")
        return connection
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return None

def fix_exam_products_table(connection):
    """修复考试产品表"""
    try:
        with connection.cursor() as cursor:
            # 检查并修复duration_minutes字段
            cursor.execute("SHOW COLUMNS FROM exam_products LIKE 'duration_minutes'")
            if cursor.fetchone():
                print("🔧 修复 exam_products.duration_minutes 字段...")
                cursor.execute("""
                    ALTER TABLE exam_products 
                    MODIFY COLUMN duration_minutes INT DEFAULT 120
                """)
                print("✅ exam_products.duration_minutes 字段修复成功")
            else:
                print("✅ exam_products.duration_minutes 字段不存在，无需修复")
                
    except Exception as e:
        print(f"❌ 修复考试产品表失败: {e}")

def fix_venues_table(connection):
    """修复场地表"""
    try:
        with connection.cursor() as cursor:
            # 检查并添加status列
            cursor.execute("SHOW COLUMNS FROM venues LIKE 'status'")
            if not cursor.fetchone():
                print("🔧 添加 venues.status 列...")
                cursor.execute("""
                    ALTER TABLE venues 
                    ADD COLUMN status ENUM('active', 'inactive') DEFAULT 'active' 
                    COMMENT '状态'
                """)
                print("✅ venues.status 列添加成功")
            else:
                print("✅ venues.status 列已存在")
                
    except Exception as e:
        print(f"❌ 修复场地表失败: {e}")

def check_and_fix_all_tables(connection):
    """检查并修复所有表"""
    try:
        with connection.cursor() as cursor:
            # 获取所有表
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            print(f"📋 数据库中的表: {tables}")
            
            # 检查每个表的结构
            for table in tables:
                print(f"\n🔍 检查表: {table}")
                cursor.execute(f"DESCRIBE {table}")
                columns = cursor.fetchall()
                for column in columns:
                    print(f"  - {column[0]}: {column[1]}")
                    
    except Exception as e:
        print(f"❌ 检查表结构失败: {e}")

def insert_test_data(connection):
    """插入测试数据"""
    try:
        with connection.cursor() as cursor:
            # 插入测试考试产品（包含所有必需字段）
            cursor.execute("""
                INSERT IGNORE INTO exam_products 
                (name, description, status, duration_minutes, code, category, exam_type, exam_class, exam_level, theory_pass_score, practical_pass_score, training_hours, price, training_price) 
                VALUES
                ('测试考试产品A', '这是一个测试产品', 'active', 120, 'TEST001', 'VLOS', 'MULTIROTOR', 'AGRICULTURE', 'PILOT', 80, 80, 40, 1000.0, 2000.0),
                ('测试考试产品B', '这是另一个测试产品', 'active', 90, 'TEST002', 'BVLOS', 'FIXED_WING', 'POWER_INSPECTION', 'CAPTAIN', 85, 85, 60, 1500.0, 3000.0)
            """)
            
            # 插入测试场地
            cursor.execute("""
                INSERT IGNORE INTO venues (name, type, status, description, capacity) VALUES
                ('理论考场A', '理论', 'active', '标准理论考场', 50),
                ('理论考场B', '理论', 'active', '备用理论考场', 30),
                ('实操考场A', '实操', 'active', '标准实操考场', 20),
                ('候考场A', '候考', 'active', '考生候考区域', 100)
            """)
            
            connection.commit()
            print("✅ 测试数据插入成功")
            
    except Exception as e:
        print(f"❌ 插入测试数据失败: {e}")

def main():
    print("🔧 开始最终数据库修复...")
    print(f"修复时间: {datetime.now()}")
    print("=" * 50)
    
    # 连接数据库
    connection = connect_db()
    if not connection:
        return
    
    try:
        # 1. 检查所有表结构
        print("\n📋 1. 检查所有表结构")
        check_and_fix_all_tables(connection)
        
        # 2. 修复表结构
        print("\n📋 2. 修复表结构")
        fix_exam_products_table(connection)
        fix_venues_table(connection)
        
        # 3. 再次检查表结构
        print("\n📋 3. 修复后检查表结构")
        check_and_fix_all_tables(connection)
        
        # 4. 插入测试数据
        print("\n📋 4. 插入测试数据")
        insert_test_data(connection)
        
        # 提交更改
        connection.commit()
        
        print("\n" + "=" * 50)
        print("✅ 最终数据库修复完成！")
        print("💡 现在可以重新测试API端点了")
        
    except Exception as e:
        print(f"❌ 修复过程中出现错误: {e}")
        connection.rollback()
    finally:
        connection.close()

if __name__ == "__main__":
    main() 