#!/usr/bin/env python3
"""
考试产品数据初始化脚本
运行此脚本将向数据库中添加真实可信的考试产品数据
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.init_exam_products import init_exam_products
from src.db.session import get_db

def main():
    """主函数"""
    print("=" * 60)
    print("考试产品数据初始化脚本")
    print("=" * 60)
    
    try:
        # 获取数据库会话
        db = next(get_db())
        
        # 初始化考试产品数据
        init_exam_products(db)
        
        print("\n✅ 考试产品数据初始化完成！")
        print("\n现在您可以:")
        print("1. 启动服务器: python -m uvicorn src.main:app --reload")
        print("2. 访问API文档: http://localhost:8000/docs")
        print("3. 测试API: python test_exam_products_api.py")
        
    except Exception as e:
        print(f"\n❌ 初始化失败: {e}")
        print("请检查:")
        print("1. 数据库连接是否正常")
        print("2. 数据库表是否已创建")
        print("3. 环境变量是否配置正确")
        
    finally:
        try:
            db.close()
        except:
            pass

if __name__ == "__main__":
    main() 