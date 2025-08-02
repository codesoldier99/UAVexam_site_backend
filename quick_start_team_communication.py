#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键启动团队沟通脚本
自动检查服务状态、启动内网穿透、生成团队信息
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

def generate_quick_info(public_ip):
    """生成快速团队信息"""
    print("\n" + "="*80)
    print("🎯 考试系统后端API - 团队沟通信息")
    print("="*80)
    
    print(f"\n📋 当前状态")
    print(f"✅ FastAPI服务: 运行中")
    print(f"🌐 本地地址: http://localhost:8000")
    print(f"📚 API文档: http://localhost:8000/docs")
    print(f"🧪 测试接口: http://localhost:8000/test")
    
    if public_ip:
        print(f"\n🌐 公网访问信息")
        print(f"公网IP: {public_ip}")
        print(f"访问地址: http://{public_ip}:8000")
        print("⚠️  需要配置路由器端口映射才能从外网访问")
    
    print(f"\n📱 微信小程序端配置")
    if public_ip:
        print(f"在微信开发者工具中设置服务器域名：")
        print(f"- request合法域名: http://{public_ip}:8000")
        print(f"- socket合法域名: ws://{public_ip}:8000")
    else:
        print("⚠️  需要先配置内网穿透")
    
    print(f"\n💻 前端端配置")
    if public_ip:
        print(f"在项目配置文件中设置API基础地址：")
        print(f"BASE_URL = 'http://{public_ip}:8000'")
    else:
        print("⚠️  需要先配置内网穿透")
    
    print(f"\n🔧 核心API接口")
    print("认证接口:")
    print("- POST /simple-login - 简化登录（测试用）")
    print("- POST /auth/jwt/login - JWT登录")
    print("- GET /users/me - 获取当前用户信息")
    print()
    print("考生管理:")
    print("- GET /candidates/ - 获取考生列表")
    print("- POST /candidates/ - 创建考生")
    print("- GET /candidates/{id} - 获取考生详情")
    print("- PUT /candidates/{id} - 更新考生信息")
    print("- DELETE /candidates/{id} - 删除考生")
    print()
    print("考试产品管理:")
    print("- GET /exam-products/ - 获取考试产品列表")
    print("- POST /exam-products/ - 创建考试产品")
    print("- GET /exam-products/{id} - 获取考试产品详情")
    print("- PUT /exam-products/{id} - 更新考试产品")
    print("- DELETE /exam-products/{id} - 删除考试产品")
    print()
    print("排期管理:")
    print("- GET /schedules/ - 获取排期列表")
    print("- POST /schedules/ - 创建排期")
    print("- GET /schedules/{id} - 获取排期详情")
    print("- PUT /schedules/{id} - 更新排期")
    print("- DELETE /schedules/{id} - 删除排期")
    print("- POST /schedules/scan-check-in - 扫码签到")
    print()
    print("机构管理:")
    print("- GET /simple-institutions/ - 获取机构列表")
    print("- POST /simple-institutions/ - 创建机构")
    print("- GET /simple-institutions/{id} - 获取机构详情")
    print("- PUT /simple-institutions/{id} - 更新机构")
    print("- DELETE /simple-institutions/{id} - 删除机构")
    
    print(f"\n🔐 测试用简化登录")
    print("POST /simple-login")
    print("{")
    print('  "username": "admin@exam.com",')
    print('  "email": "admin@exam.com",')
    print('  "password": "admin123"')
    print("}")
    
    print(f"\n🛠️ 测试命令")
    if public_ip:
        print(f"curl http://{public_ip}:8000/")
        print(f"curl -X POST http://{public_ip}:8000/simple-login \\")
        print("  -H \"Content-Type: application/json\" \\")
        print("  -d '{\"username\":\"admin@exam.com\",\"email\":\"admin@exam.com\",\"password\":\"admin123\"}'")
    else:
        print("curl http://localhost:8000/")
        print("curl -X POST http://localhost:8000/simple-login \\")
        print("  -H \"Content-Type: application/json\" \\")
        print("  -d '{\"username\":\"admin@exam.com\",\"email\":\"admin@exam.com\",\"password\":\"admin123\"}'")
    
    print(f"\n📞 沟通流程")
    print("1. 主动同步进度: 当完成一个模块的API时，主动在群里@前端")
    print("2. 清晰地响应问题: 当前端反馈接口有问题时，第一时间让他提供：")
    print("   - 请求的URL")
    print("   - 请求参数")
    print("   - Network面板里的响应内容")
    
    print(f"\n💡 下一步行动")
    print("1. 配置路由器端口映射（推荐）")
    print("2. 或使用内网穿透工具（cpolar/ngrok）")
    print("3. 将以上信息分享给前端和微信小程序端队友")
    print("4. 开始API联调测试")
    
    print("="*80)
    
    # 保存信息到文件
    with open("team_communication_quick_info.txt", "w", encoding="utf-8") as f:
        f.write("考试系统后端API - 团队沟通信息\n")
        f.write("="*80 + "\n")
        f.write(f"FastAPI服务状态: 运行中\n")
        f.write(f"本地地址: http://localhost:8000\n")
        f.write(f"API文档: http://localhost:8000/docs\n")
        if public_ip:
            f.write(f"公网IP: {public_ip}\n")
            f.write(f"公网地址: http://{public_ip}:8000\n")
        f.write("\n请将此文件分享给前端和微信小程序端队友\n")
    
    print(f"\n📄 信息已保存到 team_communication_quick_info.txt")

def main():
    print("🚀 一键启动团队沟通...")
    print("-" * 40)
    
    # 检查FastAPI服务
    if not check_fastapi_status():
        print("\n❌ FastAPI服务未启动")
        print("请先启动FastAPI服务:")
        print("python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload")
        return
    
    # 获取公网IP
    public_ip = get_public_ip()
    
    # 生成团队信息
    generate_quick_info(public_ip)
    
    print(f"\n🎉 团队沟通准备完成！")
    print(f"请将生成的信息分享给前端和微信小程序端队友")

if __name__ == "__main__":
    main() 