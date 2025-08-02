#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用cpolar的内网穿透脚本
cpolar是免费的内网穿透工具，无需认证
"""

import requests
import subprocess
import time
import json
import os
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

def download_cpolar():
    """下载cpolar"""
    print("📥 正在下载cpolar...")
    
    # Windows下载地址
    cpolar_url = "https://www.cpolar.com/static/downloads/install-release-cpolar-windows-amd64.zip"
    
    try:
        import urllib.request
        urllib.request.urlretrieve(cpolar_url, "cpolar.zip")
        print("✅ cpolar下载完成")
        
        # 解压
        import zipfile
        with zipfile.ZipFile("cpolar.zip", 'r') as zip_ref:
            zip_ref.extractall(".")
        
        print("✅ cpolar解压完成")
        return True
    except Exception as e:
        print(f"❌ 下载cpolar失败: {e}")
        return False

def install_cpolar():
    """安装cpolar"""
    print("🔧 正在安装cpolar...")
    
    try:
        # 检查是否已安装
        result = subprocess.run(["cpolar", "version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ cpolar已安装")
            return True
    except:
        pass
    
    # 尝试下载安装
    if download_cpolar():
        print("✅ cpolar安装完成")
        return True
    else:
        print("❌ cpolar安装失败")
        print("💡 请手动下载: https://www.cpolar.com/download")
        return False

def start_cpolar_tunnel():
    """启动cpolar隧道"""
    print("🚀 启动cpolar隧道...")
    
    try:
        # 启动cpolar隧道
        process = subprocess.Popen(
            ["cpolar", "http", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待隧道启动
        time.sleep(3)
        
        # 检查隧道状态
        try:
            response = requests.get("http://localhost:9200/api/tunnels", timeout=5)
            if response.status_code == 200:
                tunnels = response.json()
                if tunnels and 'tunnels' in tunnels:
                    for tunnel in tunnels['tunnels']:
                        if tunnel['proto'] == 'https':
                            public_url = tunnel['public_url']
                            print(f"✅ cpolar隧道已启动")
                            print(f"🌐 公网地址: {public_url}")
                            return public_url
        except:
            pass
        
        print("⏳ 隧道正在启动，请稍候...")
        print("💡 如果长时间无响应，请检查网络连接")
        
        return None
        
    except Exception as e:
        print(f"❌ 启动cpolar隧道失败: {e}")
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
    print("🔍 检查FastAPI服务状态...")
    
    # 检查FastAPI服务
    if not check_fastapi_status():
        print("请先启动FastAPI服务: python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload")
        return
    
    # 安装cpolar
    if not install_cpolar():
        print("❌ cpolar安装失败，请手动安装")
        return
    
    # 启动隧道
    public_url = start_cpolar_tunnel()
    
    if public_url:
        print("\n🎉 cpolar内网穿透配置完成！")
        generate_team_info(public_url)
        
        # 保存地址到文件
        with open("cpolar_tunnel_url.txt", "w", encoding="utf-8") as f:
            f.write(public_url)
        print(f"\n📄 公网地址已保存到 cpolar_tunnel_url.txt")
        
        print("\n🔄 按 Ctrl+C 停止隧道")
        
        try:
            # 保持隧道运行
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 正在停止隧道...")
            
    else:
        print("\n❌ cpolar隧道启动失败")
        print("💡 请检查网络连接或手动启动")

if __name__ == "__main__":
    main() 