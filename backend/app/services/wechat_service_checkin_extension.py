"""
WeChatService 签到功能扩展
"""

from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any

from ..models.user import User, UserRole
from ..models.schedule import Schedule, ScheduleStatus
from ..models.venue import Venue
from ..models.checkin import CheckIn, CheckInStatus, CheckInMethod
from ..schemas.wechat import CheckInResponse


def add_process_checkin_method(wechat_service_class):
    """为 WeChatService 类添加 process_checkin 方法"""
    
    def process_checkin(self, schedule_id: int, examiner_id: int, venue_id: int, qr_code_data: str = None) -> CheckInResponse:
        """
        处理考务人员签到操作
        
        Args:
            schedule_id: 考试安排ID
            examiner_id: 考务人员ID
            venue_id: 考场ID
            qr_code_data: 二维码数据（可选）
        
        Returns:
            CheckInResponse: 签到结果
        """
        try:
            # 1. 验证考试安排是否存在
            schedule = self.db.query(Schedule).filter(Schedule.id == schedule_id).first()
            if not schedule:
                raise ValueError(f"考试安排不存在: {schedule_id}")
            
            # 2. 验证考场是否存在且匹配
            venue = self.db.query(Venue).filter(Venue.id == venue_id).first()
            if not venue:
                raise ValueError(f"考场不存在: {venue_id}")
            
            if schedule.venue_id != venue_id:
                raise ValueError(f"考试安排的考场({schedule.venue_id})与指定考场({venue_id})不匹配")
            
            # 3. 验证考务人员权限
            examiner = self.db.query(User).filter(User.id == examiner_id).first()
            if not examiner:
                raise ValueError(f"考务人员不存在: {examiner_id}")
            
            if examiner.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.EXAMINER]:
                raise ValueError("只有考务人员可以执行签到操作")
            
            # 4. 检查是否已经签到过
            existing_checkin = self.db.query(CheckIn).filter(
                CheckIn.schedule_id == schedule_id,
                CheckIn.user_id == schedule.candidate_id if hasattr(schedule, 'candidate_id') else None
            ).first()
            
            if existing_checkin:
                return CheckInResponse(
                    success=False,
                    message="该考生已完成签到",
                    checkin_time=existing_checkin.checkin_time,
                    schedule_info={
                        "schedule_id": schedule_id,
                        "venue_name": venue.name,
                        "status": "already_checked_in"
                    }
                )
            
            # 5. 创建签到记录
            checkin_record = CheckIn(
                user_id=schedule.candidate_id if hasattr(schedule, 'candidate_id') else examiner_id,
                venue_id=venue_id,
                schedule_id=schedule_id,
                staff_id=examiner_id,
                checkin_time=datetime.now(),
                method=CheckInMethod.QR_CODE if qr_code_data else CheckInMethod.MANUAL,
                status=CheckInStatus.SUCCESS,
                notes=f"考务人员{examiner.real_name or examiner.username}执行签到",
                data={
                    "qr_code_data": qr_code_data,
                    "examiner_info": {
                        "id": examiner_id,
                        "name": examiner.real_name or examiner.username,
                        "role": examiner.role.value
                    }
                }
            )
            
            # 6. 更新考试安排状态
            if schedule.status == ScheduleStatus.PENDING:
                schedule.status = ScheduleStatus.IN_PROGRESS
            
            # 7. 保存到数据库
            self.db.add(checkin_record)
            self.db.commit()
            self.db.refresh(checkin_record)
            
            # 8. 构造返回结果
            schedule_info = {
                "schedule_id": schedule_id,
                "venue_name": venue.name,
                "venue_address": venue.address,
                "exam_time": schedule.exam_time.isoformat() if hasattr(schedule, 'exam_time') and schedule.exam_time else None,
                "status": schedule.status.value if schedule.status else "unknown",
                "examiner": {
                    "id": examiner_id,
                    "name": examiner.real_name or examiner.username
                }
            }
            
            return CheckInResponse(
                success=True,
                message="签到成功",
                checkin_time=checkin_record.checkin_time,
                schedule_info=schedule_info
            )
            
        except ValueError as e:
            # 业务逻辑错误
            raise e
        except Exception as e:
            # 数据库或其他系统错误
            self.db.rollback()
            raise ValueError(f"签到处理失败: {str(e)}")
    
    # 将方法添加到类中
    wechat_service_class.process_checkin = process_checkin
    return wechat_service_class


# 使用装饰器模式扩展 WeChatService
def extend_wechat_service():
    """扩展 WeChatService 类，添加 process_checkin 方法"""
    from .wechat_service import WeChatService
    return add_process_checkin_method(WeChatService)