#!/usr/bin/env python3
"""
清空数据库脚本
删除所有业务数据，保留表结构
"""

import sys
from sqlalchemy import text

try:
    from app.config.database import SessionLocal, engine
    from app.models.user import User
    from app.models.institution import Institution
    from app.models.venue import Venue
    from app.models.exam import ExamProduct, ExamRegistration
    from app.models.schedule import Schedule
    from app.models.checkin import CheckIn
    print("✅ 模块导入成功")
except Exception as e:
    print(f"❌ 模块导入失败: {e}")
    sys.exit(1)

def clear_all_data():
    """清空所有数据表"""
    print("🗑️  开始清空数据库...")
    print("⚠️  警告：此操作将删除所有业务数据！")
    
    # 确认操作
    confirm = input("请输入 'YES' 确认删除所有数据: ")
    if confirm != "YES":
        print("❌ 操作已取消")
        return False
    
    session = SessionLocal()
    
    try:
        print("📋 正在删除数据...")
        
        # 方法1：使用ORM删除（推荐，安全）
        print("  - 删除签到记录...")
        deleted_checkins = session.query(CheckIn).delete()
        print(f"    删除了 {deleted_checkins} 条签到记录")
        
        print("  - 删除考试日程...")
        deleted_schedules = session.query(Schedule).delete()
        print(f"    删除了 {deleted_schedules} 条考试日程")
        
        print("  - 删除报名记录...")
        deleted_registrations = session.query(ExamRegistration).delete()
        print(f"    删除了 {deleted_registrations} 条报名记录")
        
        print("  - 删除考试产品...")
        deleted_products = session.query(ExamProduct).delete()
        print(f"    删除了 {deleted_products} 个考试产品")
        
        print("  - 删除考场...")
        deleted_venues = session.query(Venue).delete()
        print(f"    删除了 {deleted_venues} 个考场")
        
        print("  - 删除用户...")
        deleted_users = session.query(User).delete()
        print(f"    删除了 {deleted_users} 个用户")
        
        print("  - 删除机构...")
        deleted_institutions = session.query(Institution).delete()
        print(f"    删除了 {deleted_institutions} 个机构")
        
        # 提交事务
        session.commit()
        print("✅ 数据删除完成")
        
        return True
        
    except Exception as e:
        session.rollback()
        print(f"❌ 删除数据失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()

def reset_auto_increment():
    """重置自增ID"""
    print("🔄 重置自增ID...")
    
    try:
        with engine.connect() as conn:
            # 禁用外键检查
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            
            # 重置所有表的自增ID
            tables = ['checkins', 'schedules', 'exam_registrations', 'exam_products', 'venues', 'users', 'institutions']
            for table in tables:
                conn.execute(text(f"ALTER TABLE {table} AUTO_INCREMENT = 1"))
                print(f"  - 重置表 {table} 的自增ID")
            
            # 启用外键检查
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            conn.commit()
            
        print("✅ 自增ID重置完成")
        return True
        
    except Exception as e:
        print(f"❌ 重置自增ID失败: {e}")
        return False

def verify_empty():
    """验证数据库是否为空"""
    print("🔍 验证数据库状态...")
    
    session = SessionLocal()
    try:
        user_count = session.query(User).count()
        institution_count = session.query(Institution).count()
        venue_count = session.query(Venue).count()
        product_count = session.query(ExamProduct).count()
        registration_count = session.query(ExamRegistration).count()
        
        print("📊 当前数据统计:")
        print(f"  用户: {user_count}")
        print(f"  机构: {institution_count}")
        print(f"  考场: {venue_count}")
        print(f"  考试产品: {product_count}")
        print(f"  报名记录: {registration_count}")
        
        total_records = user_count + institution_count + venue_count + product_count + registration_count
        
        if total_records == 0:
            print("✅ 数据库已完全清空")
            return True
        else:
            print(f"⚠️  数据库中还有 {total_records} 条记录")
            return False
            
    finally:
        session.close()

def main():
    """主函数"""
    print("🚀 UAV考点运营管理系统 - 数据库清空工具")
    print("=" * 50)
    
    # 显示当前状态
    verify_empty()
    print()
    
    # 清空数据
    if clear_all_data():
        print()
        # 重置自增ID
        if reset_auto_increment():
            print()
            # 最终验证
            verify_empty()
            print("\n🎉 数据库清空完成！")
        else:
            print("\n⚠️  数据已删除，但自增ID重置失败")
    else:
        print("\n❌ 数据库清空失败")
        sys.exit(1)

if __name__ == "__main__":
    main()