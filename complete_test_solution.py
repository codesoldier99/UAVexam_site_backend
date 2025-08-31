#!/usr/bin/env python3
"""
完整的API测试和ngrok部署解决方案
"""

import requests
import json
import subprocess
import time
import os
import sys
from datetime import datetime

# API基础URL
LOCAL_BASE_URL = "http://localhost:8000/api/v1"

def check_backend_status():
    """检查后端服务状态"""
    print("🔍 检查后端服务状态...")
    try:
        response = requests.get(f"{LOCAL_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ 后端服务运行正常")
            return True
        else:
            print(f"❌ 后端服务异常，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到后端服务: {e}")
        return False

def test_core_apis():
    """测试核心API功能"""
    print("\n🧪 测试核心API功能...")
    
    results = []
    
    # 1. 健康检查
    try:
        response = requests.get(f"{LOCAL_BASE_URL}/health")
        results.append(("健康检查", response.status_code == 200))
        print(f"健康检查: {'✅' if response.status_code == 200 else '❌'}")
    except:
        results.append(("健康检查", False))
        print("健康检查: ❌")
    
    # 2. 登录测试
    try:
        login_data = {"username": "admin", "password": "admin123"}
        response = requests.post(f"{LOCAL_BASE_URL}/auth/login", json=login_data)
        success = response.status_code == 200
        results.append(("管理员登录", success))
        print(f"管理员登录: {'✅' if success else '❌'}")
        
        if success:
            token = response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            
            # 3. 考场列表（需要认证）
            try:
                response = requests.get(f"{LOCAL_BASE_URL}/venues", headers=headers)
                success = response.status_code == 200
                results.append(("考场列表", success))
                print(f"考场列表: {'✅' if success else '❌'}")
            except:
                results.append(("考场列表", False))
                print("考场列表: ❌")
        else:
            results.append(("考场列表", False))
            print("考场列表: ❌ (登录失败)")
    except:
        results.append(("管理员登录", False))
        results.append(("考场列表", False))
        print("管理员登录: ❌")
        print("考场列表: ❌")
    
    # 4. 微信接口测试
    try:
        id_card = "110101199001011234"
        response = requests.get(f"{LOCAL_BASE_URL}/wechat/candidate/info-by-idcard?id_card={id_card}")
        success = response.status_code == 200
        results.append(("微信考生信息", success))
        print(f"微信考生信息: {'✅' if success else '❌'}")
    except:
        results.append(("微信考生信息", False))
        print("微信考生信息: ❌")
    
    # 5. 微信看板数据
    try:
        response = requests.get(f"{LOCAL_BASE_URL}/wechat/dashboard")
        success = response.status_code == 200
        results.append(("微信看板数据", success))
        print(f"微信看板数据: {'✅' if success else '❌'}")
    except:
        results.append(("微信看板数据", False))
        print("微信看板数据: ❌")
    
    return results

def start_ngrok():
    """启动ngrok"""
    print("\n🚀 启动ngrok...")
    
    # 检查ngrok是否已安装
    try:
        result = subprocess.run(["ngrok", "version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ ngrok未安装或不在PATH中")
            return None
    except FileNotFoundError:
        print("❌ ngrok未找到，请先安装ngrok")
        return None
    
    print("✅ ngrok已安装")
    
    # 停止现有的ngrok进程
    try:
        if os.name == 'nt':  # Windows
            subprocess.run(["taskkill", "/f", "/im", "ngrok.exe"], 
                         capture_output=True, check=False)
        else:  # Linux/Mac
            subprocess.run(["pkill", "ngrok"], capture_output=True, check=False)
        time.sleep(1)
    except:
        pass
    
    print("🔄 启动ngrok HTTP隧道...")
    print("请手动运行: ngrok http 8000")
    print("然后查看是否出现 'Forwarding https://xxxxx.ngrok-free.app' 信息")
    
    return None

def test_ngrok_connection(ngrok_url):
    """测试ngrok连接"""
    if not ngrok_url:
        return False
    
    print(f"\n🔍 测试ngrok连接: {ngrok_url}")
    
    try:
        # 测试健康检查
        response = requests.get(f"{ngrok_url}/api/v1/health", timeout=10)
        if response.status_code == 200:
            print("✅ ngrok连接成功！")
            return True
        else:
            print(f"❌ ngrok连接失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ngrok连接测试失败: {e}")
        return False

def generate_api_test_urls(ngrok_url):
    """生成API测试URL"""
    if not ngrok_url:
        print("⚠️ 未提供ngrok URL，使用本地地址")
        base_url = "http://localhost:8000"
    else:
        base_url = ngrok_url
    
    print(f"\n📋 API测试地址 (基于 {base_url}):")
    print("="*60)
    
    urls = {
        "API文档": f"{base_url}/docs",
        "健康检查": f"{base_url}/api/v1/health",
        "系统信息": f"{base_url}/api/v1/system/info",
        "微信考生信息": f"{base_url}/api/v1/wechat/candidate/info-by-idcard?id_card=110101199001011234",
        "微信看板数据": f"{base_url}/api/v1/wechat/dashboard",
        "公共考场状态": f"{base_url}/api/v1/public/venues/status",
        "微信小程序看板": f"{base_url}/api/v1/wechat/venues/dashboard"
    }
    
    for name, url in urls.items():
        print(f"{name:<15} {url}")
    
    return urls

def main():
    """主函数"""
    print("🛩️ UAV考点运营管理系统 - 完整测试方案")
    print("="*60)
    
    # 1. 检查后端状态
    if not check_backend_status():
        print("\n❌ 后端服务未运行，请先启动后端服务")
        print("启动命令: cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        return
    
    # 2. 测试核心API
    results = test_core_apis()
    
    # 3. 显示测试结果
    print("\n📊 API测试结果汇总:")
    print("="*60)
    success_count = 0
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{test_name:<15} {status}")
        if success:
            success_count += 1
    
    print(f"\n总计: {success_count}/{len(results)} 个接口测试通过")
    
    # 4. ngrok部署指导
    print("\n🌐 ngrok公网部署:")
    print("="*60)
    print("1. 手动运行: ngrok http 8000")
    print("2. 等待连接成功，获取公网地址")
    print("3. 输入公网地址进行测试")
    
    # 5. 获取用户输入的ngrok地址
    print("\n请输入ngrok公网地址 (例如: https://abc123.ngrok-free.app):")
    print("如果ngrok连接失败，直接按回车跳过")
    
    ngrok_url = input("ngrok地址: ").strip()
    
    if ngrok_url:
        # 测试ngrok连接
        if test_ngrok_connection(ngrok_url):
            # 生成测试URL
            generate_api_test_urls(ngrok_url)
            
            print(f"\n🎉 部署成功！")
            print(f"公网API地址: {ngrok_url}")
            print(f"API文档: {ngrok_url}/docs")
        else:
            print("❌ ngrok连接测试失败")
    else:
        # 生成本地测试URL
        generate_api_test_urls(None)
    
    print("\n💡 提示:")
    print("- 确保后端服务在8000端口运行")
    print("- 如果ngrok连接失败，可能是网络环境限制")
    print("- 可以使用其他内网穿透工具如frp、localtunnel等")
    print("- 本地测试地址: http://localhost:8000/docs")

if __name__ == "__main__":
    main()