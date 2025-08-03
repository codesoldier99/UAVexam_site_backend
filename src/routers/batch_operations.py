"""
批量操作API路由
支持Excel导入考生、批量排期等批量操作功能
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Depends
from fastapi.responses import StreamingResponse
from typing import Optional, List, Dict, Any
from datetime import datetime, date, time, timedelta
from pydantic import BaseModel
import io
import json

router = APIRouter(
    prefix="/batch",
    tags=["batch_operations"],
)

# ===== 数据模型 =====

class CandidateImportItem(BaseModel):
    """单个考生导入数据"""
    name: str
    id_number: str
    phone: Optional[str] = None
    exam_product_name: str
    institution_id: Optional[int] = None

class ImportResult(BaseModel):
    """导入结果"""
    total_rows: int
    success_count: int
    failed_count: int
    success_items: List[Dict]
    failed_items: List[Dict]
    import_time: str

class BatchScheduleRequest(BaseModel):
    """批量排期请求"""
    candidate_ids: List[int]
    exam_date: date
    start_time: time
    venue_id: int
    activity_name: str
    duration_minutes: int = 15

# ===== Excel模板和导入功能 =====

@router.get("/candidates/template")
async def download_candidate_template():
    """下载考生导入Excel模板"""
    
    # 模拟Excel模板内容 (实际应用中应生成真实的Excel文件)
    template_data = {
        "template_info": {
            "version": "v1.0",
            "created_date": datetime.now().isoformat(),
            "description": "考生批量导入模板"
        },
        "required_columns": [
            "考生姓名",
            "身份证号", 
            "联系电话",
            "考试产品名称"
        ],
        "sample_data": [
            {
                "考生姓名": "张三",
                "身份证号": "110101199001011234",
                "联系电话": "13800138001",
                "考试产品名称": "无人机驾驶员考试"
            },
            {
                "考生姓名": "李四", 
                "身份证号": "110101199002021234",
                "联系电话": "13800138002",
                "考试产品名称": "航拍摄影师认证"
            }
        ],
        "instructions": [
            "1. 请严格按照模板格式填写考生信息",
            "2. 身份证号必须为18位有效号码",
            "3. 考试产品名称必须与系统中已有产品匹配",
            "4. 联系电话为可选项",
            "5. 保存为.xlsx格式后上传"
        ]
    }
    
    # 生成模拟Excel文件内容
    excel_content = json.dumps(template_data, ensure_ascii=False, indent=2)
    excel_bytes = excel_content.encode('utf-8')
    
    # 返回模板文件
    return StreamingResponse(
        io.BytesIO(excel_bytes),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=candidates_import_template.xlsx"
        }
    )

@router.post("/candidates/import")
async def import_candidates_from_excel(
    file: UploadFile = File(..., description="Excel文件"),
    institution_id: int = Query(..., description="机构ID"),
    dry_run: bool = Query(False, description="是否仅验证不导入")
):
    """批量导入考生信息"""
    
    # 验证文件格式
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="请上传Excel格式文件 (.xlsx 或 .xls)")
    
    # 读取文件内容 (模拟)
    file_content = await file.read()
    
    # 模拟Excel解析和数据验证
    mock_import_data = [
        {
            "row": 2,
            "name": "测试考生1",
            "id_number": "110101199003011234", 
            "phone": "13800138111",
            "exam_product_name": "无人机驾驶员考试",
            "status": "valid"
        },
        {
            "row": 3,
            "name": "测试考生2",
            "id_number": "110101199004021234",
            "phone": "13800138222", 
            "exam_product_name": "航拍摄影师认证",
            "status": "valid"
        },
        {
            "row": 4,
            "name": "测试考生3",
            "id_number": "invalid_id",
            "phone": "13800138333",
            "exam_product_name": "无人机驾驶员考试", 
            "status": "invalid",
            "error": "身份证号格式不正确"
        },
        {
            "row": 5,
            "name": "",
            "id_number": "110101199006041234",
            "phone": "13800138444",
            "exam_product_name": "未知考试产品",
            "status": "invalid", 
            "error": "考生姓名不能为空，考试产品不存在"
        }
    ]
    
    # 分离成功和失败的数据
    success_items = [item for item in mock_import_data if item["status"] == "valid"]
    failed_items = [item for item in mock_import_data if item["status"] == "invalid"]
    
    # 如果是预览模式，只返回验证结果
    if dry_run:
        return {
            "message": "数据验证完成（预览模式）",
            "mode": "preview",
            "total_rows": len(mock_import_data),
            "valid_count": len(success_items),
            "invalid_count": len(failed_items),
            "valid_items": success_items,
            "invalid_items": failed_items,
            "next_action": "确认无误后可执行正式导入"
        }
    
    # 执行实际导入 (模拟)
    imported_candidates = []
    for item in success_items:
        imported_candidate = {
            "id": len(imported_candidates) + 100,  # 模拟新ID
            "name": item["name"],
            "id_number": item["id_number"],
            "phone": item["phone"],
            "exam_product_name": item["exam_product_name"],
            "institution_id": institution_id,
            "status": "待排期",
            "import_time": datetime.now().isoformat(),
            "row_number": item["row"]
        }
        imported_candidates.append(imported_candidate)
    
    # 构建导入结果
    result = ImportResult(
        total_rows=len(mock_import_data),
        success_count=len(success_items),
        failed_count=len(failed_items),
        success_items=imported_candidates,
        failed_items=failed_items,
        import_time=datetime.now().isoformat()
    )
    
    return {
        "message": f"批量导入完成！成功 {result.success_count} 条，失败 {result.failed_count} 条",
        "institution_id": institution_id,
        "file_name": file.filename,
        "file_size": len(file_content),
        "result": result.dict()
    }

@router.get("/candidates/import-history")
async def get_import_history(
    institution_id: Optional[int] = Query(None, description="机构ID筛选"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100)
):
    """获取导入历史记录"""
    
    # 模拟导入历史数据
    mock_history = [
        {
            "id": 1,
            "institution_id": 1,
            "institution_name": "北京航空培训中心",
            "file_name": "candidates_batch_20250803.xlsx",
            "total_rows": 45,
            "success_count": 42,
            "failed_count": 3,
            "import_time": "2025-08-03T09:30:00",
            "operator": "张经理"
        },
        {
            "id": 2,
            "institution_id": 2,
            "institution_name": "上海飞行学院", 
            "file_name": "new_students_20250802.xlsx",
            "total_rows": 23,
            "success_count": 23,
            "failed_count": 0,
            "import_time": "2025-08-02T14:15:00",
            "operator": "李主任"
        },
        {
            "id": 3,
            "institution_id": 1,
            "institution_name": "北京航空培训中心",
            "file_name": "补录学员_20250801.xlsx", 
            "total_rows": 12,
            "success_count": 10,
            "failed_count": 2,
            "import_time": "2025-08-01T16:45:00",
            "operator": "张经理"
        }
    ]
    
    # 应用筛选
    filtered_history = mock_history
    if institution_id:
        filtered_history = [h for h in filtered_history if h["institution_id"] == institution_id]
    
    # 分页
    total = len(filtered_history)
    start = (page - 1) * size
    end = start + size
    history_page = filtered_history[start:end]
    
    return {
        "message": "导入历史记录查询成功",
        "data": history_page,
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "pages": (total + size - 1) // size
        },
        "summary": {
            "total_imports": total,
            "total_candidates_imported": sum(h["success_count"] for h in filtered_history),
            "recent_import": max(h["import_time"] for h in filtered_history) if filtered_history else None
        }
    }

# ===== 批量排期功能 =====

@router.post("/schedules/batch-create")
async def batch_create_schedules(request: BatchScheduleRequest):
    """批量创建排期"""
    
    # 验证考生ID
    if not request.candidate_ids:
        raise HTTPException(status_code=400, detail="考生ID列表不能为空")
    
    if len(request.candidate_ids) > 50:
        raise HTTPException(status_code=400, detail="单次批量排期不能超过50人")
    
    # 模拟创建排期
    created_schedules = []
    failed_schedules = []
    
    for i, candidate_id in enumerate(request.candidate_ids):
        # 计算考试时间 (每人间隔指定分钟数)
        start_datetime = datetime.combine(request.exam_date, request.start_time)
        candidate_start_time = start_datetime + timedelta(minutes=i * request.duration_minutes)
        candidate_end_time = candidate_start_time + timedelta(minutes=request.duration_minutes)
        
        # 模拟验证考生状态
        if candidate_id in [999, 998]:  # 模拟无效考生
            failed_schedules.append({
                "candidate_id": candidate_id,
                "error": "考生不存在或状态不允许排期"
            })
            continue
        
        # 创建排期
        schedule = {
            "id": len(created_schedules) + 200,  # 模拟新排期ID
            "candidate_id": candidate_id,
            "candidate_name": f"考生{candidate_id}",
            "exam_date": request.exam_date.isoformat(),
            "start_time": candidate_start_time.time().isoformat(),
            "end_time": candidate_end_time.time().isoformat(),
            "venue_id": request.venue_id,
            "venue_name": "理论考场A" if request.venue_id == 1 else f"考场{request.venue_id}",
            "activity_name": request.activity_name,
            "status": "待签到",
            "created_time": datetime.now().isoformat()
        }
        created_schedules.append(schedule)
    
    return {
        "message": f"批量排期完成！成功创建 {len(created_schedules)} 条排期，失败 {len(failed_schedules)} 条",
        "exam_date": request.exam_date.isoformat(),
        "venue_id": request.venue_id,
        "activity_name": request.activity_name,
        "result": {
            "success_count": len(created_schedules),
            "failed_count": len(failed_schedules),
            "created_schedules": created_schedules,
            "failed_items": failed_schedules,
            "time_range": {
                "start": created_schedules[0]["start_time"] if created_schedules else None,
                "end": created_schedules[-1]["end_time"] if created_schedules else None
            }
        }
    }

@router.get("/schedules/candidates-available")
async def get_available_candidates_for_scheduling(
    exam_date: date = Query(..., description="排期日期"),
    institution_id: Optional[int] = Query(None, description="机构ID筛选"),
    exam_product_id: Optional[int] = Query(None, description="考试产品筛选")
):
    """获取可用于排期的考生列表"""
    
    # 模拟可排期考生数据
    available_candidates = [
        {
            "id": 1,
            "name": "张三",
            "id_number": "110101199001011234",
            "exam_product_id": 1,
            "exam_product_name": "无人机驾驶员考试",
            "institution_id": 1,
            "institution_name": "北京航空培训中心",
            "status": "待排期",
            "registration_date": "2025-08-01"
        },
        {
            "id": 3,
            "name": "王五",
            "id_number": "110101199003031234", 
            "exam_product_id": 2,
            "exam_product_name": "航拍摄影师认证",
            "institution_id": 1,
            "institution_name": "北京航空培训中心",
            "status": "待排期",
            "registration_date": "2025-08-03"
        },
        {
            "id": 4,
            "name": "赵六",
            "id_number": "110101199004041234",
            "exam_product_id": 1, 
            "exam_product_name": "无人机驾驶员考试",
            "institution_id": 2,
            "institution_name": "上海飞行学院",
            "status": "待排期",
            "registration_date": "2025-08-02"
        }
    ]
    
    # 应用筛选
    filtered_candidates = available_candidates
    if institution_id:
        filtered_candidates = [c for c in filtered_candidates if c["institution_id"] == institution_id]
    if exam_product_id:
        filtered_candidates = [c for c in filtered_candidates if c["exam_product_id"] == exam_product_id]
    
    return {
        "message": f"获取{exam_date}可排期考生成功",
        "exam_date": exam_date.isoformat(),
        "data": filtered_candidates,
        "total": len(filtered_candidates),
        "summary": {
            "by_institution": {},
            "by_exam_product": {},
            "total_available": len(filtered_candidates)
        }
    }