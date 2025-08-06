#!/usr/bin/env python3
"""
初始化角色数据
创建基本的用户角色
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from sqlalchemy.orm import Session
from src.db.session import SessionLocal
from src.models.role import Role
from sqlalchemy import text

def init_roles():
    """初始化角色数据"""
    db = SessionLocal()
    try:
        # 检查是否已有角色数据
        existing_count = db.query(Role).count()
        if existing_count > 0:
            print(f"角色数据已存在，共 {existing_count} 个角色")
            return
        
        # 创建基础角色
        roles = [
            {"name": "super_admin", "description": "超级管理员"},
            {"name": "admin", "description": "管理员"}, 
            {"name": "manager", "description": "经理"},
            {"name": "operator", "description": "操作员"},
            {"name": "viewer", "description": "查看者"},
        ]
        
        for role_data in roles:
            role = Role(name=role_data["name"])
            db.add(role)
        
        db.commit()
        print("角色数据初始化成功！")
        
        # 显示创建的角色
        roles = db.query(Role).all()
        print("已创建的角色:")
        for role in roles:
            print(f"  - ID: {role.id}, 名称: {role.name}")
            
    except Exception as e:
        print(f"角色初始化失败: {e}")
        db.rollback()
    finally:
        db.close()

def check_current_user_role():
    """检查当前登录用户的角色"""
    db = SessionLocal()
    try:
        # 查看用户角色分配情况
        result = db.execute(text("""
            SELECT u.id, u.username, u.email, r.name as role_name 
            FROM users u 
            LEFT JOIN roles r ON u.role_id = r.id 
            LIMIT 10
        """))
        
        print("\n当前用户角色分配:")
        print("=" * 50)
        for row in result:
            print(f"用户ID: {row[0]}, 用户名: {row[1]}, 邮箱: {row[2]}, 角色: {row[3] or '未分配'}")
            
    except Exception as e:
        print(f"查询用户角色失败: {e}")
    finally:
        db.close()

def assign_admin_role_to_user(user_id: int = 1):
    """为指定用户分配管理员角色"""
    db = SessionLocal()
    try:
        # 获取admin角色ID
        admin_role = db.query(Role).filter(Role.name == "admin").first()
        if not admin_role:
            print("admin角色不存在，请先初始化角色")
            return
        
        # 更新用户角色
        result = db.execute(text(f"""
            UPDATE users 
            SET role_id = {admin_role.id}
            WHERE id = {user_id}
        """))
        
        db.commit()
        
        if result.rowcount > 0:
            print(f"成功将用户ID {user_id} 的角色设置为 admin")
        else:
            print(f"用户ID {user_id} 不存在")
            
    except Exception as e:
        print(f"分配角色失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 开始初始化角色系统...")
    
    # 1. 初始化角色
    init_roles()
    
    # 2. 检查用户角色
    check_current_user_role()
    
    # 3. 为第一个用户分配admin角色
    print("\n为第一个用户分配admin角色...")
    assign_admin_role_to_user(1)
    
    # 4. 再次检查用户角色
    check_current_user_role()
    
    print("\n✅ 角色系统初始化完成！")
    print("\n权限说明:")
    print("- super_admin: 所有权限")
    print("- admin: 除删除外的所有权限")  
    print("- manager: 查看、创建、更新、统计")
    print("- operator: 查看、更新")
    print("- viewer: 仅查看")