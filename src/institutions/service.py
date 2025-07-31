from sqlalchemy.orm import Session
from typing import List, Optional
from src.institutions.models import Institution
from src.institutions.schemas import InstitutionCreate, InstitutionUpdate


class InstitutionService:
    @staticmethod
    def create(db: Session, institution: InstitutionCreate) -> Institution:
        db_institution = Institution(
            name=institution.name,
            contact_person=institution.contact_person,
            phone=institution.phone
        )
        db.add(db_institution)
        db.commit()
        db.refresh(db_institution)
        return db_institution

    @staticmethod
    def get(db: Session, institution_id: int) -> Optional[Institution]:
        return db.query(Institution).filter(Institution.id == institution_id).first()

    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[Institution]:
        return db.query(Institution).filter(Institution.name == name).first()

    @staticmethod
    def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Institution]:
        return db.query(Institution).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, institution_id: int, institution: InstitutionUpdate) -> Optional[Institution]:
        db_institution = InstitutionService.get(db, institution_id)
        if db_institution:
            update_data = institution.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_institution, field, value)
            db.commit()
            db.refresh(db_institution)
        return db_institution

    @staticmethod
    def delete(db: Session, institution_id: int) -> bool:
        db_institution = InstitutionService.get(db, institution_id)
        if db_institution:
            db.delete(db_institution)
            db.commit()
            return True
        return False 