#!/usr/bin/env python3
"""
简化的数据库重建脚本 - 修复版
"""

import sys
import random
import hashlib
from datetime import datetime, timedelta

try:
    from app.config.database import SessionLocal
    from app.models.user import User, UserRole
    from app.models.institution import Institution
    from app.models.venue import Venue, VenueStatus
    from app.models.exam import ExamProduct, ExamRegistration, RegistrationStatus
    print("✅ 模块导入成功")
except Exception as e:
    print(f"❌ 模块导入失败: {e}")
    sys.exit(1)

def hash_password(password: str) -> str:
    """密码哈希"""
    return hashlib.sha256(password.encode()).hexdigest()

def clear_data():
    """清空数据"""
    print("🗑️ 清空现有数据...")
    session = SessionLocal()
    try:
        session.query(ExamRegistration).delete()
        session.query(ExamProduct).delete()
        session.query(Venue).delete()
        session.query(User).delete()
        session.query(Institution).delete()
        session.commit()
        print("✅ 数据清空完成")
    except Exception as e:
        session.rollback()
        print(f"❌ 清空数据失败: {e}")
        raise
    finally:
        session.close()

def create_basic_data():
    """创建基础数据"""
    print("📝 创建基础数据...")
    session = SessionLocal()
    
    try:
        # 1. 创建机构
        print("创建机构...")
        institutions = []
        cities = ["北京", "上海", "深圳", "广州", "杭州"]
        
        for i, city in enumerate(cities):
            institution = Institution(
                name=f"{city}航空培训中心",
                code=f"{city[:1].upper()}UAV{i+1:03d}",
                type="培训学校",
                contact_person=f"{city}负责人",
                contact_phone=f"138{random.randint(10000000, 99999999)}",
                contact_email=f"{city.lower()}@example.com",
                province=f"{city}市",
                city=city,
                district=f"{city}区",
                address=f"{city}市航空路{random.randint(100, 999)}号",
                is_active=True,
                is_approved=True
            )
            session.add(institution)
            institutions.append(institution)
        
        session.commit()
        print(f"✅ 创建了 {len(institutions)} 个机构")
        
        # 2. 创建考场
        print("创建考场...")
        venue_count = 0
        for institution in institutions:
            for i in range(2):  # 每个机构2个考场
                venue = Venue(
                    name=f"{institution.city}考场{i+1}",
                    code=f"{institution.code}_VENUE_{i+1}",
                    description=f"{institution.city}考试场地",
                    capacity=random.randint(20, 50),
                    building="教学楼",
                    floor=f"{random.randint(1, 3)}层",
                    room_number=f"{random.randint(101, 399)}",
                    status=VenueStatus.AVAILABLE,
                    is_active=True,
                    institution_id=institution.id
                )
                session.add(venue)
                venue_count += 1
        
        session.commit()
        print(f"✅ 创建了 {venue_count} 个考场")
        
        # 3. 创建考试产品
        print("创建考试产品...")
        exam_products = [
            {"name": "多旋翼视距内驾驶员理论", "code": "MULTI_THEORY", "type": "理论", "duration": 60},
            {"name": "多旋翼视距内驾驶员实操", "code": "MULTI_PRACTICE", "type": "实操", "duration": 15},
            {"name": "固定翼视距内驾驶员理论", "code": "FIXED_THEORY", "type": "理论", "duration": 60},
            {"name": "固定翼视距内驾驶员实操", "code": "FIXED_PRACTICE", "type": "实操", "duration": 20},
            {"name": "无人机教员资格理论", "code": "INSTRUCTOR_THEORY", "type": "理论", "duration": 90},
            {"name": "无人机教员资格实操", "code": "INSTRUCTOR_PRACTICE", "type": "实操", "duration": 30}
        ]
        
        for config in exam_products:
            exam_product = ExamProduct(
                name=config["name"],
                code=config["code"],
                description=f"{config['name']}，考试时长{config['duration']}分钟",
                duration_minutes=config["duration"],
                exam_type=config["type"],
                is_active=True
            )
            session.add(exam_product)
        
        session.commit()
        print(f"✅ 创建了 {len(exam_products)} 个考试产品")
        
        # 4. 创建用户
        print("创建用户...")
        
        # 超级管理员
        admin = User(
            username="admin",
            email="admin@uav-exam.com",
            phone="13800000001",
            password_hash=hash_password("admin123"),
            real_name="系统管理员",
            role=UserRole.SUPER_ADMIN,
            is_active=True,
            is_verified=True
        )
        session.add(admin)
        
        # 机构管理员
        for i, institution in enumerate(institutions):
            operator = User(
                username=f"{institution.city.lower()}_admin",
                email=f"{institution.city.lower()}_admin@example.com",
                phone=f"1380000{i+2:04d}",
                password_hash=hash_password("123456"),
                real_name=f"{institution.city}管理员",
                role=UserRole.OPERATOR,
                institution_id=institution.id,
                is_active=True,
                is_verified=True
            )
            session.add(operator)
        
        # 考生
        names = ["张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十", "郑十一", "王十二"]
        for i, name in enumerate(names):
            institution = random.choice(institutions)
            id_card = f"11010119900{i+1:02d}{random.randint(1000, 9999)}"
            
            candidate = User(
                username=f"candidate_{id_card[-6:]}",
                email=f"candidate{i+1}@example.com",
                phone=f"1380001{i+1:04d}",
                password_hash=hash_password(id_card[-6:]),
                real_name=name,
                id_card=id_card,
                role=UserRole.CANDIDATE,
                institution_id=institution.id,
                is_active=True,
                is_verified=True,
                wechat_openid=f"wx_{random.randint(100000000000000000, 999999999999999999)}"
            )
            session.add(candidate)
        
        session.commit()
        print("✅ 创建了用户数据")
        
        # 5. 创建报名记录
        print("创建报名记录...")
        candidates = session.query(User).filter(User.role == UserRole.CANDIDATE).all()
        products = session.query(ExamProduct).all()
        
        registration_count = 0
        for candidate in candidates:
            # 每个考生随机报名1-3个考试
            num_registrations = random.randint(1, 3)
            selected_products = random.sample(products, min(num_registrations, len(products)))
            
            for j, product in enumerate(selected_products):
                reg_date = datetime.now() - timedelta(days=random.randint(0, 30))
                reg_number = f"REG{reg_date.strftime('%Y%m%d')}{candidate.id:03d}{j+1:02d}"
                
                registration = ExamRegistration(
                    user_id=candidate.id,
                    exam_product_id=product.id,
                    registration_number=reg_number,
                    status=RegistrationStatus.APPROVED,
                    notes=f"考生{candidate.real_name}报名{product.name}",
                    created_at=reg_date
                )
                session.add(registration)
                registration_count += 1
        
        session.commit()
        print(f"✅ 创建了 {registration_count} 条报名记录")
        
    except Exception as e:
        session.rollback()
        print(f"❌ 创建数据失败: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        session.close()

def show_statistics():
    """显示统计信息"""
    print("\n📊 数据统计:")
    session = SessionLocal()
    try:
        user_count = session.query(User).count()
        institution_count = session.query(Institution).count()
        venue_count = session.query(Venue).count()
        product_count = session.query(ExamProduct).count()
        registration_count = session.query(ExamRegistration).count()
        
        print(f"用户总数: {user_count}")
        print(f"机构总数: {institution_count}")
        print(f"考场总数: {venue_count}")
        print(f"考试产品: {product_count}")
        print(f"报名记录: {registration_count}")
        
        print("\n📋 测试账号:")
        print("超级管理员: admin / admin123")
        print("机构管理员: beijing_admin / 123456")
        print("考生示例: candidate_XXXXXX / XXXXXX (身份证后6位)")
        
    finally:
        session.close()

if __name__ == "__main__":
    try:
        print("🚀 开始数据库重建...")
        clear_data()
        create_basic_data()
        show_statistics()
        print("\n🎉 数据库重建完成!")
    except Exception as e:
        print(f"\n❌ 重建失败: {e}")
        sys.exit(1)