#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络状态检查脚本
检查VPN状态、IP地址、端口映射等
"""

import requests
import socket
import subprocess
import platform
import json

def check_vpn_status():
    """检查VPN状态"""
    print("🔍 检查VPN状态...")
    
    try:
        # 尝试获取真实IP
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        if response.status_code == 200:
            data = response.json()
            public_ip = data.get('ip')
            print(f"✅ 公网IP: {public_ip}")
            
            # 检查是否是VPN IP
            if public_ip.startswith(('10.', '172.', '192.168.')):
                print("⚠️  检测到可能是VPN IP地址")
                return False, public_ip
            else:
                print("✅ 检测到真实公网IP")
                return True, public_ip
        else:
            print(f"❌ 无法获取IP地址，状态码: {response.status_code}")
            return False, None
    except Exception as e:
        print(f"❌ 网络连接失败: {e}")
        print("💡 建议关闭VPN代理后重试")
        return False, None

def get_local_ip():
    """获取本地IP地址"""
    try:
        # 连接到外部地址来获取本地IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"❌ 无法获取本地IP: {e}")
        return None

def check_port_8000():
    """检查端口8000是否被占用"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8000))
        sock.close()
        
        if result == 0:
            print("✅ 端口8000正在被使用（FastAPI服务运行中）")
            return True
        else:
            print("❌ 端口8000未被使用（FastAPI服务未运行）")
            return False
    except Exception as e:
        print(f"❌ 检查端口失败: {e}")
        return False

def check_firewall():
    """检查防火墙状态"""
    print("🔍 检查防火墙状态...")
    
    try:
        if platform.system() == "Windows":
            # Windows防火墙检查
            result = subprocess.run(
                ["netsh", "advfirewall", "show", "allprofiles"], 
                capture_output=True, text=True
            )
            if result.returncode == 0:
                print("✅ Windows防火墙配置正常")
            else:
                print("⚠️  Windows防火墙可能阻止了连接")
        else:
            print("ℹ️  非Windows系统，请手动检查防火墙")
    except Exception as e:
        print(f"❌ 检查防火墙失败: {e}")

def generate_router_config():
    """生成路由器配置指南"""
    print("\n" + "="*60)
    print("🔧 路由器端口映射配置指南")
    print("="*60)
    
    local_ip = get_local_ip()
    if local_ip:
        print(f"📋 配置信息:")
        print(f"   外部端口: 8000")
        print(f"   内部IP: {local_ip}")
        print(f"   内部端口: 8000")
        print(f"   协议: TCP")
        print()
        print("📝 配置步骤:")
        print("1. 登录路由器管理界面（通常是 http://192.168.1.1）")
        print("2. 找到'端口映射'或'端口转发'设置")
        print("3. 添加新规则，填入上述信息")
        print("4. 保存设置")
        print()
        print("🧪 测试命令:")
        print(f"   curl http://你的公网IP:8000/")
        print("   curl http://45.149.92.22:8000/")
    else:
        print("❌ 无法获取本地IP地址")

def main():
    print("🔍 网络状态检查")
    print("-" * 40)
    
    # 检查VPN状态
    vpn_ok, public_ip = check_vpn_status()
    
    # 检查本地IP
    local_ip = get_local_ip()
    if local_ip:
        print(f"✅ 本地IP: {local_ip}")
    else:
        print("❌ 无法获取本地IP")
    
    # 检查端口
    port_ok = check_port_8000()
    
    # 检查防火墙
    check_firewall()
    
    # 生成配置指南
    generate_router_config()
    
    print("\n" + "="*60)
    print("💡 建议")
    print("="*60)
    
    if not vpn_ok:
        print("1. 🔴 关闭VPN代理")
        print("2. 🔄 重新运行此脚本检查网络状态")
        print("3. 🔧 配置路由器端口映射")
    else:
        print("1. ✅ 网络状态正常")
        print("2. 🔧 配置路由器端口映射")
        print("3. 🧪 测试端口映射是否成功")
    
    if not port_ok:
        print("4. 🚀 启动FastAPI服务")
    
    print("5. 📱 在群里分享API地址给前端")
    
    print("="*60)

if __name__ == "__main__":
    main() 