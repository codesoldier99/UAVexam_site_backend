#!/usr/bin/env python3
"""
UAV考试系统测试数据扩增脚本
在现有数据基础上扩增到每表50条数据
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

def check_current_data_count(db):
    """检查当前各表的数据数量"""
    print("\n📊 当前数据统计:")
    
    institutions_count = db.query(Institution).count()
    users_count = db.query(User).count()
    exam_products_count = db.query(ExamProduct).count()
    venues_count = db.query(Venue).count()
    registrations_count = db.query(ExamRegistration).count()
    schedules_count = db.query(Schedule).count()
    checkins_count = db.query(CheckIn).count()
    
    print(f"   机构 (institutions): {institutions_count} 条")
    print(f"   用户 (users): {users_count} 条")
    print(f"   考试产品 (exam_products): {exam_products_count} 条")
    print(f"   考场 (venues): {venues_count} 条")
    print(f"   考试报名 (exam_registrations): {registrations_count} 条")
    print(f"   考试安排 (schedules): {schedules_count} 条")
    print(f"   签到记录 (checkins): {checkins_count} 条")
    
    return {
        'institutions': institutions_count,
        'users': users_count,
        'exam_products': exam_products_count,
        'venues': venues_count,
        'registrations': registrations_count,
        'schedules': schedules_count,
        'checkins': checkins_count
    }

def expand_institutions_data(db):
    """扩增机构数据到50条"""
    current_count = db.query(Institution).count()
    target_count = 50
    
    if current_count >= target_count:
        print(f"   ✅ 机构数据已有 {current_count} 条，无需扩增")
        return
    
    need_count = target_count - current_count
    print(f"   📝 需要新增 {need_count} 条机构数据")
    
    # 城市和机构类型
    cities = ["北京", "上海", "深圳", "广州", "杭州", "南京", "武汉", "成都", "西安", "重庆", 
              "天津", "青岛", "大连", "厦门", "苏州", "无锡", "宁波", "长沙", "郑州", "济南",
              "福州", "合肥", "昆明", "南宁", "海口", "石家庄", "太原", "沈阳", "长春", "哈尔滨",
              "呼和浩特", "银川", "西宁", "乌鲁木齐", "拉萨", "兰州", "贵阳", "南昌", "温州", "佛山"]
    
    institution_types = ["航空学院", "无人机培训中心", "飞行培训基地", "航天科技学院", "民航培训中心", 
                        "职业技术学院", "科技大学", "工程学院", "交通学院", "理工大学"]
    
    for i in range(need_count):
        city = random.choice(cities)
        inst_type = random.choice(institution_types)
        
        # 生成唯一的机构代码
        code = f"INST{current_count + i + 1:03d}"
        
        # 检查代码是否已存在
        counter = 1
        original_code = code
        while db.query(Institution).filter(Institution.code == code).first():
            code = f"{original_code}_{counter}"
            counter += 1
            if counter > 100:  # 避免无限循环
                code = f"INST{random.randint(10000, 99999)}"
                break
        
        institution = Institution(
            name=f"{city}{inst_type}",
            code=code,
            contact_person=f"联系人{current_count + i + 1}",
            contact_phone=f"138{random.randint(10000000, 99999999)}",
            contact_email=f"contact{current_count + i + 1}@example.com",
            address=f"{city}市{random.choice(['朝阳区', '海淀区', '浦东新区', '南山区', '天河区'])}科技路{random.randint(100, 999)}号",
            is_active=random.choice([True, True, True, False])  # 大部分激活
        )
        db.add(institution)
    
    db.commit()
    print(f"   ✅ 成功新增 {need_count} 条机构数据")

def expand_users_data(db):
    """扩增用户数据到50条"""
    current_count = db.query(User).count()
    target_count = 50
    
    if current_count >= target_count:
        print(f"   ✅ 用户数据已有 {current_count} 条，无需扩增")
        return
    
    need_count = target_count - current_count
    print(f"   📝 需要新增 {need_count} 条用户数据")
    
    # 角色分布：大部分是考生
    roles = [UserRole.CANDIDATE] * int(need_count * 0.7) + \
            [UserRole.EXAMINER] * int(need_count * 0.15) + \
            [UserRole.OPERATOR] * int(need_count * 0.1) + \
            [UserRole.ADMIN] * int(need_count * 0.05)
    
    # 补齐到需要的数量
    while len(roles) < need_count:
        roles.append(UserRole.CANDIDATE)
    
    # 获取所有机构ID
    institution_ids = [inst.id for inst in db.query(Institution).all()]
    
    # 姓氏和名字
    surnames = ["王", "李", "张", "刘", "陈", "杨", "赵", "黄", "周", "吴", "徐", "孙", "胡", "朱", "高", "林", "何", "郭", "马", "罗"]
    given_names = ["伟", "芳", "娜", "秀英", "敏", "静", "丽", "强", "磊", "军", "洋", "勇", "艳", "杰", "娟", "涛", "明", "超", "秀兰", "霞"]
    
    for i in range(need_count):
        role = roles[i]
        
        # 生成姓名
        real_name = random.choice(surnames) + random.choice(given_names)
        
        # 生成用户名
        username = f"user{current_count + i + 1:03d}"
        
        # 检查用户名是否已存在
        counter = 1
        original_username = username
        while db.query(User).filter(User.username == username).first():
            username = f"{original_username}_{counter}"
            counter += 1
            if counter > 100:  # 避免无限循环
                username = f"user{random.randint(10000, 99999)}"
                break
        
        # 生成身份证号（简化版）
        id_card = f"{random.choice(['110101', '310101', '440301'])}{random.randint(1980, 2000)}{random.randint(1, 12):02d}{random.randint(1, 28):02d}{random.randint(1000, 9999)}"
        
        user = User(
            username=username,
            password_hash=get_password_hash("123456"),  # 统一密码
            real_name=real_name,
            id_card=id_card,
            phone=f"138{random.randint(10000000, 99999999)}",
            email=f"{username}@example.com",
            role=role,
            institution_id=random.choice(institution_ids) if institution_ids else None,
            is_active=random.choice([True, True, True, False]),
            is_verified=random.choice([True, True, False]),
            wechat_openid=f"wx_openid_{current_count + i + 1}_{random.randint(1000, 9999)}"
        )
        db.add(user)
    
    db.commit()
    print(f"   ✅ 成功新增 {need_count} 条用户数据")

def expand_exam_products_data(db):
    """扩增考试产品数据到50条"""
    current_count = db.query(ExamProduct).count()
    target_count = 50
    
    if current_count >= target_count:
        print(f"   ✅ 考试产品数据已有 {current_count} 条，无需扩增")
        return
    
    need_count = target_count - current_count
    print(f"   📝 需要新增 {need_count} 条考试产品数据")
    
    # 获取已存在的名称和代码，避免重复
    existing_names = set([ep.name for ep in db.query(ExamProduct).all()])
    existing_codes = set([ep.code for ep in db.query(ExamProduct).all()])
    
    # 考试类型和级别
    aircraft_types = ['多旋翼', '固定翼', '直升机', '垂直起降固定翼', '飞艇', '伞翼动力', '扑翼']
    weight_categories = ['轻型', '小型', '中型', '大型']
    operation_types = ['视距内运行', '超视距运行', '夜间运行', '人口稠密区运行', '危险品运输', '农业植保', '航拍测绘', '巡检监控']
    exam_types = ['理论', '实操', '综合']
    
    added_count = 0
    max_attempts = need_count * 10  # 最大尝试次数，避免无限循环
    attempts = 0
    
    while added_count < need_count and attempts < max_attempts:
        attempts += 1
        
        aircraft_type = random.choice(aircraft_types)
        weight_category = random.choice(weight_categories)
        operation_type = random.choice(operation_types)
        exam_type = random.choice(exam_types)
        
        # 生成唯一的名称
        name = f"{aircraft_type}无人机{weight_category}级{operation_type}驾驶员证({exam_type})"
        
        # 如果名称已存在，添加序号
        if name in existing_names:
            counter = 1
            while f"{name}-{counter}" in existing_names:
                counter += 1
            name = f"{name}-{counter}"
        
        # 生成唯一的代码
        code = f"UAV-{aircraft_type[:2]}-{weight_category[0]}{current_count + added_count + 1:02d}"
        
        # 如果代码已存在，生成随机代码
        if code in existing_codes:
            counter = 1
            while f"UAV-{random.randint(100, 999)}-{counter}" in existing_codes:
                counter += 1
            code = f"UAV-{random.randint(100, 999)}-{counter}"
        
        # 检查数据库中是否真的不存在（双重保险）
        if (not db.query(ExamProduct).filter(ExamProduct.name == name).first() and 
            not db.query(ExamProduct).filter(ExamProduct.code == code).first()):
            
            exam_product = ExamProduct(
                name=name,
                code=code,
                description=f"{name}考试，包含相关理论知识和实际操作技能考核。",
                duration_minutes=random.choice([60, 90, 120, 150]) if exam_type == '理论' else random.choice([30, 45, 60]),
                exam_type=exam_type
            )
            db.add(exam_product)
            
            # 更新已存在的集合
            existing_names.add(name)
            existing_codes.add(code)
            added_count += 1
    
    try:
        db.commit()
        print(f"   ✅ 成功新增 {added_count} 条考试产品数据")
    except Exception as e:
        print(f"   ⚠️ 提交时出现错误: {e}")
        db.rollback()
        print(f"   ✅ 实际新增 {added_count} 条考试产品数据")

def expand_venues_data(db):
    """扩增考场数据到50条"""
    current_count = db.query(Venue).count()
    target_count = 50
    
    if current_count >= target_count:
        print(f"   ✅ 考场数据已有 {current_count} 条，无需扩增")
        return
    
    need_count = target_count - current_count
    print(f"   📝 需要新增 {need_count} 条考场数据")
    
    # 考场类型和名称
    theory_names = ['理论考试教室', '多媒体教室', '计算机教室', '阶梯教室', '会议室', '培训室', '学术报告厅']
    practical_names = ['实操训练场', '飞行训练区', '模拟飞行室', '维修实训室', '组装实训室', '户外训练场', '综合实训区']
    
    # 获取所有机构ID
    institution_ids = [inst.id for inst in db.query(Institution).all()]
    
    for i in range(need_count):
        venue_type = random.choice(['理论', '实操'])
        
        if venue_type == '理论':
            base_name = random.choice(theory_names)
            capacity = random.randint(20, 100)
        else:
            base_name = random.choice(practical_names)
            capacity = random.randint(5, 30)
        
        # 生成考场名称和代码
        name = f"{base_name}{chr(65 + (current_count + i) % 26)}号"
        code = f"VEN{current_count + i + 1:03d}"
        
        # 检查代码是否已存在
        counter = 1
        original_code = code
        while db.query(Venue).filter(Venue.code == code).first():
            code = f"{original_code}_{counter}"
            counter += 1
            if counter > 100:  # 避免无限循环
                code = f"VEN{random.randint(10000, 99999)}"
                break
        
        venue = Venue(
            name=name,
            code=code,
            description=f"{name}，用于考试使用",
            capacity=capacity,
            building=f"{random.randint(1, 10)}号楼",
            floor=f"{random.randint(1, 5)}层",
            room_number=f"{random.randint(101, 599)}",
            status=random.choice([VenueStatus.AVAILABLE, VenueStatus.AVAILABLE, VenueStatus.MAINTENANCE, VenueStatus.OCCUPIED]),
            institution_id=random.choice(institution_ids) if institution_ids else None
        )
        db.add(venue)
    
    db.commit()
    print(f"   ✅ 成功新增 {need_count} 条考场数据")

def expand_exam_registrations_data(db):
    """扩增考试报名数据到50条"""
    current_count = db.query(ExamRegistration).count()
    target_count = 50
    
    if current_count >= target_count:
        print(f"   ✅ 考试报名数据已有 {current_count} 条，无需扩增")
        return
    
    need_count = target_count - current_count
    print(f"   📝 需要新增 {need_count} 条考试报名数据")
    
    # 获取用户和考试产品
    users = db.query(User).filter(User.role == UserRole.CANDIDATE).all()
    exam_products = db.query(ExamProduct).all()
    
    if not users or not exam_products:
        print("   ⚠️ 缺少考生用户或考试产品，跳过报名数据扩增")
        return
    
    for i in range(need_count):
        user = random.choice(users)
        exam_product = random.choice(exam_products)
        
        # 生成报名号
        registration_number = f"REG{datetime.now().strftime('%Y%m%d')}{current_count + i + 1:04d}"
        
        # 检查报名号是否已存在
        counter = 1
        original_registration_number = registration_number
        while db.query(ExamRegistration).filter(ExamRegistration.registration_number == registration_number).first():
            registration_number = f"{original_registration_number}_{counter}"
            counter += 1
            if counter > 100:  # 避免无限循环
                registration_number = f"REG{datetime.now().strftime('%Y%m%d')}{random.randint(100000, 999999)}"
                break
        
        registration = ExamRegistration(
            user_id=user.id,
            exam_product_id=exam_product.id,
            registration_number=registration_number,
            status=random.choice([RegistrationStatus.APPROVED, RegistrationStatus.PENDING, RegistrationStatus.REJECTED])
        )
        db.add(registration)
    
    db.commit()
    print(f"   ✅ 成功新增 {need_count} 条考试报名数据")

def expand_exam_schedules_data(db):
    """扩增考试安排数据到50条"""
    current_count = db.query(Schedule).count()
    target_count = 50
    
    if current_count >= target_count:
        print(f"   ✅ 考试安排数据已有 {current_count} 条，无需扩增")
        return
    
    need_count = target_count - current_count
    print(f"   📝 需要新增 {need_count} 条考试安排数据")
    
    # 获取已批准的报名记录和考场
    approved_registrations = db.query(ExamRegistration).filter(ExamRegistration.status == RegistrationStatus.APPROVED).all()
    venues = db.query(Venue).all()
    admin_users = db.query(User).filter(User.role.in_([UserRole.ADMIN, UserRole.SUPER_ADMIN])).all()
    
    if not approved_registrations or not venues or not admin_users:
        print("   ⚠️ 缺少已批准的报名记录、考场或管理员，跳过考试安排扩增")
        return
    
    # 时间段
    time_slots = [
        (time(9, 0), time(10, 0)),
        (time(10, 30), time(11, 30)),
        (time(14, 0), time(15, 0)),
        (time(15, 30), time(16, 30)),
        (time(16, 30), time(17, 30))
    ]
    
    # 生成未来30天的考试安排
    base_date = date.today()
    
    for i in range(min(need_count, len(approved_registrations))):
        registration = approved_registrations[i % len(approved_registrations)]
        venue = random.choice(venues)
        admin_user = random.choice(admin_users)
        
        schedule_date = base_date + timedelta(days=random.randint(1, 30))
        start_time, end_time = random.choice(time_slots)
        
        schedule = Schedule(
            registration_id=registration.id,
            venue_id=venue.id,
            schedule_date=schedule_date,
            start_time=start_time,
            end_time=end_time,
            status=random.choice([ScheduleStatus.PENDING, ScheduleStatus.IN_PROGRESS, ScheduleStatus.COMPLETED]),
            remarks=f"考试安排 - {registration.exam_product.name}",
            created_by=admin_user.id
        )
        db.add(schedule)
    
    db.commit()
    print(f"   ✅ 成功新增 {min(need_count, len(approved_registrations))} 条考试安排数据")

def expand_checkins_data(db):
    """扩增签到数据到50条"""
    current_count = db.query(CheckIn).count()
    target_count = 50
    
    if current_count >= target_count:
        print(f"   ✅ 签到数据已有 {current_count} 条，无需扩增")
        return
    
    need_count = target_count - current_count
    print(f"   📝 需要新增 {need_count} 条签到数据")
    
    # 获取考试安排和工作人员
    schedules = db.query(Schedule).all()
    staff_users = db.query(User).filter(User.role.in_([UserRole.ADMIN, UserRole.OPERATOR, UserRole.EXAMINER])).all()
    
    if not schedules or not staff_users:
        print("   ⚠️ 缺少考试安排或工作人员，跳过签到数据扩增")
        return
    
    for i in range(min(need_count, len(schedules))):
        schedule = schedules[i % len(schedules)]
        staff = random.choice(staff_users)
        
        # 获取考生信息
        candidate = db.query(User).filter(User.id == schedule.registration.user_id).first()
        if not candidate:
            continue
        
        # 计算签到时间（考试开始前5-30分钟）
        schedule_datetime = datetime.combine(schedule.schedule_date, schedule.start_time)
        checkin_time = schedule_datetime - timedelta(minutes=random.randint(5, 30))
        
        checkin = CheckIn(
            user_id=candidate.id,
            venue_id=schedule.venue_id,
            schedule_id=schedule.id,
            staff_id=staff.id,
            checkin_time=checkin_time,
            method=random.choice([CheckInMethod.QR_CODE, CheckInMethod.MANUAL, CheckInMethod.NFC]),
            status=random.choice([CheckInStatus.SUCCESS, CheckInStatus.LATE, CheckInStatus.FAILED]),
            latitude=f"{39.9 + random.uniform(-0.1, 0.1):.6f}",
            longitude=f"{116.4 + random.uniform(-0.1, 0.1):.6f}",
            location_address=f"考试地点{random.randint(1, 10)}号",
            device_info={
                "device_type": random.choice(["iPhone", "Android", "iPad"]),
                "os_version": random.choice(["iOS 15.0", "Android 11", "iOS 14.0"]),
                "app_version": "1.0.0"
            },
            ip_address=f"192.168.1.{random.randint(100, 200)}",
            user_agent="UAV Exam App/1.0.0",
            notes=f"考生 {candidate.real_name} 签到记录"
        )
        db.add(checkin)
    
    db.commit()
    print(f"   ✅ 成功新增 {min(need_count, len(schedules))} 条签到数据")

def expand_test_data():
    """扩增测试数据到每表50条"""
    db = SessionLocal()
    
    try:
        print("🚀 开始扩增测试数据到每表50条...")
        
        # 检查当前数据量
        current_counts = check_current_data_count(db)
        
        # 1. 扩增机构数据到50条
        print("\n📋 扩增机构数据...")
        expand_institutions_data(db)
        
        # 2. 扩增用户数据到50条
        print("\n👥 扩增用户数据...")
        expand_users_data(db)
        
        # 3. 扩增考试产品数据到50条
        print("\n📚 扩增考试产品数据...")
        expand_exam_products_data(db)
        
        # 4. 扩增考场数据到50条
        print("\n🏢 扩增考场数据...")
        expand_venues_data(db)
        
        # 5. 扩增考试报名数据到50条
        print("\n📝 扩增考试报名数据...")
        expand_exam_registrations_data(db)
        
        # 6. 扩增考试安排数据到50条
        print("\n📅 扩增考试安排数据...")
        expand_exam_schedules_data(db)
        
        # 7. 扩增签到数据到50条
        print("\n✅ 扩增签到数据...")
        expand_checkins_data(db)
        
        db.commit()
        print("\n🎉 扩增测试数据完成！")
        
        # 最终统计
        final_counts = check_current_data_count(db)
        
        print("\n📈 扩增统计:")
        for table, final_count in final_counts.items():
            original_count = current_counts.get(table, 0)
            added_count = final_count - original_count
            if added_count > 0:
                print(f"   {table}: {original_count} → {final_count} (+{added_count})")
            else:
                print(f"   {table}: {final_count} (无变化)")
        
    except Exception as e:
        print(f"❌ 扩增失败: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("UAV考试系统测试数据扩增脚本")
    print("=" * 50)
    
    # 检查当前数据
    db = SessionLocal()
    try:
        current_counts = check_current_data_count(db)
    finally:
        db.close()
    
    # 确认是否继续
    confirm = input("\n是否继续扩增数据到每表50条？(y/N): ")
    if confirm.lower() in ['y', 'yes']:
        expand_test_data()
    else:
        print("操作已取消")