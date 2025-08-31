#!/usr/bin/env python3
"""
简化的数据库重建脚本
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
        # 按依赖关系顺序删除
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
                    institution_id=institution.id\n                )\n                session.add(venue)\n                venue_count += 1\n        \n        session.commit()\n        print(f\"✅ 创建了 {venue_count} 个考场\")\n        \n        # 3. 创建考试产品\n        print(\"创建考试产品...\")\n        exam_products = [\n            {\"name\": \"多旋翼视距内驾驶员理论\", \"code\": \"MULTI_THEORY\", \"type\": \"理论\", \"duration\": 60},\n            {\"name\": \"多旋翼视距内驾驶员实操\", \"code\": \"MULTI_PRACTICE\", \"type\": \"实操\", \"duration\": 15},\n            {\"name\": \"固定翼视距内驾驶员理论\", \"code\": \"FIXED_THEORY\", \"type\": \"理论\", \"duration\": 60},\n            {\"name\": \"固定翼视距内驾驶员实操\", \"code\": \"FIXED_PRACTICE\", \"type\": \"实操\", \"duration\": 20},\n            {\"name\": \"无人机教员资格理论\", \"code\": \"INSTRUCTOR_THEORY\", \"type\": \"理论\", \"duration\": 90},\n            {\"name\": \"无人机教员资格实操\", \"code\": \"INSTRUCTOR_PRACTICE\", \"type\": \"实操\", \"duration\": 30}\n        ]\n        \n        for config in exam_products:\n            exam_product = ExamProduct(\n                name=config[\"name\"],\n                code=config[\"code\"],\n                description=f\"{config['name']}，考试时长{config['duration']}分钟\",\n                duration_minutes=config[\"duration\"],\n                exam_type=config[\"type\"],\n                is_active=True\n            )\n            session.add(exam_product)\n        \n        session.commit()\n        print(f\"✅ 创建了 {len(exam_products)} 个考试产品\")\n        \n        # 4. 创建用户\n        print(\"创建用户...\")\n        \n        # 超级管理员\n        admin = User(\n            username=\"admin\",\n            email=\"admin@uav-exam.com\",\n            phone=\"13800000001\",\n            password_hash=hash_password(\"admin123\"),\n            real_name=\"系统管理员\",\n            role=UserRole.SUPER_ADMIN,\n            is_active=True,\n            is_verified=True\n        )\n        session.add(admin)\n        \n        # 机构管理员\n        for i, institution in enumerate(institutions):\n            operator = User(\n                username=f\"{institution.city.lower()}_admin\",\n                email=f\"{institution.city.lower()}_admin@example.com\",\n                phone=f\"1380000{i+2:04d}\",\n                password_hash=hash_password(\"123456\"),\n                real_name=f\"{institution.city}管理员\",\n                role=UserRole.OPERATOR,\n                institution_id=institution.id,\n                is_active=True,\n                is_verified=True\n            )\n            session.add(operator)\n        \n        # 考生\n        names = [\"张三\", \"李四\", \"王五\", \"赵六\", \"钱七\", \"孙八\", \"周九\", \"吴十\", \"郑十一\", \"王十二\"]\n        for i, name in enumerate(names):\n            institution = random.choice(institutions)\n            id_card = f\"11010119900{i+1:02d}{random.randint(1000, 9999)}\"\n            \n            candidate = User(\n                username=f\"candidate_{id_card[-6:]}\",\n                email=f\"candidate{i+1}@example.com\",\n                phone=f\"1380001{i+1:04d}\",\n                password_hash=hash_password(id_card[-6:]),\n                real_name=name,\n                id_card=id_card,\n                role=UserRole.CANDIDATE,\n                institution_id=institution.id,\n                is_active=True,\n                is_verified=True,\n                wechat_openid=f\"wx_{random.randint(100000000000000000, 999999999999999999)}\"\n            )\n            session.add(candidate)\n        \n        session.commit()\n        print(\"✅ 创建了用户数据\")\n        \n        # 5. 创建报名记录\n        print(\"创建报名记录...\")\n        candidates = session.query(User).filter(User.role == UserRole.CANDIDATE).all()\n        products = session.query(ExamProduct).all()\n        \n        registration_count = 0\n        for candidate in candidates:\n            # 每个考生随机报名1-3个考试\n            num_registrations = random.randint(1, 3)\n            selected_products = random.sample(products, min(num_registrations, len(products)))\n            \n            for j, product in enumerate(selected_products):\n                reg_date = datetime.now() - timedelta(days=random.randint(0, 30))\n                reg_number = f\"REG{reg_date.strftime('%Y%m%d')}{candidate.id:03d}{j+1:02d}\"\n                \n                registration = ExamRegistration(\n                    user_id=candidate.id,\n                    exam_product_id=product.id,\n                    registration_number=reg_number,\n                    status=RegistrationStatus.APPROVED,\n                    notes=f\"考生{candidate.real_name}报名{product.name}\",\n                    created_at=reg_date\n                )\n                session.add(registration)\n                registration_count += 1\n        \n        session.commit()\n        print(f\"✅ 创建了 {registration_count} 条报名记录\")\n        \n    except Exception as e:\n        session.rollback()\n        print(f\"❌ 创建数据失败: {e}\")\n        import traceback\n        traceback.print_exc()\n        raise\n    finally:\n        session.close()\n\ndef show_statistics():\n    \"\"\"显示统计信息\"\"\"\n    print(\"\\n📊 数据统计:\")\n    session = SessionLocal()\n    try:\n        user_count = session.query(User).count()\n        institution_count = session.query(Institution).count()\n        venue_count = session.query(Venue).count()\n        product_count = session.query(ExamProduct).count()\n        registration_count = session.query(ExamRegistration).count()\n        \n        print(f\"用户总数: {user_count}\")\n        print(f\"机构总数: {institution_count}\")\n        print(f\"考场总数: {venue_count}\")\n        print(f\"考试产品: {product_count}\")\n        print(f\"报名记录: {registration_count}\")\n        \n        print(\"\\n📋 测试账号:\")\n        print(\"超级管理员: admin / admin123\")\n        print(\"机构管理员: beijing_admin / 123456\")\n        print(\"考生示例: candidate_XXXXXX / XXXXXX (身份证后6位)\")\n        \n    finally:\n        session.close()\n\nif __name__ == \"__main__\":\n    try:\n        print(\"🚀 开始数据库重建...\")\n        clear_data()\n        create_basic_data()\n        show_statistics()\n        print(\"\\n🎉 数据库重建完成!\")\n    except Exception as e:\n        print(f\"\\n❌ 重建失败: {e}\")\n        sys.exit(1)