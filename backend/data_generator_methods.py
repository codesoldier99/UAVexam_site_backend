"""
数据生成方法实现
"""

import random
from datetime import datetime, timedelta, date, time
from typing import List

from app.models.user import User, UserRole
from app.models.institution import Institution
from app.models.venue import Venue, VenueStatus
from app.models.exam import ExamProduct, ExamRegistration, RegistrationStatus
from app.models.schedule import Schedule, ScheduleStatus
from app.models.checkin import CheckIn, CheckInStatus, CheckInMethod

def create_institutions(generator):
    """创建机构数据"""
    print("🏢 创建机构数据...")
    
    institution_types = ["培训学校", "职业院校", "企业培训中心", "技术学院", "航空学院"]
    institution_names = ["航空", "无人机", "飞行", "航天", "科技", "智能", "未来"]
    
    institutions = []
    for i, city in enumerate(generator.cities):
        code = f"{city['code']}UAV{i+1:03d}"
        while code in generator.used_institution_codes:
            code = f"{city['code']}UAV{random.randint(100, 999)}"
        generator.used_institution_codes.add(code)
        
        type_name = random.choice(institution_types)
        name_prefix = random.choice(institution_names)
        name = f"{city['name']}{name_prefix}{type_name}"
        
        institution = Institution(
            name=name,
            code=code,
            type=type_name,
            contact_person=random.choice(generator.real_names),
            contact_phone=generator.generate_unique_phone(),
            contact_email=generator.generate_unique_email(),
            province=city["province"],
            city=city["name"],
            district=f"{city['name']}{random.choice(['高新区', '经开区', '新区', '区', '县'])}",
            address=f"{city['name']}市{random.choice(['科技路', '创新大道', '航空路'])}{random.randint(100, 999)}号",
            license_number=f"教民{city['area_code'][:4]}{random.randint(100000, 999999)}号",
            business_license=f"{city['area_code']}{random.randint(1000000000, 9999999999)}",
            is_active=True,
            is_approved=True,
            config={
                "max_students": random.randint(200, 800),
                "specialties": random.sample(["多旋翼", "固定翼", "垂直起降", "农业植保", "电力巡检"], 
                                            random.randint(2, 4)),
                "certification_level": random.choice(["A级", "B级", "C级"])
            }
        )
        
        generator.session.add(institution)
        institutions.append(institution)
    
    generator.session.commit()
    print(f"✅ 创建了 {len(institutions)} 个机构")
    return institutions

def create_venues(generator, institutions: List[Institution]):
    """创建考场数据"""
    print("🏛️  创建考场数据...")
    
    venue_types = [
        {"type": "理论", "prefix": "THEORY", "capacity_min": 40, "capacity_max": 100},
        {"type": "实操", "prefix": "PRACTICE", "capacity_min": 20, "capacity_max": 50},
        {"type": "综合", "prefix": "MIXED", "capacity_min": 30, "capacity_max": 80}
    ]
    
    venues = []
    for institution in institutions:
        num_venues = random.randint(3, 5)
        for i in range(num_venues):
            venue_type = random.choice(venue_types)
            
            code = f"{institution.code[:3]}_{venue_type['prefix']}_{chr(65+i)}"
            while code in generator.used_venue_codes:
                code = f"{institution.code[:3]}_{venue_type['prefix']}_{random.randint(100, 999)}"
            generator.used_venue_codes.add(code)
            
            name = f"{institution.city}{venue_type['type']}考试{'教室' if venue_type['type'] == '理论' else '场地'}{chr(65+i)}"
            
            status_weights = [0.75, 0.15, 0.10]
            status = random.choices([VenueStatus.AVAILABLE, VenueStatus.OCCUPIED, VenueStatus.MAINTENANCE], 
                                  weights=status_weights)[0]
            
            venue = Venue(
                name=name,
                code=code,
                description=f"{venue_type['type']}考试专用场地",
                capacity=random.randint(venue_type["capacity_min"], venue_type["capacity_max"]),
                current_count=random.randint(0, 8) if status == VenueStatus.OCCUPIED else 0,
                building=random.choice(["教学楼", "实训楼", "综合楼", "主楼"]),
                floor=f"{random.randint(1, 6)}层",
                room_number=f"{random.choice(['A', 'B', 'C'])}{random.randint(101, 699)}",
                equipment={
                    "computers": random.randint(30, 80) if venue_type['type'] == '理论' else 0,
                    "drones": random.randint(8, 20) if venue_type['type'] != '理论' else 0,
                    "cameras": random.randint(6, 12),
                    "projector": True,
                    "air_conditioning": True
                },
                facilities={
                    "wifi": True,
                    "power_outlets": random.randint(30, 60),
                    "emergency_exit": True,
                    "fire_safety": True
                },
                status=status,
                is_active=True,
                institution_id=institution.id,
                qr_code=f"VENUE_{code}_{random.randint(100000, 999999)}"
            )
            
            generator.session.add(venue)
            venues.append(venue)
    
    generator.session.commit()
    print(f"✅ 创建了 {len(venues)} 个考场")
    return venues

