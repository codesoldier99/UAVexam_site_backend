#!/usr/bin/env python3
"""
检查beijing_admin的密码
"""

from app.config.database import get_db
from app.models.user import User
from app.utils.security import verify_password
from sqlalchemy.orm import Session

def check_beijing_admin_password():
    """检查beijing_admin的密码"""
    
    db = next(get_db())
    
    try:
        # 查找beijing_admin用户
        user = db.query(User).filter(User.username == 'beijing_admin').first()
        
        if not user:
            print("❌ 未找到beijing_admin用户")
            return
        
        print(f"✅ 找到用户: {user.username}")
        print(f"角色: {user.role.value}")
        print(f"是否激活: {user.is_active}")
        print(f"密码哈希: {user.password_hash}")
        
        # 测试常见密码
        test_passwords = [
            'beijing123',
            'beijing_admin',
            'admin123',
            'beijing',
            '123456',
            'password',
            'admin',
            'beijing_admin123'
        ]
        
        print("\n=== 测试密码 ===")
        for pwd in test_passwords:
            try:
                is_valid = verify_password(pwd, user.password_hash)
                print(f"密码 '{pwd}': {'✅ 正确' if is_valid else '❌ 错误'}")
                if is_valid:
                    print(f"🎉 找到正确密码: {pwd}")
                    break
            except Exception as e:
                print(f"密码 '{pwd}': ❌ 验证出错 - {e}")
        
    except Exception as e:
        print(f"❌ 检查过程中出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_beijing_admin_password()