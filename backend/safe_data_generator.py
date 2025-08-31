#!/usr/bin/env python3
"""
安全数据生成器 - 避免重复数据问题
"""

import sys
import os
import random
from datetime import datetime, timedelta, date, time
from typing import List, Dict, Any
import json

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
    from app.utils.security import get_password_hash
else:
    sys.path.append(os.path.join(current_dir, 'backend'))
    from app.config.database import engine, SessionLocal
    from app.models.user import User, UserRole
    from app.models.institution import Institution
    from app.models.venue import Venue, VenueStatus
    from app.models.exam import ExamRegistration, ExamProduct, RegistrationStatus
    from app.models.schedule import Schedule, ScheduleStatus
    from app.models.checkin import CheckIn, CheckInStatus, CheckInMethod
    from app.utils.security import get_password_hash


class SafeDataGenerator:
    """安全数据生成器 - 避免重复数据"""
    
    def __init__(self):
        self.db = SessionLocal()
        
        # 基础数据
        self.real_names = [
            "张伟", "王芳", "李娜", "刘强", "陈静", "杨洋", "赵敏", "黄磊", "周杰", "吴琼",
            "徐丽", "孙勇", "马超", "朱红", "胡斌", "郭宁", "何平", "高峰", "林青", "韩雪",
            "曹操", "孔明", "关羽", "张飞", "赵云", "马良", "黄忠", "魏延", "姜维", "邓艾",
            "司马懿", "诸葛亮", "周瑜", "鲁肃", "吕蒙", "陆逊", "孙权", "刘备", "曹丕", "袁绍",
            "董卓", "吕布", "貂蝉", "王昭君", "西施", "杨贵妃", "李清照", "苏轼", "辛弃疾", "岳飞"
        ]
        
        self.cities = [
            {"name": "北京", "code": "BJ", "province": "北京市", "area_code": "010"},
            {"name": "上海", "code": "SH", "province": "上海市", "area_code": "021"},
            {"name": "深圳", "code": "SZ", "province": "广东省", "area_code": "0755"},
            {"name": "广州", "code": "GZ", "province": "广东省", "area_code": "020"},
            {"name": "杭州", "code": "HZ", "province": "浙江省", "area_code": "0571"},
            {"name": "南京", "code": "NJ", "province": "江苏省", "area_code": "025"},
            {"name": "成都", "code": "CD", "province": "四川省", "area_code": "028"},
            {"name": "武汉", "code": "WH", "province": "湖北省", "area_code": "027"},
            {"name": "西安", "code": "XA", "province": "陕西省", "area_code": "029"},
            {"name": "重庆", "code": "CQ", "province": "重庆市", "area_code": "023"}
        ]
        
        self.exam_products_config = [
            {"name": "多旋翼视距内驾驶员理论考试", "code": "MULTI_THEORY", "duration": 60, "type": "理论"},
            {"name": "多旋翼视距内驾驶员实操考试", "code": "MULTI_PRACTICE", "duration": 15, "type": "实操"},
            {"name": "多旋翼超视距驾驶员理论考试", "code": "MULTI_BVLOS_THEORY", "duration": 90, "type": "理论"},
            {"name": "多旋翼超视距驾驶员实操考试", "code": "MULTI_BVLOS_PRACTICE", "duration": 25, "type": "实操"},
            {"name": "固定翼视距内驾驶员理论考试", "code": "FIXED_THEORY", "duration": 60, "type": "理论"},
            {"name": "固定翼视距内驾驶员实操考试", "code": "FIXED_PRACTICE", "duration": 20, "type": "实操"},
            {"name": "固定翼超视距驾驶员理论考试", "code": "FIXED_BVLOS_THEORY", "duration": 90, "type": "理论"},
            {"name": "固定翼超视距驾驶员实操考试", "code": "FIXED_BVLOS_PRACTICE", "duration": 30, "type": "实操"},
            {"name": "垂直起降视距内驾驶员理论考试", "code": "VTOL_THEORY", "duration": 75, "type": "理论"},
            {"name": "垂直起降视距内驾驶员实操考试", "code": "VTOL_PRACTICE", "duration": 25, "type": "实操"},
            {"name": "无人机教员资格理论考试", "code": "INSTRUCTOR_THEORY", "duration": 120, "type": "理论"},
            {"name": "无人机教员资格实操考试", "code": "INSTRUCTOR_PRACTICE", "duration": 40, "type": "实操"},
            {"name": "农业植保无人机操作证理论", "code": "AGRI_THEORY", "duration": 45, "type": "理论"},
            {"name": "农业植保无人机操作证实操", "code": "AGRI_PRACTICE", "duration": 20, "type": "实操"},
            {"name": "电力巡检无人机操作证理论", "code": "POWER_THEORY", "duration": 60, "type": "理论"},
            {"name": "电力巡检无人机操作证实操", "code": "POWER_PRACTICE", "duration": 30, "type": "实操"}
        ]
    
    def clear_all_data(self):
        """清空所有数据"""
        print("🧹 清空现有数据...")
        try:
            # 按依赖关系顺序删除
            self.db.query(CheckIn).delete()
            self.db.query(Schedule).delete()
            self.db.query(ExamRegistration).delete()
            self.db.query(Venue).delete()
            self.db.query(ExamProduct).delete()
            self.db.query(User).delete()
            self.db.query(Institution).delete()
            self.db.commit()
            print("✅ 数据清空完成")
        except Exception as e:
            print(f"⚠️ 清空数据时出现错误: {e}")
            self.db.rollback()
    
    def is_username_exists(self, username: str) -> bool:
        """检查用户名是否存在"""
        return self.db.query(User).filter(User.username == username).first() is not None
    
    def is_email_exists(self, email: str) -> bool:
        """检查邮箱是否存在"""
        return self.db.query(User).filter(User.email == email).first() is not None
    
    def is_phone_exists(self, phone: str) -> bool:
        """检查手机号是否存在"""
        return self.db.query(User).filter(User.phone == phone).first() is not None
    
    def is_id_card_exists(self, id_card: str) -> bool:
        """检查身份证是否存在"""
        return self.db.query(User).filter(User.id_card == id_card).first() is not None
    
    def is_institution_code_exists(self, code: str) -> bool:
        """检查机构代码是否存在"""
        return self.db.query(Institution).filter(Institution.code == code).first() is not None
    
    def is_venue_code_exists(self, code: str) -> bool:
        """检查考场代码是否存在"""
        return self.db.query(Venue).filter(Venue.code == code).first() is not None
    
    def is_registration_number_exists(self, reg_number: str) -> bool:
        """检查报名号是否存在"""
        return self.db.query(ExamRegistration).filter(ExamRegistration.registration_number == reg_number).first() is not None
    
    def generate_unique_phone(self) -> str:
        """生成唯一手机号"""
        max_attempts = 100
        for _ in range(max_attempts):
            phone = f"1{random.choice([3,4,5,6,7,8,9])}{random.randint(10000000, 99999999)}"
            if not self.is_phone_exists(phone):
                return phone
        raise Exception("无法生成唯一手机号")
    
    def generate_unique_email(self, prefix: str = None) -> str:
        """生成唯一邮箱"""
        domains = ["163.com", "qq.com", "gmail.com", "126.com", "sina.com", "outlook.com", "foxmail.com"]
        max_attempts = 100
        for _ in range(max_attempts):
            if prefix:
                email = f"{prefix}_{random.randint(1000, 9999)}@{random.choice(domains)}"
            else:
                email = f"user{random.randint(10000, 99999)}@{random.choice(domains)}"
            if not self.is_email_exists(email):
                return email
        raise Exception("无法生成唯一邮箱")
    
    def generate_unique_id_card(self, city_info: Dict) -> str:
        """生成唯一身份证号"""
        max_attempts = 100
        for _ in range(max_attempts):
            area_code = city_info["area_code"].replace("0", "1") + "01"
            birth_year = random.randint(1980, 2005)
            birth_month = random.randint(1, 12)
            birth_day = random.randint(1, 28)
            birth_date = f"{birth_year:04d}{birth_month:02d}{birth_day:02d}"
            sequence = f"{random.randint(100, 999)}"
            check_digit = random.randint(0, 9)
            
            id_card = f"{area_code}{birth_date}{sequence}{check_digit}"
            if not self.is_id_card_exists(id_card):
                return id_card
        raise Exception("无法生成唯一身份证号")
    
    def generate_unique_wechat_openid(self) -> str:
        """生成唯一微信openid"""
        max_attempts = 100
        for _ in range(max_attempts):
            openid = f"wx_{random.randint(100000000000000000, 999999999999999999)}"
            if not self.db.query(User).filter(User.wechat_openid == openid).first():
                return openid
        raise Exception("无法生成唯一微信openid")
    
    def create_institutions(self) -> List[Institution]:
        """创建机构数据"""
        print("🏢 创建机构数据...")
        
        institutions = []
        institution_types = ["培训学校", "职业院校", "企业培训中心", "技术学院", "航空学院"]
        
        for i, city in enumerate(self.cities):
            # 每个城市创建2个机构
            for j in range(2):
                max_attempts = 50
                for attempt in range(max_attempts):
                    code = f"{city['code']}UAV{i+1:02d}{j+1}_{attempt:02d}" if attempt > 0 else f"{city['code']}UAV{i+1:02d}{j+1}"
                    if not self.is_institution_code_exists(code):
                        break
                else:
                    raise Exception(f"无法为城市 {city['name']} 生成唯一机构代码")
                
                type_name = random.choice(institution_types)
                name_prefix = random.choice(["航空", "无人机", "飞行", "航天", "智能", "未来", "科技"])
                name = f"{city['name']}{name_prefix}{type_name}"
                
                institution = Institution(
                    name=name,
                    code=code,
                    type=type_name,
                    contact_person=random.choice(self.real_names),
                    contact_phone=self.generate_unique_phone(),
                    contact_email=self.generate_unique_email(f"{code.lower()}_contact"),
                    province=city["province"],
                    city=city["name"],
                    district=f"{city['name']}{random.choice(['高新区', '经开区', '新区', '开发区', '科技园区'])}",
                    address=f"{city['name']}市{random.choice(['科技路', '创新大道', '航空路', '未来街', '智慧路'])}{random.randint(100, 999)}号",
                    license_number=f"教民{city['area_code'][:3]}{random.randint(100000, 999999)}号",
                    business_license=f"{city['area_code']}{random.randint(1000000000, 9999999999)}",
                    is_active=True,
                    is_approved=True,
                    config={
                        "max_students": random.randint(200, 1000),
                        "specialties": random.sample(["多旋翼", "固定翼", "垂直起降", "农业植保", "电力巡检", "航拍测绘"], 
                                                    random.randint(3, 5)),
                        "certification_level": random.choice(["A级", "B级", "C级"]),
                        "established_year": random.randint(2015, 2023),
                        "staff_count": random.randint(20, 100),
                        "training_hours_per_year": random.randint(5000, 20000)
                    }
                )
                
                self.db.add(institution)
                institutions.append(institution)
        
        self.db.commit()
        for inst in institutions:
            self.db.refresh(inst)
        
        print(f"✅ 创建了 {len(institutions)} 个机构")
        return institutions
    
    def create_exam_products(self) -> List[ExamProduct]:
        """创建考试产品数据"""
        print("📋 创建考试产品数据...")
        
        exam_products = []
        for config in self.exam_products_config:
            # 检查是否已存在
            existing = self.db.query(ExamProduct).filter(ExamProduct.code == config["code"]).first()
            if existing:
                exam_products.append(existing)
                continue
                
            exam_product = ExamProduct(
                name=config["name"],
                code=config["code"],
                description=f"{config['name']} - 专业无人机{config['type']}考试，考试时长{config['duration']}分钟。适用于相关从业人员资格认证。",
                duration_minutes=config["duration"],
                exam_type=config["type"],
                is_active=True
            )
            self.db.add(exam_product)
            exam_products.append(exam_product)
        
        self.db.commit()
        for product in exam_products:
            self.db.refresh(product)
        
        print(f"✅ 创建了 {len(exam_products)} 个考试产品")
        return exam_products
    
    def create_venues(self, institutions: List[Institution]) -> List[Venue]:
        """创建考场数据"""
        print("🏛️ 创建考场数据...")
        
        venues = []
        venue_types = [
            {"type": "理论", "prefix": "THEORY", "capacity_min": 40, "capacity_max": 100},
            {"type": "实操", "prefix": "PRACTICE", "capacity_min": 20, "capacity_max": 60},
            {"type": "综合", "prefix": "MIXED", "capacity_min": 30, "capacity_max": 80}
        ]
        
        for institution in institutions:
            # 每个机构创建4-6个考场
            num_venues = random.randint(4, 6)
            for i in range(num_venues):
                venue_type = random.choice(venue_types)
                
                # 生成唯一考场代码
                max_attempts = 50
                for attempt in range(max_attempts):
                    code = f"{institution.code[:4]}_{venue_type['prefix']}_{chr(65+i)}_{attempt:02d}" if attempt > 0 else f"{institution.code[:4]}_{venue_type['prefix']}_{chr(65+i)}"
                    if not self.is_venue_code_exists(code):
                        break
                else:
                    continue  # 跳过这个考场
                
                name = f"{institution.city}{venue_type['type']}考试{'教室' if venue_type['type'] == '理论' else '场地'}{chr(65+i)}"
                
                capacity = random.randint(venue_type["capacity_min"], venue_type["capacity_max"])
                current_count = random.randint(0, min(10, capacity//4))
                
                venue = Venue(
                    name=name,
                    code=code,
                    description=f"{venue_type['type']}考试专用场地，配备完善的考试设备和安全设施，可容纳{capacity}人同时考试。",
                    capacity=capacity,
                    current_count=current_count,
                    building=random.choice(["教学楼", "实训楼", "综合楼", "主楼", "科技楼"]),
                    floor=f"{random.randint(1, 8)}层",
                    room_number=f"{random.choice(['A', 'B', 'C', 'D'])}{random.randint(101, 899)}",
                    equipment={
                        "computers": random.randint(30, 80) if venue_type['type'] == '理论' else random.randint(5, 15),
                        "drones": random.randint(10, 25) if venue_type['type'] != '理论' else 0,
                        "cameras": random.randint(8, 16),
                        "projector": True,
                        "sound_system": True,
                        "air_conditioning": True
                    },
                    facilities={
                        "wifi": True,
                        "power_outlets": random.randint(capacity, capacity*2),
                        "emergency_exit": True,
                        "fire_safety": True,
                        "security_cameras": random.randint(4, 8)
                    },
                    status=random.choices([VenueStatus.AVAILABLE, VenueStatus.OCCUPIED, VenueStatus.MAINTENANCE], 
                                        weights=[0.70, 0.20, 0.10])[0],
                    is_active=True,
                    institution_id=institution.id,
                    qr_code=f"VENUE_{code}_{random.randint(100000, 999999)}"
                )
                
                self.db.add(venue)
                venues.append(venue)
        
        self.db.commit()
        for venue in venues:
            self.db.refresh(venue)
        
        print(f"✅ 创建了 {len(venues)} 个考场")
        return venues
    
    def create_users(self, institutions: List[Institution]) -> List[User]:
        """创建用户数据"""
        print("👥 创建用户数据...")
        
        users = []
        
        # 1. 创建超级管理员 (3人) - 逐个提交
        admin_names = ["系统管理员", "技术总监", "运营总监"]
        for i, admin_name in enumerate(admin_names):
            max_attempts = 50
            username = None
            for attempt in range(max_attempts):
                test_username = f"admin{'_' + str(i+1) if i > 0 else ''}{'_' + str(attempt) if attempt > 0 else ''}"
                if not self.is_username_exists(test_username):
                    username = test_username
                    break
            
            if username is None:
                print(f"⚠️ 跳过管理员 {admin_name}，无法生成唯一用户名")
                continue
            
            user = User(
                username=username,
                email=self.generate_unique_email(f"admin{i+1}"),
                phone=self.generate_unique_phone(),
                password_hash=get_password_hash("admin123"),
                real_name=admin_name,
                id_card=self.generate_unique_id_card(self.cities[0]),
                avatar=f"/avatars/admin_{i+1}.jpg",
                role=UserRole.SUPER_ADMIN,
                is_active=True,
                is_verified=True,
                wechat_openid=self.generate_unique_wechat_openid(),
                wechat_unionid=f"union_{random.randint(100000000000000000, 999999999999999999)}",
                last_login=datetime.now() - timedelta(days=random.randint(0, 7))
            )
            
            try:
                self.db.add(user)
                self.db.commit()
                self.db.refresh(user)
                users.append(user)
                print(f"✅ 创建管理员: {username}")
            except Exception as e:
                print(f"⚠️ 创建管理员失败: {username}, 错误: {e}")
                self.db.rollback()
        
        # 2. 创建机构管理员 (每机构3人) - 逐个提交
        roles_names = ["主管", "副主管", "教务主任"]
        for institution in institutions:
            city_info = next(city for city in self.cities if city["name"] == institution.city)
            
            for i, role_name in enumerate(roles_names):
                max_attempts = 50
                username = None
                for attempt in range(max_attempts):
                    test_username = f"{city_info['code'].lower()}_admin_{i+1}{'_' + str(attempt) if attempt > 0 else ''}"
                    if not self.is_username_exists(test_username):
                        username = test_username
                        break
                
                if username is None:
                    print(f"⚠️ 跳过机构管理员 {institution.city}{role_name}，无法生成唯一用户名")
                    continue
                
                user = User(
                    username=username,
                    email=self.generate_unique_email(username),
                    phone=self.generate_unique_phone(),
                    password_hash=get_password_hash("123456"),
                    real_name=f"{institution.city}{role_name}",
                    id_card=self.generate_unique_id_card(city_info),
                    avatar=f"/avatars/staff_{random.randint(1, 20)}.jpg",
                    role=UserRole.OPERATOR,
                    institution_id=institution.id,
                    is_active=True,
                    is_verified=True,
                    wechat_openid=self.generate_unique_wechat_openid(),
                    wechat_unionid=f"union_{random.randint(100000000000000000, 999999999999999999)}",
                    last_login=datetime.now() - timedelta(days=random.randint(0, 30))
                )
                
                try:
                    self.db.add(user)
                    self.db.commit()
                    self.db.refresh(user)
                    users.append(user)
                    print(f"✅ 创建机构管理员: {username}")
                except Exception as e:
                    print(f"⚠️ 创建机构管理员失败: {username}, 错误: {e}")
                    self.db.rollback()
        
        # 3. 创建考生 (每机构15-20人) - 逐个提交
        for institution in institutions:
            city_info = next(city for city in self.cities if city["name"] == institution.city)
            num_candidates = random.randint(15, 20)
            
            for i in range(num_candidates):
                id_card = self.generate_unique_id_card(city_info)
                
                max_attempts = 50
                username = None
                for attempt in range(max_attempts):
                    test_username = f"candidate_{id_card[-6:]}{'_' + str(attempt) if attempt > 0 else ''}"
                    if not self.is_username_exists(test_username):
                        username = test_username
                        break
                
                if username is None:
                    print(f"⚠️ 跳过考生，无法生成唯一用户名")
                    continue
                
                user = User(
                    username=username,
                    email=self.generate_unique_email(),
                    phone=self.generate_unique_phone(),
                    password_hash=get_password_hash(id_card[-6:]),
                    real_name=random.choice(self.real_names),
                    id_card=id_card,
                    avatar=f"/avatars/candidate_{random.randint(1, 50)}.jpg",
                    role=UserRole.CANDIDATE,
                    institution_id=institution.id,
                    is_active=True,
                    is_verified=random.choices([True, False], weights=[0.85, 0.15])[0],
                    wechat_openid=self.generate_unique_wechat_openid(),
                    wechat_unionid=f"union_{random.randint(100000000000000000, 999999999999999999)}",
                    last_login=datetime.now() - timedelta(days=random.randint(0, 60))
                )
                
                try:
                    self.db.add(user)
                    self.db.commit()
                    self.db.refresh(user)
                    users.append(user)
                    if len(users) % 10 == 0:  # 每10个用户打印一次进度
                        print(f"✅ 已创建 {len(users)} 个用户")
                except Exception as e:
                    print(f"⚠️ 创建考生失败: {username}, 错误: {e}")
                    self.db.rollback()
        
        print(f"✅ 总共创建了 {len(users)} 个用户")
        return users
    
    def create_exam_registrations(self, users: List[User], exam_products: List[ExamProduct]) -> List[ExamRegistration]:
        """创建考试报名数据"""
        print("📝 创建考试报名数据...")
        
        candidates = [user for user in users if user.role == UserRole.CANDIDATE]
        registrations = []
        
        for candidate in candidates:
            # 每个考生报名2-4个考试
            num_registrations = random.randint(2, 4)
            selected_products = random.sample(exam_products, min(num_registrations, len(exam_products)))
            
            for j, product in enumerate(selected_products):
                reg_date = datetime.now() - timedelta(days=random.randint(1, 180))
                
                max_attempts = 50
                for attempt in range(max_attempts):
                    reg_number = f"REG{reg_date.strftime('%Y%m%d')}{candidate.id:04d}{j+1:02d}{'_' + str(attempt) if attempt > 0 else ''}"
                    if not self.is_registration_number_exists(reg_number):
                        break
                else:
                    continue  # 跳过这个报名
                
                status = random.choices([RegistrationStatus.APPROVED, RegistrationStatus.PENDING, 
                                       RegistrationStatus.REJECTED, RegistrationStatus.CANCELLED], 
                                      weights=[0.60, 0.25, 0.10, 0.05])[0]
                
                registration = ExamRegistration(
                    user_id=candidate.id,
                    exam_product_id=product.id,
                    registration_number=reg_number,
                    status=status,
                    notes=f"考生{candidate.real_name}报名{product.name}",
                    created_at=reg_date,
                    updated_at=reg_date + timedelta(days=random.randint(1, 15))
                )
                self.db.add(registration)
                registrations.append(registration)
        
        self.db.commit()
        for registration in registrations:
            self.db.refresh(registration)
        
        print(f"✅ 创建了 {len(registrations)} 条报名记录")
        return registrations
    
    def create_schedules(self, registrations: List[ExamRegistration], venues: List[Venue], users: List[User]) -> List[Schedule]:
        """创建考试日程数据"""
        print("📅 创建考试日程数据...")
        
        approved_registrations = [reg for reg in registrations if reg.status == RegistrationStatus.APPROVED]
        admins = [user for user in users if user.role in [UserRole.SUPER_ADMIN, UserRole.OPERATOR]]
        
        schedules = []
        time_slots = [
            (time(9, 0), time(10, 30)),
            (time(10, 45), time(12, 15)),
            (time(14, 0), time(15, 30)),
            (time(15, 45), time(17, 15))
        ]
        
        # 为前100个已批准的报名创建排期
        for registration in approved_registrations[:100]:
            schedule_date = date.today() + timedelta(days=random.randint(1, 60))
            start_time, end_time = random.choice(time_slots)
            
            # 选择合适的考场
            suitable_venues = [v for v in venues if v.institution_id == registration.user.institution_id and v.is_active]
            if not suitable_venues:
                suitable_venues = [v for v in venues if v.is_active]
            
            if not suitable_venues:
                continue
                
            venue = random.choice(suitable_venues)
            
            status = random.choices([ScheduleStatus.PENDING, ScheduleStatus.COMPLETED, 
                                   ScheduleStatus.IN_PROGRESS, ScheduleStatus.CANCELLED], 
                                  weights=[0.50, 0.30, 0.15, 0.05])[0]
            
            schedule = Schedule(
                registration_id=registration.id,
                venue_id=venue.id,
                schedule_date=schedule_date,
                start_time=start_time,
                end_time=end_time,
                status=status,
                remarks=f"考试安排：{registration.exam_product.name}，考场：{venue.name}",
                created_by=random.choice(admins).id if admins else None,
                created_at=datetime.now() - timedelta(days=random.randint(1, 30)),
                updated_at=datetime.now() - timedelta(days=random.randint(0, 10))
            )
            self.db.add(schedule)
            schedules.append(schedule)
        
        self.db.commit()
        for schedule in schedules:
            self.db.refresh(schedule)
        
        print(f"✅ 创建了 {len(schedules)} 条考试日程")
        return schedules
    
    def create_checkins(self, schedules: List[Schedule], users: List[User]) -> List[CheckIn]:
        """创建签到记录数据"""
        print("✅ 创建签到记录数据...")
        
        staff_users = [user for user in users if user.role in [UserRole.OPERATOR, UserRole.EXAMINER]]
        checkins = []
        
        # 为已完成和进行中的考试创建签到记录
        active_schedules = [s for s in schedules if s.status in [ScheduleStatus.COMPLETED, ScheduleStatus.IN_PROGRESS]]
        
        for schedule in active_schedules:
            # 获取考生信息
            candidate = schedule.registration.user
            
            # 选择签到工作人员
            suitable_staff = [s for s in staff_users if s.institution_id == candidate.institution_id]
            if not suitable_staff:
                suitable_staff = staff_users
            
            if not suitable_staff:
                continue
                
            staff = random.choice(suitable_staff)
            
            status = random.choices([CheckInStatus.SUCCESS, CheckInStatus.LATE, CheckInStatus.FAILED], 
                                  weights=[0.80, 0.15, 0.05])[0]
            
            method = random.choices([CheckInMethod.QR_CODE, CheckInMethod.MANUAL, CheckInMethod.NFC], 
                                  weights=[0.70, 0.20, 0.10])[0]
            
            # 计算签到时间
            schedule_datetime = datetime.combine(schedule.schedule_date, schedule.start_time)
            if status == CheckInStatus.SUCCESS:
                checkin_time = schedule_datetime - timedelta(minutes=random.randint(5, 45))
            elif status == CheckInStatus.LATE:
                checkin_time = schedule_datetime + timedelta(minutes=random.randint(1, 20))
            else:  # FAILED
                checkin_time = schedule_datetime - timedelta(minutes=random.randint(1, 10))
            
            checkin = CheckIn(
                user_id=candidate.id,
                venue_id=schedule.venue_id,
                schedule_id=schedule.id,
                staff_id=staff.id,
                checkin_time=checkin_time,
                method=method,
                status=status,
                latitude=f"{39.9 + random.uniform(-0.1, 0.1):.6f}",
                longitude=f"{116.4 + random.uniform(-0.1, 0.1):.6f}",
                location_address=f"{candidate.institution.address}附近",
                device_info={
                    "device_type": random.choice(["iPhone 14", "Samsung Galaxy S23", "Huawei Mate 50"]),
                    "os_version": random.choice(["iOS 16.5", "Android 13", "HarmonyOS 3.0"]),
                    "app_version": "1.2.0"
                },
                ip_address=f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                user_agent="UAV-Exam-App/1.2.0",
                notes=f"考生{candidate.real_name}签到记录",
                data={"checkin_source": "mobile_app"},
                created_at=checkin_time,
                updated_at=checkin_time
            )
            self.db.add(checkin)
            checkins.append(checkin)
        
        self.db.commit()
        for checkin in checkins:
            self.db.refresh(checkin)
        
        print(f"✅ 创建了 {len(checkins)} 条签到记录")
        return checkins
    
    def generate_all_data(self):
        """生成所有数据"""
        try:
            print("🚀 开始生成安全测试数据...")
            print("=" * 60)
            
            # 0. 清空现有数据
            self.clear_all_data()
            
            # 1. 创建机构
            institutions = self.create_institutions()
            
            # 2. 创建考试产品
            exam_products = self.create_exam_products()
            
            # 3. 创建考场
            venues = self.create_venues(institutions)
            
            # 4. 创建用户
            users = self.create_users(institutions)
            
            # 5. 创建报名记录
            registrations = self.create_exam_registrations(users, exam_products)
            
            # 6. 创建考试日程
            schedules = self.create_schedules(registrations, venues, users)
            
            # 7. 创建签到记录
            checkins = self.create_checkins(schedules, users)
            
            # 统计信息
            print("\n" + "=" * 60)
            print("🎉 安全测试数据生成完成!")
            print("=" * 60)
            
            user_stats = {}
            for user in users:
                role_name = {
                    UserRole.SUPER_ADMIN: "超级管理员",
                    UserRole.OPERATOR: "机构管理员", 
                    UserRole.EXAMINER: "监考员",
                    UserRole.CANDIDATE: "考生"
                }.get(user.role, "其他")
                user_stats[role_name] = user_stats.get(role_name, 0) + 1
            
            print(f"🏢 机构: {len(institutions)} 个")
            print(f"🏛️ 考场: {len(venues)} 个")
            print(f"📋 考试产品: {len(exam_products)} 个")
            print(f"👥 用户: {len(users)} 个")
            for role, count in user_stats.items():
                print(f"   - {role}: {count} 个")
            print(f"📝 报名记录: {len(registrations)} 条")
            print(f"📅 考试日程: {len(schedules)} 条")
            print(f"✅ 签到记录: {len(checkins)} 条")
            
            print("\n📋 测试账号信息:")
            print("超级管理员: admin / admin123")
            print("机构管理员: {城市代码}_admin_1 / 123456")
            print("考生: candidate_XXXXXX / 身份证号后6位")
            
        except Exception as e:
            print(f"❌ 生成数据失败: {e}")
            import traceback
            traceback.print_exc()
            self.db.rollback()
        finally:
            self.db.close()


if __name__ == "__main__":
    generator = SafeDataGenerator()
    generator.generate_all_data()