"""
系统初始化数据脚本
创建预设角色、权限和基础数据
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.role import Role
from src.models.permission import Permission, RolePermission
from src.models.exam_product import ExamProduct
from src.models.venue import Venue
from src.core.rbac import UserRole, Permission as PermissionEnum, ROLE_PERMISSIONS
from datetime import datetime

async def init_roles(db: AsyncSession):
    """初始化系统角色"""
    roles_data = [
        {
            "name": UserRole.SUPER_ADMIN.value,
            "description": "系统超级管理员，拥有所有权限"
        },
        {
            "name": UserRole.EXAM_ADMIN.value,
            "description": "考务管理员，负责考务排期和现场监控"
        },
        {
            "name": UserRole.INSTITUTION_USER.value,
            "description": "机构用户，为本机构学员进行报名管理"
        },
        {
            "name": UserRole.STAFF.value,
            "description": "考务人员，负责现场扫码签到"
        },
        {
            "name": UserRole.CANDIDATE.value,
            "description": "考生，查看个人信息和考试安排"
        }
    ]
    
    for role_data in roles_data:
        # 检查角色是否已存在
        result = await db.execute(select(Role).where(Role.name == role_data["name"]))
        existing_role = result.scalar_one_or_none()
        
        if not existing_role:
            role = Role(name=role_data["name"])
            db.add(role)
            print(f"创建角色: {role_data['name']}")
    
    await db.commit()
    print("角色初始化完成")

async def init_exam_products(db: AsyncSession):
    """初始化考试产品"""
    exam_products_data = [
        {
            "name": "多旋翼视距内驾驶员",
            "description": "多旋翼无人机视距内驾驶员资格考试",
            "category": "理论+实操",
            "duration": 120,
            "theory_duration": 60,
            "practical_duration": 15,
            "price": 500.0,
            "status": "active"
        },
        {
            "name": "多旋翼超视距驾驶员", 
            "description": "多旋翼无人机超视距驾驶员资格考试",
            "category": "理论+实操",
            "duration": 150,
            "theory_duration": 90,
            "practical_duration": 20,
            "price": 800.0,
            "status": "active"
        },
        {
            "name": "固定翼视距内驾驶员",
            "description": "固定翼无人机视距内驾驶员资格考试",
            "category": "理论+实操",
            "duration": 130,
            "theory_duration": 60,
            "practical_duration": 20,
            "price": 600.0,
            "status": "active"
        },
        {
            "name": "航拍摄影师认证",
            "description": "专业航拍摄影师技能认证考试",
            "category": "实操",
            "duration": 90,
            "practical_duration": 30,
            "price": 400.0,
            "status": "active"
        },
        {
            "name": "植保飞行操作证",
            "description": "农业植保无人机操作资格考试",
            "category": "理论+实操",
            "duration": 100,
            "theory_duration": 40,
            "practical_duration": 20,
            "price": 550.0,
            "status": "active"
        }
    ]
    
    for product_data in exam_products_data:
        # 检查产品是否已存在
        result = await db.execute(select(ExamProduct).where(ExamProduct.name == product_data["name"]))
        existing_product = result.scalar_one_or_none()
        
        if not existing_product:
            product = ExamProduct(**product_data)
            db.add(product)
            print(f"创建考试产品: {product_data['name']}")
    
    await db.commit()
    print("考试产品初始化完成")

async def init_venues(db: AsyncSession):
    """初始化考场场地"""
    venues_data = [
        {
            "name": "理论考试一号教室",
            "type": "理论考场",
            "address": "主楼2层201室",
            "capacity": 50,
            "equipment": "投影仪、计算机、监控设备",
            "status": "active"
        },
        {
            "name": "理论考试二号教室",
            "type": "理论考场", 
            "address": "主楼2层202室",
            "capacity": 40,
            "equipment": "投影仪、计算机、监控设备",
            "status": "active"
        },
        {
            "name": "多旋翼实操A场",
            "type": "实操考场",
            "address": "户外训练场A区",
            "capacity": 8,
            "equipment": "GPS设备、安全防护网、应急设备",
            "status": "active"
        },
        {
            "name": "多旋翼实操B场",
            "type": "实操考场",
            "address": "户外训练场B区", 
            "capacity": 8,
            "equipment": "GPS设备、安全防护网、应急设备",
            "status": "active"
        },
        {
            "name": "固定翼实操场",
            "type": "实操考场",
            "address": "户外训练场C区",
            "capacity": 6,
            "equipment": "跑道、GPS设备、应急设备",
            "status": "active"
        },
        {
            "name": "候考休息区",
            "type": "候考场",
            "address": "主楼1层大厅",
            "capacity": 100,
            "equipment": "座椅、饮水设备、信息显示屏",
            "status": "active"
        }
    ]
    
    for venue_data in venues_data:
        # 检查场地是否已存在
        result = await db.execute(select(Venue).where(Venue.name == venue_data["name"]))
        existing_venue = result.scalar_one_or_none()
        
        if not existing_venue:
            venue = Venue(**venue_data)
            db.add(venue)
            print(f"创建考场: {venue_data['name']}")
    
    await db.commit()
    print("考场初始化完成")

async def init_permissions(db: AsyncSession):
    """初始化权限数据"""
    print("初始化权限数据...")
    
    for permission_enum in PermissionEnum:
        # 检查权限是否已存在
        result = await db.execute(select(Permission).where(Permission.name == permission_enum.value))
        existing_permission = result.scalar_one_or_none()
        
        if not existing_permission:
            permission = Permission(name=permission_enum.value)
            db.add(permission)
            print(f"创建权限: {permission_enum.value}")
    
    await db.commit()
    print("权限初始化完成")

async def init_role_permissions(db: AsyncSession):
    """初始化角色权限映射"""
    print("初始化角色权限映射...")
    
    # 获取所有角色
    roles_result = await db.execute(select(Role))
    roles = {role.name: role for role in roles_result.scalars().all()}
    
    # 获取所有权限
    permissions_result = await db.execute(select(Permission))
    permissions = {perm.name: perm for perm in permissions_result.scalars().all()}
    
    for role_enum, permission_list in ROLE_PERMISSIONS.items():
        role = roles.get(role_enum.value)
        if not role:
            print(f"警告: 角色 {role_enum.value} 不存在")
            continue
            
        for permission_enum in permission_list:
            permission = permissions.get(permission_enum.value)
            if not permission:
                print(f"警告: 权限 {permission_enum.value} 不存在")
                continue
            
            # 检查角色权限映射是否已存在
            result = await db.execute(
                select(RolePermission).where(
                    (RolePermission.role_id == role.id) & 
                    (RolePermission.permission_id == permission.id)
                )
            )
            existing_mapping = result.scalar_one_or_none()
            
            if not existing_mapping:
                role_permission = RolePermission(
                    role_id=role.id,
                    permission_id=permission.id
                )
                db.add(role_permission)
                print(f"分配权限 {permission_enum.value} 给角色 {role_enum.value}")
    
    await db.commit()
    print("角色权限映射初始化完成")

async def init_system_data(db: AsyncSession):
    """初始化系统基础数据"""
    print("开始初始化系统数据...")
    
    await init_roles(db)
    await init_permissions(db)
    await init_role_permissions(db)
    await init_exam_products(db)
    await init_venues(db)
    
    print("系统数据初始化完成！")