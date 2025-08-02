import asyncio
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import text
from src.db.session import get_async_session

async def update_user_table():
    """更新用户表，添加email字段"""
    print("=" * 50)
    print("更新用户表结构")
    print("=" * 50)
    
    async for session in get_async_session():
        try:
            # 检查email字段是否已存在
            result = await session.execute(text("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'users' AND COLUMN_NAME = 'email'
            """))
            
            if result.fetchone():
                print("✅ email字段已存在")
            else:
                # 添加email字段
                await session.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN email VARCHAR(255) UNIQUE NOT NULL DEFAULT 'user@example.com'
                """))
                print("✅ 成功添加email字段")
            
            await session.commit()
            print("✅ 数据库更新完成")
            
        except Exception as e:
            print(f"❌ 数据库更新失败: {e}")
            await session.rollback()
        finally:
            await session.close()

if __name__ == "__main__":
    asyncio.run(update_user_table()) 