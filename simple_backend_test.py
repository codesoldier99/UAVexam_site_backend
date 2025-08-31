#!/usr/bin/env python3
"""
简单的后端连接测试脚本
"""

import requests
import socket
import sys

def test_port():
    """测试端口8000是否开放"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex(('127.0.0.1', 8000))
        sock.close()
        return result == 0
    except:
        return False

def test_health():
    """测试健康检查接口"""
    try:
        response = requests.get('http://127.0.0.1:8000/api/v1/health', timeout=5)
        return response.status_code, response.text
    except Exception as e:
        return None, str(e)

def test_docs():
    """测试API文档"""
    try:
        response = requests.get('http://127.0.0.1:8000/docs', timeout=5)
        return response.status_code
    except:
        return None

def main():
    print("🔧 UAV Backend Connection Test")
    print("=" * 40)
    
    # 1. 测试端口
    print("1. Testing port 8000...")
    if test_port():
        print("   ✅ Port 8000 is open")
    else:
        print("   ❌ Port 8000 is not accessible")
        print("   💡 Please start the backend service:")
        print("      cd backend")
        print("      python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload")
        return
    
    # 2. 测试健康检查
    print("\n2. Testing health endpoint...")
    status, content = test_health()
    if status == 200:
        print(f"   ✅ Health check OK: {content}")
    elif status:
        print(f"   ⚠️ Health check returned status {status}")
    else:
        print(f"   ❌ Health check failed: {content}")
    
    # 3. 测试API文档
    print("\n3. Testing API docs...")
    docs_status = test_docs()
    if docs_status == 200:
        print("   ✅ API docs accessible")
    elif docs_status:
        print(f"   ⚠️ API docs returned status {docs_status}")
    else:
        print("   ❌ API docs not accessible")
    
    print("\n🔗 Access URLs:")
    print("   - API Docs: http://127.0.0.1:8000/docs")
    print("   - Health: http://127.0.0.1:8000/api/v1/health")
    
    if status == 200:
        print("\n🎉 Backend service is running normally!")
    else:
        print("\n⚠️ Backend service has some issues, check the logs.")

if __name__ == "__main__":
    main()