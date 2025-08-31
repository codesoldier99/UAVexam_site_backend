#!/usr/bin/env python3
"""
重置admin用户密码
"""

from app.config.database import get_db
from app.models.user import User
from app.utils.security import get_password_hash, verify_password
from sqlalchemy.orm import Session

def reset_admin_password():
    """重置admin用户密码为admin123"""
    
    db = next(get_db())
    
    try:
        # 查找admin用户
        admin_user = db.query(User).filter(User.username == 'admin').first()
        
        if not admin_user:
            print("❌ 未找到admin用户")
            return
        
        print(f"✅ 找到admin用户: {admin_user.username}")
        print(f"当前密码哈希: {admin_user.password_hash}")
        
        # 重置密码为admin123
        new_password = "admin123"
        new_password_hash = get_password_hash(new_password)
        
        print(f"新密码哈希: {new_password_hash}")
        
        # 更新密码
        admin_user.password_hash = new_password_hash
        db.commit()
        
        print(f"✅ admin密码已重置为: {new_password}")
        
        # 验证新密码
        db.refresh(admin_user)
        is_valid = verify_password(new_password, admin_user.password_hash)
        print(f"验证新密码: {'✅ 成功' if is_valid else '❌ 失败'}")
        
    except Exception as e:
        print(f"❌ 重置过程中出错: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    reset_admin_password()