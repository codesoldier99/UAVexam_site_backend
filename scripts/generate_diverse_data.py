#!/usr/bin/env python3
"""
UAV考点运营管理系统 - 智能数据生成脚本
生成多样化、无重复的测试数据

作者: CodeBuddy
日期: 2025-01-26
版本: 2.0.0
"""

import sys
import os
import random
import hashlib
from datetime import datetime, timedelta, date, time
from typing import List, Dict, Set, Tuple, Any
import json

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from faker import Faker
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker

    # 导入模型
    from app.models import (
        User, UserRole, Institution, Venue, VenueStatus,
        ExamProduct, ExamRegistration, RegistrationStatus,
        Schedule, ScheduleStatus, CheckIn, CheckInStatus, CheckInMethod
    )
    from app.config.database import Base
except ImportError as e:
    print(f"❌ 导入依赖失败: {e}")
    print("请先安装依赖: pip install -r requirements.txt")
    sys.exit(1)

class SmartDataGenerator:
    """智能数据生成器"""
    
    def __init__(self, db_url: str = "mysql+pymysql://root:123456@localhost:3306/exam_site_dev_db"):
        self.db_url = db_url
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.faker = Faker(['zh_CN'])
        
        # 防重复集合
        self.used_usernames: Set[str] = set()
        self.used_emails: Set[str] = set()
        self.used_phones: Set[str] = set()
        self.used_id_cards: Set[str] = set()
        self.used_institution_codes: Set[str] = set()
        self.used_venue_codes: Set[str] = set()
        self.used_registration_numbers: Set[str] = set()
        
        # 真实姓名库
        self.real_names = [
            "张伟", "王芳", "李娜", "刘强", "陈静", "杨洋", "赵敏", "黄磊", "周杰", "吴彦祖",
            "徐静蕾", "孙红雷", "朱亚文", "马伊琍", "冯绍峰", "袁泉", "胡歌", "刘诗诗", "唐嫣", "杨幂",
            "范冰冰", "李冰冰", "周迅", "赵薇", "章子怡", "巩俐", "张曼玉", "王菲", "那英", "田震",
            "刘德华", "张学友", "郭富城", "黎明", "周润发", "成龙", "李连杰", "甄子丹", "吴京", "易烊千玺",
            "王俊凯", "王源", "鹿晗", "吴亦凡", "黄子韬", "张艺兴", "陈伟霆", "李易峰", "杨洋", "邓超"
        ]
        
        # 城市信息
        self.cities = [
            {"name": "北京", "code": "BJ", "province": "北京市", "area_code": "110101"},
            {"name": "上海", "code": "SH", "province": "上海市", "area_code": "310101"},
            {"name": "深圳", "code": "SZ", "province": "广东省", "area_code": "440301"},
            {"name": "广州", "code": "GZ", "province": "广东省", "area_code": "440101"},
            {"name": "杭州", "code": "HZ", "province": "浙江省", "area_code": "330101"},
            {"name": "成都", "code": "CD", "province": "四川省", "area_code": "510101"},
            {"name": "武汉", "code": "WH", "province": "湖北省", "area_code": "420101"},
            {"name": "西安", "code": "XA", "province": "陕西省", "area_code": "610101"},
            {"name": "南京", "code": "NJ", "province": "江苏省", "area_code": "320101"},
            {"name": "苏州", "code": "SZ2", "province": "江苏省", "area_code": "320501"}
        ]
        
        # 考试产品配置
        self.exam_products_config = [
            # 理论考试
            {"name": "多旋翼视距内驾驶员理论", "code": "MULTI_THEORY_VLOS", "type": "理论", "duration": 60},
            {"name": "多旋翼超视距驾驶员理论", "code": "MULTI_THEORY_BVLOS", "type": "理论", "duration": 90},
            {"name": "固定翼视距内驾驶员理论", "code": "FIXED_THEORY_VLOS", "type": "理论", "duration": 60},
            {"name": "固定翼超视距驾驶员理论", "code": "FIXED_THEORY_BVLOS", "type": "理论", "duration": 90},
            {"name": "直升机驾驶员理论", "code": "HELI_THEORY", "type": "理论", "duration": 75},
            {"name": "无人机教员资格理论", "code": "INSTRUCTOR_THEORY", "type": "理论", "duration": 120},
            {"name": "无人机检查员理论", "code": "INSPECTOR_THEORY", "type": "理论", "duration": 90},
            {"name": "无人机维修人员理论", "code": "MAINTENANCE_THEORY", "type": "理论", "duration": 60},
            # 实操考试
            {"name": "多旋翼视距内驾驶员实操", "code": "MULTI_PRACTICE_VLOS", "type": "实操", "duration": 15},
            {"name": "多旋翼超视距驾驶员实操", "code": "MULTI_PRACTICE_BVLOS", "type": "实操", "duration": 25},
            {"name": "固定翼视距内驾驶员实操", "code": "FIXED_PRACTICE_VLOS", "type": "实操", "duration": 20},
            {"name": "固定翼超视距驾驶员实操", "code": "FIXED_PRACTICE_BVLOS", "type": "实操", "duration": 30},
            {"name": "直升机驾驶员实操", "code": "HELI_PRACTICE", "type": "实操", "duration": 25},
            {"name": "无人机教员资格实操", "code": "INSTRUCTOR_PRACTICE", "type": "实操", "duration": 45},
            {"name": "无人机检查员实操", "code": "INSPECTOR_PRACTICE", "type": "实操", "duration": 35}
        ]

    def clear_all_data(self):
        """清空所有数据表"""
        print("🗑️  清空现有数据...")
        
        with self.engine.connect() as conn:
            # 禁用外键检查
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            
            # 清空所有表
            tables = ['checkins', 'schedules', 'exam_registrations', 'exam_products', 'venues', 'institutions', 'users']
            for table in tables:
                conn.execute(text(f"TRUNCATE TABLE {table}"))
                conn.execute(text(f"ALTER TABLE {table} AUTO_INCREMENT = 1"))
            
            # 启用外键检查
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            conn.commit()
        
        print("✅ 数据清空完成")

    def generate_unique_username(self, prefix: str = "") -> str:
        """生成唯一用户名"""
        while True:
            if prefix:
                username = f"{prefix}_{random.randint(1000, 9999)}"
            else:
                username = self.faker.user_name()
            
            if username not in self.used_usernames:
                self.used_usernames.add(username)
                return username

    def generate_unique_email(self) -> str:
        """生成唯一邮箱"""
        domains = ['qq.com', '163.com', 'gmail.com', 'sina.com', 'outlook.com', 'foxmail.com']
        while True:
            domain = random.choice(domains)
            email = f"{self.faker.user_name()}{random.randint(100, 999)}@{domain}"
            if email not in self.used_emails:
                self.used_emails.add(email)
                return email

    def generate_unique_phone(self) -> str:
        """生成唯一手机号"""
        prefixes = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                   '150', '151', '152', '153', '155', '156', '157', '158', '159',
                   '180', '181', '182', '183', '184', '185', '186', '187', '188', '189']
        while True:
            phone = f"{random.choice(prefixes)}{random.randint(10000000, 99999999)}"
            if phone not in self.used_phones:
                self.used_phones.add(phone)
                return phone

    def generate_unique_id_card(self, city_info: Dict[str, Any]) -> str:
        """生成唯一身份证号"""
        while True:
            # 生成出生日期 (1970-2005)
            birth_year = random.randint(1970, 2005)
            birth_month = random.randint(1, 12)
            birth_day = random.randint(1, 28)
            
            # 生成身份证号
            area_code = city_info["area_code"]
            birth_date = f"{birth_year:04d}{birth_month:02d}{birth_day:02d}"
            sequence = f"{random.randint(100, 999)}"
            
            # 计算校验码
            id_card_17 = area_code + birth_date + sequence
            weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
            check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
            
            sum_val = sum(int(id_card_17[i]) * weights[i] for i in range(17))
            check_code = check_codes[sum_val % 11]
            
            id_card = id_card_17 + check_code
            
            if id_card not in self.used_id_cards:
                self.used_id_cards.add(id_card)
                return id_card

    def hash_password(self, password: str) -> str:
        """密码哈希"""
        return hashlib.sha256(password.encode()).hexdigest()

    def generate_institutions(self) -> List[Institution]:
        """生成机构数据"""
        print("🏢 生成机构数据...")
        
        institutions = []
        institution_types = ["培训学校", "职业院校", "企业培训中心", "技术学院"]
        
        for i, city in enumerate(self.cities):
            # 生成机构代码
            code = f"{city['code']}UAV{i+1:03d}"
            while code in self.used_institution_codes:
                code = f"{city['code']}UAV{random.randint(100, 999)}"
            self.used_institution_codes.add(code)
            
            # 生成机构名称
            type_name = random.choice(institution_types)
            name = f"{city['name']}{random.choice(['航空', '无人机', '飞行', '航天'])}{type_name}"
            
            institution = Institution(
                name=name,
                code=code,
                type=type_name,
                contact_person=random.choice(self.real_names),
                contact_phone=self.generate_unique_phone(),
                contact_email=self.generate_unique_email(),
                province=city["province"],
                city=city["name"],
                district=f"{city['name']}{random.choice(['区', '县', '市'])}",
                address=f"{city['name']}市{random.choice(['科技路', '创新大道', '航空路', '发展路'])}{random.randint(100, 999)}号",
                license_number=f"教民{city['area_code'][:4]}{random.randint(100000, 999999)}号",
                business_license=f"{city['area_code']}{random.randint(1000000000, 9999999999)}",
                is_active=True,
                is_approved=True,
                config={"max_students": random.randint(100, 500), "specialties": ["多旋翼", "固定翼"]}
            )
            institutions.append(institution)
        
        print(f"✅ 生成了 {len(institutions)} 个机构")
        return institutions

    def generate_venues(self, institutions: List[Institution]) -> List[Venue]:
        """生成考场数据"""
        print("🏛️  生成考场数据...")
        
        venues = []
        venue_types = [
            {"type": "理论", "prefix": "THEORY", "capacity_range": (30, 80)},
            {"type": "实操", "prefix": "PRACTICE", "capacity_range": (15, 40)},
            {"type": "综合", "prefix": "MIXED", "capacity_range": (20, 60)}
        ]
        
        for institution in institutions:
            # 每个机构生成3个考场
            for i in range(3):
                venue_type = random.choice(venue_types)
                
                # 生成考场代码
                code = f"{institution.code[:2]}_{venue_type['prefix']}_{chr(65+i)}"
                while code in self.used_venue_codes:
                    code = f"{institution.code[:2]}_{venue_type['prefix']}_{random.randint(100, 999)}"
                self.used_venue_codes.add(code)
                
                # 生成考场名称
                name = f"{institution.city}{venue_type['type']}考试{'教室' if venue_type['type'] == '理论' else '场地'}{chr(65+i)}"
                
                # 随机状态分布：80%可用，15%占用中，5%维护中
                status_weights = [0.8, 0.15, 0.05]
                status = random.choices([VenueStatus.AVAILABLE, VenueStatus.OCCUPIED, VenueStatus.MAINTENANCE], 
                                      weights=status_weights)[0]
                
                venue = Venue(
                    name=name,
                    code=code,
                    description=f"{venue_type['type']}考试专用场地，配备先进设备",
                    capacity=random.randint(venue_type["capacity_min"], venue_type["capacity_max"]),
                    current_count=random.randint(0, 5) if status == VenueStatus.OCCUPIED else 0,
                    building=random.choice(["教学楼", "实训楼", "综合楼", "主楼"]),
                    floor=f"{random.randint(1, 5)}层",
                    room_number=f"{random.choice(['A', 'B', 'C'])}{random.randint(101, 599)}",
                    equipment={
                        "computers": random.randint(20, 50) if venue_type['type'] == '理论' else 0,
                        "drones": random.randint(5, 15) if venue_type['type'] != '理论' else 0,
                        "cameras": random.randint(4, 8),
                        "projector": True,
                        "air_conditioning": True
                    },
                    facilities={
                        "wifi": True,
                        "power_outlets": random.randint(20, 40),
                        "emergency_exit": True,
                        "fire_safety": True
                    },
                    status=status,
                    is_active=True,
                    institution_id=institution.id,
                    qr_code=f"VENUE_{code}_{random.randint(100000, 999999)}"
                )
                venues.append(venue)
        
        print(f"✅ 生成了 {len(venues)} 个考场")
        return venues

    def generate_exam_products(self) -> List[ExamProduct]:
        """生成考试产品数据"""
        print("📋 生成考试产品数据...")
        
        exam_products = []
        for config in self.exam_products_config:
            exam_product = ExamProduct(
                name=config["name"],
                code=config["code"],
                description=f"{config['name']}，考试时长{config['duration']}分钟",
                duration_minutes=config["duration"],
                exam_type=config["type"],
                is_active=True
            )
            exam_products.append(exam_product)
        
        print(f"✅ 生成了 {len(exam_products)} 个考试产品")
        return exam_products

    def generate_users(self, institutions: List[Institution]) -> List[User]:
        """生成用户数据"""
        print("👥 生成用户数据...")
        
        users = []
        
        # 1. 生成超级管理员 (2人)
        for i in range(2):
            username = f"admin{'_backup' if i == 1 else ''}"
            user = User(
                username=username,
                email=f"admin{i+1}@uav-exam.com",
                phone=self.generate_unique_phone(),
                password_hash=self.hash_password("admin123"),
                real_name=f"系统管理员{'(备用)' if i == 1 else ''}",
                role=UserRole.SUPER_ADMIN,
                is_active=True,
                is_verified=True
            )
            users.append(user)
            self.used_usernames.add(username)
            self.used_emails.add(user.email)
        
        # 2. 生成机构管理员 (每机构3人，共30人)
        for institution in institutions:
            city_info = next(city for city in self.cities if city["name"] == institution.city)
            for i in range(3):
                roles = ["主管", "副主管", "操作员"]
                username = f"{city_info['code'].lower()}_admin_{i+1}"
                
                user = User(
                    username=username,
                    email=self.generate_unique_email(),
                    phone=self.generate_unique_phone(),
                    password_hash=self.hash_password("123456"),
                    real_name=f"{institution.city}{roles[i]}",
                    role=UserRole.OPERATOR,
                    institution_id=institution.id,
                    is_active=True,
                    is_verified=True
                )
                users.append(user)
                self.used_usernames.add(username)
        
        # 3. 生成监考员 (15人)
        for i in range(15):
            institution = random.choice(institutions)
            city_info = next(city for city in self.cities if city["name"] == institution.city)
            
            username = f"examiner_{i+1:03d}"
            user = User(
                username=username,
                email=self.generate_unique_email(),
                phone=self.generate_unique_phone(),
                password_hash=self.hash_password("examiner123"),
                real_name=random.choice(self.real_names),
                id_card=self.generate_unique_id_card(city_info),
                role=UserRole.EXAMINER,
                institution_id=institution.id,
                is_active=True,
                is_verified=True
            )
            users.append(user)
            self.used_usernames.add(username)
        
        # 4. 生成考生 (50人)
        for i in range(50):
            institution = random.choice(institutions)
            city_info = next(city for city in self.cities if city["name"] == institution.city)
            
            id_card = self.generate_unique_id_card(city_info)
            username = f"candidate_{id_card[-6:]}"
            
            user = User(
                username=username,
                email=self.generate_unique_email(),
                phone=self.generate_unique_phone(),
                password_hash=self.hash_password(id_card[-6:]),  # 密码为身份证后6位
                real_name=random.choice(self.real_names),
                id_card=id_card,
                role=UserRole.CANDIDATE,
                institution_id=institution.id,
                is_active=True,
                is_verified=random.choice([True, False]),  # 90%已验证
                wechat_openid=f"wx_{random.randint(100000000000000000, 999999999999999999)}"
            )
            users.append(user)
            self.used_usernames.add(username)
        
        print(f"✅ 生成了 {len(users)} 个用户")
        return users

    def generate_exam_registrations(self, users: List[User], exam_products: List[ExamProduct]) -> List[ExamRegistration]:
        """生成考试报名数据"""
        print("📝 生成考试报名数据...")
        
        registrations = []
        candidates = [user for user in users if user.role == UserRole.CANDIDATE]
        
        for candidate in candidates:
            # 每个考生随机报名1-5个考试
            num_registrations = random.randint(1, 5)
            selected_products = random.sample(exam_products, min(num_registrations, len(exam_products)))
            
            for j, product in enumerate(selected_products):
                # 生成报名编号
                reg_date = datetime.now() - timedelta(days=random.randint(0, 90))
                reg_number = f"REG{reg_date.strftime('%Y%m%d')}{candidate.id:03d}{j+1:02d}"
                
                while reg_number in self.used_registration_numbers:
                    reg_number = f"REG{reg_date.strftime('%Y%m%d')}{candidate.id:03d}{random.randint(10, 99)}"
                self.used_registration_numbers.add(reg_number)
                
                # 状态分布：70% approved, 20% pending, 10% rejected/cancelled
                status_weights = [0.7, 0.2, 0.05, 0.05]
                status = random.choices([RegistrationStatus.APPROVED, RegistrationStatus.PENDING, 
                                       RegistrationStatus.REJECTED, RegistrationStatus.CANCELLED], 
                                      weights=status_weights)[0]
                
                registration = ExamRegistration(
                    user_id=candidate.id,
                    exam_product_id=product.id,
                    registration_number=reg_number,
                    status=status,
                    notes=f"考生{candidate.real_name}报名{product.name}" if status == RegistrationStatus.APPROVED else 
                          f"待审核" if status == RegistrationStatus.PENDING else "审核未通过",
                    created_at=reg_date,
                    updated_at=reg_date + timedelta(days=random.randint(1, 7))
                )
                registrations.append(registration)
        
        print(f"✅ 生成了 {len(registrations)} 条报名记录")
        return registrations

    def save_to_database(self, institutions, venues, exam_products, users, registrations):
        """保存数据到数据库"""
        print("💾 保存数据到数据库...")
        
        session = self.SessionLocal()
        try:
            # 保存机构
            session.add_all(institutions)
            session.commit()
            print(f"✅ 保存了 {len(institutions)} 个机构")
            
            # 保存考场
            session.add_all(venues)
            session.commit()
            print(f"✅ 保存了 {len(venues)} 个考场")
            
            # 保存考试产品
            session.add_all(exam_products)
            session.commit()
            print(f"✅ 保存了 {len(exam_products)} 个考试产品")
            
            # 保存用户
            session.add_all(users)
            session.commit()
            print(f"✅ 保存了 {len(users)} 个用户")
            
            # 保存报名记录
            session.add_all(registrations)
            session.commit()
            print(f"✅ 保存了 {len(registrations)} 条报名记录")
            
        except Exception as e:
            session.rollback()
            print(f"❌ 保存数据失败: {e}")
            raise
        finally:
            session.close()

    def generate_statistics(self):
        """生成数据统计报告"""
        print("\n📊 数据统计报告")
        print("=" * 50)
        
        session = self.SessionLocal()
        try:
            # 用户统计
            total_users = session.query(User).count()
            admin_count = session.query(User).filter(User.role == UserRole.SUPER_ADMIN).count()
            operator_count = session.query(User).filter(User.role == UserRole.OPERATOR).count()
            examiner_count = session.query(User).filter(User.role == UserRole.EXAMINER).count()
            candidate_count = session.query(User).filter(User.role == UserRole.CANDIDATE).count()
            
            print(f"👥 用户统计:")
            print(f"   总用户数: {total_users}")
            print(f"   超级管理员: {admin_count}")
            print(f"   机构管理员: {operator_count}")
            print(f"   监考员: {examiner_count}")
            print(f"   考生: {candidate_count}")
            
            # 机构统计
            total_institutions = session.query(Institution).count()
            total_venues = session.query(Venue).count()
            available_venues = session.query(Venue).filter(Venue.status == VenueStatus.AVAILABLE).count()
            
            print(f"\n🏢 机构统计:")
            print(f"   总机构数: {total_institutions}")
            print(f"   总考场数: {total_venues}")
            print(f"   可用考场: {available_venues}")
            
            # 考试统计
            total_products = session.query(ExamProduct).count()
            theory_products = session.query(ExamProduct).filter(ExamProduct.exam_type == "理论").count()
            practice_products = session.query(ExamProduct).filter(ExamProduct.exam_type == "实操").count()
            
            print(f"\n📋 考试产品统计:")
            print(f"   总考试产品: {total_products}")
            print(f"   理论考试: {theory_products}")
            print(f"   实操考试: {practice_products}")
            
            # 报名统计
            total_registrations = session.query(ExamRegistration).count()
            approved_registrations = session.query(ExamRegistration).filter(ExamRegistration.status == RegistrationStatus.APPROVED).count()
            pending_registrations = session.query(ExamRegistration).filter(ExamRegistration.status == RegistrationStatus.PENDING).count()
            
            print(f"\n📝 报名统计:")
            print(f"   总报名数: {total_registrations}")
            print(f"   已批准: {approved_registrations}")
            print(f"   待审核: {pending_registrations}")
            
        finally:
            session.close()

    def run(self):
        """执行数据生成流程"""
        print("🚀 开始生成多样化测试数据...")
        print("=" * 50)
        
        try:
            # 1. 清空现有数据
            self.clear_all_data()
            
            # 2. 生成基础数据
            institutions = self.generate_institutions()
            venues = self.generate_venues(institutions)
            exam_products = self.generate_exam_products()
            users = self.generate_users(institutions)
            registrations = self.generate_exam_registrations(users, exam_products)
            
            # 3. 保存到数据库
            self.save_to_database(institutions, venues, exam_products, users, registrations)
            
            # 4. 生成统计报告
            self.generate_statistics()
            
            print("\n🎉 数据生成完成！")
            print("=" * 50)
            
        except Exception as e:
            print(f"\n❌ 数据生成失败: {e}")
            raise


if __name__ == "__main__":
    generator = SmartDataGenerator()
    generator.run()