#!/usr/bin/env python3
"""
API测试运行脚本
用于运行所有核心API的自动化测试用例
"""

import subprocess
import sys
import os
from pathlib import Path

def run_tests():
    """运行所有测试"""
    print("🚀 开始运行API测试...")
    print("=" * 50)
    
    # 获取项目根目录
    project_root = Path(__file__).parent
    tests_dir = project_root / "src" / "tests"
    
    # 检查测试目录是否存在
    if not tests_dir.exists():
        print(f"❌ 测试目录不存在: {tests_dir}")
        return False
    
    # 运行所有测试
    try:
        # 切换到项目根目录
        os.chdir(project_root)
        
        # 运行pytest
        cmd = [
            sys.executable, "-m", "pytest",
            str(tests_dir),
            "-v",  # 详细输出
            "--tb=short",  # 简短的错误回溯
            "--maxfail=5",  # 最多失败5个测试后停止
            "--durations=10",  # 显示最慢的10个测试
            "--cov=src",  # 代码覆盖率
            "--cov-report=term-missing",  # 显示未覆盖的代码行
            "--cov-report=html:htmlcov",  # 生成HTML覆盖率报告
        ]
        
        print(f"📋 运行命令: {' '.join(cmd)}")
        print("-" * 50)
        
        result = subprocess.run(cmd, capture_output=False, text=True)
        
        if result.returncode == 0:
            print("✅ 所有测试通过!")
        else:
            print("❌ 部分测试失败")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 运行测试时出错: {e}")
        return False

def run_specific_test(test_file):
    """运行特定的测试文件"""
    print(f"🚀 运行特定测试: {test_file}")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    test_path = project_root / "src" / "tests" / test_file
    
    if not test_path.exists():
        print(f"❌ 测试文件不存在: {test_path}")
        return False
    
    try:
        os.chdir(project_root)
        
        cmd = [
            sys.executable, "-m", "pytest",
            str(test_path),
            "-v",
            "--tb=short",
        ]
        
        print(f"📋 运行命令: {' '.join(cmd)}")
        print("-" * 50)
        
        result = subprocess.run(cmd, capture_output=False, text=True)
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 运行测试时出错: {e}")
        return False

def list_tests():
    """列出所有可用的测试文件"""
    print("📋 可用的测试文件:")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    tests_dir = project_root / "src" / "tests"
    
    if not tests_dir.exists():
        print("❌ 测试目录不存在")
        return
    
    test_files = list(tests_dir.glob("test_*.py"))
    
    if not test_files:
        print("❌ 没有找到测试文件")
        return
    
    for i, test_file in enumerate(test_files, 1):
        print(f"{i}. {test_file.name}")
    
    print(f"\n总计: {len(test_files)} 个测试文件")

def main():
    """主函数"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "list":
            list_tests()
        elif command == "run":
            if len(sys.argv) > 2:
                test_file = sys.argv[2]
                run_specific_test(test_file)
            else:
                run_tests()
        else:
            print("❌ 未知命令")
            print_usage()
    else:
        run_tests()

def print_usage():
    """打印使用说明"""
    print("""
使用方法:
  python run_tests.py                    # 运行所有测试
  python run_tests.py run               # 运行所有测试
  python run_tests.py run test_auth.py  # 运行特定测试文件
  python run_tests.py list              # 列出所有测试文件
    """)

if __name__ == "__main__":
    main() 