from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from src.institutions.models import Institution
from src.institutions.schemas import InstitutionCreate, InstitutionUpdate, InstitutionStats
from src.models.user import User
from src.core.security import get_password_hash
import uuid


class InstitutionService:
    @staticmethod
    def create(db: Session, institution: InstitutionCreate) -> Institution:
        db_institution = Institution(
            name=institution.name,
            code=institution.code or f"INST_{uuid.uuid4().hex[:8].upper()}",
            contact_person=institution.contact_person,
            phone=institution.phone,
            email=institution.email,
            address=institution.address,
            description=institution.description,
            status=institution.status,
            license_number=institution.license_number,
            business_scope=institution.business_scope
        )
        db.add(db_institution)
        db.commit()
        db.refresh(db_institution)
        return db_institution

    @staticmethod
    def create_with_admin(db: Session, institution: InstitutionCreate) -> Institution:
        """创建机构并同时创建管理员账号"""
        # 创建机构
        db_institution = Institution(
            name=institution.name,
            code=institution.code or f"INST_{uuid.uuid4().hex[:8].upper()}",
            contact_person=institution.contact_person,
            phone=institution.phone,
            email=institution.email,
            address=institution.address,
            description=institution.description,
            status=institution.status,
            license_number=institution.license_number,
            business_scope=institution.business_scope
        )
        db.add(db_institution)
        db.flush()  # 获取机构ID
        
        # 创建管理员账号
        admin_user = User(
            username=institution.admin_username,
            email=institution.admin_email,
            hashed_password=get_password_hash(institution.admin_password),
            is_active=True,
            is_superuser=False,  # 机构管理员不是超级管理员
            institution_id=db_institution.id
        )
        db.add(admin_user)
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
    def get_by_code(db: Session, code: str) -> Optional[Institution]:
        return db.query(Institution).filter(Institution.code == code).first()

    @staticmethod
    def get_multi(db: Session, skip: int = 0, limit: int = 100, 
                  search: Optional[str] = None, status: Optional[str] = None) -> List[Institution]:
        query = db.query(Institution)
        
        # 搜索过滤
        if search:
            query = query.filter(
                or_(
                    Institution.name.contains(search),
                    Institution.code.contains(search),
                    Institution.contact_person.contains(search),
                    Institution.phone.contains(search)
                )
            )
        
        # 状态过滤
        if status:
            query = query.filter(Institution.status == status)
        
        return query.offset(skip).limit(limit).all()

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
    def count(db: Session, search: Optional[str] = None, status: Optional[str] = None) -> int:
        """获取机构总数"""
        query = db.query(Institution)
        
        if search:
            query = query.filter(
                or_(
                    Institution.name.contains(search),
                    Institution.code.contains(search),
                    Institution.contact_person.contains(search),
                    Institution.phone.contains(search)
                )
            )
        
        if status:
            query = query.filter(Institution.status == status)
        
        return query.count()

    @staticmethod
    def get_stats(db: Session) -> InstitutionStats:
        """获取机构统计信息"""
        total_institutions = db.query(Institution).count()
        active_institutions = db.query(Institution).filter(Institution.status == "active").count()
        inactive_institutions = db.query(Institution).filter(Institution.status == "inactive").count()
        total_users = db.query(User).count()
        
        return InstitutionStats(
            total_institutions=total_institutions,
            active_institutions=active_institutions,
            inactive_institutions=inactive_institutions,
            total_users=total_users
        )

    @staticmethod
    def delete(db: Session, institution_id: int) -> bool:
        """逻辑删除机构及其关联的用户账号"""
        db_institution = InstitutionService.get(db, institution_id)
        if db_institution:
            # 删除关联的用户账号
            users = db.query(User).filter(User.institution_id == institution_id).all()
            for user in users:
                db.delete(user)
            
            # 删除机构
            db.delete(db_institution)
            db.commit()
            return True
        return False

    @staticmethod
    def bulk_update_status(db: Session, institution_ids: List[int], status: str) -> bool:
        """批量更新机构状态"""
        try:
            db.query(Institution).filter(Institution.id.in_(institution_ids)).update(
                {"status": status}, synchronize_session=False
            )
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False 