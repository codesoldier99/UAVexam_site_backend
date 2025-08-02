# 团队沟通指南 - 考试系统后端API

## 🚀 快速开始

### 1. 启动内网穿透
```bash
# 方法1: 使用批处理脚本（推荐）
双击运行 start_tunnel.bat

# 方法2: 使用Python脚本
python setup_tunnel.py

# 方法3: 手动启动
# 1. 启动FastAPI服务
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# 2. 启动ngrok隧道
ngrok http 8000
```

### 2. 获取公网地址
启动成功后，你会看到类似这样的地址：
```
https://abc123.ngrok.io
```

### 3. 分享给队友
将以下信息发送给前端和微信小程序端队友：

```
🎯 API联调地址
基础地址: https://abc123.ngrok.io
API文档: https://abc123.ngrok.io/docs
测试接口: https://abc123.ngrok.io/test

📱 微信小程序端配置
在微信开发者工具中设置服务器域名：
- request合法域名: https://abc123.ngrok.io
- socket合法域名: wss://abc123.ngrok.io

💻 前端端配置
在项目配置文件中设置API基础地址：
BASE_URL = 'https://abc123.ngrok.io'
```

## 📋 API接口清单

### 公开接口（无需认证）
- `GET /` - 根接口
- `GET /test` - 测试接口
- `GET /docs` - API文档
- `GET /redoc` - 另一种API文档格式

### 认证接口
- `POST /auth/jwt/login` - JWT登录
- `POST /simple-login` - 简化登录（测试用）
- `GET /users/me` - 获取当前用户信息

### 考生管理
- `GET /candidates/` - 获取考生列表
- `POST /candidates/` - 创建考生
- `GET /candidates/{id}` - 获取考生详情
- `PUT /candidates/{id}` - 更新考生信息
- `DELETE /candidates/{id}` - 删除考生
- `POST /candidates/batch-import` - 批量导入考生
- `GET /candidates/template` - 下载导入模板

### 考试产品管理
- `GET /exam-products/` - 获取考试产品列表
- `POST /exam-products/` - 创建考试产品
- `GET /exam-products/{id}` - 获取考试产品详情
- `PUT /exam-products/{id}` - 更新考试产品
- `DELETE /exam-products/{id}` - 删除考试产品

### 排期管理
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

### 机构管理
- `GET /simple-institutions/` - 获取机构列表
- `POST /simple-institutions/` - 创建机构
- `GET /simple-institutions/{id}` - 获取机构详情
- `PUT /simple-institutions/{id}` - 更新机构
- `DELETE /simple-institutions/{id}` - 删除机构

### 微信小程序接口
- `POST /wx-miniprogram/login` - 微信登录
- `GET /wx-miniprogram/user-info` - 获取用户信息
- `POST /wx-miniprogram/check-in` - 微信签到

## 🔐 认证说明

### JWT认证流程
1. 调用登录接口获取token
2. 在后续请求的Header中添加: `Authorization: Bearer <token>`

### 测试用简化登录
```json
POST /simple-login
{
  "username": "admin@exam.com",
  "email": "admin@exam.com",
  "password": "admin123"
}
```

## 📊 数据格式

### 请求格式
- Content-Type: application/json
- 数据格式: JSON

### 响应格式
```json
{
  "status": "success",
  "data": {...},
  "message": "操作成功"
}
```

### 错误响应
```json
{
  "detail": "错误信息"
}
```

## 🛠️ 联调工具推荐

### 1. Postman
- 下载: https://www.postman.com/downloads/
- 用途: API测试和调试
- 优点: 界面友好，功能强大

### 2. Insomnia
- 下载: https://insomnia.rest/download
- 用途: API测试
- 优点: 轻量级，速度快

### 3. curl（命令行）
```bash
# 测试根接口
curl https://abc123.ngrok.io/

# 测试认证接口
curl -X POST https://abc123.ngrok.io/simple-login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@exam.com","email":"admin@exam.com","password":"admin123"}'
```

## 🚨 常见问题

### 1. 连接失败
- 检查ngrok是否正常运行
- 检查FastAPI服务是否启动
- 确认防火墙设置

### 2. 认证失败
- 检查token格式是否正确
- 确认token是否过期
- 验证请求头格式

### 3. 数据格式错误
- 检查Content-Type是否为application/json
- 验证请求体JSON格式
- 确认必填字段是否完整

### 4. 权限不足
- 检查用户角色权限
- 确认是否已正确登录
- 验证token有效性

## 📞 沟通渠道

### 即时沟通
- 微信群: 考试系统开发群
- 钉钉群: 考试系统后端联调群

### 文档共享
- API文档: https://abc123.ngrok.io/docs
- 项目文档: 项目根目录/docs
- 测试报告: 项目根目录/test_reports

### 问题反馈
1. 在群里@后端开发人员
2. 提供详细的错误信息
3. 附上请求和响应数据
4. 说明复现步骤

## 🔄 开发流程

### 1. 接口开发
1. 后端开发新接口
2. 编写测试用例
3. 更新API文档
4. 通知前端和小程序端

### 2. 联调测试
1. 启动内网穿透
2. 分享地址给队友
3. 协助调试问题
4. 记录问题和解决方案

### 3. 问题处理
1. 及时响应队友问题
2. 提供详细的错误信息
3. 协助排查问题原因
4. 更新相关文档

## 📈 性能监控

### 接口响应时间
- 正常: < 500ms
- 警告: 500ms - 2s
- 异常: > 2s

### 错误率监控
- 正常: < 1%
- 警告: 1% - 5%
- 异常: > 5%

## 🎯 最佳实践

### 1. 开发阶段
- 使用简化登录进行测试
- 先测试公开接口
- 逐步测试认证接口
- 及时更新文档

### 2. 联调阶段
- 保持内网穿透稳定运行
- 及时响应队友问题
- 提供详细的错误信息
- 记录常见问题和解决方案

### 3. 测试阶段
- 全面测试所有接口
- 验证数据格式正确性
- 检查权限控制
- 确认错误处理

## 📝 更新日志

### v1.0.0 (2024-01-01)
- 完成基础API开发
- 实现内网穿透功能
- 建立团队沟通机制
- 编写完整API文档

---

**联系方式**
- 后端开发: [你的联系方式]
- 技术支持: [技术负责人联系方式]
- 项目文档: [项目文档地址] 