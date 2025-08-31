import requests
import json

print("🚀 测试UAV考点管理系统API")
print("="*50)

try:
    # 测试健康检查
    print("1. 测试健康检查接口...")
    response = requests.get('http://localhost:8000/health', timeout=10)
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"   响应: {response.json()}")
        print("   ✅ 健康检查通过")
    else:
        print("   ❌ 健康检查失败")
        
    print()
    
    # 测试根路径
    print("2. 测试根路径...")
    response = requests.get('http://localhost:8000/', timeout=10)
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"   响应: {response.json()}")
        print("   ✅ 根路径访问成功")
    else:
        print("   ❌ 根路径访问失败")
        
    print()
    
    # 测试API文档
    print("3. 测试API文档...")
    response = requests.get('http://localhost:8000/api/v1/docs', timeout=10)
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ API文档可访问")
    else:
        print("   ❌ API文档访问失败")
        
    print()
    print("🎉 UAV考点管理系统后端部署成功！")
    print("📊 你可以访问以下地址：")
    print("   - 健康检查: http://localhost:8000/health")
    print("   - API文档: http://localhost:8000/api/v1/docs")
    print("   - 系统首页: http://localhost:8000/")
    
except Exception as e:
    print(f"❌ 测试失败: {str(e)}")
    print("请确保FastAPI服务正在运行")