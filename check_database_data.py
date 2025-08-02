#!/usr/bin/env python3
"""
检查数据库中的机构和角色数据
"""
import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.db.session import async_session_maker
from src.models.user import User

async def check_database_data():
    """检查数据库中的机构和角色数据"""
    try:
        async with async_session_maker() as session:
            # 检查机构表
            from sqlalchemy import text
            result = await session.execute(text("SELECT id, name FROM institutions LIMIT 5"))
            institutions = result.fetchall()
            
            print("🏢 机构数据:")
            if institutions:
                for inst in institutions:
                    print(f"   ID: {inst[0]}, 名称: {inst[1]}")
            else:
                print("   ❌ 没有找到机构数据")
            
            # 检查角色表
            result = await session.execute(text("SELECT id, name FROM roles LIMIT 5"))
            roles = result.fetchall()
            
            print("\n👥 角色数据:")
            if roles:
                for role in roles:
                    print(f"   ID: {role[0]}, 名称: {role[1]}")
            else:
                print("   ❌ 没有找到角色数据")
            
            # 检查用户表
            result = await session.execute(text("SELECT id, username, email, role_id, institution_id FROM users LIMIT 5"))
            users = result.fetchall()
            
            print("\n👤 用户数据:")
            if users:
                for user in users:
                    print(f"   ID: {user[0]}, 用户名: {user[1]}, 邮箱: {user[2]}, 角色ID: {user[3]}, 机构ID: {user[4]}")
            else:
                print("   ❌ 没有找到用户数据")
                
    except Exception as e:
        print(f"❌ 检查数据库失败: {e}")

if __name__ == "__main__":
    print("🔍 检查数据库数据...")
    asyncio.run(check_database_data()) 