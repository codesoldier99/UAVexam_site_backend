#!/usr/bin/env python3
"""
创建测试用户脚本
"""
import asyncio
from src.db.session import async_session_maker
from src.models.user import User
from src.core.security import get_password_hash

async def create_test_user():
    """创建测试用户"""
    async with async_session_maker() as session:
        # 检查用户是否已存在
        from sqlalchemy import select
        stmt = select(User).where(User.email == "admin@exam.com")
        result = await session.execute(stmt)
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            print("✅ 测试用户已存在")
            return
        
        # 创建测试用户
        test_user = User(
            username="admin",
            email="admin@exam.com",
            hashed_password=get_password_hash("admin123"),
            is_superuser=True,
            is_active=True
        )
        
        session.add(test_user)
        await session.commit()
        print("✅ 测试用户创建成功")
        print(f"   用户名: admin")
        print(f"   邮箱: admin@exam.com")
        print(f"   密码: admin123")

if __name__ == "__main__":
    asyncio.run(create_test_user()) 