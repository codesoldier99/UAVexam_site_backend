import requests
import json

def test_optimized_interfaces():
    """测试优化后的接口"""
    base_url = "http://127.0.0.1:8000/api/v1/pc"
    
    # 登录获取token
    login_data = {"username": "beijing_admin", "password": "123456"}
    response = requests.post(f"{base_url}/auth/login", json=login_data)
    
    if response.status_code == 200:
        data = response.json()
        token = data.get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        print("🔧 测试优化后的接口...")
        
        # 测试报名统计接口
        print("\n1. 测试报名统计接口:")
        response = requests.get(f"{base_url}/registrations/statistics", headers=headers)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ 报名统计接口优化成功!")
        elif response.status_code == 422:
            print("   ⚠️  仍有422错误，需要进一步优化")
        
        # 测试批量确认接口
        print("\n2. 测试批量确认接口:")
        batch_data = [1, 2, 3]
        response = requests.post(f"{base_url}/registrations/batch-confirm", json=batch_data, headers=headers)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 403:
            print("   ✅ 权限检查正常，返回403而不是500!")
        elif response.status_code == 500:
            print("   ❌ 仍有500错误，需要进一步优化")
        
        print("\n🎯 优化测试完成!")
    else:
        print("❌ 登录失败")

if __name__ == "__main__":
    test_optimized_interfaces()