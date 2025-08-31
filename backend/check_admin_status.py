#!/usr/bin/env python3
"""
检查admin用户状态
"""

from app.config.database import get_db
from app.models.user import User
from app.utils.security import verify_password
from sqlalchemy.orm import Session

def check_admin_status():
    """检查admin用户状态"""
    
    db = next(get_db())
    
    try:
        # 查找admin用户
        admin_user = db.query(User).filter(User.username == 'admin').first()
        
        if not admin_user:
            print("❌ 未找到admin用户")
            return
        
        print(f"✅ 找到admin用户")
        print(f"用户ID: {admin_user.id}")
        print(f"用户名: {admin_user.username}")
        print(f"邮箱: {admin_user.email}")
        print(f"真实姓名: {admin_user.real_name}")
        print(f"角色: {admin_user.role.value}")
        print(f"是否激活: {admin_user.is_active}")
        print(f"是否验证: {admin_user.is_verified}")
        print(f"密码哈希: {admin_user.password_hash}")
        
        # 测试密码
        test_passwords = ['admin123', 'admin', '123456']
        print("\n=== 测试密码 ===")
        for pwd in test_passwords:
            try:
                is_valid = verify_password(pwd, admin_user.password_hash)
                print(f"密码 '{pwd}': {'✅ 正确' if is_valid else '❌ 错误'}")
            except Exception as e:
                print(f"密码 '{pwd}': ❌ 验证出错 - {e}")
        
    except Exception as e:
        print(f"❌ 检查过程中出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_admin_status()