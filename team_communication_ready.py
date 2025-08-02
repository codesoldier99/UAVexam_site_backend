#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
团队沟通准备脚本
提供多种内网穿透方案和团队协作信息
"""

import requests
import json
import time
import subprocess
import sys
import os

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

def generate_team_info():
    """生成团队分享信息"""
    public_ip = get_public_ip()
    
    print("\n" + "="*80)
    print("🎯 考试系统后端API - 团队沟通信息")
    print("="*80)
    
    print("\n📋 当前状态")
    print("-" * 40)
    if check_fastapi_status():
        print("✅ FastAPI服务: 运行中")
        print("🌐 本地地址: http://localhost:8000")
        print("📚 API文档: http://localhost:8000/docs")
        print("🧪 测试接口: http://localhost:8000/test")
    else:
        print("❌ FastAPI服务: 未运行")
        print("💡 启动命令: python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload")
    
    print("\n🌐 内网穿透方案")
    print("-" * 40)
    
    # 方案1: 本地网络访问
    print("📡 方案1: 本地网络访问")
    if public_ip:
        print(f"   公网IP: {public_ip}")
        print(f"   访问地址: http://{public_ip}:8000")
        print("   ⚠️  需要配置路由器端口映射")
    else:
        print("   ❌ 无法获取公网IP")
    
    # 方案2: ngrok（需要认证）
    print("\n📡 方案2: ngrok内网穿透")
    print("   ❌ 需要ngrok认证token")
    print("   💡 注册地址: https://dashboard.ngrok.com/signup")
    print("   💡 获取token: https://dashboard.ngrok.com/get-started/your-authtoken")
    print("   💡 配置命令: ngrok config add-authtoken YOUR_TOKEN")
    
    # 方案3: 其他内网穿透工具
    print("\n📡 方案3: 其他内网穿透工具")
    print("   🔧 cpolar: https://www.cpolar.com/")
    print("   🔧 frp: https://github.com/fatedier/frp")
    print("   🔧 natapp: https://natapp.cn/")
    print("   🔧 花生壳: https://hsk.oray.com/")
    
    # 方案4: 云服务器
    print("\n📡 方案4: 云服务器部署")
    print("   ☁️  阿里云ECS")
    print("   ☁️  腾讯云CVM")
    print("   ☁️  华为云ECS")
    print("   ☁️  本地Docker部署")
    
    print("\n📱 微信小程序端配置")
    print("-" * 40)
    if public_ip:
        print(f"   在微信开发者工具中设置服务器域名：")
        print(f"   - request合法域名: http://{public_ip}:8000")
        print(f"   - socket合法域名: ws://{public_ip}:8000")
    else:
        print("   ⚠️  需要先配置内网穿透")
    
    print("\n💻 前端端配置")
    print("-" * 40)
    if public_ip:
        print(f"   在项目配置文件中设置API基础地址：")
        print(f"   BASE_URL = 'http://{public_ip}:8000'")
    else:
        print("   ⚠️  需要先配置内网穿透")
    
    print("\n🔧 API接口清单")
    print("-" * 40)
    print("   公开接口（无需认证）:")
    print("   - GET / - 根接口")
    print("   - GET /test - 测试接口")
    print("   - GET /docs - API文档")
    print("   - GET /redoc - 另一种API文档格式")
    print()
    print("   认证接口:")
    print("   - POST /auth/jwt/login - JWT登录")
    print("   - POST /simple-login - 简化登录（测试用）")
    print("   - GET /users/me - 获取当前用户信息")
    print()
    print("   考生管理:")
    print("   - GET /candidates/ - 获取考生列表")
    print("   - POST /candidates/ - 创建考生")
    print("   - GET /candidates/{id} - 获取考生详情")
    print("   - PUT /candidates/{id} - 更新考生信息")
    print("   - DELETE /candidates/{id} - 删除考生")
    print("   - POST /candidates/batch-import - 批量导入考生")
    print()
    print("   考试产品管理:")
    print("   - GET /exam-products/ - 获取考试产品列表")
    print("   - POST /exam-products/ - 创建考试产品")
    print("   - GET /exam-products/{id} - 获取考试产品详情")
    print("   - PUT /exam-products/{id} - 更新考试产品")
    print("   - DELETE /exam-products/{id} - 删除考试产品")
    print()
    print("   排期管理:")
    print("   - GET /schedules/ - 获取排期列表")
    print("   - POST /schedules/ - 创建排期")
    print("   - GET /schedules/{id} - 获取排期详情")
    print("   - PUT /schedules/{id} - 更新排期")
    print("   - DELETE /schedules/{id} - 删除排期")
    print("   - POST /schedules/scan-check-in - 扫码签到")
    print()
    print("   机构管理:")
    print("   - GET /simple-institutions/ - 获取机构列表")
    print("   - POST /simple-institutions/ - 创建机构")
    print("   - GET /simple-institutions/{id} - 获取机构详情")
    print("   - PUT /simple-institutions/{id} - 更新机构")
    print("   - DELETE /simple-institutions/{id} - 删除机构")
    
    print("\n🔐 认证说明")
    print("-" * 40)
    print("   JWT认证流程:")
    print("   1. 调用登录接口获取token")
    print("   2. 在后续请求的Header中添加: Authorization: Bearer <token>")
    print()
    print("   测试用简化登录:")
    print("   POST /simple-login")
    print("   {")
    print('     "username": "admin@exam.com",')
    print('     "email": "admin@exam.com",')
    print('     "password": "admin123"')
    print("   }")
    
    print("\n📊 数据格式")
    print("-" * 40)
    print("   请求格式:")
    print("   - Content-Type: application/json")
    print("   - 数据格式: JSON")
    print()
    print("   响应格式:")
    print("   {")
    print('     "status": "success",')
    print('     "data": {...},')
    print('     "message": "操作成功"')
    print("   }")
    
    print("\n🛠️ 联调工具推荐")
    print("-" * 40)
    print("   📱 Postman: https://www.postman.com/downloads/")
    print("   📱 Insomnia: https://insomnia.rest/download")
    print("   📱 curl（命令行）")
    print()
    print("   测试命令:")
    if public_ip:
        print(f"   curl http://{public_ip}:8000/")
        print(f"   curl -X POST http://{public_ip}:8000/simple-login \\")
        print("     -H \"Content-Type: application/json\" \\")
        print("     -d '{\"username\":\"admin@exam.com\",\"email\":\"admin@exam.com\",\"password\":\"admin123\"}'")
    else:
        print("   curl http://localhost:8000/")
        print("   curl -X POST http://localhost:8000/simple-login \\")
        print("     -H \"Content-Type: application/json\" \\")
        print("     -d '{\"username\":\"admin@exam.com\",\"email\":\"admin@exam.com\",\"password\":\"admin123\"}'")
    
    print("\n🚨 常见问题")
    print("-" * 40)
    print("   1. 连接失败")
    print("      - 检查FastAPI服务是否启动")
    print("      - 确认防火墙设置")
    print("      - 验证网络连接")
    print()
    print("   2. 认证失败")
    print("      - 检查token格式是否正确")
    print("      - 确认token是否过期")
    print("      - 验证请求头格式")
    print()
    print("   3. 数据格式错误")
    print("      - 检查Content-Type是否为application/json")
    print("      - 验证请求体JSON格式")
    print("      - 确认必填字段是否完整")
    
    print("\n📞 沟通渠道")
    print("-" * 40)
    print("   💬 即时沟通:")
    print("   - 微信群: 考试系统开发群")
    print("   - 钉钉群: 考试系统后端联调群")
    print()
    print("   📄 文档共享:")
    print("   - API文档: http://localhost:8000/docs")
    print("   - 项目文档: 项目根目录/docs")
    print("   - 测试报告: 项目根目录/test_reports")
    print()
    print("   🆘 问题反馈:")
    print("   1. 在群里@后端开发人员")
    print("   2. 提供详细的错误信息")
    print("   3. 附上请求和响应数据")
    print("   4. 说明复现步骤")
    
    print("\n🔄 开发流程")
    print("-" * 40)
    print("   1. 接口开发")
    print("      - 后端开发新接口")
    print("      - 编写测试用例")
    print("      - 更新API文档")
    print("      - 通知前端和小程序端")
    print()
    print("   2. 联调测试")
    print("      - 启动内网穿透")
    print("      - 分享地址给队友")
    print("      - 协助调试问题")
    print("      - 记录问题和解决方案")
    print()
    print("   3. 问题处理")
    print("      - 及时响应队友问题")
    print("      - 提供详细的错误信息")
    print("      - 协助排查问题原因")
    print("      - 更新相关文档")
    
    print("\n📈 性能监控")
    print("-" * 40)
    print("   接口响应时间:")
    print("   - 正常: < 500ms")
    print("   - 警告: 500ms - 2s")
    print("   - 异常: > 2s")
    print()
    print("   错误率监控:")
    print("   - 正常: < 1%")
    print("   - 警告: 1% - 5%")
    print("   - 异常: > 5%")
    
    print("\n🎯 最佳实践")
    print("-" * 40)
    print("   1. 开发阶段")
    print("      - 使用简化登录进行测试")
    print("      - 先测试公开接口")
    print("      - 逐步测试认证接口")
    print("      - 及时更新文档")
    print()
    print("   2. 联调阶段")
    print("      - 保持内网穿透稳定运行")
    print("      - 及时响应队友问题")
    print("      - 提供详细的错误信息")
    print("      - 记录常见问题和解决方案")
    print()
    print("   3. 测试阶段")
    print("      - 全面测试所有接口")
    print("      - 验证数据格式正确性")
    print("      - 检查权限控制")
    print("      - 确认错误处理")
    
    print("\n" + "="*80)
    print("💡 下一步行动")
    print("="*80)
    print("   1. 配置ngrok认证token（推荐）")
    print("   2. 或使用其他内网穿透工具")
    print("   3. 或配置路由器端口映射")
    print("   4. 将以上信息分享给前端和微信小程序端队友")
    print("   5. 开始API联调测试")
    
    # 保存信息到文件
    with open("team_communication_info.txt", "w", encoding="utf-8") as f:
        f.write("考试系统后端API - 团队沟通信息\n")
        f.write("="*80 + "\n")
        f.write(f"FastAPI服务状态: {'运行中' if check_fastapi_status() else '未运行'}\n")
        f.write(f"本地地址: http://localhost:8000\n")
        f.write(f"API文档: http://localhost:8000/docs\n")
        if public_ip:
            f.write(f"公网IP: {public_ip}\n")
            f.write(f"公网地址: http://{public_ip}:8000\n")
        f.write("\n请将此文件分享给前端和微信小程序端队友\n")
    
    print(f"\n📄 信息已保存到 team_communication_info.txt")

def main():
    print("🔍 生成团队沟通信息...")
    generate_team_info()

if __name__ == "__main__":
    main() 