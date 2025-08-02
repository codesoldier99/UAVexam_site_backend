import asyncio
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import text
from src.db.session import get_async_session

async def init_test_data():
    """初始化测试数据"""
    print("=" * 50)
    print("初始化测试数据")
    print("=" * 50)
    
    async for session in get_async_session():
        try:
            # 1. 创建角色
            print("\n1. 创建角色...")
            await session.execute(text("""
                INSERT IGNORE INTO roles (id, name, description) VALUES 
                (1, 'admin', '管理员'),
                (2, 'user', '普通用户')
            """))
            
            # 2. 创建机构
            print("2. 创建机构...")
            await session.execute(text("""
                INSERT IGNORE INTO institutions (id, name, code, contact_person, phone, email, address, description, status) VALUES 
                (1, '测试机构', 'TEST_001', '张三', '13800138000', 'test@example.com', '北京市朝阳区', '测试机构', 'active')
            """))
            
            await session.commit()
            print("✅ 测试数据初始化完成")
            
        except Exception as e:
            print(f"❌ 初始化失败: {e}")
            await session.rollback()
        finally:
            await session.close()

if __name__ == "__main__":
    asyncio.run(init_test_data()) 