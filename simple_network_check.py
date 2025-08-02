#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的网络检查脚本
"""

import socket
import subprocess

def get_local_ip():
    """获取本地IP地址"""
    try:
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
            return True
        else:
            return False
    except Exception as e:
        print(f"❌ 检查端口失败: {e}")
        return False

def main():
    print("🔍 网络状态检查")
    print("-" * 40)
    
    # 检查本地IP
    local_ip = get_local_ip()
    if local_ip:
        print(f"✅ 本地IP: {local_ip}")
    else:
        print("❌ 无法获取本地IP")
    
    # 检查端口
    if check_port_8000():
        print("✅ 端口8000正在被使用（FastAPI服务运行中）")
    else:
        print("❌ 端口8000未被使用（FastAPI服务未运行）")
    
    print("\n" + "="*60)
    print("🔧 路由器端口映射配置")
    print("="*60)
    
    if local_ip:
        print(f"📋 配置信息:")
        print(f"   外部端口: 8000")
        print(f"   内部IP: {local_ip}")
        print(f"   内部端口: 8000")
        print(f"   协议: TCP")
        print()
        print("📝 配置步骤:")
        print("1. 登录路由器管理界面")
        print("   - 尝试: http://192.168.1.1")
        print("   - 尝试: http://192.168.2.1")
        print("   - 尝试: http://192.168.0.1")
        print("2. 找到'端口映射'或'端口转发'设置")
        print("3. 添加新规则，填入上述信息")
        print("4. 保存设置")
        print()
        print("💡 重要提醒:")
        print("- 确保已关闭VPN代理")
        print("- 确保使用真实网络连接")
        print("- 配置完成后测试连接")
    else:
        print("❌ 无法获取本地IP地址")
    
    print("="*60)

if __name__ == "__main__":
    main() 