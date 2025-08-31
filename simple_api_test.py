"""
简单的API测试脚本 - 用于快速验证后端服务
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """测试健康检查接口"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health")
        print(f"健康检查: {response.status_code}")
        if response.status_code == 200:
            print(f"响应: {response.json()}")
            return True
    except Exception as e:
        print(f"健康检查失败: {e}")
    return False

def test_id_card_lookup():
    """测试身份证查询接口"""
    test_cases = [
        "110101199001011234",  # 有效格式
        "12345",              # 无效格式
    ]
    
    for id_card in test_cases:
        try:
            response = requests.get(f"{BASE_URL}/api/v1/wechat/candidate/info-by-idcard", 
                                  params={"id_card": id_card})
            print(f"\n身份证查询 ({id_card}): {response.status_code}")
            
            if response.status_code in [200, 400, 404]:
                try:
                    data = response.json()
                    print(f"响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
                except:
                    print(f"响应文本: {response.text}")
            else:
                print(f"错误响应: {response.text}")
                
        except Exception as e:
            print(f"请求异常: {e}")

def test_login_and_protected_apis():
    """测试登录和受保护的API"""
    # 先尝试登录
    login_data = {
        "id_card": "110101199001011234",
        "openid": "test_openid_123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/wechat/login", json=login_data)
        print(f"\n登录测试: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print("登录成功，获取到token")
            
            # 测试受保护的API
            headers = {"Authorization": f"Bearer {token}"}
            
            # 测试二维码刷新
            refresh_data = {"reason": "测试刷新"}
            response = requests.post(f"{BASE_URL}/api/v1/wechat/candidate/qrcode/refresh", 
                                   json=refresh_data, headers=headers)
            print(f"二维码刷新: {response.status_code}")
            if response.status_code in [200, 400, 429]:
                try:
                    print(f"响应: {response.json()}")
                except:
                    print(f"响应文本: {response.text}")
            
        else:
            print(f"登录失败: {response.text}")
            
    except Exception as e:
        print(f"登录测试异常: {e}")

if __name__ == "__main__":
    print("🚀 开始简单API测试")
    print("=" * 50)
    
    # 测试健康检查
    if test_health():
        print("\n✅ 后端服务正常运行")
        
        # 测试身份证查询
        test_id_card_lookup()
        
        # 测试登录和受保护API
        test_login_and_protected_apis()
        
    else:
        print("\n❌ 后端服务未运行，请先启动服务")
        print("启动命令: cd backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload")
    
    print("\n" + "=" * 50)
    print("🎉 测试完成")