def create_exam_products(generator):
    """创建考试产品数据"""
    print("📋 创建考试产品数据...")
    
    exam_products = []
    for config in generator.exam_products_config:
        exam_product = ExamProduct(
            name=config["name"],
            code=config["code"],
            description=f"{config['name']} - 考试时长{config['duration']}分钟",
            duration_minutes=config["duration"],
            exam_type=config["type"],
            is_active=True
        )
        generator.session.add(exam_product)
        exam_products.append(exam_product)
    
    generator.session.commit()
    print(f"✅ 创建了 {len(exam_products)} 个考试产品")
    return exam_products

def create_users(generator, institutions: List[Institution]):
    """创建用户数据"""
    print("👥 创建用户数据...")
    
    users = []
    
    # 1. 创建超级管理员 (2人)
    for i in range(2):
        username = f"admin{'_backup' if i == 1 else ''}"
        user = User(
            username=username,
            email=f"admin{i+1}@uav-exam.com",
            phone=generator.generate_unique_phone(),
            password_hash=generator.hash_password("admin123"),
            real_name=f"系统管理员{'(备用)' if i == 1 else ''}",
            role=UserRole.SUPER_ADMIN,
            is_active=True,
            is_verified=True
        )
        generator.session.add(user)
        users.append(user)
        generator.used_usernames.add(username)
    
    # 2. 创建机构管理员 (每机构2人)
    for institution in institutions:
        city_info = next(city for city in generator.cities if city["name"] == institution.city)
        
        for i in range(2):
            roles = ["主管", "副主管"]
            username = f"{city_info['code'].lower()}_admin_{i+1}"
            
            user = User(
                username=username,
                email=generator.generate_unique_email(),
                phone=generator.generate_unique_phone(),
                password_hash=generator.hash_password("123456"),
                real_name=f"{institution.city}{roles[i]}",
                role=UserRole.OPERATOR,
                institution_id=institution.id,
                is_active=True,
                is_verified=True
            )
            generator.session.add(user)
            users.append(user)
            generator.used_usernames.add(username)
    
    # 3. 创建考生 (60人)
    for i in range(60):
        institution = random.choice(institutions)
        city_info = next(city for city in generator.cities if city["name"] == institution.city)
        
        id_card = generator.generate_unique_id_card(city_info)
        username = f"candidate_{id_card[-6:]}"
        
        user = User(
            username=username,
            email=generator.generate_unique_email(),
            phone=generator.generate_unique_phone(),
            password_hash=generator.hash_password(id_card[-6:]),
            real_name=random.choice(generator.real_names),
            id_card=id_card,
            role=UserRole.CANDIDATE,
            institution_id=institution.id,
            is_active=True,
            is_verified=random.choices([True, False], weights=[0.85, 0.15])[0],
            wechat_openid=f"wx_{random.randint(100000000000000000, 999999999999999999)}"
        )
        generator.session.add(user)
        users.append(user)
        generator.used_usernames.add(username)
    
    generator.session.commit()
    print(f"✅ 创建了 {len(users)} 个用户")
    return users

def create_exam_registrations(generator, users: List[User], exam_products: List[ExamProduct]):
    """创建考试报名数据"""
    print("📝 创建考试报名数据...")
    
    candidates = [user for user in users if user.role == UserRole.CANDIDATE]
    registrations = []
    
    for candidate in candidates:
        num_registrations = random.randint(2, 5)
        selected_products = random.sample(exam_products, min(num_registrations, len(exam_products)))
        
        for j, product in enumerate(selected_products):
            reg_date = datetime.now() - timedelta(days=random.randint(0, 120))
            reg_number = f"REG{reg_date.strftime('%Y%m%d')}{candidate.id:03d}{j+1:02d}"
            
            while reg_number in generator.used_registration_numbers:
                reg_number = f"REG{reg_date.strftime('%Y%m%d')}{candidate.id:03d}{random.randint(10, 99)}"
            generator.used_registration_numbers.add(reg_number)
            
            status_weights = [0.65, 0.25, 0.05, 0.05]
            status = random.choices([RegistrationStatus.APPROVED, RegistrationStatus.PENDING, 
                                   RegistrationStatus.REJECTED, RegistrationStatus.CANCELLED], 
                                  weights=status_weights)[0]
            
            registration = ExamRegistration(
                user_id=candidate.id,
                exam_product_id=product.id,
                registration_number=reg_number,
                status=status,
                notes=generate_registration_note(candidate, product, status),
                created_at=reg_date,
                updated_at=reg_date + timedelta(days=random.randint(1, 10))
            )
            generator.session.add(registration)
            registrations.append(registration)
    
    generator.session.commit()
    print(f"✅ 创建了 {len(registrations)} 条报名记录")
    return registrations

