#!/usr/bin/env python3
"""
重新创建测试用户脚本
"""
import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.db.session import async_session_maker
from src.models.user import User
from passlib.context import CryptContext

# 创建密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def recreate_test_user():
    """重新创建测试用户"""
    try:
        async with async_session_maker() as session:
            # 删除现有用户
            from sqlalchemy import select, delete
            stmt = select(User).where(User.email == "test@example.com")
            result = await session.execute(stmt)
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                print(f"🗑️ 删除现有用户: {existing_user.id}")
                delete_stmt = delete(User).where(User.id == existing_user.id)
                await session.execute(delete_stmt)
                await session.commit()
            
            # 创建新用户
            hashed_password = pwd_context.hash("testpassword123")
            print(f"🔐 密码哈希: {hashed_password}")
            
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
            
            print(f"✅ 测试用户重新创建成功!")
            print(f"   用户ID: {new_user.id}")
            print(f"   邮箱: {new_user.email}")
            print(f"   用户名: {new_user.username}")
            print(f"   密码哈希: {new_user.hashed_password}")
            print(f"   角色ID: {new_user.role_id}")
            print(f"   机构ID: {new_user.institution_id}")
            print("\n📝 登录信息:")
            print("   邮箱: test@example.com")
            print("   用户名: testuser")
            print("   密码: testpassword123")
            
            # 测试密码验证
            is_valid = pwd_context.verify("testpassword123", new_user.hashed_password)
            print(f"🔍 密码验证测试: {'✅ 通过' if is_valid else '❌ 失败'}")
            
            return True
                
    except Exception as e:
        print(f"❌ 重新创建用户失败: {e}")
        return False

if __name__ == "__main__":
    print("🔧 重新创建测试用户...")
    asyncio.run(recreate_test_user()) 