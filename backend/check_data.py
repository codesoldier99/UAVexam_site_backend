#!/usr/bin/env python3
"""
检查数据库中的数据
"""

import sys
sys.path.append('.')

from app.config.database import SessionLocal
from app.models import *

def check_data():
    """检查数据库中的数据"""
    db = SessionLocal()
    
    try:
        print("🔍 检查数据库中的数据:")
        print("=" * 50)
        
        # 检查用户
        users = db.query(User).all()
        print(f"👥 用户表 (users): {len(users)} 条记录")
        for user in users:
            print(f"  - {user.username} ({user.role.value}) - {user.real_name}")
        
        # 检查机构
        institutions = db.query(Institution).all()
        print(f"\n🏢 机构表 (institutions): {len(institutions)} 条记录")
        for inst in institutions:
            print(f"  - {inst.name} ({inst.code})")
        
        # 检查考试产品
        exam_products = db.query(ExamProduct).all()
        print(f"\n📝 考试产品表 (exam_products): {len(exam_products)} 条记录")
        for product in exam_products:
            print(f"  - {product.name} ({product.code}) - {product.duration_minutes}分钟")
        
        # 检查考场
        venues = db.query(Venue).all()
        print(f"\n🏫 考场表 (venues): {len(venues)} 条记录")
        for venue in venues:
            print(f"  - {venue.name} ({venue.code}) - 容量:{venue.capacity}")
        
        # 检查报名记录
        registrations = db.query(ExamRegistration).all()
        print(f"\n📋 报名表 (exam_registrations): {len(registrations)} 条记录")
        for reg in registrations:
            user = db.query(User).filter(User.id == reg.user_id).first()
            product = db.query(ExamProduct).filter(ExamProduct.id == reg.exam_product_id).first()
            print(f"  - {user.real_name if user else 'Unknown'} -> {product.name if product else 'Unknown'}")
        
        # 检查排期
        schedules = db.query(Schedule).all()
        print(f"\n📅 排期表 (schedules): {len(schedules)} 条记录")
        
        # 检查签到
        checkins = db.query(CheckIn).all()
        print(f"\n✅ 签到表 (checkins): {len(checkins)} 条记录")
        
        print("\n" + "=" * 50)
        print("🎉 数据检查完成!")
        
    except Exception as e:
        print(f"❌ 检查数据失败: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_data()
