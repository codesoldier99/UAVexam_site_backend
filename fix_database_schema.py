#!/usr/bin/env python3
"""
Direct database schema fix script
Adds missing fields to schedules table without importing the full app
"""

import pymysql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('backend/.env')

def get_db_connection():
    """Get direct database connection"""
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'exam_site_dev_db'),
        charset='utf8mb4'
    )

def check_column_exists(cursor, table_name, column_name):
    """Check if a column exists in the table"""
    cursor.execute(f"""
        SELECT COUNT(*) 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = DATABASE() 
        AND TABLE_NAME = '{table_name}' 
        AND COLUMN_NAME = '{column_name}'
    """)
    return cursor.fetchone()[0] > 0

def add_missing_fields():
    """Add missing fields to schedules table"""
    
    print("🔧 Direct Database Schema Fix")
    print("=" * 50)
    
    try:
        # Connect to database
        connection = get_db_connection()
        cursor = connection.cursor()
        
        print("✅ Connected to database")
        
        # Define the fields to add
        fields_to_add = [
            ("exam_result", "VARCHAR(50) DEFAULT NULL COMMENT '考试结果: PASS/FAIL/ABSENT'"),
            ("exam_score", "DECIMAL(5,2) DEFAULT NULL COMMENT '考试分数'"),
            ("max_score", "DECIMAL(5,2) DEFAULT 100.00 COMMENT '满分'"),
            ("pass_score", "DECIMAL(5,2) DEFAULT 60.00 COMMENT '及格分数'"),
            ("actual_duration", "INT DEFAULT NULL COMMENT '实际考试时长(分钟)'"),
            ("result_notes", "TEXT DEFAULT NULL COMMENT '考试结果备注'")
        ]
        
        # Check current table structure
        cursor.execute("DESCRIBE schedules")
        existing_columns = [row[0] for row in cursor.fetchall()]
        print(f"📋 Current columns: {existing_columns}")
        
        # Add missing fields
        added_count = 0
        for field_name, field_definition in fields_to_add:
            if not check_column_exists(cursor, 'schedules', field_name):
                sql = f"ALTER TABLE schedules ADD COLUMN {field_name} {field_definition}"
                print(f"➕ Adding field: {field_name}")
                cursor.execute(sql)
                added_count += 1
            else:
                print(f"✅ Field already exists: {field_name}")
        
        # Commit changes
        connection.commit()
        
        # Verify the changes
        cursor.execute("DESCRIBE schedules")
        new_columns = [row[0] for row in cursor.fetchall()]
        
        print(f"\n📊 Results:")
        print(f"   - Fields added: {added_count}")
        print(f"   - Total columns now: {len(new_columns)}")
        print(f"   - New columns: {new_columns}")
        
        if added_count > 0:
            print(f"\n🎉 Successfully added {added_count} missing fields!")
        else:
            print(f"\n✅ All fields already exist, no changes needed")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
        
    finally:
        if 'connection' in locals():
            connection.close()
            print("🔌 Database connection closed")

def test_database_access():
    """Test if we can access the database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        connection.close()
        return result[0] == 1
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing database connection...")
    if test_database_access():
        print("✅ Database connection successful")
        add_missing_fields()
    else:
        print("❌ Cannot connect to database")
        print("💡 Please check:")
        print("   - Database server is running")
        print("   - Credentials in backend/.env are correct")
        print("   - Database 'exam_site_dev_db' exists")