"""
测试不同的登录组合
"""

import requests
import json

# 配置
BASE_URL = "http://localhost:8000"

# 可能的密码组合
PASSWORD_COMBINATIONS = [
    {"username": "admin", "password": "admin123"},
    {"username": "admin", "password": "admin"},
    {"username": "admin", "password": "123456"},
    {"username": "admin", "password": "password"},
    {"username": "admin", "password": "Admin123"},
    {"username": "admin", "password": "admin@123"},
]

def test_login_combinations():
    """测试不同的登录组合"""
    print("🔐 测试admin用户登录组合")
    print("=" * 50)
    
    for i, combo in enumerate(PASSWORD_COMBINATIONS, 1):
        print(f"\n🧪 测试组合 {i}: {combo['username']} / {combo['password']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/v1/auth/login",
                json=combo,
                timeout=10
            )
            
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("   ✅ 登录成功!")
                print(f"   Token: {result.get('access_token', 'N/A')[:50]}...")
                print(f"   用户信息: {result.get('user_info', {})}")
                return combo
            else:
                try:
                    error = response.json()
                    print(f"   ❌ 登录失败: {error.get('detail', 'Unknown error')}")
                except:
                    print(f"   ❌ 登录失败: HTTP {response.status_code}")
                    
        except requests.exceptions.RequestException as e:
            print(f"   ❌ 请求异常: {e}")
        except Exception as e:
            print(f"   ❌ 其他异常: {e}")
    
    print("\n❌ 所有密码组合都失败了")
    return None

def test_other_users():
    """测试其他用户"""
    print("\n🔐 测试其他用户登录")
    print("=" * 50)
    
    other_users = [
        {"username": "beijing_admin", "password": "123456"},
        {"username": "shanghai_admin", "password": "123456"},
        {"username": "candidate_011234", "password": "011234"},
    ]
    
    for user in other_users:
        print(f"\n🧪 测试用户: {user['username']} / {user['password']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/v1/auth/login",
                json=user,
                timeout=10
            )
            
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("   ✅ 登录成功!")
                print(f"   用户信息: {result.get('user_info', {})}")
                return user
            else:
                try:
                    error = response.json()
                    print(f"   ❌ 登录失败: {error.get('detail', 'Unknown error')}")
                except:
                    print(f"   ❌ 登录失败: HTTP {response.status_code}")
                    
        except Exception as e:
            print(f"   ❌ 异常: {e}")
    
    return None

def main():
    """主函数"""
    print("🧪 UAV考试系统登录测试工具")
    print("=" * 50)
    
    # 首先测试服务器连接
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ 后端服务连接正常")
        else:
            print(f"⚠️  后端服务响应异常: {response.status_code}")
    except Exception as e:
        print(f"❌ 无法连接后端服务: {e}")
        print("请确保后端服务正在运行在 http://localhost:8000")
        return
    
    # 测试admin用户
    successful_combo = test_login_combinations()
    
    if successful_combo:
        print(f"\n🎉 找到有效的admin登录组合:")
        print(f"   用户名: {successful_combo['username']}")
        print(f"   密码: {successful_combo['password']}")
    else:
        # 测试其他用户
        other_user = test_other_users()
        
        if other_user:
            print(f"\n💡 建议使用其他有效用户进行测试:")
            print(f"   用户名: {other_user['username']}")
            print(f"   密码: {other_user['password']}")
        else:
            print("\n❌ 所有用户登录都失败了")
            print("\n💡 可能的解决方案:")
            print("1. 检查数据库是否正确初始化")
            print("2. 检查密码哈希算法是否一致")
            print("3. 重新运行数据初始化脚本")
            print("4. 检查后端日志获取更多信息")

if __name__ == "__main__":
    main()