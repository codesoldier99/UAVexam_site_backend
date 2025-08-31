#!/usr/bin/env python3
"""
测试数据库连接
"""

try:
    from app.config.database import engine, SessionLocal
    from app.models.user import User
    print("✅ 模块导入成功")
    
    # 测试数据库连接
    session = SessionLocal()
    user_count = session.query(User).count()
    print(f"✅ 数据库连接成功，当前用户数: {user_count}")
    session.close()
    
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()