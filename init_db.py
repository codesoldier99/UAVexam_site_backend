#!/usr/bin/env python3
"""
数据库初始化脚本
用于创建初始角色和超级用户
"""

import asyncio
import json
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_async_session
from src.models.user import User
from src.models.role import Role
from src.auth.fastapi_users_config import UserManager
from src.core.config import settings


async def create_initial_roles():
    """创建初始角色"""
    async for session in get_async_session():
        try:
            # 检查是否已存在角色
            existing_roles = await session.execute(
                "SELECT COUNT(*) FROM roles"
            )
            if existing_roles.scalar() > 0:
                print("角色已存在，跳过创建")
                return
            
            # 创建默认角色
            roles_data = [
                {
                    "name": "超级管理员",
                    "description": "拥有所有权限的超级管理员",
                    "permissions": json.dumps([
                        "user:read", "user:write", "user:delete",
                        "institution:read", "institution:write", "institution:delete",
                        "exam:read", "exam:write", "exam:delete",
                        "admin:all"
                    ])
                },
                {
                    "name": "机构管理员",
                    "description": "机构级别的管理员",
                    "permissions": json.dumps([
                        "institution:read", "institution:write",
                        "exam:read", "exam:write",
                        "user:read"
                    ])
                },
                {
                    "name": "普通用户",
                    "description": "普通用户",
                    "permissions": json.dumps([
                        "user:read",
                        "exam:read"
                    ])
                }
            ]
            
            for role_data in roles_data:
                role = Role(**role_data)
                session.add(role)
            
            await session.commit()
            print("初始角色创建成功")
            
        except Exception as e:
            print(f"创建角色失败: {e}")
            await session.rollback()


async def create_superuser():
    """创建超级用户"""
    async for session in get_async_session():
        try:
            # 检查是否已存在超级用户
            existing_superuser = await session.execute(
                "SELECT COUNT(*) FROM users WHERE is_superuser = 1"
            )
            if existing_superuser.scalar() > 0:
                print("超级用户已存在，跳过创建")
                return
            
            # 获取超级管理员角色
            superuser_role = await session.execute(
                "SELECT id FROM roles WHERE name = '超级管理员'"
            )
            role_id = superuser_role.scalar()
            
            # 创建超级用户
            superuser = User(
                email="admin@exam.com",
                username="admin",
                hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8J5QKq",  # admin123
                is_active=True,
                is_superuser=True,
                is_verified=True,
                role_id=role_id
            )
            
            session.add(superuser)
            await session.commit()
            print("超级用户创建成功")
            print("默认登录信息:")
            print("  邮箱: admin@exam.com")
            print("  用户名: admin")
            print("  密码: admin123")
            
        except Exception as e:
            print(f"创建超级用户失败: {e}")
            await session.rollback()


async def main():
    """主函数"""
    print("开始初始化数据库...")
    
    await create_initial_roles()
    await create_superuser()
    
    print("数据库初始化完成!")


if __name__ == "__main__":
    asyncio.run(main()) 