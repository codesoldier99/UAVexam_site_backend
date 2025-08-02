#!/usr/bin/env python3
"""
项目状态检查脚本
验证所有配置是否符合团队约定
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """检查文件是否存在"""
    if Path(file_path).exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} (缺失)")
        return False

def check_config_value(file_path, key, expected_value, description):
    """检查配置文件中的值"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if expected_value in content:
                print(f"✅ {description}: {key} = {expected_value}")
                return True
            else:
                print(f"❌ {description}: {key} 不匹配期望值 {expected_value}")
                return False
    except Exception as e:
        print(f"❌ 无法读取文件 {file_path}: {e}")
        return False

def main():
    """主检查函数"""
    print("🔍 检查 Exam Site Backend 项目配置")
    print("=" * 50)
    
    checks_passed = 0
    total_checks = 0
    
    # 检查项目名称
    total_checks += 1
    if check_config_value("src/main.py", "Exam Site Backend", "Exam Site Backend", "项目名称"):
        checks_passed += 1
    
    # 检查数据库配置
    total_checks += 1
    if check_config_value("docker-compose.yml", "3307", "3307", "数据库端口"):
        checks_passed += 1
    
    # 检查ORM配置
    total_checks += 1
    if check_config_value("requirements.txt", "sqlalchemy", "sqlalchemy", "SQLAlchemy ORM"):
        checks_passed += 1
    
    # 检查MySQL配置
    total_checks += 1
    if check_config_value("requirements.txt", "pymysql", "pymysql", "MySQL驱动"):
        checks_passed += 1
    
    # 检查Alembic配置
    total_checks += 1
    if check_file_exists("alembic.ini", "Alembic配置文件"):
        checks_passed += 1
    
    # 检查Docker支持
    total_checks += 1
    if check_file_exists("docker-compose.yml", "Docker Compose配置"):
        checks_passed += 1
    
    # 检查FastAPI-Users认证
    total_checks += 1
    if check_config_value("requirements.txt", "fastapi-users", "fastapi-users", "FastAPI-Users认证"):
        checks_passed += 1
    
    # 检查社交认证
    total_checks += 1
    if check_file_exists("src/auth/social.py", "社交认证模块"):
        checks_passed += 1
    
    # 检查角色模型
    total_checks += 1
    if check_file_exists("src/models/role.py", "角色模型"):
        checks_passed += 1
    
    # 检查环境变量配置
    total_checks += 1
    if check_file_exists("env.example", "环境变量示例"):
        checks_passed += 1
    
    # 检查启动脚本
    total_checks += 1
    if check_file_exists("start_dev.py", "开发启动脚本"):
        checks_passed += 1
    
    # 检查数据库初始化脚本
    total_checks += 1
    if check_file_exists("init_db.py", "数据库初始化脚本"):
        checks_passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 检查结果: {checks_passed}/{total_checks} 项通过")
    
    if checks_passed == total_checks:
        print("🎉 所有配置都符合团队约定!")
        print("\n📋 项目特性:")
        print("   ✅ 项目名称: exam_site_backend")
        print("   ✅ ORM: SQLAlchemy")
        print("   ✅ 数据库: MySQL")
        print("   ✅ 数据库端口: 3307")
        print("   ✅ 迁移工具: Alembic")
        print("   ✅ Docker支持: 已配置")
        print("   ✅ 认证系统: FastAPI-Users")
        print("   ✅ 社交认证: 已准备（微信登录）")
        print("   ✅ 角色权限: 已配置")
        
        print("\n🚀 启动命令:")
        print("   python start_dev.py")
        
        print("\n📚 文档地址:")
        print("   API文档: http://localhost:8000/docs")
        print("   管理界面: http://localhost:8000/redoc")
        
    else:
        print("⚠️  部分配置需要完善")
        print("请检查上述失败的配置项")

if __name__ == "__main__":
    main() 