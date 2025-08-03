"""
考务排期管理服务模块
支持按机构分组、批量排期、时间线展示等功能
"""
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta, time, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from fastapi import HTTPException

from src.models.candidate import Candidate
from src.models.schedule import Schedule
from src.models.exam_product import ExamProduct
from src.models.venue import Venue
from src.db.models import User


class ScheduleManagementService:
    """考务排期管理服务"""
    
    def __init__(self):
        self.theory_duration = 60  # 理论考试时长(分钟)
        self.practical_base_duration = 15  # 实操考试基础时长(分钟)
        self.break_time = 10  # 间隔时间(分钟)
        self.work_start_time = time(8, 0)  # 工作开始时间
        self.work_end_time = time(18, 0)  # 工作结束时间
    
    async def get_pending_candidates(
        self,
        db: AsyncSession,
        exam_date: date,
        institution_id: Optional[int] = None,
        exam_product_id: Optional[int] = None,
        status: str = "待排期"
    ) -> List[Dict[str, Any]]:
        """获取待排期的考生列表"""
        
        # 构建查询条件
        query = select(Candidate).where(Candidate.status == status)
        
        if institution_id:
            query = query.where(Candidate.institution_id == institution_id)
        
        if exam_product_id:
            query = query.where(Candidate.exam_product_id == exam_product_id)
        
        # 排除已有当日排期的考生
        existing_schedules_query = select(Schedule.candidate_id).where(
            Schedule.scheduled_date == exam_date
        )
        existing_result = await db.execute(existing_schedules_query)
        existing_candidate_ids = [row[0] for row in existing_result.all()]
        
        if existing_candidate_ids:
            query = query.where(~Candidate.id.in_(existing_candidate_ids))
        
        result = await db.execute(query)
        candidates = result.scalars().all()
        
        # 转换为响应格式并获取关联信息
        candidate_list = []
        for candidate in candidates:
            # 获取考试产品信息
            exam_product_result = await db.execute(
                select(ExamProduct).where(ExamProduct.id == candidate.exam_product_id)
            )
            exam_product = exam_product_result.scalar_one_or_none()
            
            # 获取机构信息
            from src.institutions.models import Institution
            institution_result = await db.execute(
                select(Institution).where(Institution.id == candidate.institution_id)
            )
            institution = institution_result.scalar_one_or_none()
            
            candidate_list.append({
                "id": candidate.id,
                "name": candidate.name,
                "id_number": candidate.id_number,
                "phone": candidate.phone,
                "exam_product_name": exam_product.name if exam_product else "未知",
                "exam_product_id": candidate.exam_product_id,
                "institution_name": institution.name if institution else "未知",
                "institution_id": candidate.institution_id,
                "status": candidate.status,
                "created_at": candidate.created_at.isoformat() if candidate.created_at else None
            })
        
        return candidate_list
    
    async def group_candidates_by_institution(
        self,
        candidates: List[Dict[str, Any]]
    ) -> Dict[int, List[Dict[str, Any]]]:
        """按机构对考生进行分组"""
        
        groups = {}
        for candidate in candidates:
            institution_id = candidate["institution_id"]
            if institution_id not in groups:
                groups[institution_id] = []
            groups[institution_id].append(candidate)
        
        return groups
    
    async def calculate_time_slots(
        self,
        candidate_count: int,
        exam_type: str,
        exam_product: ExamProduct,
        start_time: datetime
    ) -> List[Dict[str, Any]]:
        """计算考试时间段"""
        
        slots = []
        current_time = start_time
        
        if exam_type == "theory":
            # 理论考试，通常是批次进行
            duration = getattr(exam_product, 'theory_duration', self.theory_duration)
            
            # 按考场容量分批
            venue_capacity = 50  # 默认理论考场容量
            batch_count = (candidate_count + venue_capacity - 1) // venue_capacity
            
            for batch in range(batch_count):
                batch_candidates = min(venue_capacity, candidate_count - batch * venue_capacity)
                slots.append({
                    "batch": batch + 1,
                    "start_time": current_time,
                    "end_time": current_time + timedelta(minutes=duration),
                    "candidate_count": batch_candidates,
                    "duration": duration
                })
                current_time += timedelta(minutes=duration + self.break_time)
        
        elif exam_type == "practical":
            # 实操考试，逐个进行
            duration = getattr(exam_product, 'practical_duration', self.practical_base_duration)
            
            for i in range(candidate_count):
                slots.append({
                    "sequence": i + 1,
                    "start_time": current_time,
                    "end_time": current_time + timedelta(minutes=duration),
                    "candidate_count": 1,
                    "duration": duration
                })
                current_time += timedelta(minutes=duration + self.break_time)
        
        return slots
    
    async def check_venue_availability(
        self,
        db: AsyncSession,
        venue_id: int,
        start_time: datetime,
        end_time: datetime
    ) -> bool:
        """检查场地在指定时间段是否可用"""
        
        # 查询是否有冲突的排期
        conflict_query = select(Schedule).where(
            and_(
                Schedule.venue_id == venue_id,
                or_(
                    and_(Schedule.start_time <= start_time, Schedule.end_time > start_time),
                    and_(Schedule.start_time < end_time, Schedule.end_time >= end_time),
                    and_(Schedule.start_time >= start_time, Schedule.end_time <= end_time)
                )
            )
        )
        
        result = await db.execute(conflict_query)
        conflicts = result.scalars().all()
        
        return len(conflicts) == 0
    
    async def get_available_venues(
        self,
        db: AsyncSession,
        venue_type: str,
        start_time: datetime,
        end_time: datetime
    ) -> List[Dict[str, Any]]:
        """获取指定时间段可用的场地"""
        
        # 获取指定类型的所有场地
        venues_query = select(Venue).where(
            and_(
                Venue.type == venue_type,
                Venue.status == "active"
            )
        )
        
        result = await db.execute(venues_query)
        venues = result.scalars().all()
        
        available_venues = []
        for venue in venues:
            if await self.check_venue_availability(db, venue.id, start_time, end_time):
                available_venues.append({
                    "id": venue.id,
                    "name": venue.name,
                    "type": venue.type,
                    "capacity": venue.capacity,
                    "address": venue.address
                })
        
        return available_venues
    
    async def create_batch_schedule(
        self,
        db: AsyncSession,
        candidate_ids: List[int],
        exam_type: str,
        venue_id: int,
        start_date: date,
        start_time: time,
        current_user: User
    ) -> Dict[str, Any]:
        """批量创建排期"""
        
        try:
            # 验证考生是否存在且可排期
            candidates_query = select(Candidate).where(
                and_(
                    Candidate.id.in_(candidate_ids),
                    Candidate.status == "待排期"
                )
            )
            result = await db.execute(candidates_query)
            candidates = result.scalars().all()
            
            if len(candidates) != len(candidate_ids):
                raise HTTPException(
                    status_code=400,
                    detail="部分考生不存在或状态不正确"
                )
            
            # 验证场地是否存在
            venue_result = await db.execute(select(Venue).where(Venue.id == venue_id))
            venue = venue_result.scalar_one_or_none()
            if not venue:
                raise HTTPException(status_code=400, detail="场地不存在")
            
            # 获取考试产品信息
            exam_product_result = await db.execute(
                select(ExamProduct).where(ExamProduct.id == candidates[0].exam_product_id)
            )
            exam_product = exam_product_result.scalar_one_or_none()
            
            # 计算时间段
            start_datetime = datetime.combine(start_date, start_time)
            time_slots = await self.calculate_time_slots(
                len(candidates), exam_type, exam_product, start_datetime
            )
            
            # 验证场地可用性
            total_end_time = time_slots[-1]["end_time"] if time_slots else start_datetime
            if not await self.check_venue_availability(db, venue_id, start_datetime, total_end_time):
                raise HTTPException(
                    status_code=400,
                    detail=f"场地在 {start_datetime} 到 {total_end_time} 时间段不可用"
                )
            
            # 创建排期记录
            created_schedules = []
            for i, candidate in enumerate(candidates):
                if exam_type == "theory":
                    # 理论考试按批次分配
                    venue_capacity = venue.capacity or 50
                    batch_index = i // venue_capacity
                    time_slot = time_slots[batch_index] if batch_index < len(time_slots) else time_slots[-1]
                else:
                    # 实操考试逐个分配
                    time_slot = time_slots[i] if i < len(time_slots) else time_slots[-1]
                
                schedule = Schedule(
                    candidate_id=candidate.id,
                    exam_product_id=candidate.exam_product_id,
                    venue_id=venue_id,
                    scheduled_date=start_date,
                    start_time=time_slot["start_time"],
                    end_time=time_slot["end_time"],
                    schedule_type=exam_type,
                    status="待确认",
                    check_in_status="not_checked_in",
                    created_by=current_user.id
                )
                
                db.add(schedule)
                created_schedules.append({
                    "candidate_id": candidate.id,
                    "candidate_name": candidate.name,
                    "start_time": time_slot["start_time"].isoformat(),
                    "end_time": time_slot["end_time"].isoformat()
                })
                
                # 更新考生状态
                candidate.status = "已排期"
            
            await db.commit()
            
            return {
                "success": True,
                "message": f"成功为 {len(candidates)} 名考生创建 {exam_type} 考试排期",
                "exam_type": exam_type,
                "venue_name": venue.name,
                "start_date": start_date.isoformat(),
                "created_count": len(created_schedules),
                "schedules": created_schedules
            }
            
        except Exception as e:
            await db.rollback()
            if isinstance(e, HTTPException):
                raise
            raise HTTPException(
                status_code=500,
                detail=f"批量排期失败: {str(e)}"
            )
    
    async def get_schedule_timeline(
        self,
        db: AsyncSession,
        start_date: date,
        end_date: Optional[date] = None,
        venue_id: Optional[int] = None,
        institution_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """获取排期时间线"""
        
        if not end_date:
            end_date = start_date
        
        # 构建查询条件
        query = select(Schedule).where(
            and_(
                Schedule.scheduled_date >= start_date,
                Schedule.scheduled_date <= end_date
            )
        )
        
        if venue_id:
            query = query.where(Schedule.venue_id == venue_id)
        
        if institution_id:
            query = query.join(Candidate).where(Candidate.institution_id == institution_id)
        
        query = query.order_by(Schedule.start_time)
        
        result = await db.execute(query)
        schedules = result.scalars().all()
        
        # 组织时间线数据
        timeline_data = {}
        
        for schedule in schedules:
            # 获取关联信息
            candidate_result = await db.execute(
                select(Candidate).where(Candidate.id == schedule.candidate_id)
            )
            candidate = candidate_result.scalar_one_or_none()
            
            venue_result = await db.execute(
                select(Venue).where(Venue.id == schedule.venue_id)
            )
            venue = venue_result.scalar_one_or_none()
            
            exam_product_result = await db.execute(
                select(ExamProduct).where(ExamProduct.id == schedule.exam_product_id)
            )
            exam_product = exam_product_result.scalar_one_or_none()
            
            # 按日期分组
            date_key = schedule.scheduled_date.isoformat()
            if date_key not in timeline_data:
                timeline_data[date_key] = []
            
            timeline_data[date_key].append({
                "id": schedule.id,
                "start_time": schedule.start_time.isoformat(),
                "end_time": schedule.end_time.isoformat(),
                "schedule_type": schedule.schedule_type,
                "status": schedule.status,
                "check_in_status": schedule.check_in_status,
                "candidate": {
                    "id": candidate.id if candidate else None,
                    "name": candidate.name if candidate else "未知",
                    "id_number": candidate.id_number if candidate else "未知"
                },
                "venue": {
                    "id": venue.id if venue else None,
                    "name": venue.name if venue else "未知",
                    "type": venue.type if venue else "未知"
                },
                "exam_product": {
                    "id": exam_product.id if exam_product else None,
                    "name": exam_product.name if exam_product else "未知"
                }
            })
        
        # 按机构统计
        institution_stats = {}
        for schedule in schedules:
            candidate_result = await db.execute(
                select(Candidate).where(Candidate.id == schedule.candidate_id)
            )
            candidate = candidate_result.scalar_one_or_none()
            
            if candidate and candidate.institution_id:
                inst_id = candidate.institution_id
                if inst_id not in institution_stats:
                    institution_stats[inst_id] = {
                        "total_schedules": 0,
                        "theory_count": 0,
                        "practical_count": 0
                    }
                
                institution_stats[inst_id]["total_schedules"] += 1
                if schedule.schedule_type == "theory":
                    institution_stats[inst_id]["theory_count"] += 1
                elif schedule.schedule_type == "practical":
                    institution_stats[inst_id]["practical_count"] += 1
        
        return {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "total_schedules": len(schedules),
            "timeline": timeline_data,
            "institution_stats": institution_stats
        }

# 单例服务实例
schedule_management_service = ScheduleManagementService()