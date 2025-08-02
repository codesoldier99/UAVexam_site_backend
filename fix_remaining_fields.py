#!/usr/bin/env python3
"""
修复剩余的数据库字段默认值问题
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

def fix_exam_products_fields(connection):
    """修复考试产品表的字段默认值"""
    try:
        with connection.cursor() as cursor:
            # 修复code字段
            cursor.execute("SHOW COLUMNS FROM exam_products LIKE 'code'")
            if cursor.fetchone():
                print("🔧 修复 exam_products.code 字段默认值...")
                cursor.execute("""
                    ALTER TABLE exam_products 
                    MODIFY COLUMN code VARCHAR(50) DEFAULT 'PROD_001'
                """)
                print("✅ exam_products.code 字段修复成功")
            
            # 修复其他必需字段
            fields_to_fix = [
                ('duration_minutes', 'INT DEFAULT 120'),
                ('category', "ENUM('VLOS','BVLOS') DEFAULT 'VLOS'"),
                ('exam_type', "ENUM('MULTIROTOR','FIXED_WING','VTOL') DEFAULT 'MULTIROTOR'"),
                ('exam_class', "ENUM('AGRICULTURE','POWER_INSPECTION','FILM_PHOTOGRAPHY','LOGISTICS') DEFAULT 'AGRICULTURE'"),
                ('exam_level', "ENUM('PILOT','CAPTAIN','INSTRUCTOR') DEFAULT 'PILOT'"),
                ('theory_pass_score', 'INT DEFAULT 80'),
                ('practical_pass_score', 'INT DEFAULT 80'),
                ('training_hours', 'INT DEFAULT 40'),
                ('price', 'FLOAT DEFAULT 1000.0'),
                ('training_price', 'FLOAT DEFAULT 2000.0')
            ]
            
            for field_name, field_def in fields_to_fix:
                cursor.execute(f"SHOW COLUMNS FROM exam_products LIKE '{field_name}'")
                if cursor.fetchone():
                    print(f"🔧 修复 exam_products.{field_name} 字段默认值...")
                    cursor.execute(f"""
                        ALTER TABLE exam_products 
                        MODIFY COLUMN {field_name} {field_def}
                    """)
                    print(f"✅ exam_products.{field_name} 字段修复成功")
                
    except Exception as e:
        print(f"❌ 修复考试产品表字段失败: {e}")

def fix_venues_fields(connection):
    """修复场地表的字段默认值"""
    try:
        with connection.cursor() as cursor:
            # 修复capacity字段
            cursor.execute("SHOW COLUMNS FROM venues LIKE 'capacity'")
            if cursor.fetchone():
                print("🔧 修复 venues.capacity 字段默认值...")
                cursor.execute("""
                    ALTER TABLE venues 
                    MODIFY COLUMN capacity INT DEFAULT 50
                """)
                print("✅ venues.capacity 字段修复成功")
            
            # 修复description字段
            cursor.execute("SHOW COLUMNS FROM venues LIKE 'description'")
            if cursor.fetchone():
                print("🔧 修复 venues.description 字段默认值...")
                cursor.execute("""
                    ALTER TABLE venues 
                    MODIFY COLUMN description TEXT DEFAULT '标准考场'
                """)
                print("✅ venues.description 字段修复成功")
                
    except Exception as e:
        print(f"❌ 修复场地表字段失败: {e}")

def test_api_creation(connection):
    """测试API创建功能"""
    try:
        with connection.cursor() as cursor:
            # 测试创建考试产品
            print("\n🧪 测试创建考试产品...")
            cursor.execute("""
                INSERT INTO exam_products (name, description) VALUES
                ('测试产品', '这是一个测试产品')
            """)
            product_id = cursor.lastrowid
            print(f"✅ 考试产品创建成功，ID: {product_id}")
            
            # 测试创建场地
            print("🧪 测试创建场地...")
            cursor.execute("""
                INSERT INTO venues (name, type) VALUES
                ('测试考场', '理论')
            """)
            venue_id = cursor.lastrowid
            print(f"✅ 场地创建成功，ID: {venue_id}")
            
            # 清理测试数据
            cursor.execute("DELETE FROM exam_products WHERE id = %s", (product_id,))
            cursor.execute("DELETE FROM venues WHERE id = %s", (venue_id,))
            print("🧹 测试数据已清理")
            
            connection.commit()
            
    except Exception as e:
        print(f"❌ API创建测试失败: {e}")
        connection.rollback()

def main():
    print("🔧 开始修复剩余字段默认值...")
    print(f"修复时间: {datetime.now()}")
    print("=" * 50)
    
    # 连接数据库
    connection = connect_db()
    if not connection:
        return
    
    try:
        # 1. 修复考试产品表字段
        print("\n📋 1. 修复考试产品表字段")
        fix_exam_products_fields(connection)
        
        # 2. 修复场地表字段
        print("\n📋 2. 修复场地表字段")
        fix_venues_fields(connection)
        
        # 3. 测试API创建功能
        print("\n📋 3. 测试API创建功能")
        test_api_creation(connection)
        
        # 提交更改
        connection.commit()
        
        print("\n" + "=" * 50)
        print("✅ 剩余字段修复完成！")
        print("💡 现在可以测试POST API端点了")
        
    except Exception as e:
        print(f"❌ 修复过程中出现错误: {e}")
        connection.rollback()
    finally:
        connection.close()

if __name__ == "__main__":
    main() 