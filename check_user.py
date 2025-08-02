#!/usr/bin/env python3
"""
检查用户信息的脚本
"""
import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.db.session import async_session_maker
from src.models.user import User

async def check_user():
    """检查用户信息"""
    try:
        async with async_session_maker() as session:
            from sqlalchemy import select
            stmt = select(User).where(User.email == "test@example.com")
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            
            if user:
                print(f"✅ 找到测试用户!")
                print(f"   用户ID: {user.id}")
                print(f"   邮箱: {user.email}")
                print(f"   用户名: {user.username}")
                print(f"   密码哈希: {user.hashed_password[:50]}...")
                print(f"   角色ID: {user.role_id}")
                print(f"   机构ID: {user.institution_id}")
                print(f"   是否激活: {user.is_active}")
                print(f"   是否超级用户: {user.is_superuser}")
                print(f"   是否已验证: {user.is_verified}")
            else:
                print("❌ 未找到测试用户")
                
    except Exception as e:
        print(f"❌ 检查用户失败: {e}")

if __name__ == "__main__":
    print("🔍 检查用户信息...")
    asyncio.run(check_user()) 