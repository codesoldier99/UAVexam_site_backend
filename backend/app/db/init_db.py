from sqlalchemy.orm import Session
from app.db.session import SessionLocal, sync_engine
from app.db.base_class import Base
from app.models.user import User, Role, Permission
from app.models.institution import Institution
from app.models.exam import ExamProduct, Venue, VenueType
from app.core.security import get_password_hash
from app.core.config import settings

def init_db():
    """初始化数据库，创建表和默认数据"""
    
    # 创建所有表
    Base.metadata.create_all(bind=sync_engine)
    
    db = SessionLocal()
    
    try:
        # 创建默认角色
        roles = [
            Role(id=1, name="super_admin", description="超级管理员"),
            Role(id=2, name="exam_admin", description="考务管理员"),
            Role(id=3, name="institution", description="培训机构"),
            Role(id=4, name="staff", description="考务人员")
        ]
        
        for role in roles:
            existing = db.query(Role).filter_by(id=role.id).first()
            if not existing:
                db.add(role)
        
        # 创建默认权限
        permissions = [
            Permission(name="user.create", description="创建用户", resource="user", action="create"),
            Permission(name="user.read", description="查看用户", resource="user", action="read"),
            Permission(name="user.update", description="更新用户", resource="user", action="update"),
            Permission(name="user.delete", description="删除用户", resource="user", action="delete"),
            Permission(name="candidate.create", description="创建考生", resource="candidate", action="create"),
            Permission(name="candidate.read", description="查看考生", resource="candidate", action="read"),
            Permission(name="candidate.update", description="更新考生", resource="candidate", action="update"),
            Permission(name="schedule.create", description="创建排期", resource="schedule", action="create"),
            Permission(name="schedule.read", description="查看排期", resource="schedule", action="read"),
            Permission(name="schedule.update", description="更新排期", resource="schedule", action="update"),
        ]
        
        for perm in permissions:
            existing = db.query(Permission).filter_by(name=perm.name).first()
            if not existing:
                db.add(perm)
        
        # 创建超级管理员账号
        admin = db.query(User).filter_by(username=settings.FIRST_SUPERUSER).first()
        if not admin:
            admin = User(
                username=settings.FIRST_SUPERUSER,
                email="admin@example.com",
                full_name="系统管理员",
                hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
                is_active=True,
                is_superuser=True,
                role_id=1
            )
            db.add(admin)
        
        # 创建测试考务管理员
        exam_admin = db.query(User).filter_by(username="examadmin").first()
        if not exam_admin:
            exam_admin = User(
                username="examadmin",
                email="examadmin@example.com",
                full_name="考务管理员",
                hashed_password=get_password_hash("exam123"),
                is_active=True,
                is_superuser=False,
                role_id=2
            )
            db.add(exam_admin)
        
        # 创建测试机构
        institution = db.query(Institution).filter_by(code="INST001").first()
        if not institution:
            institution = Institution(
                name="福建飞行培训中心",
                code="INST001",
                contact_person="张经理",
                phone="13800138000",
                email="contact@fjftc.com",
                address="福建省福州市仓山区",
                is_active=True
            )
            db.add(institution)
            db.flush()  # 获取ID
            
            # 创建机构用户
            inst_user = User(
                username="institution",
                email="institution@example.com",
                full_name="机构用户",
                hashed_password=get_password_hash("inst123"),
                is_active=True,
                is_superuser=False,
                role_id=3,
                institution_id=institution.id
            )
            db.add(inst_user)
        
        # 创建默认考试产品
        products = [
            ExamProduct(
                name="多旋翼视距内驾驶员",
                code="MR_VLOS_PILOT",
                description="多旋翼无人机视距内驾驶员执照考试",
                exam_duration_theory=120,
                exam_duration_practice=15
            ),
            ExamProduct(
                name="多旋翼超视距驾驶员",
                code="MR_BVLOS_PILOT",
                description="多旋翼无人机超视距驾驶员执照考试",
                exam_duration_theory=120,
                exam_duration_practice=20
            ),
            ExamProduct(
                name="固定翼视距内驾驶员",
                code="FW_VLOS_PILOT",
                description="固定翼无人机视距内驾驶员执照考试",
                exam_duration_theory=120,
                exam_duration_practice=20
            )
        ]
        
        for product in products:
            existing = db.query(ExamProduct).filter_by(code=product.code).first()
            if not existing:
                db.add(product)
        
        # 创建默认考场
        venues = [
            Venue(name="理论考场1", code="THEORY_1", type=VenueType.THEORY, capacity=30, location="教学楼3楼301室"),
            Venue(name="理论考场2", code="THEORY_2", type=VenueType.THEORY, capacity=30, location="教学楼3楼302室"),
            Venue(name="实操场A", code="PRACTICE_A", type=VenueType.PRACTICE, capacity=1, location="室外飞行场A区"),
            Venue(name="实操场B", code="PRACTICE_B", type=VenueType.PRACTICE, capacity=1, location="室外飞行场B区"),
            Venue(name="候考室", code="WAITING_1", type=VenueType.WAITING, capacity=50, location="教学楼2楼大厅")
        ]
        
        for venue in venues:
            existing = db.query(Venue).filter_by(code=venue.code).first()
            if not existing:
                db.add(venue)
        
        db.commit()
        print("数据库初始化完成")
        
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()