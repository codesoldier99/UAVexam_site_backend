from sqlalchemy.orm import Session
from src.models.exam_product import ExamProduct, ExamCategory, ExamType, ExamClass, ExamLevel
from src.db.session import get_db

def init_exam_products(db: Session):
    """初始化考试产品数据"""
    
    # 检查是否已有数据
    existing_count = db.query(ExamProduct).count()
    if existing_count > 0:
        print(f"数据库中已有 {existing_count} 个考试产品，跳过初始化")
        return
    
    # 真实可信的考试产品数据
    exam_products = [
        {
            "name": "VLOS多旋翼无人机驾驶员考试",
            "description": "视距内多旋翼无人机驾驶员资格考试，适用于农业植保、航拍摄影等应用场景",
            "code": "VLOS_MULTIROTOR_001",
            "category": ExamCategory.VLOS,
            "exam_type": ExamType.MULTIROTOR,
            "exam_class": ExamClass.AGRICULTURE,
            "exam_level": ExamLevel.PILOT,
            "duration_minutes": 120,
            "theory_pass_score": 80,
            "practical_pass_score": 80,
            "training_hours": 40,
            "price": 1500.0,
            "training_price": 3000.0,
            "theory_content": "无人机飞行原理、航空法规、气象知识、飞行安全等",
            "practical_content": "无人机操控、起降操作、航线规划、应急处理等",
            "requirements": "年满18周岁，身体健康，无色盲色弱，具备基本计算机操作能力",
            "status": "active"
        },
        {
            "name": "BVLOS固定翼无人机驾驶员考试",
            "description": "超视距固定翼无人机驾驶员资格考试，适用于电力巡检、测绘测量等专业应用",
            "code": "BVLOS_FIXEDWING_001",
            "category": ExamCategory.BVLOS,
            "exam_type": ExamType.FIXED_WING,
            "exam_class": ExamClass.POWER_INSPECTION,
            "exam_level": ExamLevel.CAPTAIN,
            "duration_minutes": 180,
            "theory_pass_score": 85,
            "practical_pass_score": 85,
            "training_hours": 60,
            "price": 2500.0,
            "training_price": 5000.0,
            "theory_content": "超视距飞行原理、空域管理、通信系统、导航技术等",
            "practical_content": "长距离飞行、复杂气象条件飞行、应急返航等",
            "requirements": "年满20周岁，具备VLOS证书，有固定翼飞行经验",
            "status": "active"
        },
        {
            "name": "VTOL垂直起降无人机考试",
            "description": "垂直起降无人机驾驶员资格考试，适用于物流配送、应急救援等应用",
            "code": "VTOL_001",
            "category": ExamCategory.BVLOS,
            "exam_type": ExamType.VTOL,
            "exam_class": ExamClass.LOGISTICS,
            "exam_level": ExamLevel.PILOT,
            "duration_minutes": 150,
            "theory_pass_score": 80,
            "practical_pass_score": 80,
            "training_hours": 50,
            "price": 2000.0,
            "training_price": 4000.0,
            "theory_content": "VTOL飞行原理、垂直起降技术、载荷管理、航线优化等",
            "practical_content": "垂直起降操作、悬停控制、精确着陆、载荷投放等",
            "requirements": "年满18周岁，具备多旋翼飞行基础，有物流或救援相关经验优先",
            "status": "active"
        },
        {
            "name": "航拍摄影师专业认证",
            "description": "专业航拍摄影师技能认证，涵盖摄影技术、后期制作、安全飞行等",
            "code": "AERIAL_PHOTO_001",
            "category": ExamCategory.VLOS,
            "exam_type": ExamType.MULTIROTOR,
            "exam_class": ExamClass.FILM_PHOTOGRAPHY,
            "exam_level": ExamLevel.PILOT,
            "duration_minutes": 90,
            "theory_pass_score": 75,
            "practical_pass_score": 85,
            "training_hours": 30,
            "price": 1200.0,
            "training_price": 2500.0,
            "theory_content": "摄影构图、光线控制、后期处理、版权法律等",
            "practical_content": "航拍技巧、镜头运用、稳定飞行、创意拍摄等",
            "requirements": "具备基础摄影知识，有无人机飞行经验，对摄影有浓厚兴趣",
            "status": "active"
        },
        {
            "name": "无人机维修技师考试",
            "description": "无人机维修保养技师资格考试，涵盖机械、电子、软件等多方面技能",
            "code": "MAINTENANCE_001",
            "category": ExamCategory.VLOS,
            "exam_type": ExamType.MULTIROTOR,
            "exam_class": ExamClass.AGRICULTURE,
            "exam_level": ExamLevel.INSTRUCTOR,
            "duration_minutes": 200,
            "theory_pass_score": 85,
            "practical_pass_score": 90,
            "training_hours": 80,
            "price": 3000.0,
            "training_price": 6000.0,
            "theory_content": "无人机结构原理、电子电路、软件系统、故障诊断等",
            "practical_content": "机械维修、电子调试、软件升级、故障排除等",
            "requirements": "具备机械或电子相关专业背景，有维修工作经验",
            "status": "active"
        },
        {
            "name": "无人机教练员资格考试",
            "description": "无人机培训教练员资格考试，培养专业培训师资力量",
            "code": "INSTRUCTOR_001",
            "category": ExamCategory.VLOS,
            "exam_type": ExamType.MULTIROTOR,
            "exam_class": ExamClass.AGRICULTURE,
            "exam_level": ExamLevel.INSTRUCTOR,
            "duration_minutes": 240,
            "theory_pass_score": 90,
            "practical_pass_score": 90,
            "training_hours": 100,
            "price": 4000.0,
            "training_price": 8000.0,
            "theory_content": "教学方法论、课程设计、安全培训、考核标准等",
            "practical_content": "教学演示、学员指导、安全监督、考核评估等",
            "requirements": "具备高级无人机驾驶员证书，有教学经验，通过教练员培训",
            "status": "active"
        },
        {
            "name": "消防救援无人机操作考试",
            "description": "消防救援专用无人机操作资格考试，适用于消防、救援等紧急情况",
            "code": "FIRE_RESCUE_001",
            "category": ExamCategory.BVLOS,
            "exam_type": ExamType.MULTIROTOR,
            "exam_class": ExamClass.LOGISTICS,
            "exam_level": ExamLevel.CAPTAIN,
            "duration_minutes": 160,
            "theory_pass_score": 85,
            "practical_pass_score": 90,
            "training_hours": 70,
            "price": 2800.0,
            "training_price": 5500.0,
            "theory_content": "消防救援知识、应急响应、危险品识别、救援技术等",
            "practical_content": "复杂环境飞行、应急物资投放、现场勘察、救援协调等",
            "requirements": "具备消防救援相关经验，有紧急情况处理能力",
            "status": "active"
        },
        {
            "name": "农业植保无人机考试",
            "description": "农业植保无人机操作资格考试，专门针对农业应用场景",
            "code": "AGRI_SPRAY_001",
            "category": ExamCategory.VLOS,
            "exam_type": ExamType.MULTIROTOR,
            "exam_class": ExamClass.AGRICULTURE,
            "exam_level": ExamLevel.PILOT,
            "duration_minutes": 100,
            "theory_pass_score": 80,
            "practical_pass_score": 85,
            "training_hours": 35,
            "price": 1000.0,
            "training_price": 2000.0,
            "theory_content": "农业知识、植保技术、农药使用、作物保护等",
            "practical_content": "植保飞行、喷洒控制、航线规划、作业效率等",
            "requirements": "具备农业基础知识，有植保工作经验优先",
            "status": "active"
        }
    ]
    
    # 批量创建考试产品
    for product_data in exam_products:
        exam_product = ExamProduct(**product_data)
        db.add(exam_product)
    
    db.commit()
    print(f"成功初始化 {len(exam_products)} 个考试产品")

if __name__ == "__main__":
    # 直接运行时的测试代码
    db = next(get_db())
    try:
        init_exam_products(db)
        print("考试产品初始化完成")
    except Exception as e:
        print(f"初始化失败: {e}")
    finally:
        db.close() 