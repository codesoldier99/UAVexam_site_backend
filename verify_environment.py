#!/usr/bin/env python3
"""
环境验证脚本
确保团队成员使用相同的Python版本和依赖
"""

import sys
import pkg_resources
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    required_version = (3, 11, 9)
    current_version = sys.version_info[:3]
    
    print(f"当前Python版本: {'.'.join(map(str, current_version))}")
    print(f"要求Python版本: {'.'.join(map(str, required_version))}")
    
    if current_version != required_version:
        print("❌ Python版本不匹配！")
        print("请安装Python 3.11.9")
        return False
    else:
        print("✅ Python版本正确")
        return True

def check_dependencies():
    """检查关键依赖包版本"""
    key_packages = {
        'fastapi': '0.104.1',
        'sqlalchemy': '2.0.23',
        'uvicorn': '0.24.0',
        'pydantic': '2.11.7',
        'redis': '5.0.1'
    }
    
    print("\n检查关键依赖包:")
    all_correct = True
    
    for package, expected_version in key_packages.items():
        try:
            installed_version = pkg_resources.get_distribution(package).version
            if installed_version == expected_version:
                print(f"✅ {package}: {installed_version}")
            else:
                print(f"❌ {package}: 安装版本 {installed_version}, 期望版本 {expected_version}")
                all_correct = False
        except pkg_resources.DistributionNotFound:
            print(f"❌ {package}: 未安装")
            all_correct = False
    
    return all_correct

def check_files():
    """检查必要的配置文件"""
    required_files = [
        '.python-version',
        'backend/requirements.txt',
        'backend/requirements.lock',
        'backend/.env.example',
        'docker-compose.yml'
    ]
    
    print("\n检查配置文件:")
    all_exist = True
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}: 文件不存在")
            all_exist = False
    
    return all_exist

def main():
    """主验证函数"""
    print("🔍 UAV考试系统环境验证")
    print("=" * 50)
    
    python_ok = check_python_version()
    deps_ok = check_dependencies()
    files_ok = check_files()
    
    print("\n" + "=" * 50)
    if python_ok and deps_ok and files_ok:
        print("🎉 环境验证通过！团队环境一致性确认。")
        return 0
    else:
        print("⚠️  环境验证失败！请检查上述问题。")
        print("\n修复建议:")
        if not python_ok:
            print("- 安装Python 3.11.9")
        if not deps_ok:
            print("- 运行: pip install -r backend/requirements.lock")
        if not files_ok:
            print("- 确保从最新的git仓库拉取所有文件")
        return 1

if __name__ == "__main__":
    exit(main())
