from sqlalchemy.orm import Session
from typing import List, Optional
from src.models.venue import Venue
from src.schemas.venue import VenueCreate, VenueUpdate


class VenueService:
    @staticmethod
    def create(db: Session, venue: VenueCreate) -> Venue:
        db_venue = Venue(
            name=venue.name,
            description=venue.description,
            capacity=venue.capacity,
            is_active=venue.is_active
        )
        db.add(db_venue)
        db.commit()
        db.refresh(db_venue)
        return db_venue

    @staticmethod
    def get(db: Session, venue_id: int) -> Optional[Venue]:
        return db.query(Venue).filter(Venue.id == venue_id).first()

    @staticmethod
    def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Venue]:
        return db.query(Venue).offset(skip).limit(limit).all()

    @staticmethod
    def count(db: Session) -> int:
        """获取考场总数"""
        return db.query(Venue).count()

    @staticmethod
    def update(db: Session, venue_id: int, venue: VenueUpdate) -> Optional[Venue]:
        db_venue = VenueService.get(db, venue_id)
        if db_venue:
            update_data = venue.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_venue, field, value)
            db.commit()
            db.refresh(db_venue)
        return db_venue

    @staticmethod
    def delete(db: Session, venue_id: int) -> bool:
        db_venue = VenueService.get(db, venue_id)
        if db_venue:
            db.delete(db_venue)
            db.commit()
            return True
        return False
    
    @staticmethod
    def get_all_active(db: Session) -> List[Venue]:
        """获取所有活跃的考场"""
        return db.query(Venue).filter(Venue.is_active == True).all() 