"""
考生批量导入服务模块
支持Excel模板下载、批量导入和数据验证
"""
import pandas as pd
import io
from typing import List, Dict, Any, Tuple, Optional
from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import re

from src.models.candidate import Candidate
from src.models.exam_product import ExamProduct
from src.db.models import User


class CandidateImportService:
    """考生导入服务"""
    
    # Excel模板列定义
    TEMPLATE_COLUMNS = [
        "考生姓名",
        "身份证号", 
        "联系电话",
        "邮箱",
        "性别",
        "考试产品名称",
        "备注"
    ]
    
    # 必填字段
    REQUIRED_FIELDS = ["考生姓名", "身份证号", "联系电话", "考试产品名称"]
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    async def generate_template(self) -> bytes:
        """生成Excel导入模板"""
        # 创建示例数据
        sample_data = {
            "考生姓名": ["张三", "李四", "王五"],
            "身份证号": ["110101199001011234", "110101199002021234", "110101199003031234"],
            "联系电话": ["13800138001", "13800138002", "13800138003"],
            "邮箱": ["zhangsan@example.com", "lisi@example.com", "wangwu@example.com"],
            "性别": ["男", "女", "男"],
            "考试产品名称": ["多旋翼视距内驾驶员", "航拍摄影师认证", "植保飞行操作证"],
            "备注": ["", "有经验", "新手"]
        }
        
        # 创建DataFrame
        df = pd.DataFrame(sample_data)
        
        # 创建Excel文件
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # 写入数据表
            df.to_excel(writer, sheet_name='考生信息', index=False)
            
            # 创建说明表
            instructions = {
                "字段名": self.TEMPLATE_COLUMNS,
                "是否必填": ["是" if col in self.REQUIRED_FIELDS else "否" for col in self.TEMPLATE_COLUMNS],
                "说明": [
                    "考生真实姓名",
                    "18位身份证号码",
                    "11位手机号码",
                    "电子邮箱地址（选填）",
                    "男/女（选填）",
                    "必须为系统中已存在的考试产品名称",
                    "其他备注信息（选填）"
                ]
            }
            instructions_df = pd.DataFrame(instructions)
            instructions_df.to_excel(writer, sheet_name='填写说明', index=False)
        
        output.seek(0)
        return output.getvalue()
    
    async def validate_excel_file(self, file: UploadFile) -> bool:
        """验证Excel文件格式"""
        # 检查文件类型
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(
                status_code=400,
                detail="文件格式错误，请上传Excel文件（.xlsx或.xls）"
            )
        
        # 检查文件大小（限制10MB）
        if file.size and file.size > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="文件大小超限，请上传小于10MB的文件"
            )
        
        return True
    
    async def parse_excel_file(self, file: UploadFile) -> pd.DataFrame:
        """解析Excel文件"""
        try:
            # 读取文件内容
            contents = await file.read()
            
            # 使用pandas读取Excel
            df = pd.read_excel(io.BytesIO(contents), sheet_name=0)
            
            # 验证列名
            expected_columns = set(self.TEMPLATE_COLUMNS)
            actual_columns = set(df.columns.tolist())
            
            missing_columns = expected_columns - actual_columns
            if missing_columns:
                raise HTTPException(
                    status_code=400,
                    detail=f"Excel文件缺少必要列：{', '.join(missing_columns)}"
                )
            
            return df
            
        except Exception as e:
            if isinstance(e, HTTPException):
                raise
            raise HTTPException(
                status_code=400,
                detail=f"Excel文件解析失败：{str(e)}"
            )
    
    def validate_candidate_data(self, row: pd.Series, row_index: int) -> Dict[str, Any]:
        """验证单行考生数据"""
        errors = []
        warnings = []
        
        # 提取数据
        name = str(row.get("考生姓名", "")).strip()
        id_number = str(row.get("身份证号", "")).strip()
        phone = str(row.get("联系电话", "")).strip()
        email = str(row.get("邮箱", "")).strip() if pd.notna(row.get("邮箱")) else None
        gender = str(row.get("性别", "")).strip() if pd.notna(row.get("性别")) else None
        exam_product_name = str(row.get("考试产品名称", "")).strip()
        notes = str(row.get("备注", "")).strip() if pd.notna(row.get("备注")) else None
        
        # 验证必填字段
        if not name:
            errors.append(f"第{row_index + 2}行：考生姓名不能为空")
        elif len(name) > 50:
            errors.append(f"第{row_index + 2}行：考生姓名不能超过50个字符")
        
        if not id_number:
            errors.append(f"第{row_index + 2}行：身份证号不能为空")
        elif not self._validate_id_number(id_number):
            errors.append(f"第{row_index + 2}行：身份证号格式不正确")
        
        if not phone:
            errors.append(f"第{row_index + 2}行：联系电话不能为空")
        elif not self._validate_phone(phone):
            errors.append(f"第{row_index + 2}行：联系电话格式不正确")
        
        if not exam_product_name:
            errors.append(f"第{row_index + 2}行：考试产品名称不能为空")
        
        # 验证可选字段
        if email and not self._validate_email(email):
            errors.append(f"第{row_index + 2}行：邮箱格式不正确")
        
        if gender and gender not in ["男", "女"]:
            warnings.append(f"第{row_index + 2}行：性别应为'男'或'女'，已设置为空")
            gender = None
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "data": {
                "name": name,
                "id_number": id_number,
                "phone": phone,
                "email": email,
                "gender": gender,
                "exam_product_name": exam_product_name,
                "notes": notes
            }
        }
    
    def _validate_id_number(self, id_number: str) -> bool:
        """验证身份证号格式"""
        if len(id_number) != 18:
            return False
        
        # 前17位必须是数字
        if not id_number[:17].isdigit():
            return False
        
        # 最后一位可以是数字或X
        if not (id_number[17].isdigit() or id_number[17].upper() == 'X'):
            return False
        
        return True
    
    def _validate_phone(self, phone: str) -> bool:
        """验证手机号格式"""
        pattern = r'^1[3-9]\d{9}$'
        return bool(re.match(pattern, phone))
    
    def _validate_email(self, email: str) -> bool:
        """验证邮箱格式"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    async def import_candidates_batch(
        self,
        df: pd.DataFrame,
        db: AsyncSession,
        current_user: User
    ) -> Dict[str, Any]:
        """批量导入考生"""
        
        # 获取所有考试产品，用于验证
        result = await db.execute(select(ExamProduct))
        exam_products = {product.name: product.id for product in result.scalars().all()}
        
        validation_results = []
        valid_candidates = []
        total_errors = []
        total_warnings = []
        
        # 逐行验证数据
        for index, row in df.iterrows():
            validation = self.validate_candidate_data(row, index)
            validation_results.append(validation)
            
            if validation["valid"]:
                # 验证考试产品是否存在
                exam_product_name = validation["data"]["exam_product_name"]
                if exam_product_name not in exam_products:
                    validation["valid"] = False
                    validation["errors"].append(
                        f"第{index + 2}行：考试产品'{exam_product_name}'不存在"
                    )
                else:
                    validation["data"]["exam_product_id"] = exam_products[exam_product_name]
                    valid_candidates.append(validation["data"])
            
            total_errors.extend(validation["errors"])
            total_warnings.extend(validation["warnings"])
        
        # 如果有错误，返回错误信息
        if total_errors:
            return {
                "success": False,
                "total_rows": len(df),
                "valid_count": len(valid_candidates),
                "error_count": len(total_errors),
                "warning_count": len(total_warnings),
                "errors": total_errors[:20],  # 最多返回20个错误
                "warnings": total_warnings[:10],  # 最多返回10个警告
                "message": f"数据验证失败，共{len(total_errors)}个错误"
            }
        
        # 检查重复的身份证号
        id_numbers = [candidate["id_number"] for candidate in valid_candidates]
        duplicate_ids = []
        seen_ids = set()
        for id_number in id_numbers:
            if id_number in seen_ids:
                duplicate_ids.append(id_number)
            else:
                seen_ids.add(id_number)
        
        if duplicate_ids:
            return {
                "success": False,
                "message": f"Excel中存在重复的身份证号：{', '.join(duplicate_ids)}"
            }
        
        # 检查数据库中是否已存在
        existing_result = await db.execute(
            select(Candidate.id_number).where(
                Candidate.id_number.in_(id_numbers)
            )
        )
        existing_ids = [row[0] for row in existing_result.all()]
        
        if existing_ids:
            return {
                "success": False,
                "message": f"以下身份证号已存在于系统中：{', '.join(existing_ids)}"
            }
        
        # 执行批量导入
        try:
            imported_count = 0
            for candidate_data in valid_candidates:
                candidate = Candidate(
                    name=candidate_data["name"],
                    id_number=candidate_data["id_number"],
                    phone=candidate_data["phone"],
                    email=candidate_data["email"],
                    gender=candidate_data["gender"],
                    exam_product_id=candidate_data["exam_product_id"],
                    institution_id=current_user.institution_id,
                    created_by=current_user.id,
                    notes=candidate_data["notes"],
                    status="待排期"
                )
                db.add(candidate)
                imported_count += 1
            
            await db.commit()
            
            return {
                "success": True,
                "total_rows": len(df),
                "imported_count": imported_count,
                "warning_count": len(total_warnings),
                "warnings": total_warnings,
                "message": f"成功导入{imported_count}条考生记录"
            }
            
        except Exception as e:
            await db.rollback()
            return {
                "success": False,
                "message": f"导入失败：{str(e)}"
            }

# 单例服务实例
candidate_import_service = CandidateImportService()