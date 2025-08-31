"""
数据生成方法实现
"""

import random
from datetime import datetime, timedelta, date, time
from typing import List, Dict, Any

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
        # 生成机构代码
        code = f"{city['code']}UAV{i+1:03d}"
        while code in generator.used_institution_codes:
            code = f"{city['code']}UAV{random.randint(100, 999)}"
        generator.used_institution_codes.add(code)
        
        # 生成机构名称
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
            address=f"{city['name']}市{random.choice(['科技路', '创新大道', '航空路', '发展路', '未来街'])}{random.randint(100, 999)}号",
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
        {"type": "综合", "prefix": "MIXED", "capacity_min": 30, "capacity_max": 80},
        {"type": "模拟", "prefix": "SIMULATOR", "capacity_min": 15, "capacity_max": 30}
    ]
    
    venues = []
    for institution in institutions:
        # 每个机构生成4-6个考场
        num_venues = random.randint(4, 6)
        for i in range(num_venues):
            venue_type = random.choice(venue_types)
            
            # 生成考场代码
            code = f"{institution.code[:3]}_{venue_type['prefix']}_{chr(65+i)}"
            while code in generator.used_venue_codes:
                code = f"{institution.code[:3]}_{venue_type['prefix']}_{random.randint(100, 999)}"
            generator.used_venue_codes.add(code)
            
            # 生成考场名称
            name = f"{institution.city}{venue_type['type']}考试{'教室' if venue_type['type'] in ['理论', '模拟'] else '场地'}{chr(65+i)}"
            
            # 状态分布：75%可用，15%占用中，10%维护中
            status_weights = [0.75, 0.15, 0.10]
            status = random.choices([VenueStatus.AVAILABLE, VenueStatus.OCCUPIED, VenueStatus.MAINTENANCE], 
                                  weights=status_weights)[0]
            
            venue = Venue(
                name=name,
                code=code,
                description=f"{venue_type['type']}考试专用场地，配备{random.choice(['标准', '高级', '专业'])}设备",
                capacity=random.randint(venue_type["capacity_min"], venue_type["capacity_max"]),
                current_count=random.randint(0, 8) if status == VenueStatus.OCCUPIED else 0,
                building=random.choice(["教学楼", "实训楼", "综合楼", "主楼", "科技楼"]),
                floor=f"{random.randint(1, 6)}层",
                room_number=f"{random.choice(['A', 'B', 'C', 'D'])}{random.randint(101, 699)}",
                equipment={
                    "computers": random.randint(30, 80) if venue_type['type'] in ['理论', '模拟'] else 0,
                    "drones": random.randint(8, 20) if venue_type['type'] != '理论' else 0,
                    "simulators": random.randint(5, 15) if venue_type['type'] == '模拟' else 0,
                    "cameras": random.randint(6, 12),
                    "projector": True,
                    "air_conditioning": True,
                    "sound_system": True
                },
                facilities={
                    "wifi": True,
                    "power_outlets": random.randint(30, 60),
                    "emergency_exit": True,
                    "fire_safety": True,
                    "accessibility": random.choice([True, False])
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
    
    # 2. 创建机构管理员 (每机构2-3人)
    for institution in institutions:
        city_info = next(city for city in generator.cities if city["name"] == institution.city)
        num_operators = random.randint(2, 3)
        
        for i in range(num_operators):
            roles = ["主管", "副主管", "操作员", "协调员"]
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
    
    # 3. 创建考生 (80人)
    for i in range(80):
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