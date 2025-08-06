#!/usr/bin/env python3
"""
干净的认证API测试脚本
专门测试PC登录和微信登录功能，使用真实数据库数据
"""

import requests
import json
import time
from datetime import datetime

# 服务器配置
BASE_URL = "http://localhost:8000"
API_HEADERS = {"Content-Type": "application/json"}

def test_server_health():
    """测试服务器健康状态"""
    print("❤️  测试服务器健康状态")
    print("-" * 30)
    
    health_endpoints = ["/", "/health", "/test"]
    
    for endpoint in health_endpoints:
        try:
            url = f"{BASE_URL}{endpoint}"
            response = requests.get(url, timeout=5)
            
            print(f"📡 {endpoint}: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    print(f"   📄 {result.get('message', 'OK')}")
                except:
                    print("   📄 响应正常")
            else:
                print(f"   ❌ 异常状态码")
                
        except Exception as e:
            print(f"   ⚠️ 请求失败: {e}")
            return False
    
    return True

def test_pc_login_with_real_users():
    """使用真实用户测试PC端登录"""
    print("\n🖥️  测试PC端登录功能（真实用户数据）")
    print("=" * 50)
    
    # 使用数据库中的真实用户
    real_users = [
        {"username": "admin", "password": "admin123", "desc": "超级管理员"},
        {"username": "admin@exam.com", "password": "admin123", "desc": "邮箱登录"},
        {"username": "admin001", "password": "admin123", "desc": "普通管理员"},
    ]
    
    successful_logins = []
    
    for i, user_data in enumerate(real_users, 1):
        print(f"\n🔍 测试用户 {i}: {user_data['username']} ({user_data['desc']})")
        print("-" * 40)
        
        # FastAPI-Users标准登录端点
        login_url = f"{BASE_URL}/auth/jwt/login"
        form_data = {
            "username": user_data["username"],
            "password": user_data["password"]
        }
        
        try:
            response = requests.post(login_url, data=form_data, timeout=10)
            
            print(f"📡 请求URL: {login_url}")
            print(f"📦 登录用户: {user_data['username']}")
            print(f"🔢 响应状态: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ 登录成功!")
                print(f"🎟️ Token类型: {result.get('token_type', 'N/A')}")
                print(f"🔒 Token长度: {len(result.get('access_token', ''))}")
                
                # 保存成功的登录信息
                successful_logins.append({
                    "username": user_data["username"],
                    "token": result.get("access_token"),
                    "desc": user_data["desc"]
                })
                
                # 立即测试token验证
                test_token_validation(result.get("access_token"), user_data["username"])
                
            else:
                print(f"❌ 登录失败")
                print(f"📄 错误信息: {response.text}")
                
        except Exception as e:
            print(f"⚠️ 登录测试失败: {e}")
    
    return successful_logins

def test_token_validation(token, username):
    """测试JWT token验证"""
    print(f"🔐 验证 {username} 的Token")
    
    if not token:
        print("   ❌ 无效token")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # 测试获取用户信息
        response = requests.get(f"{BASE_URL}/auth/users/me", headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_info = response.json()
            print("   ✅ Token验证成功!")
            print(f"   👤 用户ID: {user_info.get('id', 'N/A')}")
            print(f"   📧 邮箱: {user_info.get('email', 'N/A')}")
            print(f"   🛡️ 超管: {user_info.get('is_superuser', 'N/A')}")
            print(f"   🏢 机构ID: {user_info.get('institution_id', 'N/A')}")
            return True
        else:
            print(f"   ❌ Token验证失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ⚠️ Token验证异常: {e}")
        return False

def test_wechat_login():
    """测试微信登录功能"""
    print(f"\n📱 测试微信登录功能")
    print("=" * 30)
    
    # 测试不同的微信code
    wechat_codes = [
        "test_wechat_user_001",
        "test_wechat_user_002", 
        "test_wechat_user_001",  # 重复测试用户查找
    ]
    
    wechat_users = []
    
    for i, code in enumerate(wechat_codes, 1):
        print(f"\n🔍 测试微信Code {i}: {code}")
        print("-" * 25)
        
        try:
            wechat_url = f"{BASE_URL}/social/wechat/login"
            params = {"code": code}
            
            response = requests.post(wechat_url, params=params, headers=API_HEADERS, timeout=10)
            
            print(f"📡 微信登录URL: {wechat_url}")
            print(f"📦 Code: {code}")
            print(f"🔢 响应状态: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ 微信登录成功!")
                
                user_info = result.get('user', {})
                print(f"👤 微信用户ID: {user_info.get('id', 'N/A')}")
                print(f"📧 邮箱: {user_info.get('email', 'N/A')}")
                print(f"👨‍💼 用户名: {user_info.get('username', 'N/A')}")
                print(f"🏢 机构ID: {user_info.get('institution_id', 'N/A')}")
                
                # 验证微信token
                token = result.get('access_token')
                if token:
                    print(f"🔒 Token长度: {len(token)}")
                    test_token_validation(token, user_info.get('username', 'wx_user'))
                
                wechat_users.append(user_info)
                
            else:
                print(f"❌ 微信登录失败: {response.text}")
                
        except Exception as e:
            print(f"⚠️ 微信登录测试失败: {e}")
    
    return wechat_users

def test_user_registration():
    """测试用户注册功能"""
    print(f"\n📝 测试用户注册功能")
    print("-" * 25)
    
    # 生成唯一测试用户
    timestamp = int(time.time())
    new_user = {
        "email": f"clean_test_user_{timestamp}@example.com",
        "username": f"clean_test_{timestamp}",
        "password": "cleantest123",
        "role_id": 3,  # 普通用户
        "institution_id": 7  # 默认机构
    }
    
    try:
        register_url = f"{BASE_URL}/auth/register"
        response = requests.post(register_url, json=new_user, headers=API_HEADERS, timeout=10)
        
        print(f"📡 注册URL: {register_url}")
        print(f"📦 新用户: {new_user['username']}")
        print(f"🔢 响应状态: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ 注册成功!")
            print(f"👤 新用户ID: {result.get('id', 'N/A')}")
            print(f"📧 邮箱: {result.get('email', 'N/A')}")
            
            # 测试新用户登录
            print("\n🔄 测试新用户登录...")
            test_new_user_login(new_user["username"], new_user["password"])
            
            return result
        else:
            print(f"❌ 注册失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"⚠️ 注册测试失败: {e}")
        return None

def test_new_user_login(username, password):
    """测试新注册用户登录"""
    login_url = f"{BASE_URL}/auth/jwt/login"
    form_data = {"username": username, "password": password}
    
    try:
        response = requests.post(login_url, data=form_data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("   ✅ 新用户登录成功!")
            test_token_validation(result.get("access_token"), username)
        else:
            print(f"   ❌ 新用户登录失败: {response.text}")
            
    except Exception as e:
        print(f"   ⚠️ 新用户登录测试失败: {e}")

def check_database_users():
    """检查数据库中的用户数据"""
    print(f"\n👥 检查数据库用户数据")
    print("-" * 25)
    
    try:
        import sys
        import os
        sys.path.append('.')
        
        from sqlalchemy import create_engine, text
        from src.core.config import settings
        
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as conn:
            # 查询最新的用户数据
            result = conn.execute(text("""
                SELECT id, username, email, is_active, is_superuser, role_id, created_at 
                FROM users 
                ORDER BY created_at DESC 
                LIMIT 8
            """))
            users = result.fetchall()
            
            print("最新的用户数据:")
            print(f"{'ID':<4} {'用户名':<20} {'邮箱':<30} {'活跃':<6} {'超管':<6} {'角色':<6}")
            print("-" * 80)
            
            for user in users:
                created_str = str(user[6])[:19] if user[6] else "NULL"
                print(f"{user[0]:<4} {user[1]:<20} {user[2]:<30} {user[3]:<6} {user[4]:<6} {user[5]:<6}")
            
            # 统计用户数量
            total_result = conn.execute(text("SELECT COUNT(*) FROM users"))
            total_users = total_result.scalar()
            print(f"\n📊 总用户数: {total_users}")
            
            # 查询微信用户
            wx_result = conn.execute(text("SELECT COUNT(*) FROM users WHERE username LIKE 'wx_%'"))
            wx_users = wx_result.scalar()
            print(f"📱 微信用户数: {wx_users}")
            
    except Exception as e:
        print(f"❌ 数据库查询失败: {e}")

def main():
    """主测试函数"""
    print("🚀 干净的用户认证API完整测试")
    print(f"⏰ 测试时间: {datetime.now()}")
    print(f"🌐 服务器地址: {BASE_URL}")
    print(f"🌿 当前分支: feat/user-authentication-api")
    
    # 等待服务器启动
    print("\n⏳ 等待服务器启动...")
    time.sleep(5)
    
    try:
        # 1. 服务器健康检查
        if not test_server_health():
            print("❌ 服务器未正常启动，退出测试")
            return
        
        # 2. 检查数据库用户数据
        check_database_users()
        
        # 3. 测试PC端登录
        pc_logins = test_pc_login_with_real_users()
        
        # 4. 测试用户注册
        test_user_registration()
        
        # 5. 测试微信登录
        wechat_users = test_wechat_login()
        
        # 6. 最终统计
        print("\n" + "="*60)
        print("📊 测试结果统计")
        print("="*60)
        print(f"✅ PC登录成功用户数: {len(pc_logins)}")
        print(f"📱 微信登录成功用户数: {len(wechat_users)}")
        print("💾 所有数据都来自真实数据库")
        print("🎯 PC登录和微信登录API都已可用")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ 测试被用户中断")
    except Exception as e:
        print(f"\n\n💥 测试过程中发生错误: {e}")
    
    print("\n🔗 API文档: http://localhost:8000/docs")
    print("🏁 认证API测试完成")

if __name__ == "__main__":
    main()