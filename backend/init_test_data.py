#!/usr/bin/env python3
"""
初始化测试数据脚本 - 增强版
"""

import sys
import os
import random

# 添加当前目录到Python路径，适应不同的运行环境
current_dir = os.path.dirname(os.path.abspath(__file__))
if 'backend' in current_dir:
    # 在backend目录内运行
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
    # 在项目根目录运行
    sys.path.append(os.path.join(current_dir, 'backend'))
    from app.config.database import engine, SessionLocal
    from app.models.user import User, UserRole
    from app.models.institution import Institution
    from app.models.venue import Venue, VenueStatus
    from app.models.exam import ExamRegistration, ExamProduct, RegistrationStatus
    from app.models.schedule import Schedule, ScheduleStatus
    from app.models.checkin import CheckIn, CheckInStatus, CheckInMethod
    from app.utils.security import get_password_hash
from datetime import datetime, timedelta, date, time

def create_test_data():
    """创建测试数据"""
    db = SessionLocal()
    
    try:
        print("🚀 开始创建增强版测试数据...")
        
        # 1. 创建超级管理员
        print("📝 创建超级管理员...")
        existing_admin = db.query(User).filter(User.username == "admin").first()
        if existing_admin:
            print("⚠️ 超级管理员已存在，跳过创建")
            admin_user = existing_admin
        else:
            admin_user = User(
                username="admin",
                password_hash=get_password_hash("admin123"),
                email="admin@example.com",
                real_name="系统管理员",
                role=UserRole.SUPER_ADMIN,
                is_active=True,
                is_verified=True
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print("✅ 超级管理员创建成功")
        
        # 2. 创建多个机构
        print("📝 创建测试机构...")
        institutions_data = [
            {
                "name": "北京航空培训中心",
                "code": "BJAV001",
                "contact_person": "张主任",
                "contact_phone": "13800138001",
                "contact_email": "beijing@example.com",
                "address": "北京市朝阳区航空路123号"
            },
            {
                "name": "上海无人机学院",
                "code": "SHUAV002",
                "contact_person": "李院长",
                "contact_phone": "13800138002",
                "contact_email": "shanghai@example.com",
                "address": "上海市浦东新区科技路456号"
            },
            {
                "name": "深圳飞行技术学校",
                "code": "SZAV003",
                "contact_person": "王校长",
                "contact_phone": "13800138003",
                "contact_email": "shenzhen@example.com",
                "address": "深圳市南山区创新路789号"
            }
        ]
        
        institutions = []
        for inst_data in institutions_data:
            existing_institution = db.query(Institution).filter(Institution.code == inst_data["code"]).first()
            if existing_institution:
                institutions.append(existing_institution)
            else:
                institution = Institution(
                    name=inst_data["name"],
                    code=inst_data["code"],
                    contact_person=inst_data["contact_person"],
                    contact_phone=inst_data["contact_phone"],
                    contact_email=inst_data["contact_email"],
                    address=inst_data["address"],
                    is_active=True
                )
                db.add(institution)
                institutions.append(institution)
        
        db.commit()
        for inst in institutions:
            db.refresh(inst)
        print(f"✅ 创建了 {len(institutions)} 个机构")
        
        # 3. 创建机构管理员用户
        print("📝 创建机构管理员...")
        institution_users_data = [
            {
                "username": "beijing_admin",
                "real_name": "北京管理员",
                "email": "beijing_admin@example.com",
                "institution_id": institutions[0].id
            },
            {
                "username": "shanghai_admin",
                "real_name": "上海管理员",
                "email": "shanghai_admin@example.com",
                "institution_id": institutions[1].id
            },
            {
                "username": "shenzhen_admin",
                "real_name": "深圳管理员",
                "email": "shenzhen_admin@example.com",
                "institution_id": institutions[2].id
            }
        ]
        
        institution_users = []
        for user_data in institution_users_data:
            existing_user = db.query(User).filter(User.username == user_data["username"]).first()
            if existing_user:
                institution_users.append(existing_user)
            else:
                user = User(
                    username=user_data["username"],
                    password_hash=get_password_hash("123456"),
                    email=user_data["email"],
                    real_name=user_data["real_name"],
                    role=UserRole.OPERATOR,
                    institution_id=user_data["institution_id"],
                    is_active=True,
                    is_verified=True
                )
                db.add(user)
                institution_users.append(user)
        
        db.commit()
        for user in institution_users:
            db.refresh(user)
        print(f"✅ 创建了 {len(institution_users)} 个机构管理员")
        
        # 4. 创建考试产品
        print("📝 创建考试产品...")
        exam_products_data = [
            {
                "name": "多旋翼视距内驾驶员理论",
                "code": "MULTI_THEORY",
                "description": "多旋翼无人机视距内驾驶员理论考试",
                "duration_minutes": 60,
                "exam_type": "理论"
            },
            {
                "name": "多旋翼视距内驾驶员实操",
                "code": "MULTI_PRACTICE",
                "description": "多旋翼无人机视距内驾驶员实操考试",
                "duration_minutes": 15,
                "exam_type": "实操"
            },
            {
                "name": "固定翼视距内驾驶员理论",
                "code": "FIXED_THEORY",
                "description": "固定翼无人机视距内驾驶员理论考试",
                "duration_minutes": 60,
                "exam_type": "理论"
            },
            {
                "name": "固定翼视距内驾驶员实操",
                "code": "FIXED_PRACTICE",
                "description": "固定翼无人机视距内驾驶员实操考试",
                "duration_minutes": 20,
                "exam_type": "实操"
            },
            {
                "name": "无人机教员资格理论",
                "code": "INSTRUCTOR_THEORY",
                "description": "无人机教员资格理论考试",
                "duration_minutes": 90,
                "exam_type": "理论"
            },
            {
                "name": "无人机教员资格实操",
                "code": "INSTRUCTOR_PRACTICE",
                "description": "无人机教员资格实操考试",
                "duration_minutes": 30,
                "exam_type": "实操"
            }
        ]
        
        exam_products = []
        for product_data in exam_products_data:
            existing_product = db.query(ExamProduct).filter(ExamProduct.code == product_data["code"]).first()
            if existing_product:
                exam_products.append(existing_product)
            else:
                product = ExamProduct(**product_data)
                db.add(product)
                exam_products.append(product)
        
        db.commit()
        for product in exam_products:
            db.refresh(product)
        print(f"✅ 创建了 {len(exam_products)} 个考试产品")
        
        # 5. 创建考场
        print("📝 创建考场...")
        venues_data = [
            # 北京机构考场
            {
                "name": "北京理论考试教室A",
                "code": "BJ_THEORY_A",
                "description": "理论考试专用教室",
                "capacity": 50,
                "building": "教学楼",
                "floor": "2层",
                "room_number": "201",
                "status": VenueStatus.AVAILABLE,
                "institution_id": institutions[0].id
            },
            {
                "name": "北京多旋翼实操场A",
                "code": "BJ_MULTI_A",
                "description": "多旋翼实操考试场地",
                "capacity": 20,
                "building": "实操楼",
                "floor": "1层",
                "room_number": "A101",
                "status": VenueStatus.AVAILABLE,
                "institution_id": institutions[0].id
            },
            {
                "name": "北京固定翼实操场",
                "code": "BJ_FIXED_A",
                "description": "固定翼实操考试场地",
                "capacity": 15,
                "building": "实操楼",
                "floor": "1层",
                "room_number": "B101",
                "status": VenueStatus.AVAILABLE,
                "institution_id": institutions[0].id
            },
            # 上海机构考场
            {
                "name": "上海理论考试教室B",
                "code": "SH_THEORY_B",
                "description": "理论考试专用教室",
                "capacity": 40,
                "building": "主楼",
                "floor": "3层",
                "room_number": "301",
                "status": VenueStatus.AVAILABLE,
                "institution_id": institutions[1].id
            },
            {
                "name": "上海多旋翼实操场B",
                "code": "SH_MULTI_B",
                "description": "多旋翼实操考试场地",
                "capacity": 25,
                "building": "实训楼",
                "floor": "1层",
                "room_number": "C101",
                "status": VenueStatus.AVAILABLE,
                "institution_id": institutions[1].id
            },
            # 深圳机构考场
            {
                "name": "深圳综合考试教室",
                "code": "SZ_MIXED_A",
                "description": "理论和实操综合考试教室",
                "capacity": 30,
                "building": "综合楼",
                "floor": "2层",
                "room_number": "202",
                "status": VenueStatus.AVAILABLE,
                "institution_id": institutions[2].id
            },
            {
                "name": "深圳户外实操场",
                "code": "SZ_OUTDOOR_A",
                "description": "户外实操考试场地",
                "capacity": 35,
                "building": "户外场地",
                "floor": "1层",
                "room_number": "D101",
                "status": VenueStatus.MAINTENANCE,
                "institution_id": institutions[2].id
            }
        ]
        
        venues = []
        for venue_data in venues_data:
            existing_venue = db.query(Venue).filter(Venue.code == venue_data["code"]).first()
            if existing_venue:
                venues.append(existing_venue)
            else:
                venue = Venue(**venue_data)
                db.add(venue)
                venues.append(venue)
        
        db.commit()
        for venue in venues:
            db.refresh(venue)
        print(f"✅ 创建了 {len(venues)} 个考场")
        
        # 6. 创建测试考生
        print("📝 创建测试考生...")
        candidates_data = [
            # 北京机构考生
            {
                "real_name": "张三",
                "id_card": "110101199001011234",
                "phone": "13800138001",
                "email": "zhangsan@example.com",
                "institution_id": institutions[0].id
            },
            {
                "real_name": "李四",
                "id_card": "110101199002022345",
                "phone": "13800138002",
                "email": "lisi@example.com",
                "institution_id": institutions[0].id
            },
            {
                "real_name": "王五",
                "id_card": "110101199003033456",
                "phone": "13800138003",
                "email": "wangwu@example.com",
                "institution_id": institutions[0].id
            },
            # 上海机构考生
            {
                "real_name": "赵六",
                "id_card": "310101199004044567",
                "phone": "13800138004",
                "email": "zhaoliu@example.com",
                "institution_id": institutions[1].id
            },
            {
                "real_name": "钱七",
                "id_card": "310101199005055678",
                "phone": "13800138005",
                "email": "qianqi@example.com",
                "institution_id": institutions[1].id
            },
            # 深圳机构考生
            {
                "real_name": "孙八",
                "id_card": "440301199006066789",
                "phone": "13800138006",
                "email": "sunba@example.com",
                "institution_id": institutions[2].id
            },
            {
                "real_name": "周九",
                "id_card": "440301199007077890",
                "phone": "13800138007",
                "email": "zhoujiu@example.com",
                "institution_id": institutions[2].id
            },
            {
                "real_name": "吴十",
                "id_card": "440301199008088901",
                "phone": "13800138008",
                "email": "wushi@example.com",
                "institution_id": institutions[2].id
            }
        ]
        
        candidates = []
        for candidate_data in candidates_data:
            # 生成用户名
            username = f"candidate_{candidate_data['id_card'][-6:]}"
            
            # 检查考生是否已存在
            existing_candidate = db.query(User).filter(User.username == username).first()
            if existing_candidate:
                candidates.append(existing_candidate)
                continue
            
            # 创建考生用户
            candidate = User(
                username=username,
                password_hash=get_password_hash(candidate_data['id_card'][-6:]),
                real_name=candidate_data['real_name'],
                id_card=candidate_data['id_card'],
                phone=candidate_data['phone'],
                email=candidate_data['email'],
                role=UserRole.CANDIDATE,
                institution_id=candidate_data['institution_id'],
                is_active=True
            )
            db.add(candidate)
            candidates.append(candidate)
        
        db.commit()
        for candidate in candidates:
            db.refresh(candidate)
        print(f"✅ 创建了 {len(candidates)} 个测试考生")
        
        # 7. 创建报名记录
        # 7. 创建报名记录
        print("📝 创建报名记录...")
        registrations = []
        registration_statuses = [RegistrationStatus.APPROVED, RegistrationStatus.PENDING, RegistrationStatus.REJECTED]
        
        # 为每个考生创建报名记录
        for i, candidate in enumerate(candidates):
            if candidate.real_name == "张三":
                # 张三只创建一个理论考试报名
                theory_product = next((p for p in exam_products if "理论" in p.name), exam_products[0])
                registration = ExamRegistration(
                    user_id=candidate.id,
                    exam_product_id=theory_product.id,
                    registration_number=f"REG{datetime.now().strftime('%Y%m%d')}{candidate.id:03d}01",
                    status=RegistrationStatus.APPROVED
                )
                db.add(registration)
                registrations.append(registration)
            else:
                # 其他考生创建1-3个报名记录
                num_registrations = random.randint(1, 3)
                selected_products = random.sample(exam_products, min(num_registrations, len(exam_products)))
                
                for j, product in enumerate(selected_products):
                    registration = ExamRegistration(
                        user_id=candidate.id,
                        exam_product_id=product.id,
                        registration_number=f"REG{datetime.now().strftime('%Y%m%d')}{candidate.id:03d}{j+1:02d}",
                        status=random.choice(registration_statuses)
                    )
                    db.add(registration)
                    registrations.append(registration)
        
        db.commit()
        for registration in registrations:
            db.refresh(registration)
        print(f"✅ 创建了 {len(registrations)} 个报名记录")
        
        # 8. 创建考试排期
        # 8. 创建考试排期
        print("📝 创建考试排期...")
        schedules = []
        
        # 只为已批准的报名创建排期
        approved_registrations = [r for r in registrations if r.status == RegistrationStatus.APPROVED]
        
        # 生成未来7天的排期
        base_date = date.today()
        time_slots = [
            (time(9, 0), time(10, 0)),   # 9:00-10:00
            (time(10, 30), time(11, 30)), # 10:30-11:30
            (time(14, 0), time(15, 0)),   # 14:00-15:00
            (time(15, 30), time(16, 30)), # 15:30-16:30
        ]
        
        schedule_statuses = [ScheduleStatus.PENDING, ScheduleStatus.IN_PROGRESS, ScheduleStatus.COMPLETED]
        
        # 特殊处理：为张三（第一个考生）只创建一个考试安排
        zhangsan_registration = None
        other_registrations = []
        
        for registration in approved_registrations:
            candidate = db.query(User).filter(User.id == registration.user_id).first()
            if candidate and candidate.real_name == "张三":
                if zhangsan_registration is None:  # 只取张三的第一个报名
                    zhangsan_registration = registration
            else:
                other_registrations.append(registration)
        
        # 为张三创建唯一的考试安排
        if zhangsan_registration:
            # 选择合适的考场（理论考试用理论教室）
            if "理论" in zhangsan_registration.exam_product.exam_type:
                suitable_venues = [v for v in venues if "理论" in v.name]
            else:
                suitable_venues = [v for v in venues if "实操" in v.name]
            
            if not suitable_venues:
                suitable_venues = venues
            
            venue = suitable_venues[0]  # 使用第一个合适的考场
            schedule_date = base_date + timedelta(days=1)  # 明天
            start_time, end_time = time_slots[0]  # 9:00-10:00
            
            schedule = Schedule(
                registration_id=zhangsan_registration.id,
                venue_id=venue.id,
                schedule_date=schedule_date,
                start_time=start_time,
                end_time=end_time,
                status=ScheduleStatus.PENDING,  # 固定为待考状态
                remarks=f"考试安排 - {zhangsan_registration.exam_product.name}",
                created_by=admin_user.id
            )
            db.add(schedule)
            schedules.append(schedule)
        
        # 为其他考生创建考试安排（限制数量）
        for i, registration in enumerate(other_registrations[:8]):  # 限制其他考生的排期数量
            # 选择合适的考场（根据考试类型）
            suitable_venues = []
            if "理论" in registration.exam_product.exam_type:
                suitable_venues = [v for v in venues if "理论" in v.name or "综合" in v.name]
            else:
                suitable_venues = [v for v in venues if "实操" in v.name or "综合" in v.name]
            
            if not suitable_venues:
                suitable_venues = venues
            
            venue = random.choice(suitable_venues)
            schedule_date = base_date + timedelta(days=random.randint(0, 6))
            start_time, end_time = random.choice(time_slots)
            
            schedule = Schedule(
                registration_id=registration.id,
                venue_id=venue.id,
                schedule_date=schedule_date,
                start_time=start_time,
                end_time=end_time,
                status=random.choice(schedule_statuses),
                remarks=f"考试安排 - {registration.exam_product.name}",
                created_by=admin_user.id
            )
            db.add(schedule)
            schedules.append(schedule)
        
        db.commit()
        for schedule in schedules:
            db.refresh(schedule)
        print(f"✅ 创建了 {len(schedules)} 个考试排期")
        
        # 9. 创建签到记录
        print("📝 创建签到记录...")
        checkins = []
        
        # 只为已完成或进行中的排期创建签到记录
        completed_schedules = [s for s in schedules if s.status in [ScheduleStatus.COMPLETED, ScheduleStatus.IN_PROGRESS]]
        
        checkin_methods = [CheckInMethod.QR_CODE, CheckInMethod.MANUAL, CheckInMethod.NFC]
        checkin_statuses = [CheckInStatus.SUCCESS, CheckInStatus.LATE, CheckInStatus.FAILED]
        
        for schedule in completed_schedules:
            # 获取考生信息
            candidate = db.query(User).filter(User.id == schedule.registration.user_id).first()
            
            # 随机选择签到工作人员（机构管理员）
            staff = random.choice(institution_users)
            
            # 计算签到时间（考试开始前5-30分钟）
            schedule_datetime = datetime.combine(schedule.schedule_date, schedule.start_time)
            checkin_time = schedule_datetime - timedelta(minutes=random.randint(5, 30))
            
            checkin = CheckIn(
                user_id=candidate.id,
                venue_id=schedule.venue_id,
                schedule_id=schedule.id,
                staff_id=staff.id,
                checkin_time=checkin_time,
                method=random.choice(checkin_methods),
                status=random.choice(checkin_statuses),
                latitude=f"{39.9 + random.uniform(-0.1, 0.1):.6f}",  # 北京附近坐标
                longitude=f"{116.4 + random.uniform(-0.1, 0.1):.6f}",
                location_address=schedule.venue.address if hasattr(schedule.venue, 'address') else "考试地点",
                device_info={
                    "device_type": random.choice(["iPhone", "Android", "iPad"]),
                    "os_version": random.choice(["iOS 15.0", "Android 11", "iOS 14.0"]),
                    "app_version": "1.0.0"
                },
                ip_address=f"192.168.1.{random.randint(100, 200)}",
                user_agent="UAV Exam App/1.0.0",
                notes=f"考生 {candidate.real_name} 签到"
            )
            db.add(checkin)
            checkins.append(checkin)
        
        db.commit()
        for checkin in checkins:
            db.refresh(checkin)
        print(f"✅ 创建了 {len(checkins)} 个签到记录")
        
        # 10. 数据统计
        print("\n" + "="*60)
        print("🎉 增强版测试数据创建完成!")
        print("="*60)
        print(f"👥 用户: {len([admin_user] + institution_users + candidates)} 个")
        print(f"   - 超级管理员: 1 个")
        print(f"   - 机构管理员: {len(institution_users)} 个")
        print(f"   - 考生: {len(candidates)} 个")
        print(f"🏢 机构: {len(institutions)} 个")
        print(f"🏫 考场: {len(venues)} 个")
        print(f"📝 考试产品: {len(exam_products)} 个")
        print(f"📋 报名记录: {len(registrations)} 个")
        print(f"📅 考试排期: {len(schedules)} 个")
        print(f"✅ 签到记录: {len(checkins)} 个")
        
        print("\n📋 测试账号信息:")
        print("超级管理员: admin / admin123")
        print("机构管理员: beijing_admin, shanghai_admin, shenzhen_admin / 123456")
        print("考生登录: candidate_XXXXXX / 身份证号后6位")
        print("\n🔗 API文档: http://localhost:8000/api/v1/docs")
        
    except Exception as e:
        print(f"❌ 创建测试数据失败: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()