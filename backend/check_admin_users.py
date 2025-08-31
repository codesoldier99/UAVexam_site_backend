#!/usr/bin/env python3
"""
检查数据库中的管理员用户
"""

from app.config.database import get_db
from app.models.user import User, UserRole
from sqlalchemy.orm import Session

def check_admin_users():
    """检查数据库中的管理员用户"""
    
    # 获取数据库会话
    db = next(get_db())
    
    try:
        print("=== 检查PC端可登录的用户 ===\n")
        
        # PC端允许的角色
        allowed_roles = [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR, UserRole.EXAMINER]
        
        # 查询所有管理类用户
        admin_users = db.query(User).filter(User.role.in_(allowed_roles)).all()
        
        if not admin_users:
            print("❌ 数据库中没有找到任何管理员用户")
            return
        
        print(f"找到 {len(admin_users)} 个管理类用户：\n")
        
        for user in admin_users:
            print(f"用户ID: {user.id}")
            print(f"用户名: {user.username}")
            print(f"邮箱: {user.email}")
            print(f"真实姓名: {user.real_name}")
            print(f"角色: {user.role.value}")
            print(f"是否激活: {user.is_active}")
            print(f"机构ID: {user.institution_id}")
            print(f"创建时间: {user.created_at}")
            print("-" * 50)
        
        # 特别检查常用的管理员账户
        print("\n=== 检查常用管理员账户 ===")
        common_admins = ['admin', 'super_admin', 'beijing_admin', 'administrator']
        
        for username in common_admins:
            user = db.query(User).filter(User.username == username).first()
            if user:
                print(f"✅ 找到用户: {username}")
                print(f"   角色: {user.role.value}")
                print(f"   是否激活: {user.is_active}")
                print(f"   密码哈希: {user.password_hash[:20]}...")
            else:
                print(f"❌ 未找到用户: {username}")
        
        # 测试密码验证
        print("\n=== 测试admin用户密码 ===")
        admin_user = db.query(User).filter(User.username == 'admin').first()
        if admin_user:
            from app.utils.security import verify_password
            
            test_passwords = ['admin123', 'admin', '123456', 'password']
            for pwd in test_passwords:
                is_valid = verify_password(pwd, admin_user.password_hash)
                print(f"密码 '{pwd}': {'✅ 正确' if is_valid else '❌ 错误'}")
        
    except Exception as e:
        print(f"❌ 检查过程中出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_admin_users()