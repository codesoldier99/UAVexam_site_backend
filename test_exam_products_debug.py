#!/usr/bin/env python3
"""
考试产品API调试脚本
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from src.dependencies.get_db import get_db
from src.models.exam_product import ExamProduct
from src.services.exam_product import ExamProductService

def test_database_connection():
    """测试数据库连接"""
    print("🔍 测试数据库连接...")
    try:
        # 获取数据库会话
        db_gen = get_db()
        db = next(db_gen)
        
        # 测试基本查询
        print("✅ 数据库连接成功")
        
        # 检查表是否存在
        try:
            count = db.query(ExamProduct).count()
            print(f"✅ exam_products 表存在，当前有 {count} 条记录")
            
            # 测试搜索查询
            try:
                search_term = "%多旋翼%"
                from sqlalchemy import or_
                query = db.query(ExamProduct).filter(
                    or_(
                        ExamProduct.name.ilike(search_term),
                        ExamProduct.description.ilike(search_term),
                        ExamProduct.code.ilike(search_term)
                    )
                )
                
                # 执行查询但不获取结果，只是测试SQL是否有效
                query_str = str(query.statement.compile(compile_kwargs={"literal_binds": True}))
                print(f"✅ 搜索SQL语句生成成功")
                print(f"SQL: {query_str}")
                
                # 尝试执行查询
                results = query.all()
                print(f"✅ 搜索查询执行成功，找到 {len(results)} 条记录")
                
            except Exception as search_error:
                print(f"❌ 搜索查询失败: {search_error}")
                import traceback
                print(f"详细错误: {traceback.format_exc()}")
                
        except Exception as table_error:
            print(f"❌ exam_products 表访问失败: {table_error}")
            import traceback
            print(f"详细错误: {traceback.format_exc()}")
            
    except Exception as db_error:
        print(f"❌ 数据库连接失败: {db_error}")
        import traceback
        print(f"详细错误: {traceback.format_exc()}")
    
    finally:
        try:
            db.close()
        except:
            pass

if __name__ == "__main__":
    test_database_connection()