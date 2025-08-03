"""
二维码生成和扫码签到服务模块
支持动态二维码生成、扫码签到、状态更新等功能
"""
import qrcode
import io
import base64
import json
import secrets
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from fastapi import HTTPException

from src.models.candidate import Candidate
from src.models.schedule import Schedule
from src.models.venue import Venue
from src.db.models import User


class QRCodeService:
    """二维码服务"""
    
    def __init__(self):
        self.secret_key = "exam_site_qrcode_secret_2025"
        self.qr_expire_minutes = 60  # 二维码有效期(分钟)
    
    async def generate_candidate_qrcode(
        self,
        db: AsyncSession,
        candidate_id: int
    ) -> Dict[str, Any]:
        """为考生生成动态二维码"""
        
        # 获取考生信息
        candidate_result = await db.execute(
            select(Candidate).where(Candidate.id == candidate_id)
        )
        candidate = candidate_result.scalar_one_or_none()
        
        if not candidate:
            raise HTTPException(status_code=404, detail="考生不存在")
        
        # 获取考生的下一个待进行的排期
        next_schedule = await self._get_next_schedule(db, candidate_id)
        
        if not next_schedule:
            # 如果没有待进行的排期，生成基础二维码
            qr_data = {
                "type": "candidate_info",
                "candidate_id": candidate_id,
                "candidate_name": candidate.name,
                "id_number": candidate.id_number,
                "timestamp": datetime.utcnow().isoformat(),
                "expires_at": (datetime.utcnow() + timedelta(minutes=self.qr_expire_minutes)).isoformat(),
                "token": self._generate_secure_token(candidate_id)
            }
        else:
            # 生成包含排期信息的二维码
            venue_result = await db.execute(
                select(Venue).where(Venue.id == next_schedule.venue_id)
            )
            venue = venue_result.scalar_one_or_none()
            
            qr_data = {
                "type": "schedule_checkin",
                "schedule_id": next_schedule.id,
                "candidate_id": candidate_id,
                "candidate_name": candidate.name,
                "id_number": candidate.id_number,
                "schedule_type": next_schedule.schedule_type,
                "venue_name": venue.name if venue else "未知场地",
                "start_time": next_schedule.start_time.isoformat(),
                "timestamp": datetime.utcnow().isoformat(),
                "expires_at": (datetime.utcnow() + timedelta(minutes=self.qr_expire_minutes)).isoformat(),
                "token": self._generate_secure_token(f"{next_schedule.id}_{candidate_id}")
            }
        
        # 生成二维码图像
        qr_image_base64 = self._generate_qr_image(json.dumps(qr_data, ensure_ascii=False))
        
        return {
            "qr_data": qr_data,
            "qr_image": qr_image_base64,
            "next_schedule": {
                "id": next_schedule.id if next_schedule else None,
                "schedule_type": next_schedule.schedule_type if next_schedule else None,
                "start_time": next_schedule.start_time.isoformat() if next_schedule else None,
                "venue_name": venue.name if next_schedule and venue else None,
                "status": next_schedule.status if next_schedule else None
            } if next_schedule else None
        }
    
    async def _get_next_schedule(
        self,
        db: AsyncSession,
        candidate_id: int
    ) -> Optional[Schedule]:
        """获取考生的下一个待进行的排期"""
        
        # 查询待进行的排期（按时间排序）
        query = select(Schedule).where(
            and_(
                Schedule.candidate_id == candidate_id,
                Schedule.status.in_(["待确认", "confirmed"]),
                Schedule.check_in_status == "not_checked_in",
                Schedule.start_time > datetime.utcnow()
            )
        ).order_by(Schedule.start_time)
        
        result = await db.execute(query)
        return result.scalars().first()
    
    def _generate_secure_token(self, data: str) -> str:
        """生成安全令牌"""
        import hashlib
        timestamp = str(int(datetime.utcnow().timestamp()))
        raw_token = f"{data}_{timestamp}_{self.secret_key}"
        return hashlib.sha256(raw_token.encode()).hexdigest()[:16]
    
    def _generate_qr_image(self, data: str) -> str:
        """生成二维码图像（Base64编码）"""
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # 创建图像
        img = qr.make_image(fill_color="black", back_color="white")
        
        # 转换为Base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    async def scan_qrcode_checkin(
        self,
        db: AsyncSession,
        qr_data_str: str,
        staff_user: User
    ) -> Dict[str, Any]:
        """扫码签到处理"""
        
        try:
            # 解析二维码数据
            qr_data = json.loads(qr_data_str)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="二维码格式错误")
        
        # 验证二维码是否过期
        try:
            expires_at = datetime.fromisoformat(qr_data.get("expires_at", ""))
            if datetime.utcnow() > expires_at:
                raise HTTPException(status_code=400, detail="二维码已过期，请刷新")
        except ValueError:
            raise HTTPException(status_code=400, detail="二维码时间格式错误")
        
        # 验证二维码类型
        qr_type = qr_data.get("type")
        if qr_type == "schedule_checkin":
            return await self._process_schedule_checkin(db, qr_data, staff_user)
        elif qr_type == "candidate_info":
            return await self._process_candidate_info_scan(db, qr_data, staff_user)
        else:
            raise HTTPException(status_code=400, detail="不支持的二维码类型")
    
    async def _process_schedule_checkin(
        self,
        db: AsyncSession,
        qr_data: Dict[str, Any],
        staff_user: User
    ) -> Dict[str, Any]:
        """处理排期签到"""
        
        schedule_id = qr_data.get("schedule_id")
        if not schedule_id:
            raise HTTPException(status_code=400, detail="二维码中缺少排期信息")
        
        # 获取排期信息
        schedule_result = await db.execute(
            select(Schedule).where(Schedule.id == schedule_id)
        )
        schedule = schedule_result.scalar_one_or_none()
        
        if not schedule:
            raise HTTPException(status_code=404, detail="排期记录不存在")
        
        # 检查是否已经签到
        if schedule.check_in_status == "checked_in":
            raise HTTPException(status_code=400, detail="该考生已完成签到")
        
        # 获取考生信息
        candidate_result = await db.execute(
            select(Candidate).where(Candidate.id == schedule.candidate_id)
        )
        candidate = candidate_result.scalar_one_or_none()
        
        # 获取场地信息
        venue_result = await db.execute(
            select(Venue).where(Venue.id == schedule.venue_id)
        )
        venue = venue_result.scalar_one_or_none()
        
        # 检查签到时间（可以在开始前30分钟签到）
        now = datetime.utcnow()
        earliest_checkin = schedule.start_time - timedelta(minutes=30)
        latest_checkin = schedule.end_time
        
        checkin_status = "checked_in"
        if now < earliest_checkin:
            raise HTTPException(
                status_code=400, 
                detail=f"签到时间未到，请在 {earliest_checkin.strftime('%H:%M')} 后签到"
            )
        elif now > latest_checkin:
            checkin_status = "late"
        
        # 更新签到状态
        schedule.check_in_status = checkin_status
        schedule.check_in_time = now
        schedule.status = "confirmed"
        
        # 更新考生状态
        if candidate:
            if checkin_status == "checked_in":
                candidate.status = "考试中"
            else:
                candidate.status = "迟到"
        
        # 更新排队信息
        await self._update_queue_position(db, schedule)
        
        await db.commit()
        
        return {
            "success": True,
            "message": f"考生 {candidate.name if candidate else '未知'} 签到成功",
            "checkin_status": checkin_status,
            "candidate": {
                "id": candidate.id if candidate else None,
                "name": candidate.name if candidate else "未知",
                "id_number": qr_data.get("id_number", "未知")
            },
            "schedule": {
                "id": schedule.id,
                "schedule_type": schedule.schedule_type,
                "start_time": schedule.start_time.isoformat(),
                "venue_name": venue.name if venue else "未知场地"
            },
            "checkin_time": now.isoformat(),
            "staff_user": staff_user.username
        }
    
    async def _process_candidate_info_scan(
        self,
        db: AsyncSession,
        qr_data: Dict[str, Any],
        staff_user: User
    ) -> Dict[str, Any]:
        """处理考生信息扫描"""
        
        candidate_id = qr_data.get("candidate_id")
        if not candidate_id:
            raise HTTPException(status_code=400, detail="二维码中缺少考生信息")
        
        # 获取考生信息
        candidate_result = await db.execute(
            select(Candidate).where(Candidate.id == candidate_id)
        )
        candidate = candidate_result.scalar_one_or_none()
        
        if not candidate:
            raise HTTPException(status_code=404, detail="考生不存在")
        
        # 获取考生的排期信息
        schedules_result = await db.execute(
            select(Schedule).where(
                and_(
                    Schedule.candidate_id == candidate_id,
                    Schedule.scheduled_date == datetime.utcnow().date()
                )
            ).order_by(Schedule.start_time)
        )
        schedules = schedules_result.scalars().all()
        
        schedule_info = []
        for schedule in schedules:
            venue_result = await db.execute(
                select(Venue).where(Venue.id == schedule.venue_id)
            )
            venue = venue_result.scalar_one_or_none()
            
            schedule_info.append({
                "id": schedule.id,
                "schedule_type": schedule.schedule_type,
                "start_time": schedule.start_time.isoformat(),
                "end_time": schedule.end_time.isoformat(),
                "venue_name": venue.name if venue else "未知场地",
                "status": schedule.status,
                "check_in_status": schedule.check_in_status
            })
        
        return {
            "success": True,
            "message": f"考生信息扫描成功",
            "candidate": {
                "id": candidate.id,
                "name": candidate.name,
                "id_number": candidate.id_number,
                "phone": candidate.phone,
                "status": candidate.status
            },
            "schedules": schedule_info,
            "staff_user": staff_user.username,
            "scan_time": datetime.utcnow().isoformat()
        }
    
    async def _update_queue_position(
        self,
        db: AsyncSession,
        current_schedule: Schedule
    ):
        """更新排队位置信息"""
        
        # 获取同一场地、同一类型考试的排队情况
        query = select(Schedule).where(
            and_(
                Schedule.venue_id == current_schedule.venue_id,
                Schedule.schedule_type == current_schedule.schedule_type,
                Schedule.scheduled_date == current_schedule.scheduled_date,
                Schedule.check_in_status == "not_checked_in",
                Schedule.start_time > current_schedule.start_time
            )
        ).order_by(Schedule.start_time)
        
        result = await db.execute(query)
        waiting_schedules = result.scalars().all()
        
        # 更新排队位置
        for i, schedule in enumerate(waiting_schedules):
            schedule.queue_position = i + 1
            # 估算等待时间（基于平均考试时长）
            schedule.estimated_wait_time = (i + 1) * 15  # 15分钟每人
    
    async def get_candidate_queue_status(
        self,
        db: AsyncSession,
        candidate_id: int
    ) -> Dict[str, Any]:
        """获取考生排队状态"""
        
        # 获取考生今日的排期
        today_schedules_result = await db.execute(
            select(Schedule).where(
                and_(
                    Schedule.candidate_id == candidate_id,
                    Schedule.scheduled_date == datetime.utcnow().date(),
                    Schedule.check_in_status == "not_checked_in"
                )
            ).order_by(Schedule.start_time)
        )
        schedules = today_schedules_result.scalars().all()
        
        queue_status = []
        for schedule in schedules:
            venue_result = await db.execute(
                select(Venue).where(Venue.id == schedule.venue_id)
            )
            venue = venue_result.scalar_one_or_none()
            
            # 计算当前排队位置
            queue_query = select(Schedule).where(
                and_(
                    Schedule.venue_id == schedule.venue_id,
                    Schedule.schedule_type == schedule.schedule_type,
                    Schedule.scheduled_date == schedule.scheduled_date,
                    Schedule.check_in_status == "not_checked_in",
                    Schedule.start_time <= schedule.start_time
                )
            ).order_by(Schedule.start_time)
            
            queue_result = await db.execute(queue_query)
            queue_schedules = queue_result.scalars().all()
            queue_position = len(queue_schedules)
            
            queue_status.append({
                "schedule_id": schedule.id,
                "schedule_type": schedule.schedule_type,
                "venue_name": venue.name if venue else "未知场地",
                "start_time": schedule.start_time.isoformat(),
                "queue_position": queue_position,
                "estimated_wait_time": queue_position * 15,
                "status": schedule.status
            })
        
        return {
            "candidate_id": candidate_id,
            "queue_status": queue_status,
            "updated_at": datetime.utcnow().isoformat()
        }

# 单例服务实例
qrcode_service = QRCodeService()