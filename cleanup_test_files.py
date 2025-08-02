#!/usr/bin/env python3
"""
测试文件清理脚本
帮助整理新旧测试文件，避免冲突
"""

import os
import shutil
from pathlib import Path

def analyze_test_files():
    """分析测试文件结构"""
    print("🔍 分析测试文件结构...")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    
    # 根目录的测试文件
    root_test_files = []
    for file in project_root.glob("test_*.py"):
        if file.name != "test_environment.py":  # 保留环境验证脚本
            root_test_files.append(file)
    
    # src/tests目录的测试文件
    src_tests_dir = project_root / "src" / "tests"
    src_test_files = []
    if src_tests_dir.exists():
        for file in src_tests_dir.glob("test_*.py"):
            src_test_files.append(file)
    
    print(f"📁 根目录测试文件 ({len(root_test_files)} 个):")
    for file in root_test_files:
        print(f"   - {file.name}")
    
    print(f"\n📁 src/tests目录测试文件 ({len(src_test_files)} 个):")
    for file in src_test_files:
        print(f"   - {file.name}")
    
    return root_test_files, src_test_files

def categorize_files(root_files, src_files):
    """分类文件"""
    print("\n📋 文件分类:")
    print("=" * 50)
    
    # 手动测试脚本 (根目录)
    manual_tests = []
    # 自动化pytest测试 (src/tests)
    auto_tests = []
    # 可能冲突的文件
    conflicts = []
    
    for file in root_files:
        if file.name.startswith("test_"):
            manual_tests.append(file)
    
    for file in src_files:
        if file.name.startswith("test_"):
            auto_tests.append(file)
    
    # 检查冲突
    manual_names = [f.name for f in manual_tests]
    auto_names = [f.name for f in auto_tests]
    
    for manual_file in manual_tests:
        for auto_file in auto_tests:
            if manual_file.name == auto_file.name:
                conflicts.append((manual_file, auto_file))
    
    print("🔧 手动测试脚本 (根目录):")
    for file in manual_tests:
        print(f"   ✅ {file.name}")
    
    print("\n🤖 自动化pytest测试 (src/tests):")
    for file in auto_tests:
        print(f"   ✅ {file.name}")
    
    if conflicts:
        print("\n⚠️  发现冲突文件:")
        for manual, auto in conflicts:
            print(f"   ❌ {manual.name} (根目录) vs {auto.name} (src/tests)")
    
    return manual_tests, auto_tests, conflicts

def suggest_cleanup(manual_tests, auto_tests, conflicts):
    """建议清理方案"""
    print("\n💡 清理建议:")
    print("=" * 50)
    
    if conflicts:
        print("🔧 需要处理的冲突:")
        for manual, auto in conflicts:
            print(f"   - 删除根目录的 {manual.name}，保留 src/tests 的 {auto.name}")
    
    print("\n📁 建议的目录结构:")
    print("   exam_site_backend/")
    print("   ├── src/tests/           # 自动化pytest测试")
    print("   │   ├── test_auth.py")
    print("   │   ├── test_candidates_api.py")
    print("   │   ├── test_schedules_api.py")
    print("   │   └── test_exam_products_api.py")
    print("   ├── manual_tests/        # 手动测试脚本 (可选)")
    print("   └── test_environment.py  # 环境验证脚本")
    
    return conflicts

def create_manual_tests_backup(manual_tests):
    """创建手动测试脚本备份"""
    backup_dir = Path(__file__).parent / "manual_tests_backup"
    
    if manual_tests:
        print(f"\n📦 创建手动测试脚本备份到: {backup_dir}")
        
        if not backup_dir.exists():
            backup_dir.mkdir()
        
        for file in manual_tests:
            if file.name != "test_environment.py":
                backup_path = backup_dir / file.name
                shutil.copy2(file, backup_path)
                print(f"   ✅ 备份: {file.name}")
        
        return backup_dir
    return None

def cleanup_conflicts(conflicts):
    """清理冲突文件"""
    if not conflicts:
        return
    
    print(f"\n🗑️  清理冲突文件...")
    
    for manual, auto in conflicts:
        try:
            os.remove(manual)
            print(f"   ✅ 删除: {manual.name}")
        except Exception as e:
            print(f"   ❌ 删除失败 {manual.name}: {e}")

def main():
    """主函数"""
    print("🧹 测试文件清理工具")
    print("=" * 50)
    
    # 分析文件
    root_files, src_files = analyze_test_files()
    manual_tests, auto_tests, conflicts = categorize_files(root_files, src_files)
    
    # 建议清理
    suggest_cleanup(manual_tests, auto_tests, conflicts)
    
    # 询问用户
    print("\n❓ 是否要执行清理操作？")
    print("   1. 备份手动测试脚本")
    print("   2. 删除冲突文件")
    print("   3. 退出")
    
    choice = input("\n请选择 (1/2/3): ").strip()
    
    if choice == "1":
        backup_dir = create_manual_tests_backup(manual_tests)
        if backup_dir:
            print(f"\n✅ 备份完成！手动测试脚本已保存到: {backup_dir}")
    
    elif choice == "2":
        cleanup_conflicts(conflicts)
        print("\n✅ 冲突文件清理完成！")
    
    elif choice == "3":
        print("\n👋 退出清理工具")
        return
    
    else:
        print("\n❌ 无效选择")
        return
    
    print("\n📋 清理后的建议:")
    print("   1. 使用 pytest 运行自动化测试: pytest src/tests/ -v")
    print("   2. 使用测试运行脚本: python run_tests.py")
    print("   3. 验证测试环境: python test_environment.py")

if __name__ == "__main__":
    main() 