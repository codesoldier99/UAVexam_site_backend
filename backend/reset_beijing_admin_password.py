#!/usr/bin/env python3
"""
重置beijing_admin的密码
"""

from app.config.database import get_db
from app.models.user import User
from app.utils.security import get_password_hash, verify_password
from sqlalchemy.orm import Session

def reset_beijing_admin_password():
    """重置beijing_admin的密码为beijing123"""
    
    db = next(get_db())
    
    try:
        # 查找beijing_admin用户
        user = db.query(User).filter(User.username == 'beijing_admin').first()
        
        if not user:
            print("❌ 未找到beijing_admin用户")
            return
        
        print(f"✅ 找到用户: {user.username}")
        print(f"当前密码哈希: {user.password_hash}")
        
        # 重置密码为beijing123
        new_password = "beijing123"
        new_password_hash = get_password_hash(new_password)
        
        print(f"新密码哈希: {new_password_hash}")
        
        # 更新密码
        user.password_hash = new_password_hash
        db.commit()
        
        print(f"✅ 密码已重置为: {new_password}")
        
        # 验证新密码
        db.refresh(user)
        is_valid = verify_password(new_password, user.password_hash)
        print(f"验证新密码: {'✅ 成功' if is_valid else '❌ 失败'}")
        
        # 同时重置其他管理员的密码
        other_admins = [
            ('shanghai_admin', 'shanghai123'),
            ('shenzhen_admin', 'shenzhen123')
        ]
        
        for username, password in other_admins:
            admin_user = db.query(User).filter(User.username == username).first()
            if admin_user:
                admin_user.password_hash = get_password_hash(password)
                db.commit()
                print(f"✅ {username} 密码已重置为: {password}")
        
    except Exception as e:
        print(f"❌ 重置过程中出错: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    reset_beijing_admin_password()