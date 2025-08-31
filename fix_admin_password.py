"""
修复admin用户密码的简单脚本
"""

import os
import sys

# 添加backend路径到Python路径
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

try:
    from app.utils.security import get_password_hash, verify_password
    from app.config.database import get_db
    from app.models.user import User
    
    def fix_admin_password():
        """修复admin密码"""
        print("🔧 修复admin用户密码...")
        
        # 获取数据库连接
        db = next(get_db())
        
        try:
            # 查找admin用户
            admin_user = db.query(User).filter(User.username == "admin").first()
            
            if not admin_user:
                print("❌ 未找到admin用户")
                return False
            
            print(f"✅ 找到admin用户: {admin_user.real_name}")
            
            # 生成新的密码哈希
            new_password = "admin123"
            new_password_hash = get_password_hash(new_password)
            
            print(f"🔐 生成新密码哈希...")
            
            # 更新密码
            admin_user.password_hash = new_password_hash
            db.commit()
            
            print(f"✅ 密码已更新")
            print(f"   用户名: admin")
            print(f"   密码: {new_password}")
            
            # 验证新密码
            if verify_password(new_password, admin_user.password_hash):
                print("✅ 密码验证成功")
                return True
            else:
                print("❌ 密码验证失败")
                return False
                
        except Exception as e:
            print(f"❌ 修复失败: {e}")
            db.rollback()
            return False
        finally:
            db.close()
    
    if __name__ == "__main__":
        print("🛠️  UAV考试系统 - Admin密码修复工具")
        print("=" * 50)
        
        success = fix_admin_password()
        
        if success:
            print("\n🎉 修复完成！现在可以使用以下凭据登录:")
            print("   用户名: admin")
            print("   密码: admin123")
        else:
            print("\n❌ 修复失败，请检查数据库连接和配置")

except ImportError as e:
    print(f"❌ 导入模块失败: {e}")
    print("请确保在正确的目录下运行此脚本")
except Exception as e:
    print(f"❌ 执行失败: {e}")