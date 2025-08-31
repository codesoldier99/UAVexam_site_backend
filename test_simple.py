import requests
import json

# 配置
BASE_URL = "http://127.0.0.1:8000"
API_V1 = f"{BASE_URL}/api/v1"

def test_wechat_login():
    """测试微信登录功能"""
    print("=== 测试微信登录功能 ===")
    
    test_id_card = "110101199001011234"  # 使用你数据库中的真实身份证号
    
    response = requests.post(
        f"{API_V1}/wechat/login",
        json={
            "id_card": test_id_card,
            "openid": "test_openid_123"
        }
    )
    
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("登录成功!")
        print(f"访问令牌: {data.get('access_token', '')[:50]}...")
        print(f"用户信息: {data.get('user_info', {})}")
        print(f"当前考试: {data.get('current_exam', {})}")
        print(f"即将到来的考试数量: {len(data.get('upcoming_exams', []))}")
        return data.get('access_token')
    else:
        print(f"登录失败: {response.text}")
        return None

def test_dashboard():
    """测试看板数据"""
    print("\n=== 测试看板数据 ===")
    
    response = requests.get(f"{API_V1}/wechat/dashboard")
    
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("查询成功!")
        print(f"统计数据: {data.get('statistics', {})}")
        print(f"考场数量: {len(data.get('venues', []))}")
        print(f"公告数量: {len(data.get('announcements', []))}")
    else:
        print(f"查询失败: {response.text}")

def test_candidate_info():
    """测试考生信息查询"""
    print("\n=== 测试考生信息查询 ===")
    
    test_id_card = "110101199001011234"
    
    response = requests.get(
        f"{API_V1}/wechat/candidate/info-by-idcard?id_card={test_id_card}"
    )
    
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("查询成功!")
        print(f"考生信息: {json.dumps(data, indent=2, ensure_ascii=False)}")
    else:
        print(f"查询失败: {response.text}")

def main():
    """主测试函数"""
    print("开始测试微信API功能...")
    print(f"后端地址: {BASE_URL}")
    
    try:
        # 测试后端连接
        health_response = requests.get(f"{BASE_URL}/health", timeout=5)
        if health_response.status_code == 200:
            print("✓ 后端连接正常")
        else:
            print("✗ 后端连接异常")
            return
    except requests.exceptions.RequestException as e:
        print(f"✗ 无法连接到后端: {e}")
        return
    
    # 执行测试
    test_candidate_info()
    token = test_wechat_login()
    test_dashboard()
    
    print("\n=== 测试完成 ===")
    
    if token:
        print(f"✓ 获得访问令牌，可以进行需要认证的API测试")
    else:
        print("✗ 未能获得访问令牌")

if __name__ == "__main__":
    main()