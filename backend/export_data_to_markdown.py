#!/usr/bin/env python3
"""
数据库数据导出为Markdown文档
"""

import sys
import os
from datetime import datetime
from typing import List, Dict, Any

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


class DataExporter:
    """数据导出器"""
    
    def __init__(self):
        self.db = SessionLocal()
        self.markdown_content = []
    
    def add_title(self, title: str, level: int = 1):
        """添加标题"""
        self.markdown_content.append(f"{'#' * level} {title}\n")
    
    def add_text(self, text: str):
        """添加文本"""
        self.markdown_content.append(f"{text}\n")
    
    def add_table(self, headers: List[str], rows: List[List[str]], title: str = None):
        """添加表格"""
        if title:
            self.add_text(f"**{title}**")
        
        # 表头
        header_row = "| " + " | ".join(headers) + " |"
        separator_row = "| " + " | ".join(["---"] * len(headers)) + " |"
        
        self.markdown_content.append(header_row)
        self.markdown_content.append(separator_row)
        
        # 数据行
        for row in rows:
            # 处理None值和长文本
            processed_row = []
            for cell in row:
                if cell is None:
                    processed_row.append("-")
                elif isinstance(cell, str) and len(cell) > 50:
                    processed_row.append(cell[:47] + "...")
                else:
                    processed_row.append(str(cell))
            
            data_row = "| " + " | ".join(processed_row) + " |"
            self.markdown_content.append(data_row)
        
        self.markdown_content.append("")  # 空行
    
    def add_statistics(self, title: str, stats: Dict[str, Any]):
        """添加统计信息"""
        self.add_text(f"**{title}**")
        for key, value in stats.items():
            self.add_text(f"- {key}: {value}")
        self.add_text("")
    
    def export_institutions(self):
        """导出机构数据"""
        self.add_title("机构信息", 2)
        
        institutions = self.db.query(Institution).all()
        
        # 统计信息
        total_count = len(institutions)
        active_count = len([i for i in institutions if i.is_active])
        approved_count = len([i for i in institutions if i.is_approved])
        
        self.add_statistics("机构统计", {
            "总数": total_count,
            "活跃机构": active_count,
            "已认证机构": approved_count
        })
        
        # 机构列表
        headers = ["ID", "机构名称", "机构代码", "类型", "城市", "联系人", "联系电话", "状态"]
        rows = []
        
        for inst in institutions:
            status = "✅活跃" if inst.is_active else "❌停用"
            if inst.is_approved:
                status += "/已认证"
            else:
                status += "/待认证"
            
            rows.append([
                str(inst.id),
                inst.name,
                inst.code,
                inst.type or "-",
                inst.city,
                inst.contact_person or "-",
                inst.contact_phone or "-",
                status
            ])
        
        self.add_table(headers, rows, "机构详细信息")
    
    def export_users(self):
        """导出用户数据"""
        self.add_title("用户信息", 2)
        
        users = self.db.query(User).all()
        
        # 按角色统计
        role_stats = {}
        role_names = {
            UserRole.SUPER_ADMIN: "超级管理员",
            UserRole.ADMIN: "管理员",
            UserRole.OPERATOR: "机构管理员",
            UserRole.EXAMINER: "监考员",
            UserRole.CANDIDATE: "考生"
        }
        
        for user in users:
            role_name = role_names.get(user.role, "其他")
            role_stats[role_name] = role_stats.get(role_name, 0) + 1
        
        # 状态统计
        active_count = len([u for u in users if u.is_active])
        verified_count = len([u for u in users if u.is_verified])
        
        self.add_statistics("用户统计", {
            "总用户数": len(users),
            "活跃用户": active_count,
            "已验证用户": verified_count,
            **role_stats
        })
        
        # 按角色分组显示用户
        for role, role_name in role_names.items():
            role_users = [u for u in users if u.role == role]
            if not role_users:
                continue
            
            self.add_title(f"{role_name} ({len(role_users)}人)", 3)
            
            headers = ["ID", "用户名", "真实姓名", "邮箱", "手机号", "所属机构", "状态"]
            rows = []
            
            for user in role_users:
                status = "✅活跃" if user.is_active else "❌停用"
                if user.is_verified:
                    status += "/已验证"
                else:
                    status += "/未验证"
                
                institution_name = user.institution.name if user.institution else "-"
                
                rows.append([
                    str(user.id),
                    user.username,
                    user.real_name or "-",
                    user.email or "-",
                    user.phone or "-",
                    institution_name,
                    status
                ])
            
            self.add_table(headers, rows)
    
    def export_venues(self):
        """导出考场数据"""
        self.add_title("考场信息", 2)
        
        venues = self.db.query(Venue).all()
        
        # 统计信息
        status_stats = {}
        status_names = {
            VenueStatus.AVAILABLE: "可用",
            VenueStatus.OCCUPIED: "占用中",
            VenueStatus.MAINTENANCE: "维护中",
            VenueStatus.DISABLED: "已禁用"
        }
        
        for venue in venues:
            status_name = status_names.get(venue.status, "未知")
            status_stats[status_name] = status_stats.get(status_name, 0) + 1
        
        total_capacity = sum(v.capacity for v in venues)
        avg_capacity = total_capacity / len(venues) if venues else 0
        
        self.add_statistics("考场统计", {
            "总考场数": len(venues),
            "总容量": total_capacity,
            "平均容量": f"{avg_capacity:.1f}人",
            **status_stats
        })
        
        # 考场列表
        headers = ["ID", "考场名称", "考场代码", "所属机构", "容量", "当前人数", "建筑", "楼层", "房间号", "状态"]
        rows = []
        
        for venue in venues:
            status_name = status_names.get(venue.status, "未知")
            institution_name = venue.institution.name if venue.institution else "-"
            
            rows.append([
                str(venue.id),
                venue.name,
                venue.code,
                institution_name,
                str(venue.capacity),
                str(venue.current_count),
                venue.building or "-",
                venue.floor or "-",
                venue.room_number or "-",
                status_name
            ])
        
        self.add_table(headers, rows, "考场详细信息")
    
    def export_exam_products(self):
        """导出考试产品数据"""
        self.add_title("考试产品信息", 2)
        
        products = self.db.query(ExamProduct).all()
        
        # 统计信息
        theory_count = len([p for p in products if "理论" in p.exam_type])
        practice_count = len([p for p in products if "实操" in p.exam_type])
        active_count = len([p for p in products if p.is_active])
        
        self.add_statistics("考试产品统计", {
            "总产品数": len(products),
            "理论考试": theory_count,
            "实操考试": practice_count,
            "活跃产品": active_count
        })
        
        # 产品列表
        headers = ["ID", "产品名称", "产品代码", "考试类型", "时长(分钟)", "状态"]
        rows = []
        
        for product in products:
            status = "✅活跃" if product.is_active else "❌停用"
            
            rows.append([
                str(product.id),
                product.name,
                product.code,
                product.exam_type,
                str(product.duration_minutes),
                status
            ])
        
        self.add_table(headers, rows, "考试产品详细信息")
    
    def export_registrations(self):
        """导出报名数据"""
        self.add_title("报名信息", 2)
        
        registrations = self.db.query(ExamRegistration).all()
        
        # 统计信息
        status_stats = {}
        status_names = {
            RegistrationStatus.PENDING: "待审核",
            RegistrationStatus.APPROVED: "已通过",
            RegistrationStatus.REJECTED: "已拒绝",
            RegistrationStatus.CANCELLED: "已取消"
        }
        
        for reg in registrations:
            status_name = status_names.get(reg.status, "未知")
            status_stats[status_name] = status_stats.get(status_name, 0) + 1
        
        self.add_statistics("报名统计", {
            "总报名数": len(registrations),
            **status_stats
        })
        
        # 报名列表（只显示前50条，避免文档过长）
        headers = ["ID", "报名号", "考生姓名", "考试产品", "状态", "报名时间"]
        rows = []
        
        for reg in registrations[:50]:  # 限制显示数量
            status_name = status_names.get(reg.status, "未知")
            user_name = reg.user.real_name if reg.user else "-"
            product_name = reg.exam_product.name if reg.exam_product else "-"
            created_time = reg.created_at.strftime("%Y-%m-%d") if reg.created_at else "-"
            
            rows.append([
                str(reg.id),
                reg.registration_number,
                user_name,
                product_name,
                status_name,
                created_time
            ])
        
        title = f"报名详细信息 (显示前50条，共{len(registrations)}条)"
        self.add_table(headers, rows, title)
    
    def export_schedules(self):
        """导出考试日程数据"""
        self.add_title("考试日程信息", 2)
        
        schedules = self.db.query(Schedule).all()
        
        # 统计信息
        status_stats = {}
        status_names = {
            ScheduleStatus.PENDING: "待进行",
            ScheduleStatus.IN_PROGRESS: "进行中",
            ScheduleStatus.COMPLETED: "已完成",
            ScheduleStatus.CANCELLED: "已取消"
        }
        
        for schedule in schedules:
            status_name = status_names.get(schedule.status, "未知")
            status_stats[status_name] = status_stats.get(status_name, 0) + 1
        
        self.add_statistics("考试日程统计", {
            "总日程数": len(schedules),
            **status_stats
        })
        
        # 日程列表
        headers = ["ID", "考试日期", "开始时间", "结束时间", "考生姓名", "考试产品", "考场", "状态"]
        rows = []
        
        for schedule in schedules[:50]:  # 限制显示数量
            status_name = status_names.get(schedule.status, "未知")
            user_name = schedule.registration.user.real_name if schedule.registration and schedule.registration.user else "-"
            product_name = schedule.registration.exam_product.name if schedule.registration and schedule.registration.exam_product else "-"
            venue_name = schedule.venue.name if schedule.venue else "-"
            
            rows.append([
                str(schedule.id),
                str(schedule.schedule_date),
                str(schedule.start_time),
                str(schedule.end_time),
                user_name,
                product_name,
                venue_name,
                status_name
            ])
        
        title = f"考试日程详细信息 (显示前50条，共{len(schedules)}条)"
        self.add_table(headers, rows, title)
    
    def export_checkins(self):
        """导出签到数据"""
        self.add_title("签到信息", 2)
        
        checkins = self.db.query(CheckIn).all()
        
        # 统计信息
        status_stats = {}
        method_stats = {}
        
        status_names = {
            CheckInStatus.SUCCESS: "成功",
            CheckInStatus.LATE: "迟到",
            CheckInStatus.FAILED: "失败",
            CheckInStatus.INVALID: "无效"
        }
        
        method_names = {
            CheckInMethod.QR_CODE: "二维码",
            CheckInMethod.MANUAL: "手动",
            CheckInMethod.NFC: "NFC",
            CheckInMethod.BIOMETRIC: "生物识别"
        }
        
        for checkin in checkins:
            status_name = status_names.get(checkin.status, "未知")
            method_name = method_names.get(checkin.method, "未知")
            
            status_stats[status_name] = status_stats.get(status_name, 0) + 1
            method_stats[method_name] = method_stats.get(method_name, 0) + 1
        
        self.add_statistics("签到统计", {
            "总签到数": len(checkins),
            **status_stats
        })
        
        self.add_statistics("签到方式统计", method_stats)
        
        # 签到列表
        headers = ["ID", "签到时间", "考生姓名", "考场", "签到方式", "状态", "工作人员"]
        rows = []
        
        for checkin in checkins[:50]:  # 限制显示数量
            status_name = status_names.get(checkin.status, "未知")
            method_name = method_names.get(checkin.method, "未知")
            user_name = checkin.user.real_name if checkin.user else "-"
            venue_name = checkin.venue.name if checkin.venue else "-"
            staff_name = checkin.staff.real_name if checkin.staff else "-"
            checkin_time = checkin.checkin_time.strftime("%Y-%m-%d %H:%M") if checkin.checkin_time else "-"
            
            rows.append([
                str(checkin.id),
                checkin_time,
                user_name,
                venue_name,
                method_name,
                status_name,
                staff_name
            ])
        
        title = f"签到详细信息 (显示前50条，共{len(checkins)}条)"
        self.add_table(headers, rows, title)
    
    def export_summary(self):
        """导出数据汇总"""
        self.add_title("数据汇总", 2)
        
        # 获取各表数据量
        institutions_count = self.db.query(Institution).count()
        users_count = self.db.query(User).count()
        venues_count = self.db.query(Venue).count()
        products_count = self.db.query(ExamProduct).count()
        registrations_count = self.db.query(ExamRegistration).count()
        schedules_count = self.db.query(Schedule).count()
        checkins_count = self.db.query(CheckIn).count()
        
        self.add_statistics("数据总览", {
            "机构数量": institutions_count,
            "用户数量": users_count,
            "考场数量": venues_count,
            "考试产品": products_count,
            "报名记录": registrations_count,
            "考试日程": schedules_count,
            "签到记录": checkins_count
        })
        
        # 业务数据分析
        active_users = self.db.query(User).filter(User.is_active == True).count()
        approved_registrations = self.db.query(ExamRegistration).filter(ExamRegistration.status == RegistrationStatus.APPROVED).count()
        completed_schedules = self.db.query(Schedule).filter(Schedule.status == ScheduleStatus.COMPLETED).count()
        successful_checkins = self.db.query(CheckIn).filter(CheckIn.status == CheckInStatus.SUCCESS).count()
        
        self.add_statistics("业务指标", {
            "活跃用户率": f"{(active_users/users_count*100):.1f}%" if users_count > 0 else "0%",
            "报名通过率": f"{(approved_registrations/registrations_count*100):.1f}%" if registrations_count > 0 else "0%",
            "考试完成率": f"{(completed_schedules/schedules_count*100):.1f}%" if schedules_count > 0 else "0%",
            "签到成功率": f"{(successful_checkins/checkins_count*100):.1f}%" if checkins_count > 0 else "0%"
        })
    
    def generate_markdown(self) -> str:
        """生成完整的Markdown文档"""
        # 文档头部
        self.add_title("无人机考试系统数据报告", 1)
        self.add_text(f"**生成时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        self.add_text(f"**数据来源**: UAV考试管理系统数据库")
        self.add_text("")
        
        # 导出各模块数据
        self.export_summary()
        self.export_institutions()
        self.export_users()
        self.export_venues()
        self.export_exam_products()
        self.export_registrations()
        self.export_schedules()
        self.export_checkins()
        
        # 文档尾部
        self.add_title("说明", 2)
        self.add_text("- 本报告由系统自动生成，数据来源于UAV考试管理系统数据库")
        self.add_text("- 为保证文档可读性，部分表格仅显示前50条记录")
        self.add_text("- 长文本内容会被截断显示")
        self.add_text("- 数据统计基于生成时刻的数据库状态")
        
        return "\n".join(self.markdown_content)
    
    def export_to_file(self, filename: str = None):
        """导出到文件"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"UAV考试系统数据报告_{timestamp}.md"
        
        try:
            markdown_content = self.generate_markdown()
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"✅ 数据报告已导出到: {filename}")
            print(f"📊 报告包含以下内容:")
            print(f"   - 数据汇总统计")
            print(f"   - 机构信息 ({self.db.query(Institution).count()} 个)")
            print(f"   - 用户信息 ({self.db.query(User).count()} 个)")
            print(f"   - 考场信息 ({self.db.query(Venue).count()} 个)")
            print(f"   - 考试产品 ({self.db.query(ExamProduct).count()} 个)")
            print(f"   - 报名记录 ({self.db.query(ExamRegistration).count()} 条)")
            print(f"   - 考试日程 ({self.db.query(Schedule).count()} 条)")
            print(f"   - 签到记录 ({self.db.query(CheckIn).count()} 条)")
            
            return filename
            
        except Exception as e:
            print(f"❌ 导出失败: {e}")
            return None
        finally:
            self.db.close()


if __name__ == "__main__":
    exporter = DataExporter()
    exporter.export_to_file()