#!/usr/bin/env python3
"""
简单的测试用户创建脚本
"""
import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.db.session import async_session_maker
from src.models.user import User
from src.auth.fastapi_users_config import UserManager
from passlib.context import CryptContext

# 创建密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_simple_test_user():
    """创建简单的测试用户"""
    try:
        async with async_session_maker() as session:
            # 检查用户是否已存在
            from sqlalchemy import select
            stmt = select(User).where(User.email == "test@example.com")
            result = await session.execute(stmt)
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                print(f"✅ 测试用户已存在!")
                print(f"   用户ID: {existing_user.id}")
                print(f"   邮箱: {existing_user.email}")
                print(f"   用户名: {existing_user.username}")
                print("\n📝 登录信息:")
                print("   邮箱: test@example.com")
                print("   用户名: testuser")
                print("   密码: testpassword123")
                return True
            
            # 创建新用户
            hashed_password = pwd_context.hash("testpassword123")
            
            new_user = User(
                email="test@example.com",
                username="testuser",
                hashed_password=hashed_password,
                role_id=1,
                institution_id=1,
                is_active=True,
                is_superuser=False,
                is_verified=True
            )
            
            session.add(new_user)
            await session.commit()
            
            print(f"✅ 测试用户创建成功!")
            print(f"   用户ID: {new_user.id}")
            print(f"   邮箱: {new_user.email}")
            print(f"   用户名: {new_user.username}")
            print(f"   角色ID: {new_user.role_id}")
            print(f"   机构ID: {new_user.institution_id}")
            print("\n📝 登录信息:")
            print("   邮箱: test@example.com")
            print("   用户名: testuser")
            print("   密码: testpassword123")
            return True
                
    except Exception as e:
        print(f"❌ 创建用户失败: {e}")
        return False

if __name__ == "__main__":
    print("🔧 创建测试用户...")
    asyncio.run(create_simple_test_user()) 