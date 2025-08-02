#!/usr/bin/env python3
"""
路由器映射配置脚本
用于设置端口转发，让前端和微信小程序端能够访问本地API
"""

import subprocess
import requests
import socket
import json
from pathlib import Path

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
        print(f"❌ 获取本地IP失败: {e}")
        return None

def get_public_ip():
    """获取公网IP地址"""
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        if response.status_code == 200:
            return response.json()["ip"]
        else:
            return None
    except Exception as e:
        print(f"❌ 获取公网IP失败: {e}")
        return None

def check_port_open(ip, port):
    """检查端口是否开放"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except Exception:
        return False

def create_router_config_guide():
    """创建路由器配置指南"""
    local_ip = get_local_ip()
    public_ip = get_public_ip()
    
    if not local_ip:
        print("❌ 无法获取本地IP地址")
        return
    
    guide_content = f"""
# 路由器映射配置指南

## 📋 当前网络信息
- **本地IP地址**: {local_ip}
- **公网IP地址**: {public_ip or "无法获取"}
- **API端口**: 8000
- **服务地址**: http://{local_ip}:8000

## 🔧 路由器配置步骤

### 1. 登录路由器管理界面
- 打开浏览器，访问: http://192.168.1.1 或 http://192.168.0.1
- 用户名/密码: 通常是 admin/admin 或 admin/password
- 如果不知道密码，查看路由器背面标签

### 2. 找到端口转发设置
不同品牌路由器的设置位置：
- **TP-Link**: 应用管理 → 端口转发
- **华为**: 高级设置 → 端口映射
- **小米**: 高级设置 → 端口转发
- **华硕**: 高级设置 → 端口转发
- **其他品牌**: 查找"端口转发"、"端口映射"、"Port Forwarding"

### 3. 添加端口转发规则
```
服务名称: exam_site_backend_api
协议类型: TCP
外部端口: 8000
内部IP地址: {local_ip}
内部端口: 8000
```

### 4. 保存设置
- 点击"保存"或"应用"
- 等待路由器重启（如果需要）

## 🧪 测试连接

### 1. 测试本地连接
```bash
curl http://{local_ip}:8000/
```

### 2. 测试公网连接
```bash
curl http://{public_ip or "你的公网IP"}:8000/
```

## 📱 分享给队友的信息

### 前端端配置
```javascript
// 在项目配置文件中设置
const API_BASE_URL = 'http://{public_ip or "你的公网IP"}:8000';

// 或者使用本地IP（如果在内网）
const API_BASE_URL = 'http://{local_ip}:8000';
```

### 微信小程序端配置
在微信开发者工具中设置服务器域名：
- **request合法域名**: http://{public_ip or "你的公网IP"}:8000
- **socket合法域名**: ws://{public_ip or "你的公网IP"}:8000

## 🚨 注意事项

### 1. 安全考虑
- 确保API有适当的认证机制
- 考虑使用HTTPS（需要SSL证书）
- 定期检查访问日志

### 2. 网络稳定性
- 确保路由器24小时运行
- 考虑设置DDNS（动态域名解析）
- 备份路由器配置

### 3. 故障排除
- 检查防火墙设置
- 确认端口转发规则正确
- 测试网络连接

## 📞 常见问题

### Q: 外部无法访问
A: 检查以下几点：
1. 端口转发规则是否正确
2. 防火墙是否阻止了连接
3. ISP是否封锁了端口

### Q: 地址经常变化
A: 解决方案：
1. 设置静态IP地址
2. 使用DDNS服务
3. 使用固定IP（联系ISP）

### Q: 连接不稳定
A: 可能原因：
1. 网络带宽不足
2. 路由器性能问题
3. 网络干扰

## 🔄 动态IP解决方案

如果你的公网IP经常变化，建议：

### 1. 使用DDNS服务
- 注册DDNS账号（如花生壳、3322.org）
- 在路由器中配置DDNS
- 使用固定域名访问

### 2. 使用内网穿透工具
- ngrok（免费版地址会变化）
- cpolar（国内服务）
- frp（自建服务器）

## 📊 监控工具

### 1. 网络状态监控
```bash
# 检查端口是否开放
telnet {public_ip or "你的公网IP"} 8000

# 检查服务状态
curl -I http://{public_ip or "你的公网IP"}:8000/
```

### 2. 日志监控
- 查看API访问日志
- 监控网络流量
- 检查错误日志

## 🎯 最佳实践

1. **定期备份**: 备份路由器配置
2. **安全加固**: 使用强密码，定期更新
3. **监控告警**: 设置网络监控
4. **文档记录**: 记录配置步骤和问题解决方案

