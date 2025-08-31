#!/usr/bin/env python3
"""
UAV考点运营管理系统 - 全面数据插入脚本
基于CAAC无人机驾驶员考试分类体系
"""

import sys
import random
import hashlib
from datetime import datetime, timedelta, date, time
from typing import List, Dict, Set, Any

try:
    from app.config.database import SessionLocal
    from app.models.user import User, UserRole
    from app.models.institution import Institution
    from app.models.venue import Venue, VenueStatus
    from app.models.exam import ExamProduct, ExamRegistration, RegistrationStatus
    from app.models.schedule import Schedule, ScheduleStatus
    from app.models.checkin import CheckIn, CheckInStatus, CheckInMethod
    print("✅ 模块导入成功")
except Exception as e:
    print(f"❌ 模块导入失败: {e}")
    sys.exit(1)

class ComprehensiveDataGenerator:
    """全面数据生成器"""
    
    def __init__(self):
        self.session = SessionLocal()
        
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
            "范冰冰", "李冰冰", "周迅", "赵薇", "章子怡", "巩俐", "张曼玉", "王菲", "那英", "田震"
        ]
        
        # 全国主要城市信息
        self.cities = [
            {"name": "北京", "code": "BJ", "province": "北京市", "area_code": "110101"},
            {"name": "上海", "code": "SH", "province": "上海市", "area_code": "310101"},
            {"name": "深圳", "code": "SZ", "province": "广东省", "area_code": "440301"},
            {"name": "广州", "code": "GZ", "province": "广东省", "area_code": "440101"},
            {"name": "杭州", "code": "HZ", "province": "浙江省", "area_code": "330101"},
            {"name": "成都", "code": "CD", "province": "四川省", "area_code": "510101"},
            {"name": "武汉", "code": "WH", "province": "湖北省", "area_code": "420101"},
            {"name": "西安", "code": "XA", "province": "陕西省", "area_code": "610101"}
        ]
        
        # 基于CAAC分类的考试产品配置
        self.exam_products_config = [
            # 视距内驾驶员
            {"name": "多旋翼视距内驾驶员理论", "code": "MULTI_VLOS_THEORY", "type": "理论", "duration": 90},
            {"name": "多旋翼视距内驾驶员实操", "code": "MULTI_VLOS_PRACTICE", "type": "实操", "duration": 20},
            {"name": "固定翼视距内驾驶员理论", "code": "FIXED_VLOS_THEORY", "type": "理论", "duration": 90},
            {"name": "固定翼视距内驾驶员实操", "code": "FIXED_VLOS_PRACTICE", "type": "实操", "duration": 25},
            {"name": "垂直起降固定翼视距内驾驶员理论", "code": "VTOL_VLOS_THEORY", "type": "理论", "duration": 90},
            {"name": "垂直起降固定翼视距内驾驶员实操", "code": "VTOL_VLOS_PRACTICE", "type": "实操", "duration": 30},
            
            # 超视距驾驶员
            {"name": "多旋翼超视距驾驶员理论", "code": "MULTI_BVLOS_THEORY", "type": "理论", "duration": 120},
            {"name": "多旋翼超视距驾驶员实操", "code": "MULTI_BVLOS_PRACTICE", "type": "实操", "duration": 35},
            {"name": "固定翼超视距驾驶员理论", "code": "FIXED_BVLOS_THEORY", "type": "理论", "duration": 120},
            {"name": "固定翼超视距驾驶员实操", "code": "FIXED_BVLOS_PRACTICE", "type": "实操", "duration": 40},
            {"name": "垂直起降固定翼超视距驾驶员理论", "code": "VTOL_BVLOS_THEORY", "type": "理论", "duration": 120},
            {"name": "垂直起降固定翼超视距驾驶员实操", "code": "VTOL_BVLOS_PRACTICE", "type": "实操", "duration": 45},
            
            # 教员等级
            {"name": "无人机教员资格理论", "code": "INSTRUCTOR_THEORY", "type": "理论", "duration": 150},
            {"name": "无人机教员资格实操", "code": "INSTRUCTOR_PRACTICE", "type": "实操", "duration": 60},
            
            # 专业应用
            {"name": "农业植保专项理论", "code": "AGRI_THEORY", "type": "理论", "duration": 90},
            {"name": "农业植保专项实操", "code": "AGRI_PRACTICE", "type": "实操", "duration": 30},
            {"name": "电力巡检专项理论", "code": "POWER_THEORY", "type": "理论", "duration": 90},
            {"name": "电力巡检专项实操", "code": "POWER_PRACTICE", "type": "实操", "duration": 35},
            {"name": "影视航拍专项理论", "code": "FILM_THEORY", "type": "理论", "duration": 75},
            {"name": "影视航拍专项实操", "code": "FILM_PRACTICE", "type": "实操", "duration": 25}
        ]

    def hash_password(self, password: str) -> str:
        """密码哈希"""
        return hashlib.sha256(password.encode()).hexdigest()

    def generate_unique_email(self) -> str:
        """生成唯一邮箱"""
        domains = ['qq.com', '163.com', 'gmail.com', 'sina.com', 'outlook.com']
        while True:
            domain = random.choice(domains)
            email = f"user{random.randint(10000, 99999)}@{domain}"
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
            birth_year = random.randint(1980, 2005)
            birth_month = random.randint(1, 12)
            birth_day = random.randint(1, 28)
            
            area_code = city_info["area_code"]
            birth_date = f"{birth_year:04d}{birth_month:02d}{birth_day:02d}"
            sequence = f"{random.randint(100, 999)}"
            
            id_card_17 = area_code + birth_date + sequence
            weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
            check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
            
            sum_val = sum(int(id_card_17[i]) * weights[i] for i in range(17))
            check_code = check_codes[sum_val % 11]
            
            id_card = id_card_17 + check_code
            
            if id_card not in self.used_id_cards:
                self.used_id_cards.add(id_card)
                return id_card

    def run(self):
        """执行数据生成"""
        try:
            print("🚀 开始生成全面数据...")
            
            # 导入数据生成方法
            import data_generator_methods
            
            # 1. 创建机构
            institutions = data_generator_methods.create_institutions(self)
            
            # 2. 创建考场
            venues = data_generator_methods.create_venues(self, institutions)
            
            # 3. 创建考试产品
            exam_products = data_generator_methods.create_exam_products(self)
            
            # 4. 创建用户
            users = data_generator_methods.create_users(self, institutions)
            
            # 5. 创建报名记录
            registrations = data_generator_methods.create_exam_registrations(self, users, exam_products)
            
            # 6. 创建考试日程
            schedules = data_generator_methods.create_schedules(self, registrations, venues, users)
            
            # 7. 创建签到记录
            checkins = data_generator_methods.create_checkins(self, schedules, users)
            
            print("\n🎉 数据生成完成！")
            print(f"📊 数据统计:")
            print(f"   - 机构: {len(institutions)} 个")
            print(f"   - 考场: {len(venues)} 个")
            print(f"   - 考试产品: {len(exam_products)} 个")
            print(f"   - 用户: {len(users)} 个")
            print(f"   - 报名记录: {len(registrations)} 条")
            print(f"   - 考试日程: {len(schedules)} 条")
            print(f"   - 签到记录: {len(checkins)} 条")
            
        except Exception as e:
            print(f"❌ 数据生成失败: {e}")
            self.session.rollback()
            raise
        finally:
            self.session.close()

if __name__ == "__main__":
    generator = ComprehensiveDataGenerator()
    generator.run()