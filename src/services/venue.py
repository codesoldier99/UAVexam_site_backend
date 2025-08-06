from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional, Tuple
from src.models.venue import Venue
from src.schemas.venue import VenueCreate, VenueUpdate
from src.core.cache import cache_result, invalidate_cache_on_change, CacheConfig


class VenueService:
    @staticmethod
    @invalidate_cache_on_change(["venue_list", "venue_stats"])
    async def create(db: Session, venue: VenueCreate) -> Venue:
        """创建新考场"""
        db_venue = Venue(
            name=venue.name,
            type=venue.type,
            address=venue.address,
            description=venue.description,
            capacity=venue.capacity,
            is_active=venue.is_active,
            contact_person=venue.contact_person,
            contact_phone=venue.contact_phone,
            equipment_info=venue.equipment_info
        )
        db.add(db_venue)
        db.commit()
        db.refresh(db_venue)
        return db_venue

    @staticmethod
    @cache_result(expire=CacheConfig.VENUE_DETAIL["expire"], key_prefix=CacheConfig.VENUE_DETAIL["key"])
    async def get(db: Session, venue_id: int) -> Optional[Venue]:
        """根据ID获取考场"""
        return db.query(Venue).filter(Venue.id == venue_id).first()

    @staticmethod
    @cache_result(expire=CacheConfig.VENUE_LIST["expire"], key_prefix=CacheConfig.VENUE_LIST["key"])
    async def get_multi(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[str] = None,
        venue_type: Optional[str] = None,
        search: Optional[str] = None
    ) -> Tuple[List[Venue], int]:
        """获取考场列表，支持筛选和搜索"""
        query = db.query(Venue)
        
        # 状态筛选
        if status:
            query = query.filter(Venue.status == status)
        
        # 类型筛选
        if venue_type:
            query = query.filter(Venue.type == venue_type)
        
        # 搜索功能 - 支持按名称、地址、联系人搜索
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Venue.name.ilike(search_pattern),
                    Venue.address.ilike(search_pattern),
                    Venue.contact_person.ilike(search_pattern)
                )
            )
        
        # 获取总数
        total = query.count()
        
        # 分页
        venues = query.offset(skip).limit(limit).all()
        
        return venues, total

    @staticmethod
    def count(db: Session) -> int:
        """获取考场总数"""
        return db.query(Venue).count()

    @staticmethod
    @invalidate_cache_on_change(["venue_list", "venue_detail", "venue_stats"])
    async def update(db: Session, venue_id: int, venue: VenueUpdate) -> Optional[Venue]:
        """更新考场信息"""
        db_venue = await VenueService.get(db, venue_id)
        if db_venue:
            update_data = venue.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_venue, field, value)
            db.commit()
            db.refresh(db_venue)
        return db_venue

    @staticmethod
    @invalidate_cache_on_change(["venue_list", "venue_detail", "venue_stats"])
    async def delete(db: Session, venue_id: int) -> bool:
        """删除考场"""
        db_venue = await VenueService.get(db, venue_id)
        if db_venue:
            db.delete(db_venue)
            db.commit()
            return True
        return False
    
    @staticmethod
    def get_all_active(db: Session) -> List[Venue]:
        """获取所有活跃的考场"""
        return db.query(Venue).filter(
            and_(Venue.is_active == True, Venue.status == 'active')
        ).all()
    
    @staticmethod
    def get_by_type(db: Session, venue_type: str) -> List[Venue]:
        """根据类型获取考场"""
        return db.query(Venue).filter(
            and_(
                Venue.type == venue_type, 
                Venue.is_active == True,
                Venue.status == 'active'
            )
        ).all()
    
    @staticmethod
    @invalidate_cache_on_change(["venue_list", "venue_detail", "venue_stats"])
    async def bulk_update_status(db: Session, venue_ids: List[int], status: str) -> int:
        """批量更新考场状态"""
        updated_count = db.query(Venue).filter(
            Venue.id.in_(venue_ids)
        ).update({Venue.status: status}, synchronize_session=False)
        db.commit()
        return updated_count

    @staticmethod
    @cache_result(expire=CacheConfig.VENUE_STATS["expire"], key_prefix=CacheConfig.VENUE_STATS["key"])
    async def get_venue_stats(db: Session) -> dict:
        """获取考场统计信息"""
        total = db.query(Venue).count()
        active = db.query(Venue).filter(
            and_(Venue.is_active == True, Venue.status == 'active')
        ).count()
        inactive = total - active
        
        # 按类型统计
        type_stats = {}
        types = db.query(Venue.type).distinct().all()
        for (venue_type,) in types:
            count = db.query(Venue).filter(Venue.type == venue_type).count()
            active_count = db.query(Venue).filter(
                and_(Venue.type == venue_type, Venue.is_active == True)
            ).count()
            type_stats[venue_type] = {
                "total": count,
                "active": active_count
            }
        
        # 容量统计
        total_capacity = db.query(func.sum(Venue.capacity)).scalar() or 0
        avg_capacity = db.query(func.avg(Venue.capacity)).scalar() or 0
        
        return {
            "total": total,
            "active": active,
            "inactive": inactive,
            "by_type": type_stats,
            "capacity": {
                "total": int(total_capacity),
                "average": round(float(avg_capacity), 2)
            }
        } 