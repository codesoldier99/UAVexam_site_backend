import requests
import json

# 配置
BASE_URL = "http://127.0.0.1:8000"
API_V1 = f"{BASE_URL}/api/v1"

def get_auth_token():
    """获取认证token"""
    test_id_card = "110101199001011234"
    
    response = requests.post(
        f"{API_V1}/wechat/login",
        json={
            "id_card": test_id_card,
            "openid": "test_openid_123"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        return data.get('access_token')
    else:
        print(f"获取token失败: {response.text}")
        return None

def test_with_auth():
    """测试需要认证的API"""
    print("=== 获取认证token ===")
    token = get_auth_token()
    
    if not token:
        print("无法获取认证token，跳过认证测试")
        return
    
    print(f"✓ 获得token: {token[:50]}...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 测试考生考试安排
    print("\n=== 测试考生考试安排查询 ===")
    response = requests.get(f"{API_V1}/wechat/candidate/schedule", headers=headers)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"考试安排: {json.dumps(data, indent=2, ensure_ascii=False)}")
    else:
        print(f"查询失败: {response.text}")
    
    # 测试二维码刷新
    print("\n=== 测试二维码刷新 ===")
    response = requests.post(
        f"{API_V1}/wechat/candidate/qrcode/refresh",
        headers=headers,
        json={"candidate_id": 5}
    )
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"新二维码: {data.get('qr_code_data', '')[:100]}...")
    else:
        print(f"刷新失败: {response.text}")
    
    # 测试考场状态
    print("\n=== 测试考场状态查询 ===")
    response = requests.get(f"{API_V1}/wechat/venues/status", headers=headers)
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"考场状态: {json.dumps(data, indent=2, ensure_ascii=False)}")
    else:
        print(f"查询失败: {response.text}")
    
    # 测试签到
    print("\n=== 测试签到功能 ===")
    checkin_data = {
        "schedule_id": 1,
        "examiner_id": 1,
        "venue_id": 1,
        "qr_code_data": "test_qr_data"
    }
    response = requests.post(
        f"{API_V1}/wechat/checkin",
        headers=headers,
        json=checkin_data
    )
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"签到结果: {json.dumps(data, indent=2, ensure_ascii=False)}")
    else:
        print(f"签到失败: {response.text}")

def main():
    """主测试函数"""
    print("开始测试需要认证的API...")
    print(f"后端地址: {BASE_URL}")
    
    test_with_auth()
    
    print("\n=== 认证测试完成 ===")

if __name__ == "__main__":
    main()