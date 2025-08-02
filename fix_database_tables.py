#!/usr/bin/env python3
"""
修复数据库表结构问题
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

def check_table_structure(connection, table_name):
    """检查表结构"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            print(f"\n📋 {table_name} 表结构:")
            for column in columns:
                print(f"  - {column[0]}: {column[1]}")
            return [col[0] for col in columns]
    except Exception as e:
        print(f"❌ 检查表结构失败: {e}")
        return []

def fix_exam_products_table(connection):
    """修复考试产品表"""
    try:
        with connection.cursor() as cursor:
            # 检查是否存在status列
            cursor.execute("SHOW COLUMNS FROM exam_products LIKE 'status'")
            if not cursor.fetchone():
                print("🔧 添加 exam_products.status 列...")
                cursor.execute("""
                    ALTER TABLE exam_products 
                    ADD COLUMN status ENUM('active', 'inactive') DEFAULT 'active' 
                    COMMENT '状态'
                """)
                print("✅ exam_products.status 列添加成功")
            else:
                print("✅ exam_products.status 列已存在")
                
    except Exception as e:
        print(f"❌ 修复考试产品表失败: {e}")

def fix_venues_table(connection):
    """修复场地表"""
    try:
        with connection.cursor() as cursor:
            # 检查是否存在type列
            cursor.execute("SHOW COLUMNS FROM venues LIKE 'type'")
            if not cursor.fetchone():
                print("🔧 添加 venues.type 列...")
                cursor.execute("""
                    ALTER TABLE venues 
                    ADD COLUMN type VARCHAR(50) NOT NULL DEFAULT '理论' 
                    COMMENT '考场类型（理论、实操、候考）'
                """)
                print("✅ venues.type 列添加成功")
            else:
                print("✅ venues.type 列已存在")
                
    except Exception as e:
        print(f"❌ 修复场地表失败: {e}")

def create_missing_tables(connection):
    """创建缺失的表"""
    try:
        with connection.cursor() as cursor:
            # 检查并创建exam_products表
            cursor.execute("SHOW TABLES LIKE 'exam_products'")
            if not cursor.fetchone():
                print("🔧 创建 exam_products 表...")
                cursor.execute("""
                    CREATE TABLE exam_products (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL COMMENT '产品名称',
                        description VARCHAR(255) COMMENT '产品描述',
                        status ENUM('active', 'inactive') DEFAULT 'active' COMMENT '状态',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='考试产品表'
                """)
                print("✅ exam_products 表创建成功")
            
            # 检查并创建venues表
            cursor.execute("SHOW TABLES LIKE 'venues'")
            if not cursor.fetchone():
                print("🔧 创建 venues 表...")
                cursor.execute("""
                    CREATE TABLE venues (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL COMMENT '考场名称',
                        type VARCHAR(50) NOT NULL DEFAULT '理论' COMMENT '考场类型（理论、实操、候考）',
                        status ENUM('active', 'inactive') DEFAULT 'active' COMMENT '状态',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='考场资源表'
                """)
                print("✅ venues 表创建成功")
                
    except Exception as e:
        print(f"❌ 创建表失败: {e}")

def insert_test_data(connection):
    """插入测试数据"""
    try:
        with connection.cursor() as cursor:
            # 插入测试考试产品
            cursor.execute("""
                INSERT IGNORE INTO exam_products (name, description, status) VALUES
                ('多旋翼理论考试', '多旋翼无人机理论考试产品', 'active'),
                ('多旋翼实操考试', '多旋翼无人机实操考试产品', 'active'),
                ('固定翼理论考试', '固定翼无人机理论考试产品', 'active')
            """)
            
            # 插入测试场地
            cursor.execute("""
                INSERT IGNORE INTO venues (name, type, status) VALUES
                ('理论考场A', '理论', 'active'),
                ('理论考场B', '理论', 'active'),
                ('实操考场A', '实操', 'active'),
                ('候考场A', '候考', 'active')
            """)
            
            connection.commit()
            print("✅ 测试数据插入成功")
            
    except Exception as e:
        print(f"❌ 插入测试数据失败: {e}")

def main():
    print("🔧 开始修复数据库表结构...")
    print(f"修复时间: {datetime.now()}")
    print("=" * 50)
    
    # 连接数据库
    connection = connect_db()
    if not connection:
        return
    
    try:
        # 1. 创建缺失的表
        print("\n📋 1. 检查并创建缺失的表")
        create_missing_tables(connection)
        
        # 2. 修复表结构
        print("\n📋 2. 修复表结构")
        fix_exam_products_table(connection)
        fix_venues_table(connection)
        
        # 3. 检查表结构
        print("\n📋 3. 检查表结构")
        check_table_structure(connection, "exam_products")
        check_table_structure(connection, "venues")
        
        # 4. 插入测试数据
        print("\n📋 4. 插入测试数据")
        insert_test_data(connection)
        
        # 提交更改
        connection.commit()
        
        print("\n" + "=" * 50)
        print("✅ 数据库表结构修复完成！")
        print("💡 现在可以重新测试API端点了")
        
    except Exception as e:
        print(f"❌ 修复过程中出现错误: {e}")
        connection.rollback()
    finally:
        connection.close()

if __name__ == "__main__":
    main() 