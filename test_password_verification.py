"""
密码验证测试脚本
用于检查数据库中的密码哈希是否正确
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.utils.security import verify_password, get_password_hash
from backend.app.config.database import get_db
from backend.app.models.user import User
from sqlalchemy.orm import Session

def test_password_verification():
    """测试密码验证"""
    print("🔐 密码验证测试")
    print("=" * 50)
    
    # 获取数据库连接
    db = next(get_db())
    
    try:
        # 查询admin用户
        admin_user = db.query(User).filter(User.username == "admin").first()
        
        if not admin_user:
            print("❌ 未找到admin用户")
            return
        
        print(f"✅ 找到admin用户:")
        print(f"   ID: {admin_user.id}")
        print(f"   用户名: {admin_user.username}")
        print(f"   真实姓名: {admin_user.real_name}")
        print(f"   角色: {admin_user.role}")
        print(f"   是否激活: {admin_user.is_active}")
        print(f"   密码哈希: {admin_user.password_hash[:50]}...")
        
        # 测试不同的密码
        test_passwords = ["admin123", "admin", "123456", "password"]
        
        print(f"\n🧪 测试密码验证:")
        for password in test_passwords:
            is_valid = verify_password(password, admin_user.password_hash)
            status = "✅" if is_valid else "❌"
            print(f"   {status} 密码 '{password}': {'有效' if is_valid else '无效'}")
            
            if is_valid:
                print(f"🎉 找到正确密码: {password}")
                break
        
        # 生成新的密码哈希进行对比
        print(f"\n🔧 生成新的密码哈希:")
        new_hash = get_password_hash("admin123")
        print(f"   新哈希: {new_hash[:50]}...")
        print(f"   验证新哈希: {'✅ 有效' if verify_password('admin123', new_hash) else '❌ 无效'}")
        
        # 检查哈希格式
        print(f"\n📋 哈希格式分析:")
        print(f"   当前哈希长度: {len(admin_user.password_hash)}")
        print(f"   新哈希长度: {len(new_hash)}")
        print(f"   当前哈希前缀: {admin_user.password_hash[:10]}")
        print(f"   新哈希前缀: {new_hash[:10]}")
        
        # 判断哈希类型
        if admin_user.password_hash.startswith('$2b$'):
            print("   当前哈希类型: bcrypt")
        elif admin_user.password_hash.startswith('$2a$'):
            print("   当前哈希类型: bcrypt (旧版)")
        else:
            print("   当前哈希类型: 未知")
            
        if new_hash.startswith('$2b$'):
            print("   新哈希类型: bcrypt")
        
    except Exception as e:
        print(f"❌ 测试异常: {e}")
    finally:
        db.close()

def fix_admin_password():
    """修复admin密码"""
    print("\n🔧 修复admin密码")
    print("=" * 50)
    
    db = next(get_db())
    
    try:
        admin_user = db.query(User).filter(User.username == "admin").first()
        
        if not admin_user:
            print("❌ 未找到admin用户")
            return
        
        # 生成新的密码哈希
        new_password_hash = get_password_hash("admin123")
        
        # 更新密码
        admin_user.password_hash = new_password_hash
        db.commit()
        
        print("✅ admin密码已更新")
        print(f"   新密码: admin123")
        print(f"   新哈希: {new_password_hash[:50]}...")
        
        # 验证更新后的密码
        is_valid = verify_password("admin123", admin_user.password_hash)
        print(f"   验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        
    except Exception as e:
        print(f"❌ 修复失败: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """主函数"""
    print("🧪 UAV考试系统密码验证工具")
    print("=" * 50)
    
    # 先测试密码验证
    test_password_verification()
    
    # 询问是否修复密码
    print("\n" + "=" * 50)
    fix_choice = input("是否修复admin密码? (y/n): ").strip().lower()
    
    if fix_choice in ['y', 'yes', '是']:
        fix_admin_password()
        
        # 再次测试
        print("\n" + "=" * 50)
        print("🔄 重新测试密码验证:")
        test_password_verification()
    
    print("\n✅ 测试完成")

if __name__ == "__main__":
    main()