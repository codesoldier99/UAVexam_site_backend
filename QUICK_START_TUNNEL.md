# 🚀 快速启动内网穿透指南

## 方法一：使用批处理脚本（推荐）

1. **双击运行** `start_tunnel.bat`
2. **等待启动**，会自动安装ngrok并启动隧道
3. **查看地址**，在ngrok窗口中找到公网地址

## 方法二：手动启动

### 1. 启动FastAPI服务
```bash
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. 安装ngrok（如果未安装）
```bash
winget install Ngrok.Ngrok
```

### 3. 启动ngrok隧道
```bash
ngrok http 8000
```

### 4. 获取公网地址
在ngrok窗口中，你会看到类似这样的信息：
```
Forwarding    https://abc123.ngrok.io -> http://localhost:8000
```

## 📋 分享给队友的信息

### 基础信息
```
🎯 API联调地址
基础地址: https://abc123.ngrok.io
API文档: https://abc123.ngrok.io/docs
测试接口: https://abc123.ngrok.io/test
```

### 微信小程序端配置
```
📱 微信小程序端配置
在微信开发者工具中设置服务器域名：
- request合法域名: https://abc123.ngrok.io
- socket合法域名: wss://abc123.ngrok.io
```

### 前端端配置
```
💻 前端端配置
在项目配置文件中设置API基础地址：
BASE_URL = 'https://abc123.ngrok.io'
```

## 🔧 测试连接

### 1. 测试根接口
```bash
curl https://abc123.ngrok.io/
```

### 2. 测试API文档
在浏览器中访问：`https://abc123.ngrok.io/docs`

### 3. 测试简化登录
```bash
curl -X POST https://abc123.ngrok.io/simple-login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@exam.com","email":"admin@exam.com","password":"admin123"}'
```

## ⚠️ 注意事项

1. **地址变化**：免费版ngrok每次重启地址会变化
2. **稳定性**：确保ngrok和FastAPI服务都正常运行
3. **防火墙**：确保端口8000没有被防火墙阻止
4. **网络**：确保网络连接正常

## 🚨 常见问题

### 1. ngrok启动失败
- 检查网络连接
- 确认端口8000未被占用
- 尝试重启ngrok

### 2. 连接超时
- 检查FastAPI服务是否正常运行
- 确认防火墙设置
- 验证网络连接

### 3. 地址无法访问
- 检查ngrok是否正常运行
- 确认地址是否正确
- 尝试重新启动隧道

## 📞 技术支持

如果遇到问题，请：
1. 检查错误信息
2. 重启相关服务
3. 联系后端开发人员

---

**快速命令**
```bash
# 启动服务
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# 启动隧道
ngrok http 8000

# 测试连接
curl https://你的ngrok地址/
``` 