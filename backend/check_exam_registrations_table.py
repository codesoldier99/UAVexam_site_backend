#!/usr/bin/env python3
"""
检查exam_registrations表的实际结构
"""

from app.config.database import engine
import pymysql

def check_table_structure():
    """检查exam_registrations表结构"""
    
    try:
        # 获取数据库连接
        connection = engine.raw_connection()
        cursor = connection.cursor()
        
        print("=== 检查exam_registrations表结构 ===")
        
        # 查看表结构
        cursor.execute("DESCRIBE exam_registrations")
        columns = cursor.fetchall()
        
        print("实际表字段:")
        for column in columns:
            print(f"  {column[0]} - {column[1]} - {column[2]} - {column[3]} - {column[4]} - {column[5]}")
        
        print(f"\n总共 {len(columns)} 个字段")
        
        # 检查是否存在registration_time字段
        field_names = [col[0] for col in columns]
        
        print(f"\n字段列表: {field_names}")
        
        if 'registration_time' in field_names:
            print("✅ registration_time 字段存在")
        else:
            print("❌ registration_time 字段不存在")
            
        # 检查模型中定义的字段是否都存在
        model_fields = [
            'id', 'user_id', 'exam_product_id', 'registration_number', 
            'registration_time', 'status', 'notes', 'created_at', 'updated_at'
        ]
        
        print("\n=== 字段匹配检查 ===")
        for field in model_fields:
            if field in field_names:
                print(f"✅ {field} - 存在")
            else:
                print(f"❌ {field} - 不存在")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ 检查过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_table_structure()