def generate_registration_note(candidate: User, product: ExamProduct, status: RegistrationStatus) -> str:
    """生成报名备注"""
    if status == RegistrationStatus.APPROVED:
        return f"考生{candidate.real_name}报名{product.name}，审核通过"
    elif status == RegistrationStatus.PENDING:
        return f"考生{candidate.real_name}报名{product.name}，待审核"
    elif status == RegistrationStatus.REJECTED:
        reasons = ["资料不全", "不符合报考条件", "培训时长不足", "体检不合格"]
        return f"审核未通过：{random.choice(reasons)}"
    else:
        return f"考生主动取消报名"

def create_schedules(generator, registrations: List[ExamRegistration], venues: List[Venue], users: List[User]):
    """创建考试日程数据"""
    print("📅 创建考试日程数据...")
    
    approved_registrations = [reg for reg in registrations if reg.status == RegistrationStatus.APPROVED]
    admins = [user for user in users if user.role == UserRole.SUPER_ADMIN]
    
    schedules = []
    time_slots = [
        (time(9, 0), time(10, 30)),
        (time(10, 45), time(12, 15)),
        (time(14, 0), time(15, 30)),
        (time(15, 45), time(17, 15))
    ]
    
    for registration in approved_registrations[:100]:
        schedule_date = date.today() + timedelta(days=random.randint(7, 30))
        start_time, end_time = random.choice(time_slots)
        
        suitable_venues = [v for v in venues if v.institution_id == registration.user.institution_id]
        if not suitable_venues:
            suitable_venues = venues
        
        venue = random.choice(suitable_venues)
        
        status_weights = [0.70, 0.20, 0.10]
        status = random.choices([ScheduleStatus.SCHEDULED, ScheduleStatus.COMPLETED, ScheduleStatus.CANCELLED], 
                              weights=status_weights)[0]
        
        schedule = Schedule(
            exam_registration_id=registration.id,
            venue_id=venue.id,
            exam_date=schedule_date,
            start_time=start_time,
            end_time=end_time,
            status=status,
            max_candidates=random.randint(20, venue.capacity),
            current_candidates=random.randint(1, 15) if status != ScheduleStatus.CANCELLED else 0,
            created_by=random.choice(admins).id,
            notes=f"考试安排：{registration.exam_product.name}",
            created_at=datetime.now() - timedelta(days=random.randint(1, 30)),
            updated_at=datetime.now() - timedelta(days=random.randint(0, 5))
        )
        generator.session.add(schedule)
        schedules.append(schedule)
    
    generator.session.commit()
    print(f"✅ 创建了 {len(schedules)} 条考试日程")
    return schedules

def create_checkins(generator, schedules: List[Schedule], users: List[User]):
    """创建签到记录数据"""
    print("✅ 创建签到记录数据...")
    
    candidates = [user for user in users if user.role == UserRole.CANDIDATE]
    checkins = []
    
    active_schedules = [s for s in schedules if s.status in [ScheduleStatus.SCHEDULED, ScheduleStatus.COMPLETED]]
    
    for schedule in active_schedules[:50]:
        num_checkins = random.randint(1, min(8, len(candidates)))
        selected_candidates = random.sample(candidates, num_checkins)
        
        for candidate in selected_candidates:
            status_weights = [0.70, 0.20, 0.10]
            status = random.choices([CheckInStatus.CHECKED_IN, CheckInStatus.ABSENT, CheckInStatus.LATE], 
                                  weights=status_weights)[0]
            
            method_weights = [0.60, 0.30, 0.10]
            method = random.choices([CheckInMethod.QR_CODE, CheckInMethod.MANUAL, CheckInMethod.ID_CARD], 
                                  weights=method_weights)[0]
            
            if status == CheckInStatus.CHECKED_IN:
                checkin_time = datetime.combine(schedule.exam_date, schedule.start_time) - timedelta(minutes=random.randint(5, 30))
            elif status == CheckInStatus.LATE:
                checkin_time = datetime.combine(schedule.exam_date, schedule.start_time) + timedelta(minutes=random.randint(1, 15))
            else:
                checkin_time = None
            
            checkin = CheckIn(
                user_id=candidate.id,
                schedule_id=schedule.id,
                status=status,
                method=method,
                checkin_time=checkin_time,
                notes=f"考生{candidate.real_name}{'签到成功' if status == CheckInStatus.CHECKED_IN else '迟到' if status == CheckInStatus.LATE else '缺席'}",
                created_at=checkin_time or datetime.now(),
                updated_at=checkin_time or datetime.now()
            )
            generator.session.add(checkin)
            checkins.append(checkin)
    
    generator.session.commit()
    print(f"✅ 创建了 {len(checkins)} 条签到记录")
    return checkins