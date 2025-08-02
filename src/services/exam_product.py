from sqlalchemy.orm import Session
from typing import List, Optional
from src.models.exam_product import ExamProduct
from src.schemas.exam_product import ExamProductCreate, ExamProductUpdate


class ExamProductService:
    @staticmethod
    def create(db: Session, exam_product: ExamProductCreate) -> ExamProduct:
        db_exam_product = ExamProduct(
            name=exam_product.name,
            code=exam_product.code,
            description=exam_product.description,
            category=exam_product.category,
            exam_type=exam_product.exam_type,
            exam_class=exam_product.exam_class,
            exam_level=exam_product.exam_level,
            theory_pass_score=exam_product.theory_pass_score,
            practical_pass_score=exam_product.practical_pass_score,
            duration_minutes=exam_product.duration_minutes,
            training_hours=exam_product.training_hours,
            price=exam_product.price,
            training_price=exam_product.training_price,
            theory_content=exam_product.theory_content,
            practical_content=exam_product.practical_content,
            requirements=exam_product.requirements,
            is_active=exam_product.is_active
        )
        db.add(db_exam_product)
        db.commit()
        db.refresh(db_exam_product)
        return db_exam_product

    @staticmethod
    def get(db: Session, exam_product_id: int) -> Optional[ExamProduct]:
        return db.query(ExamProduct).filter(ExamProduct.id == exam_product_id).first()

    @staticmethod
    def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[ExamProduct]:
        return db.query(ExamProduct).offset(skip).limit(limit).all()

    @staticmethod
    def count(db: Session) -> int:
        """获取考试产品总数"""
        return db.query(ExamProduct).count()

    @staticmethod
    def update(db: Session, exam_product_id: int, exam_product: ExamProductUpdate) -> Optional[ExamProduct]:
        db_exam_product = ExamProductService.get(db, exam_product_id)
        if db_exam_product:
            update_data = exam_product.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_exam_product, field, value)
            db.commit()
            db.refresh(db_exam_product)
        return db_exam_product

    @staticmethod
    def delete(db: Session, exam_product_id: int) -> bool:
        db_exam_product = ExamProductService.get(db, exam_product_id)
        if db_exam_product:
            db.delete(db_exam_product)
            db.commit()
            return True
        return False 