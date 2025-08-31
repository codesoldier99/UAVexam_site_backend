#!/usr/bin/env python3
"""
快速清空数据库脚本（无确认）
"""

from app.config.database import SessionLocal
from app.models.user import User
from app.models.institution import Institution
from app.models.venue import Venue
from app.models.exam import ExamProduct, ExamRegistration
from app.models.schedule import Schedule
from app.models.checkin import CheckIn

def quick_clear():
    """快速清空所有数据"""
    print("🗑️ 快速清空数据库...")
    
    session = SessionLocal()
    try:
        # 按依赖关系顺序删除
        session.query(CheckIn).delete()
        session.query(Schedule).delete()
        session.query(ExamRegistration).delete()
        session.query(ExamProduct).delete()
        session.query(Venue).delete()
        session.query(User).delete()
        session.query(Institution).delete()
        
        session.commit()
        print("✅ 数据清空完成")
        
        # 显示统计
        print(f"用户: {session.query(User).count()}")
        print(f"机构: {session.query(Institution).count()}")
        print(f"考场: {session.query(Venue).count()}")
        
    except Exception as e:
        session.rollback()
        print(f"❌ 清空失败: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    quick_clear()