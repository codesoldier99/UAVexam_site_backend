#!/usr/bin/env python3
"""
权限系统测试脚本
"""

import asyncio
from src.dependencies.permissions import require_user_read, require_admin
from src.auth.fastapi_users_config import UserManager
from src.models.user import User

async def test_permission_dependencies():
    """测试权限依赖函数"""
    print("🔐 测试权限依赖系统")
    print("=" * 50)
    
    # 测试权限依赖函数是否正确返回依赖函数
    print("\n1. 测试权限依赖函数类型")
    print(f"require_user_read 类型: {type(require_user_read)}")
    print(f"require_admin 类型: {type(require_admin)}")
    
    # 测试用户权限获取
    print("\n2. 测试用户权限获取")
    user_manager = UserManager(None)
    
    # 创建测试用户
    test_user = User(
        id=1,
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_password",
        is_active=True,
        is_superuser=False,
        is_verified=True,
        role_id=1  # 机构管理员
    )
    
    # 获取用户权限
    permissions = await user_manager.get_user_permissions(test_user)
    print(f"测试用户权限: {permissions}")
    
    # 测试超级管理员用户
    admin_user = User(
        id=2,
        email="admin@exam.com",
        username="admin",
        hashed_password="hashed_password",
        is_active=True,
        is_superuser=True,
        is_verified=True,
        role_id=1
    )
    
    admin_permissions = await user_manager.get_user_permissions(admin_user)
    print(f"管理员权限: {admin_permissions}")
    
    print("\n✅ 权限系统测试完成")

def test_imports():
    """测试导入"""
    print("📦 测试模块导入")
    print("=" * 30)
    
    try:
        from src.dependencies.permissions import (
            require_user_read,
            require_user_write,
            require_admin,
            require_permission
        )
        print("✅ 权限依赖导入成功")
        
        from src.auth.fastapi_users_config import (
            UserManager,
            current_active_user,
            fastapi_users
        )
        print("✅ 认证配置导入成功")
        
        from src.models.user import User
        print("✅ 用户模型导入成功")
        
    except Exception as e:
        print(f"❌ 导入失败: {e}")

def main():
    """主函数"""
    print("🚀 开始权限系统测试")
    
    # 测试导入
    test_imports()
    
    # 测试权限依赖
    asyncio.run(test_permission_dependencies())
    
    print("\n🎉 所有测试完成")

if __name__ == "__main__":
    main() 