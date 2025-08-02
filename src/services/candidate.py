from sqlalchemy.orm import Session
from typing import List, Optional
from src.models.candidate import Candidate
from src.schemas.candidate import CandidateCreate, CandidateUpdate, BatchImportResponse
import pandas as pd
from io import BytesIO

class CandidateService:
    @staticmethod
    def create(db: Session, candidate: CandidateCreate, created_by: int) -> Candidate:
        db_candidate = Candidate(
            name=candidate.name,
            id_number=candidate.id_number,
            phone=candidate.phone,
            email=candidate.email,
            gender=candidate.gender,
            birth_date=candidate.birth_date,
            address=candidate.address,
            emergency_contact=candidate.emergency_contact,
            emergency_phone=candidate.emergency_phone,
            target_exam_product_id=candidate.target_exam_product_id,
            institution_id=candidate.institution_id,
            status=candidate.status,
            notes=candidate.notes,
            created_by=created_by
        )
        db.add(db_candidate)
        db.commit()
        db.refresh(db_candidate)
        return db_candidate

    @staticmethod
    def get(db: Session, candidate_id: int) -> Optional[Candidate]:
        return db.query(Candidate).filter(Candidate.id == candidate_id).first()

    @staticmethod
    def get_multi(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        institution_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[Candidate]:
        query = db.query(Candidate)
        
        if institution_id:
            query = query.filter(Candidate.institution_id == institution_id)
        
        if status:
            query = query.filter(Candidate.status == status)
        
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def count(db: Session, institution_id: Optional[int] = None) -> int:
        query = db.query(Candidate)
        if institution_id:
            query = query.filter(Candidate.institution_id == institution_id)
        return query.count()

    @staticmethod
    def update(db: Session, candidate_id: int, candidate: CandidateUpdate) -> Optional[Candidate]:
        db_candidate = CandidateService.get(db, candidate_id)
        if db_candidate:
            update_data = candidate.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_candidate, field, value)
            db.commit()
            db.refresh(db_candidate)
        return db_candidate

    @staticmethod
    def delete(db: Session, candidate_id: int) -> bool:
        db_candidate = CandidateService.get(db, candidate_id)
        if db_candidate:
            db.delete(db_candidate)
            db.commit()
            return True
        return False

    @staticmethod
    def batch_import(db: Session, file_content: bytes, institution_id: int, created_by: int) -> BatchImportResponse:
        """批量导入考生"""
        try:
            # 读取Excel文件
            df = pd.read_excel(BytesIO(file_content))
            
            success_count = 0
            failed_count = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    # 验证必填字段
                    if pd.isna(row.get('name')) or pd.isna(row.get('id_number')) or pd.isna(row.get('phone')):
                        failed_count += 1
                        errors.append(f"第{index+1}行：缺少必填字段")
                        continue
                    
                    # 检查身份证号是否已存在
                    existing = db.query(Candidate).filter(Candidate.id_number == str(row['id_number'])).first()
                    if existing:
                        failed_count += 1
                        errors.append(f"第{index+1}行：身份证号已存在")
                        continue
                    
                    # 创建考生
                    candidate_data = CandidateCreate(
                        name=str(row['name']),
                        id_number=str(row['id_number']),
                        phone=str(row['phone']),
                        email=str(row['email']) if not pd.isna(row.get('email')) else None,
                        gender=str(row['gender']) if not pd.isna(row.get('gender')) else None,
                        address=str(row['address']) if not pd.isna(row.get('address')) else None,
                        emergency_contact=str(row['emergency_contact']) if not pd.isna(row.get('emergency_contact')) else None,
                        emergency_phone=str(row['emergency_phone']) if not pd.isna(row.get('emergency_phone')) else None,
                        institution_id=institution_id
                    )
                    
                    CandidateService.create(db, candidate_data, created_by)
                    success_count += 1
                    
                except Exception as e:
                    failed_count += 1
                    errors.append(f"第{index+1}行：{str(e)}")
            
            return BatchImportResponse(
                success_count=success_count,
                failed_count=failed_count,
                errors=errors
            )
            
        except Exception as e:
            return BatchImportResponse(
                success_count=0,
                failed_count=0,
                errors=[f"文件解析错误：{str(e)}"]
            )

    @staticmethod
    def get_template_data() -> bytes:
        """生成导入模板"""
        template_data = {
            'name': ['张三', '李四'],
            'id_number': ['110101199001011234', '110101199002021234'],
            'phone': ['13800138001', '13800138002'],
            'email': ['zhangsan@example.com', 'lisi@example.com'],
            'gender': ['男', '女'],
            'address': ['北京市朝阳区', '北京市海淀区'],
            'emergency_contact': ['张父', '李父'],
            'emergency_phone': ['13900139001', '13900139002']
        }
        
        df = pd.DataFrame(template_data)
        output = BytesIO()
        df.to_excel(output, index=False)
        return output.getvalue() 