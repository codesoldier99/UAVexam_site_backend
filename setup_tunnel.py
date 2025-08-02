#!/usr/bin/env python3
"""
内网穿透设置脚本
用于将本地FastAPI服务暴露给前端和微信小程序端队友
"""

import subprocess
import sys
import time
import requests
from pathlib import Path

def check_ngrok_installed():
    """检查ngrok是否已安装"""
    try:
        result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ngrok已安装")
            return True
        else:
            print("❌ ngrok未正确安装")
            return False
    except FileNotFoundError:
        print("❌ ngrok未安装")
        return False

def install_ngrok():
    """安装ngrok"""
    print("正在安装ngrok...")
    try:
        # 下载ngrok
        import urllib.request
        import zipfile
        import os
        
        ngrok_url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
        zip_path = "ngrok.zip"
        
        print("下载ngrok...")
        urllib.request.urlretrieve(ngrok_url, zip_path)
        
        print("解压ngrok...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(".")
        
        # 清理
        os.remove(zip_path)
        
        print("✅ ngrok安装完成")
        return True
    except Exception as e:
        print(f"❌ 安装失败: {e}")
        return False

def start_ngrok_tunnel(port=8000):
    """启动ngrok隧道"""
    try:
        print(f"🚀 启动ngrok隧道，端口: {port}")
        print("正在启动隧道...")
        
        # 启动ngrok
        process = subprocess.Popen(
            ['ngrok', 'http', str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待隧道启动
        time.sleep(3)
        
        # 获取隧道URL
        try:
            response = requests.get('http://localhost:4040/api/tunnels')
            if response.status_code == 200:
                tunnels = response.json()['tunnels']
                if tunnels:
                    public_url = tunnels[0]['public_url']
                    print(f"\n🎉 隧道启动成功!")
                    print(f"🌐 公网地址: {public_url}")
                    print(f"📱 微信小程序端可以使用此地址进行联调")
                    print(f"💻 前端端可以使用此地址进行联调")
                    print(f"\n📋 分享给队友的信息:")
                    print(f"API基础地址: {public_url}")
                    print(f"示例接口: {public_url}/")
                    print(f"API文档: {public_url}/docs")
                    print(f"测试接口: {public_url}/test")
                    print(f"\n⚠️  注意事项:")
                    print(f"1. 此地址仅在ngrok运行时有效")
                    print(f"2. 免费版ngrok每次重启地址会变化")
                    print(f"3. 建议使用付费版获得固定域名")
                    print(f"\n🔄 按Ctrl+C停止隧道")
                    
                    return process, public_url
                else:
                    print("❌ 隧道启动失败")
                    return None, None
            else:
                print("❌ 无法获取隧道信息")
                return None, None
        except requests.exceptions.RequestException:
            print("❌ 无法连接到ngrok API")
            return None, None
            
    except Exception as e:
        print(f"❌ 启动隧道失败: {e}")
        return None, None

def create_api_documentation():
    """创建API文档"""
    doc_content = """
# 考试系统后端API文档

## 基础信息
- 开发环境: FastAPI + SQLAlchemy + MySQL
- 认证方式: JWT Token
- 数据格式: JSON

## 主要接口

### 1. 认证接口
- `POST /auth/jwt/login` - JWT登录
- `POST /simple-login` - 简化登录（测试用）
- `GET /users/me` - 获取当前用户信息

### 2. 考生管理
- `GET /candidates/` - 获取考生列表
- `POST /candidates/` - 创建考生
- `GET /candidates/{id}` - 获取考生详情
- `PUT /candidates/{id}` - 更新考生信息
- `DELETE /candidates/{id}` - 删除考生
- `POST /candidates/batch-import` - 批量导入考生
- `GET /candidates/template` - 下载导入模板

### 3. 考试产品管理
- `GET /exam-products/` - 获取考试产品列表
- `POST /exam-products/` - 创建考试产品
- `GET /exam-products/{id}` - 获取考试产品详情
- `PUT /exam-products/{id}` - 更新考试产品
- `DELETE /exam-products/{id}` - 删除考试产品

### 4. 排期管理
- `GET /schedules/` - 获取排期列表
- `POST /schedules/` - 创建排期
- `GET /schedules/{id}` - 获取排期详情
- `PUT /schedules/{id}` - 更新排期
- `DELETE /schedules/{id}` - 删除排期
- `GET /schedules/candidates-to-schedule` - 获取待排期考生
- `POST /schedules/batch-create` - 批量创建排期
- `POST /schedules/scan-check-in` - 扫码签到
- `POST /schedules/batch-scan-check-in` - 批量扫码签到
- `GET /schedules/check-in-stats` - 获取签到统计

### 5. 机构管理
- `GET /simple-institutions/` - 获取机构列表
- `POST /simple-institutions/` - 创建机构
- `GET /simple-institutions/{id}` - 获取机构详情
- `PUT /simple-institutions/{id}` - 更新机构
- `DELETE /simple-institutions/{id}` - 删除机构

### 6. 微信小程序接口
- `POST /wx-miniprogram/login` - 微信登录
- `GET /wx-miniprogram/user-info` - 获取用户信息
- `POST /wx-miniprogram/check-in` - 微信签到

## 数据模型

### 考生 (Candidate)
```json
{
  "id": 1,
  "name": "张三",
  "phone": "13800138000",
  "id_card": "110101199001011234",
  "email": "zhangsan@example.com",
  "institution_id": 1,
  "target_exam_product_id": 1,
  "status": "pending",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### 考试产品 (ExamProduct)
```json
{
  "id": 1,
  "name": "无人机驾驶员理论考试",
  "code": "UAV_THEORY",
  "description": "无人机驾驶员理论考试",
  "category": "VLOS",
  "exam_type": "MULTIROTOR",
  "exam_class": "AGRICULTURE",
  "exam_level": "PILOT",
  "theory_pass_score": 80,
  "practical_pass_score": 85,
  "duration_minutes": 120,
  "training_hours": 40,
  "price": 1000.0,
  "is_active": true
}
```

### 排期 (Schedule)
```json
{
  "id": 1,
  "candidate_id": 1,
  "exam_product_id": 1,
  "venue_id": 1,
  "scheduled_date": "2024-01-01",
  "start_time": "09:00:00",
  "end_time": "11:00:00",
  "schedule_type": "theory",
  "status": "scheduled",
  "check_in_time": null,
  "notes": "测试排期"
}
```

## 认证说明

### JWT认证
1. 调用登录接口获取token
2. 在后续请求的Header中添加: `Authorization: Bearer <token>`

### 权限说明
- 机构用户: 只能访问本机构的考生和排期
- 超级管理员: 可以访问所有数据
- 微信用户: 只能访问自己的信息

## 错误码说明
- 200: 成功
- 201: 创建成功
- 400: 请求参数错误
- 401: 未认证
- 403: 权限不足
- 404: 资源不存在
- 422: 数据验证失败
- 500: 服务器内部错误

## 测试接口
- `GET /` - 根接口
- `GET /test` - 测试接口
- `GET /docs` - API文档
- `GET /redoc` - 另一种API文档格式

## 联调建议
1. 使用Postman或类似工具测试接口
2. 先测试公开接口（如 `/` 和 `/test`）
3. 再测试需要认证的接口
4. 注意请求格式和认证方式
5. 遇到问题及时沟通
"""
    
    with open("API_DOCUMENTATION.md", "w", encoding="utf-8") as f:
        f.write(doc_content)
    
    print("📄 API文档已生成: API_DOCUMENTATION.md")

def main():
    """主函数"""
    print("🚀 考试系统后端API内网穿透设置")
    print("=" * 50)
    
    # 检查ngrok
    if not check_ngrok_installed():
        print("尝试安装ngrok...")
        if not install_ngrok():
            print("❌ 无法安装ngrok，请手动安装")
            print("下载地址: https://ngrok.com/download")
            return
    
    # 检查FastAPI服务是否运行
    try:
        response = requests.get('http://localhost:8000/', timeout=5)
        if response.status_code == 200:
            print("✅ FastAPI服务正在运行")
        else:
            print("❌ FastAPI服务未正常运行")
            return
    except requests.exceptions.RequestException:
        print("❌ FastAPI服务未启动")
        print("请先运行: python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload")
        return
    
    # 创建API文档
    create_api_documentation()
    
    # 启动隧道
    process, public_url = start_ngrok_tunnel()
    
    if process and public_url:
        try:
            # 保持隧道运行
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 正在停止隧道...")
            process.terminate()
            print("✅ 隧道已停止")
    else:
        print("❌ 隧道启动失败")

if __name__ == "__main__":
    main() 