#!/usr/bin/env python3
"""
真实数据生成器 - 精简版
生成少量但真实的测试数据
"""

import sys
import os
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
import bcrypt

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if 'backend' in current_dir:
    sys.path.append(os.path.dirname(current_dir))
    from app.config.database import engine, SessionLocal
    from app.models.user import User, UserRole
    from app.models.institution import Institution
    from app.models.venue import Venue, VenueStatus
    from app.models.exam import ExamRegistration, ExamProduct, RegistrationStatus
    from app.models.schedule import Schedule, ScheduleStatus
    from app.models.checkin import CheckIn, CheckInStatus, CheckInMethod
else:
    sys.path.append(os.path.join(current_dir, 'backend'))
    from app.config.database import engine, SessionLocal
    from app.models.user import User, UserRole
    from app.models.institution import Institution
    from app.models.venue import Venue, VenueStatus
    from app.models.exam import ExamRegistration, ExamProduct, RegistrationStatus
    from app.models.schedule import Schedule, ScheduleStatus
    from app.models.checkin import CheckIn, CheckInStatus, CheckInMethod


class RealisticDataGenerator:
    """真实数据生成器"""
    
    def __init__(self):
        self.db = SessionLocal()
        
        # 真实的城市数据
        self.cities = [
            {"name": "北京", "code": "110000", "province": "北京市"},
            {"name": "上海", "code": "310000", "province": "上海市"},
            {"name": "广州", "code": "440100", "province": "广东省"},
            {"name": "深圳", "code": "440300", "province": "广东省"},
            {"name": "杭州", "code": "330100", "province": "浙江省"},
            {"name": "成都", "code": "510100", "province": "四川省"},
            {"name": "西安", "code": "610100", "province": "陕西省"},
            {"name": "武汉", "code": "420100", "province": "湖北省"},
            {"name": "南京", "code": "320100", "province": "江苏省"},
            {"name": "重庆", "code": "500000", "province": "重庆市"}
        ]
        
        # 真实的姓名数据
        self.surnames = ["王", "李", "张", "刘", "陈", "杨", "赵", "黄", "周", "吴", "徐", "孙", "胡", "朱", "高", "林", "何", "郭", "马", "罗"]
        self.given_names = ["伟", "芳", "娜", "秀英", "敏", "静", "丽", "强", "磊", "军", "洋", "勇", "艳", "杰", "娟", "涛", "明", "超", "秀兰", "霞"]
        
        # 真实的机构名称
        self.institution_types = [
            "航空培训学校", "无人机培训中心", "飞行技术学院", "航空职业学院", 
            "无人机技术培训基地", "航空培训机构", "飞行员培训中心", "航空教育中心"
        ]
        
        # 真实的考试产品
        self.exam_products_data = [
            {"name": "多旋翼无人机驾驶员理论考试", "code": "MULTI_THEORY", "type": "理论考试", "duration": 90},
            {"name": "多旋翼无人机驾驶员实操考试", "code": "MULTI_PRACTICE", "type": "实操考试", "duration": 120},
            {"name": "固定翼无人机驾驶员理论考试", "code": "FIXED_THEORY", "type": "理论考试", "duration": 90},
            {"name": "固定翼无人机驾驶员实操考试", "code": "FIXED_PRACTICE", "type": "实操考试", "duration": 120},
            {"name": "直升机无人机驾驶员理论考试", "code": "HELI_THEORY", "type": "理论考试", "duration": 90},
            {"name": "直升机无人机驾驶员实操考试", "code": "HELI_PRACTICE", "type": "实操考试", "duration": 120},
            {"name": "无人机教员理论考试", "code": "INSTRUCTOR_THEORY", "type": "理论考试", "duration": 120},
            {"name": "无人机教员实操考试", "code": "INSTRUCTOR_PRACTICE", "type": "实操考试", "duration": 150},
            {"name": "无人机机长理论考试", "code": "CAPTAIN_THEORY", "type": "理论考试", "duration": 120},
            {"name": "无人机机长实操考试", "code": "CAPTAIN_PRACTICE", "type": "实操考试", "duration": 180}
        ]
    
    def generate_real_id_card(self, birth_year: int = None) -> str:
        """生成真实格式的身份证号"""
        if birth_year is None:
            birth_year = random.randint(1980, 2000)
        
        # 地区代码（前6位）- 使用真实的地区代码
        area_codes = ["110101", "310101", "440106", "440307", "330106", "510104", "610103", "420106", "320102", "500103"]
        area_code = random.choice(area_codes)
        
        # 出生日期（8位）
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)  # 避免月份天数问题
        birth_date = f"{birth_year:04d}{birth_month:02d}{birth_day:02d}"
        
        # 顺序码（3位）
        sequence = random.randint(1, 999)
        sequence_str = f"{sequence:03d}"
        
        # 前17位
        id_17 = area_code + birth_date + sequence_str
        
        # 计算校验码
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
        
        sum_val = sum(int(id_17[i]) * weights[i] for i in range(17))
        check_code = check_codes[sum_val % 11]
        
        return id_17 + check_code
    
    def generate_real_phone(self) -> str:
        """生成真实格式的手机号"""
        # 中国移动、联通、电信的号段
        prefixes = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139",
                   "150", "151", "152", "153", "155", "156", "157", "158", "159",
                   "180", "181", "182", "183", "184", "185", "186", "187", "188", "189"]
        
        prefix = random.choice(prefixes)
        suffix = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        return prefix + suffix
    
    def generate_real_email(self, name: str) -> str:
        """生成真实格式的邮箱"""
        domains = ["qq.com", "163.com", "126.com", "gmail.com", "sina.com", "sohu.com", "outlook.com"]
        domain = random.choice(domains)
        
        # 使用拼音或数字组合
        username_parts = [name.lower(), str(random.randint(100, 9999))]
        username = ''.join(username_parts)
        
        return f"{username}@{domain}"
    
    def clear_all_data(self):
        """清空所有数据"""
        try:
            print("🧹 清空现有数据...")
            
            # 按依赖关系顺序删除
            self.db.query(CheckIn).delete()
            self.db.query(Schedule).delete()
            self.db.query(ExamRegistration).delete()
            self.db.query(ExamProduct).delete()
            self.db.query(Venue).delete()
            self.db.query(User).delete()
            self.db.query(Institution).delete()
            
            self.db.commit()
            print("✅ 数据清空完成")
            
        except Exception as e:
            print(f"❌ 清空数据失败: {e}")
            self.db.rollback()
            raise
    
    def create_institutions(self) -> List[Institution]:
        """创建10个机构"""
        print("🏢 创建机构数据...")
        institutions = []
        
        for i in range(10):
            city = self.cities[i]
            institution_type = random.choice(self.institution_types)
            
            institution = Institution(
                name=f"{city['name']}{institution_type}",
                code=f"{city['code'][:4]}{i+1:02d}",
                type="培训机构",
                province=city['province'],
                city=city['name'],
                district=f"{city['name']}市区",
                address=f"{city['name']}市航空大道{100+i}号",
                contact_person=f"{random.choice(self.surnames)}{random.choice(self.given_names)}",
                contact_phone=self.generate_real_phone(),
                contact_email=self.generate_real_email(f"contact{i+1}"),
                license_number=f"教民{city['code'][:4]}{2020+i}第{i+1:03d}号",
                business_license=f"{city['code'][:6]}{2020+i}{i+1:06d}",
                is_active=True,
                is_approved=True,
                config={
                    "max_students": random.randint(100, 500), 
                    "has_simulator": True,
                    "legal_person": f"{random.choice(self.surnames)}{random.choice(self.given_names)}",
                    "registered_capital": random.randint(100, 1000) * 10000,
                    "established_date": f"{2020+i}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
                }
            )
            
            self.db.add(institution)
            institutions.append(institution)
        
        self.db.commit()
        print(f"✅ 创建了 {len(institutions)} 个机构")
        return institutions
    
    def create_exam_products(self) -> List[ExamProduct]:
        """创建考试产品"""
        print("📋 创建考试产品数据...")
        products = []
        
        for product_data in self.exam_products_data:
            product = ExamProduct(
                name=product_data["name"],
                code=product_data["code"],
                exam_type=product_data["type"],
                duration_minutes=product_data["duration"],
                description=f"{product_data['name']}，考试时长{product_data['duration']}分钟",
                passing_score=80,
                total_score=100,
                is_active=True
            )
            
            self.db.add(product)
            products.append(product)
        
        self.db.commit()
        print(f"✅ 创建了 {len(products)} 个考试产品")
        return products
    
    def create_venues(self, institutions: List[Institution]) -> List[Venue]:
        """为每个机构创建1-2个考场"""
        print("🏛️ 创建考场数据...")
        venues = []
        
        for institution in institutions:
            venue_count = random.randint(1, 2)
            
            for i in range(venue_count):
                venue = Venue(
                    name=f"{institution.name}考场{i+1}",
                    code=f"{institution.code}_ROOM_{i+1:02d}",
                    capacity=random.choice([20, 30, 40, 50]),
                    current_count=0,
                    status=VenueStatus.AVAILABLE,
                    institution_id=institution.id,
                    building=f"{i+1}号楼",
                    floor=f"{random.randint(1, 5)}楼",
                    room_number=f"{random.randint(101, 599)}",
                    equipment={
                        "computers": random.randint(20, 50),
                        "projector": True,
                        "air_conditioning": True,
                        "camera_count": random.randint(4, 8)
                    },
                    facilities={
                        "wifi": True,
                        "power_outlets": True,
                        "emergency_exit": True,
                        "fire_extinguisher": True
                    }
                )
                
                self.db.add(venue)
                venues.append(venue)
        
        self.db.commit()
        print(f"✅ 创建了 {len(venues)} 个考场")
        return venues
    
    def create_users(self, institutions: List[Institution]) -> List[User]:
        """创建用户数据"""
        print("👥 创建用户数据...")
        users = []
        
        # 创建1个超级管理员
        super_admin = User(
            username="superadmin",
            email="admin@uav-exam.com",
            phone=self.generate_real_phone(),
            password_hash=bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            real_name="系统管理员",
            id_card=self.generate_real_id_card(1985),
            avatar="/avatars/admin.jpg",
            role=UserRole.SUPER_ADMIN,
            is_active=True,
            is_verified=True,
            wechat_openid=f"wx_admin_{random.randint(100000, 999999)}",
            wechat_unionid=f"union_admin_{random.randint(100000, 999999)}",
            last_login=datetime.now() - timedelta(days=random.randint(1, 7))
        )
        self.db.add(super_admin)
        users.append(super_admin)
        
        # 为每个机构创建用户
        for i, institution in enumerate(institutions):
            # 1个机构管理员
            admin_name = f"{random.choice(self.surnames)}{random.choice(self.given_names)}"
            admin = User(
                username=f"admin_{institution.code.lower()}",
                email=self.generate_real_email(f"admin_{i+1}"),
                phone=self.generate_real_phone(),
                password_hash=bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                real_name=admin_name,
                id_card=self.generate_real_id_card(random.randint(1975, 1990)),
                avatar=f"/avatars/admin_{i+1}.jpg",
                role=UserRole.ADMIN,
                is_active=True,
                is_verified=True,
                institution_id=institution.id,
                wechat_openid=f"wx_admin_{i+1}_{random.randint(100000, 999999)}",
                wechat_unionid=f"union_admin_{i+1}_{random.randint(100000, 999999)}",
                last_login=datetime.now() - timedelta(days=random.randint(1, 30))
            )
            self.db.add(admin)
            users.append(admin)
            
            # 1个监考员
            examiner_name = f"{random.choice(self.surnames)}{random.choice(self.given_names)}"
            examiner = User(
                username=f"examiner_{institution.code.lower()}",
                email=self.generate_real_email(f"examiner_{i+1}"),
                phone=self.generate_real_phone(),
                password_hash=bcrypt.hashpw("exam123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                real_name=examiner_name,
                id_card=self.generate_real_id_card(random.randint(1980, 1995)),
                avatar=f"/avatars/examiner_{i+1}.jpg",
                role=UserRole.EXAMINER,
                is_active=True,
                is_verified=True,
                institution_id=institution.id,
                wechat_openid=f"wx_examiner_{i+1}_{random.randint(100000, 999999)}",
                wechat_unionid=f"union_examiner_{i+1}_{random.randint(100000, 999999)}",
                last_login=datetime.now() - timedelta(days=random.randint(1, 15))
            )
            self.db.add(examiner)
            users.append(examiner)
            
            # 3个考生
            for j in range(3):
                candidate_name = f"{random.choice(self.surnames)}{random.choice(self.given_names)}"
                candidate = User(
                    username=f"student_{institution.code.lower()}_{j+1}",
                    email=self.generate_real_email(f"student_{i+1}_{j+1}"),
                    phone=self.generate_real_phone(),
                    password_hash=bcrypt.hashpw("student123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                    real_name=candidate_name,
                    id_card=self.generate_real_id_card(random.randint(1990, 2005)),
                    avatar=f"/avatars/student_{i+1}_{j+1}.jpg",
                    role=UserRole.CANDIDATE,
                    is_active=True,
                    is_verified=random.choice([True, False]),
                    institution_id=institution.id,
                    wechat_openid=f"wx_student_{i+1}_{j+1}_{random.randint(100000, 999999)}",
                    wechat_unionid=f"union_student_{i+1}_{j+1}_{random.randint(100000, 999999)}",
                    last_login=datetime.now() - timedelta(days=random.randint(1, 60))
                )
                self.db.add(candidate)
                users.append(candidate)
        
        self.db.commit()
        print(f"✅ 创建了 {len(users)} 个用户")
        return users
    
    def create_registrations(self, users: List[User], products: List[ExamProduct]) -> List[ExamRegistration]:
        """创建报名记录"""
        print("📝 创建考试报名数据...")
        registrations = []
        
        # 只为考生创建报名记录
        candidates = [u for u in users if u.role == UserRole.CANDIDATE]
        
        for i, candidate in enumerate(candidates):
            # 每个考生报名1-2个考试
            exam_count = random.randint(1, 2)
            selected_products = random.sample(products, exam_count)
            
            for j, product in enumerate(selected_products):
                registration = ExamRegistration(
                    user_id=candidate.id,
                    exam_product_id=product.id,
                    registration_number=f"REG{datetime.now().year}{i+1:03d}{j+1:02d}",
                    status=random.choice([
                        RegistrationStatus.APPROVED,
                        RegistrationStatus.APPROVED,
                        RegistrationStatus.APPROVED,  # 大部分通过
                        RegistrationStatus.PENDING,
                        RegistrationStatus.REJECTED
                    ]),
                    registration_fee=random.choice([500, 800, 1000, 1200]),
                    payment_status="已支付" if random.random() > 0.1 else "待支付",
                    created_at=datetime.now() - timedelta(days=random.randint(1, 90)),
                    notes=f"报名{product.name}"
                )
                
                self.db.add(registration)
                registrations.append(registration)
        
        self.db.commit()
        print(f"✅ 创建了 {len(registrations)} 条报名记录")
        return registrations
    
    def create_schedules(self, registrations: List[ExamRegistration], venues: List[Venue], users: List[User]) -> List[Schedule]:
        """创建考试日程"""
        print("📅 创建考试日程数据...")
        schedules = []
        
        # 只为已通过的报名创建日程
        approved_registrations = [r for r in registrations if r.status == RegistrationStatus.APPROVED]
        examiners = [u for u in users if u.role == UserRole.EXAMINER]
        
        for i, registration in enumerate(approved_registrations[:20]):  # 限制20个日程
            venue = random.choice(venues)
            examiner = random.choice(examiners)
            
            # 生成未来的考试日期
            schedule_date = datetime.now().date() + timedelta(days=random.randint(1, 30))
            start_time = datetime.combine(schedule_date, datetime.min.time().replace(hour=random.choice([9, 14]), minute=0))
            end_time = start_time + timedelta(minutes=registration.exam_product.duration_minutes)
            
            schedule = Schedule(
                registration_id=registration.id,
                venue_id=venue.id,
                schedule_date=schedule_date,
                start_time=start_time.time(),
                end_time=end_time.time(),
                status=random.choice([
                    ScheduleStatus.PENDING,
                    ScheduleStatus.PENDING,
                    ScheduleStatus.PENDING,  # 大部分待进行
                    ScheduleStatus.COMPLETED,
                    ScheduleStatus.IN_PROGRESS
                ]),
                exam_result=random.choice(["通过", "不通过", None]) if random.random() > 0.7 else None,
                score=random.randint(60, 100) if random.random() > 0.7 else None,
                created_by=examiner.id,
                notes=f"考试安排：{registration.exam_product.name}"
            )
            
            self.db.add(schedule)
            schedules.append(schedule)
        
        self.db.commit()
        print(f"✅ 创建了 {len(schedules)} 条考试日程")
        return schedules
    
    def create_checkins(self, schedules: List[Schedule], users: List[User]) -> List[CheckIn]:
        """创建签到记录"""
        print("✅ 创建签到记录数据...")
        checkins = []
        
        # 只为已完成的考试创建签到记录
        completed_schedules = [s for s in schedules if s.status == ScheduleStatus.COMPLETED]
        staff_users = [u for u in users if u.role in [UserRole.ADMIN, UserRole.EXAMINER]]
        
        for schedule in completed_schedules[:10]:  # 限制10个签到记录
            staff = random.choice(staff_users)
            
            # 签到时间应该在考试开始前
            checkin_time = datetime.combine(schedule.schedule_date, schedule.start_time) - timedelta(minutes=random.randint(5, 30))
            
            checkin = CheckIn(
                user_id=schedule.registration.user_id,
                venue_id=schedule.venue_id,
                schedule_id=schedule.id,
                staff_id=staff.id,
                checkin_time=checkin_time,
                method=random.choice([
                    CheckInMethod.QR_CODE,
                    CheckInMethod.QR_CODE,  # 大部分使用二维码
                    CheckInMethod.MANUAL,
                    CheckInMethod.NFC
                ]),
                status=random.choice([
                    CheckInStatus.SUCCESS,
                    CheckInStatus.SUCCESS,
                    CheckInStatus.SUCCESS,  # 大部分成功
                    CheckInStatus.LATE,
                    CheckInStatus.FAILED
                ]),
                device_info={
                    "device_type": "mobile",
                    "os": random.choice(["iOS", "Android"]),
                    "app_version": "1.0.0",
                    "location": f"{schedule.venue.building}{schedule.venue.room_number}"
                },
                notes="正常签到"
            )
            
            self.db.add(checkin)
            checkins.append(checkin)
        
        self.db.commit()
        print(f"✅ 创建了 {len(checkins)} 条签到记录")
        return checkins
    
    def generate_all_data(self):
        """生成所有数据"""
        try:
            print("🚀 开始生成精简真实测试数据...")
            
            # 清空现有数据
            self.clear_all_data()
            
            # 按顺序创建数据
            institutions = self.create_institutions()
            products = self.create_exam_products()
            venues = self.create_venues(institutions)
            users = self.create_users(institutions)
            registrations = self.create_registrations(users, products)
            schedules = self.create_schedules(registrations, venues, users)
            checkins = self.create_checkins(schedules, users)
            
            print("🎉 精简真实测试数据生成完成!")
            print(f"📊 数据统计:")
            print(f"   - 机构: {len(institutions)} 个")
            print(f"   - 考试产品: {len(products)} 个")
            print(f"   - 考场: {len(venues)} 个")
            print(f"   - 用户: {len(users)} 个")
            print(f"   - 报名记录: {len(registrations)} 条")
            print(f"   - 考试日程: {len(schedules)} 条")
            print(f"   - 签到记录: {len(checkins)} 条")
            
        except Exception as e:
            print(f"❌ 生成数据失败: {e}")
            self.db.rollback()
            raise
        finally:
            self.db.close()


if __name__ == "__main__":
    generator = RealisticDataGenerator()
    generator.generate_all_data()