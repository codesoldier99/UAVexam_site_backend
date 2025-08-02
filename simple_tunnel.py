#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的内网穿透脚本
使用Python实现基本的端口转发功能
"""

import socket
import threading
import time
import requests
import json
from urllib.parse import urlparse

class SimpleTunnel:
    def __init__(self, local_port=8000, public_port=8080):
        self.local_port = local_port
        self.public_port = public_port
        self.running = False
        
    def start_server(self):
        """启动简单的转发服务器"""
        try:
            # 创建服务器socket
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('0.0.0.0', self.public_port))
            server.listen(5)
            
            print(f"🚀 简单内网穿透已启动")
            print(f"📡 本地端口: {self.local_port}")
            print(f"🌐 公网端口: {self.public_port}")
            print(f"🔗 访问地址: http://localhost:{self.public_port}")
            
            self.running = True
            
            while self.running:
                try:
                    client, addr = server.accept()
                    print(f"📥 收到来自 {addr} 的连接")
                    
                    # 为每个连接创建新线程
                    thread = threading.Thread(target=self.handle_client, args=(client,))
                    thread.daemon = True
                    thread.start()
                    
                except Exception as e:
                    print(f"❌ 处理连接时出错: {e}")
                    
        except Exception as e:
            print(f"❌ 启动服务器失败: {e}")
            
    def handle_client(self, client_socket):
        """处理客户端连接"""
        try:
            # 连接到本地FastAPI服务
            local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            local_socket.connect(('localhost', self.local_port))
            
            # 转发数据
            self.forward_data(client_socket, local_socket)
            
        except Exception as e:
            print(f"❌ 处理客户端连接失败: {e}")
        finally:
            client_socket.close()
            
    def forward_data(self, client_socket, local_socket):
        """转发数据"""
        def forward(src, dst):
            try:
                while self.running:
                    data = src.recv(4096)
                    if not data:
                        break
                    dst.send(data)
            except:
                pass
            finally:
                src.close()
                dst.close()
        
        # 创建双向转发
        t1 = threading.Thread(target=forward, args=(client_socket, local_socket))
        t2 = threading.Thread(target=forward, args=(local_socket, client_socket))
        
        t1.daemon = True
        t2.daemon = True
        
        t1.start()
        t2.start()
        
        t1.join()
        t2.join()
        
    def stop(self):
        """停止服务器"""
        self.running = False
        print("🛑 内网穿透已停止")

def get_public_ip():
    """获取公网IP地址"""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('ip')
    except:
        pass
    return None

def main():
    print("🔍 检查FastAPI服务状态...")
    
    # 检查FastAPI服务
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ FastAPI服务正常运行")
        else:
            print(f"❌ FastAPI服务异常，状态码: {response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        print(f"❌ FastAPI服务未启动: {e}")
        print("请先启动FastAPI服务: python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload")
        return
    
    # 获取公网IP
    public_ip = get_public_ip()
    
    # 启动内网穿透
    tunnel = SimpleTunnel(local_port=8000, public_port=8080)
    
    print("\n" + "="*60)
    print("🎯 内网穿透配置信息")
    print("="*60)
    print(f"📋 本地访问地址")
    print(f"基础地址: http://localhost:8080")
    print(f"API文档: http://localhost:8080/docs")
    print(f"测试接口: http://localhost:8080/test")
    print()
    
    if public_ip:
        print(f"🌐 公网访问地址（需要端口映射）")
        print(f"基础地址: http://{public_ip}:8080")
        print(f"API文档: http://{public_ip}:8080/docs")
        print(f"测试接口: http://{public_ip}:8080/test")
        print()
        print("⚠️  注意：公网访问需要配置路由器端口映射")
        print("   将外网端口映射到本机的8080端口")
    else:
        print("❌ 无法获取公网IP地址")
        print("建议使用ngrok或其他内网穿透工具")
    
    print("="*60)
    print("🔄 按 Ctrl+C 停止内网穿透")
    
    try:
        tunnel.start_server()
    except KeyboardInterrupt:
        print("\n🛑 正在停止内网穿透...")
        tunnel.stop()

if __name__ == "__main__":
    main() 