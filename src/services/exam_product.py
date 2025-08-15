from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc
from typing import List, Optional, Dict, Any, Tuple
import logging
from src.models.exam_product import ExamProduct, ExamCategory, ExamType, ExamClass, ExamLevel
from src.schemas.exam_product import (
    ExamProductCreate, ExamProductUpdate, ExamProductQuery, 
    ExamProductBatchUpdate, ExamProductStatus
)

logger = logging.getLogger(__name__)

class ExamProductService:
    """考试产品服务层 - 产业级业务逻辑实现"""
    
    @staticmethod
    def create(db: Session, exam_product: ExamProductCreate, user_id: Optional[int] = None) -> ExamProduct:
        """创建考试产品"""
        try:
            # 检查产品代码唯一性
            existing = db.query(ExamProduct).filter(ExamProduct.code == exam_product.code).first()
            if existing:
                raise ValueError(f"产品代码 '{exam_product.code}' 已存在")
            
            # 创建新产品
            db_exam_product = ExamProduct(
                name=exam_product.name,
                description=exam_product.description,
                code=exam_product.code,
                category=exam_product.category,
                exam_type=exam_product.exam_type,
                exam_class=exam_product.exam_class,
                exam_level=exam_product.exam_level,
                duration_minutes=exam_product.duration_minutes,
                theory_pass_score=exam_product.theory_pass_score,
                practical_pass_score=exam_product.practical_pass_score,
                training_hours=exam_product.training_hours,
                price=exam_product.price,
                training_price=exam_product.training_price,
                theory_content=exam_product.theory_content,
                practical_content=exam_product.practical_content,
                requirements=exam_product.requirements,
                is_active=1,
                status='active'
            )
            
            db.add(db_exam_product)
            db.commit()
            db.refresh(db_exam_product)
            
            logger.info(f"成功创建考试产品: {exam_product.name} (ID: {db_exam_product.id})")
            return db_exam_product
            
        except Exception as e:
            db.rollback()
            logger.error(f"创建考试产品失败: {e}")
            raise

    @staticmethod
    def get(db: Session, product_id: int) -> Optional[ExamProduct]:
        """根据ID获取考试产品"""
        try:
            return db.query(ExamProduct).filter(ExamProduct.id == product_id).first()
        except Exception as e:
            logger.error(f"获取考试产品失败 (ID: {product_id}): {e}")
            raise

    @staticmethod
    def get_multi(
        db: Session, 
        page: int = 1, 
        size: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> Tuple[List[ExamProduct], int]:
        """获取考试产品列表（分页）"""
        try:
            query = db.query(ExamProduct)
            
            # 应用筛选条件
            if filters:
                if filters.get('search'):
                    try:
                        search_term = f"%{filters['search']}%"
                        logger.info(f"执行搜索查询，搜索词: {search_term}")
                        query = query.filter(
                            or_(
                                ExamProduct.name.ilike(search_term),
                                ExamProduct.description.ilike(search_term),
                                ExamProduct.code.ilike(search_term)
                            )
                        )
                        logger.info("搜索筛选条件应用成功")
                    except Exception as search_error:
                        logger.error(f"搜索筛选失败: {search_error}")
                        raise
                
                if filters.get('category'):
                    query = query.filter(ExamProduct.category == filters['category'])
                
                if filters.get('exam_type'):
                    query = query.filter(ExamProduct.exam_type == filters['exam_type'])
                
                if filters.get('exam_class'):
                    query = query.filter(ExamProduct.exam_class == filters['exam_class'])
                
                if filters.get('exam_level'):
                    query = query.filter(ExamProduct.exam_level == filters['exam_level'])
                
                if filters.get('status'):
                    query = query.filter(ExamProduct.status == filters['status'])
                
                if filters.get('min_price') is not None:
                    query = query.filter(ExamProduct.price >= filters['min_price'])
                
                if filters.get('max_price') is not None:
                    query = query.filter(ExamProduct.price <= filters['max_price'])
            
            # 获取总数
            total = query.count()
            
            # 排序
            sort_by = filters.get('sort_by', 'created_at') if filters else 'created_at'
            sort_order = filters.get('sort_order', 'desc') if filters else 'desc'
            
            if hasattr(ExamProduct, sort_by):
                column = getattr(ExamProduct, sort_by)
                if sort_order == 'asc':
                    query = query.order_by(asc(column))
                else:
                    query = query.order_by(desc(column))
            
            # 分页
            offset = (page - 1) * size
            products = query.offset(offset).limit(size).all()
            
            return products, total
            
        except Exception as e:
            logger.error(f"获取考试产品列表失败: {e}")
            logger.error(f"查询参数: page={page}, size={size}, filters={filters}")
            import traceback
            logger.error(f"详细错误信息: {traceback.format_exc()}")
            raise

    @staticmethod
    def update(
        db: Session, 
        product_id: int, 
        exam_product: ExamProductUpdate,
        user_id: Optional[int] = None
    ) -> Optional[ExamProduct]:
        """更新考试产品"""
        try:
            db_exam_product = db.query(ExamProduct).filter(ExamProduct.id == product_id).first()
            if not db_exam_product:
                return None
            
            # 检查代码唯一性（如果要更新代码）
            if exam_product.code and exam_product.code != db_exam_product.code:
                existing = db.query(ExamProduct).filter(
                    and_(
                        ExamProduct.code == exam_product.code,
                        ExamProduct.id != product_id
                    )
                ).first()
                if existing:
                    raise ValueError(f"产品代码 '{exam_product.code}' 已存在")
            
            # 更新字段
            update_data = exam_product.dict(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(db_exam_product, field):
                    setattr(db_exam_product, field, value)
            
            db.commit()
            db.refresh(db_exam_product)
            
            logger.info(f"成功更新考试产品: {db_exam_product.name} (ID: {product_id})")
            return db_exam_product
            
        except Exception as e:
            db.rollback()
            logger.error(f"更新考试产品失败 (ID: {product_id}): {e}")
            raise

    @staticmethod
    def delete(db: Session, product_id: int, user_id: Optional[int] = None) -> bool:
        """删除考试产品（软删除）"""
        try:
            db_exam_product = db.query(ExamProduct).filter(ExamProduct.id == product_id).first()
            if not db_exam_product:
                return False
            
            # 软删除：设置为未激活状态
            db_exam_product.is_active = 0
            db_exam_product.status = 'inactive'
            
            db.commit()
            
            logger.info(f"成功删除考试产品: {db_exam_product.name} (ID: {product_id})")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"删除考试产品失败 (ID: {product_id}): {e}")
            raise

    @staticmethod
    def batch_update_status(
        db: Session, 
        batch_update: ExamProductBatchUpdate,
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """批量更新考试产品状态"""
        try:
            updated_count = 0
            failed_ids = []
            
            for product_id in batch_update.ids:
                try:
                    db_exam_product = db.query(ExamProduct).filter(ExamProduct.id == product_id).first()
                    if db_exam_product:
                        if batch_update.status:
                            db_exam_product.status = batch_update.status.value
                        if batch_update.is_active is not None:
                            db_exam_product.is_active = batch_update.is_active
                        updated_count += 1
                    else:
                        failed_ids.append(product_id)
                except Exception as e:
                    logger.error(f"批量更新失败 (ID: {product_id}): {e}")
                    failed_ids.append(product_id)
            
            db.commit()
            
            result = {
                "updated_count": updated_count,
                "total_count": len(batch_update.ids),
                "failed_ids": failed_ids,
                "success": len(failed_ids) == 0
            }
            
            logger.info(f"批量更新完成: 成功 {updated_count}/{len(batch_update.ids)}")
            return result
            
        except Exception as e:
            db.rollback()
            logger.error(f"批量更新考试产品失败: {e}")
            raise

    @staticmethod
    def get_statistics(db: Session) -> Dict[str, Any]:
        """获取考试产品统计信息"""
        try:
            total_products = db.query(ExamProduct).count()
            active_products = db.query(ExamProduct).filter(ExamProduct.is_active == 1).count()
            inactive_products = total_products - active_products
            
            # 平均价格
            avg_price_result = db.query(func.avg(ExamProduct.price)).scalar()
            avg_training_price_result = db.query(func.avg(ExamProduct.training_price)).scalar()
            
            avg_price = float(avg_price_result) if avg_price_result else 0.0
            avg_training_price = float(avg_training_price_result) if avg_training_price_result else 0.0
            
            # 类别统计
            category_stats = {}
            category_results = db.query(
                ExamProduct.category, 
                func.count(ExamProduct.id)
            ).group_by(ExamProduct.category).all()
            
            for category, count in category_results:
                category_stats[category.value if category else 'unknown'] = count
            
            # 类型统计
            type_stats = {}
            type_results = db.query(
                ExamProduct.exam_type, 
                func.count(ExamProduct.id)
            ).group_by(ExamProduct.exam_type).all()
            
            for exam_type, count in type_results:
                type_stats[exam_type.value if exam_type else 'unknown'] = count
            
            return {
                "total_products": total_products,
                "active_products": active_products,
                "inactive_products": inactive_products,
                "avg_price": avg_price,
                "avg_training_price": avg_training_price,
                "category_stats": category_stats,
                "type_stats": type_stats
            }
            
        except Exception as e:
            logger.error(f"获取统计信息失败: {e}")
            raise

    @staticmethod
    def get_active_products(db: Session, limit: int = 50) -> List[ExamProduct]:
        """获取激活的考试产品"""
        try:
            return db.query(ExamProduct).filter(
                and_(
                    ExamProduct.is_active == 1,
                    ExamProduct.status == 'active'
                )
            ).limit(limit).all()
            
        except Exception as e:
            logger.error(f"获取激活产品失败: {e}")
            raise