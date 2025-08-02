#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查内网穿透状态并获取公网地址
"""

import requests
import time
import json
import sys

def check_fastapi_status():
    """检查FastAPI服务状态"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ FastAPI服务正常运行")
            return True
        else:
            print(f"❌ FastAPI服务异常，状态码: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ FastAPI服务未启动: {e}")
        return False

def get_ngrok_tunnel():
    """获取ngrok隧道信息"""
    try:
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        if response.status_code == 200:
            tunnels = response.json()
            if tunnels and 'tunnels' in tunnels:
                for tunnel in tunnels['tunnels']:
                    if tunnel['proto'] == 'https':
                        public_url = tunnel['public_url']
                        print(f"✅ ngrok隧道已启动")
                        print(f"🌐 公网地址: {public_url}")
                        return public_url
            print("❌ 未找到可用的ngrok隧道")
            return None
        else:
            print(f"❌ 无法获取ngrok隧道信息，状态码: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ ngrok隧道未启动: {e}")
        return None

def generate_team_info(public_url):
    """生成团队分享信息"""
    print("\n" + "="*60)
    print("🎯 分享给前端和微信小程序端的信息")
    print("="*60)
    print(f"📋 API联调地址")
    print(f"基础地址: {public_url}")
    print(f"API文档: {public_url}/docs")
    print(f"测试接口: {public_url}/test")
    print(f"简化登录: {public_url}/simple-login")
    print()
    print("📱 微信小程序端配置")
    print("在微信开发者工具中设置服务器域名：")
    print(f"- request合法域名: {public_url}")
    print(f"- socket合法域名: wss://{public_url.split('//')[1]}")
    print()
    print("💻 前端端配置")
    print("在项目配置文件中设置API基础地址：")
    print(f"BASE_URL = '{public_url}'")
    print()
    print("🔧 测试命令")
    print(f"curl {public_url}/")
    print(f"curl -X POST {public_url}/simple-login \\")
    print("  -H \"Content-Type: application/json\" \\")
    print("  -d '{\"username\":\"admin@exam.com\",\"email\":\"admin@exam.com\",\"password\":\"admin123\"}'")
    print("="*60)

def main():
    print("🔍 检查内网穿透状态...")
    print("-" * 40)
    
    # 检查FastAPI服务
    fastapi_ok = check_fastapi_status()
    
    # 检查ngrok隧道
    public_url = get_ngrok_tunnel()
    
    if fastapi_ok and public_url:
        print("\n🎉 内网穿透配置完成！")
        generate_team_info(public_url)
        
        # 保存地址到文件
        with open("tunnel_url.txt", "w", encoding="utf-8") as f:
            f.write(public_url)
        print(f"\n📄 公网地址已保存到 tunnel_url.txt")
        
    else:
        print("\n❌ 内网穿透配置失败")
        if not fastapi_ok:
            print("请启动FastAPI服务: python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload")
        if not public_url:
            print("请启动ngrok隧道: ngrok http 8000")

if __name__ == "__main__":
    main() 