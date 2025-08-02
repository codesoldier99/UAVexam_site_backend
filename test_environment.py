#!/usr/bin/env python3
"""
测试环境验证脚本
检查测试环境是否正确配置
"""

import sys
import subprocess
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    print("🐍 检查Python版本...")
    version = sys.version_info
    print(f"   当前版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("   ✅ Python版本符合要求")
        return True
    else:
        print("   ❌ Python版本过低，需要3.8+")
        return False

def check_dependencies():
    """检查依赖包"""
    print("\n📦 检查依赖包...")
    
    required_packages = [
        "fastapi",
        "pytest", 
        "pytest_cov",  # 修正包名
        "httpx",
        "sqlalchemy",
        "pandas"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n   需要安装的包: {', '.join(missing_packages)}")
        print("   运行: pip install -r requirements.txt")
        return False
    else:
        print("   ✅ 所有依赖包已安装")
        return True

def check_project_structure():
    """检查项目结构"""
    print("\n📁 检查项目结构...")
    
    project_root = Path(__file__).parent
    required_dirs = [
        "src",
        "src/tests",
        "src/models",
        "src/routers",
        "src/services"
    ]
    
    missing_dirs = []
    
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if full_path.exists():
            print(f"   ✅ {dir_path}")
        else:
            print(f"   ❌ {dir_path} - 不存在")
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"\n   缺少的目录: {', '.join(missing_dirs)}")
        return False
    else:
        print("   ✅ 项目结构完整")
        return True

def check_test_files():
    """检查测试文件"""
    print("\n🧪 检查测试文件...")
    
    project_root = Path(__file__).parent
    tests_dir = project_root / "src" / "tests"
    
    if not tests_dir.exists():
        print("   ❌ 测试目录不存在")
        return False
    
    test_files = list(tests_dir.glob("test_*.py"))
    
    if not test_files:
        print("   ❌ 没有找到测试文件")
        return False
    
    print(f"   ✅ 找到 {len(test_files)} 个测试文件:")
    for test_file in test_files:
        print(f"      - {test_file.name}")
    
    return True

def check_database_config():
    """检查数据库配置"""
    print("\n🗄️ 检查数据库配置...")
    
    try:
        # 检查数据库会话配置
        from src.db.session import SessionLocal
        print("   ✅ 数据库会话配置导入成功")
        
        # 检查是否有必要的模型
        from src.models.user import User
        from src.models.candidate import Candidate
        from src.models.schedule import Schedule
        from src.models.exam_product import ExamProduct
        
        print("   ✅ 核心模型导入成功")
        return True
        
    except ImportError as e:
        print(f"   ❌ 数据库配置错误: {e}")
        return False

def run_simple_test():
    """运行简单测试"""
    print("\n🚀 运行简单测试...")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "src/tests/test_main.py",
            "-v",
            "--tb=no"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("   ✅ 简单测试通过")
            return True
        else:
            print("   ❌ 简单测试失败")
            print(f"   错误信息: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("   ❌ 测试超时")
        return False
    except Exception as e:
        print(f"   ❌ 运行测试时出错: {e}")
        return False

def main():
    """主函数"""
    print("🔍 测试环境验证")
    print("=" * 50)
    
    checks = [
        check_python_version,
        check_dependencies,
        check_project_structure,
        check_test_files,
        check_database_config,
        run_simple_test
    ]
    
    results = []
    for check in checks:
        results.append(check())
    
    print("\n" + "=" * 50)
    print("📊 验证结果总结")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print("🎉 所有检查都通过！测试环境已准备就绪。")
        print("\n📋 下一步:")
        print("   1. 运行完整测试: python run_tests.py")
        print("   2. 运行特定测试: python run_tests.py run test_auth.py")
        print("   3. 查看测试列表: python run_tests.py list")
    else:
        print(f"⚠️  {passed}/{total} 项检查通过")
        print("\n🔧 请修复上述问题后重新运行验证")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 