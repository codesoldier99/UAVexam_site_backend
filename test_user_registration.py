import requests
import json

def test_user_registration():
    """测试用户注册功能"""
    print("=" * 50)
    print("测试用户注册功能")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # 测试数据
    test_user = {
        "username": "testuser3",
        "email": "test3@example.com",
        "password": "testpassword123",
        "role_id": 1,
        "institution_id": 1
    }
    
    try:
        # 测试用户注册
        print(f"\n测试用户注册...")
        response = requests.post(
            f"{base_url}/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        if response.status_code == 200:
            print("✅ 用户注册成功")
        else:
            print("❌ 用户注册失败")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def test_user_login():
    """测试用户登录功能"""
    print("\n" + "=" * 50)
    print("测试用户登录功能")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # 测试数据
    login_data = {
        "email": "test3@example.com",
        "password": "testpassword123"
    }
    
    try:
        # 测试用户登录
        print(f"\n测试用户登录...")
        response = requests.post(
            f"{base_url}/auth/jwt/login",
            data={
                "username": "test3@example.com",
                "password": login_data["password"]
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        if response.status_code == 200:
            print("✅ 用户登录成功")
        else:
            print("❌ 用户登录失败")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_user_registration()
    test_user_login() 