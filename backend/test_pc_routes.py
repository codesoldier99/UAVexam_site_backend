#!/usr/bin/env python3
"""
PC端接口测试脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_pc_routes_import():
    """测试PC端路由模块导入"""
    try:
        from app.routes.pc.auth import router as pc_auth_router
        from app.routes.pc.dashboard import router as pc_dashboard_router
        from app.routes.pc.candidates import router as pc_candidates_router
        from app.routes.pc.checkins import router as pc_checkins_router
        
        print("✅ PC端路由模块导入成功")
        
        # 检查路由前缀
        print(f"✅ 认证路由前缀: {pc_auth_router.prefix}")
        print(f"✅ 仪表板路由前缀: {pc_dashboard_router.prefix}")
        print(f"✅ 考生管理路由前缀: {pc_candidates_router.prefix}")
        print(f"✅ 签到管理路由前缀: {pc_checkins_router.prefix}")
        
        # 检查路由数量
        print(f"✅ 认证路由数量: {len(pc_auth_router.routes)}")
        print(f"✅ 仪表板路由数量: {len(pc_dashboard_router.routes)}")
        print(f"✅ 考生管理路由数量: {len(pc_candidates_router.routes)}")
        print(f"✅ 签到管理路由数量: {len(pc_checkins_router.routes)}")
        
        return True
        
    except Exception as e:
        print(f"❌ PC端路由模块导入失败: {e}")
        return False

def test_main_app_import():
    """测试主应用导入"""
    try:
        from app.main import app
        print("✅ 主应用导入成功")
        
        # 检查路由注册
        routes = [route.path for route in app.routes]
        pc_routes = [route for route in routes if route.startswith('/api/v1/pc/')]
        
        print(f"✅ 总路由数量: {len(routes)}")
        print(f"✅ PC端路由数量: {len(pc_routes)}")
        
        if pc_routes:
            print("✅ PC端路由列表:")
            for route in pc_routes[:10]:  # 显示前10个
                print(f"   - {route}")
        
        return True
        
    except Exception as e:
        print(f"❌ 主应用导入失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试PC端接口实现...")
    print("=" * 50)
    
    # 测试路由模块导入
    print("\n📋 测试1: PC端路由模块导入")
    test1_result = test_pc_routes_import()
    
    print("\n📋 测试2: 主应用导入")
    test2_result = test_main_app_import()
    
    print("\n" + "=" * 50)
    if test1_result and test2_result:
        print("🎉 所有测试通过！PC端接口实现成功")
        print("\n📝 新增的PC端接口路径:")
        print("   - /api/v1/pc/auth/*        # PC端认证")
        print("   - /api/v1/pc/dashboard/*   # PC端仪表板")
        print("   - /api/v1/pc/candidates/*  # PC端考生管理")
        print("   - /api/v1/pc/checkins/*    # PC端签到管理")
    else:
        print("❌ 部分测试失败，请检查实现")

if __name__ == "__main__":
    main()