---
*配置完成后，请将公网地址分享给前端和微信小程序端队友*
"""
    
    with open("ROUTER_PORT_FORWARD_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    
    print("📄 路由器配置指南已生成: ROUTER_PORT_FORWARD_GUIDE.md")
    return local_ip, public_ip

def test_api_accessibility():
    """测试API可访问性"""
    local_ip = get_local_ip()
    public_ip = get_public_ip()
    
    print("\n🧪 测试API可访问性")
    print("=" * 50)
    
    # 测试本地访问
    if local_ip:
        print(f"🔍 测试本地访问: http://{local_ip}:8000/")
        try:
            response = requests.get(f"http://{local_ip}:8000/", timeout=5)
            if response.status_code == 200:
                print("✅ 本地访问正常")
            else:
                print(f"❌ 本地访问失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 本地访问失败: {e}")
    
    # 测试公网访问
    if public_ip:
        print(f"🔍 测试公网访问: http://{public_ip}:8000/")
        try:
            response = requests.get(f"http://{public_ip}:8000/", timeout=10)
            if response.status_code == 200:
                print("✅ 公网访问正常")
            else:
                print(f"❌ 公网访问失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 公网访问失败: {e}")
            print("💡 这可能是因为端口转发未配置或ISP封锁了端口")

def create_team_communication_info(local_ip, public_ip):
    """创建团队沟通信息"""
    info_content = f"""
# 🎯 团队沟通信息

## 📱 分享给前端和微信小程序端的信息

### API基础信息
- **本地地址**: http://{local_ip}:8000
- **公网地址**: http://{public_ip or "待配置"}:8000
- **API文档**: http://{public_ip or local_ip}:8000/docs
- **测试接口**: http://{public_ip or local_ip}:8000/test

### 认证信息
- **测试用户**: admin@exam.com
- **测试密码**: admin123
- **登录接口**: POST /auth/jwt/login

### 主要接口
1. **认证接口**
   - POST /auth/jwt/login - JWT登录
   - POST /simple-login - 简化登录（测试用）

2. **考生管理**
   - GET /candidates/ - 获取考生列表
   - POST /candidates/ - 创建考生
   - POST /candidates/batch-import - 批量导入

3. **考试产品**
   - GET /exam-products/ - 获取考试产品列表
   - POST /exam-products/ - 创建考试产品

4. **排期管理**
   - GET /schedules/ - 获取排期列表
   - POST /schedules/ - 创建排期
   - POST /schedules/scan-check-in - 扫码签到

5. **机构管理**
   - GET /simple-institutions/ - 获取机构列表
   - POST /simple-institutions/ - 创建机构

### 微信小程序配置
在微信开发者工具中设置：
- **request合法域名**: http://{public_ip or local_ip}:8000
- **socket合法域名**: ws://{public_ip or local_ip}:8000

### 前端配置
```javascript
// 配置API基础地址
const API_BASE_URL = 'http://{public_ip or local_ip}:8000';

// 请求示例
fetch(`${API_BASE_URL}/candidates/`, {{
  method: 'GET',
  headers: {{
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
  }}
}});
```

### 测试工具
- **Postman**: 导入项目中的Postman集合
- **curl**: 使用命令行测试
- **浏览器**: 直接访问API文档

### 问题反馈
如果遇到问题，请提供：
1. 请求的URL和参数
2. 错误响应内容
3. 网络面板的详细信息
4. 复现步骤

### 联系方式
- 后端开发: [你的联系方式]
- 技术支持: [技术负责人联系方式]

---
*请将此信息分享给前端和微信小程序端队友*
"""
    
    with open("TEAM_COMMUNICATION_INFO.md", "w", encoding="utf-8") as f:
        f.write(info_content)
    
    print("📄 团队沟通信息已生成: TEAM_COMMUNICATION_INFO.md")

def main():
    """主函数"""
    print("🚀 路由器映射配置工具")
    print("=" * 50)
    
    # 创建配置指南
    local_ip, public_ip = create_router_config_guide()
    
    # 测试API可访问性
    test_api_accessibility()
    
    # 创建团队沟通信息
    create_team_communication_info(local_ip, public_ip)
    
    print("\n🎉 配置完成！")
    print("\n📋 下一步操作：")
    print("1. 查看 ROUTER_PORT_FORWARD_GUIDE.md 配置路由器")
    print("2. 查看 TEAM_COMMUNICATION_INFO.md 分享给队友")
    print("3. 测试公网访问是否正常")
    print("4. 通知前端和微信小程序端开始联调")

if __name__ == "__main__":
    main() 