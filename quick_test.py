#!/usr/bin/env python3
"""
快速测试脚本 - 检查后端服务状态
"""

try:
    import requests
    
    print("Testing backend connection...")
    
    # Test health endpoint
    try:
        response = requests.get('http://127.0.0.1:8000/api/v1/health', timeout=3)
        print(f"✅ Health check: Status {response.status_code}")
        print(f"   Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend service on port 8000")
        print("💡 Make sure the backend is running:")
        print("   cd backend")
        print("   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test new WeChat API
    try:
        response = requests.get('http://127.0.0.1:8000/api/v1/wechat/candidate/info-by-idcard?id_card=110101199001011234', timeout=3)
        print(f"✅ WeChat API: Status {response.status_code}")
        if response.status_code in [200, 404]:
            print(f"   Response: {response.text[:100]}...")
    except Exception as e:
        print(f"❌ WeChat API Error: {e}")
        
except ImportError:
    print("❌ requests module not found. Please install it:")
    print("   pip install requests")