# 🎯 考试系统后端API - 团队沟通总结

## 📋 当前状态
- ✅ **FastAPI服务**: 运行中 (http://localhost:8000)
- ✅ **API文档**: 可用 (http://localhost:8000/docs)
- ✅ **测试接口**: 可用 (http://localhost:8000/test)
- 🌐 **公网IP**: 45.149.92.22

## 🚀 内网穿透方案

### 方案1: 路由器端口映射（推荐）
- **公网地址**: http://45.149.92.22:8000
- **配置步骤**: 在路由器管理界面将外网端口映射到本机8000端口
- **优点**: 稳定、免费、无限制
- **缺点**: 需要路由器配置权限

### 方案2: cpolar内网穿透（备选）
- **下载地址**: https://www.cpolar.com/download
- **启动命令**: `cpolar http 8000`
- **优点**: 免费、无需认证、简单易用
- **缺点**: 地址会变化

### 方案3: ngrok内网穿透（需要认证）
- **注册地址**: https://dashboard.ngrok.com/signup
- **获取token**: https://dashboard.ngrok.com/get-started/your-authtoken
- **配置命令**: `ngrok config add-authtoken YOUR_TOKEN`
- **启动命令**: `ngrok http 8000`

## 📱 前端配置信息

### 微信小程序端配置
在微信开发者工具中设置服务器域名：
```
request合法域名: http://45.149.92.22:8000
socket合法域名: ws://45.149.92.22:8000
```

### 前端端配置
在项目配置文件中设置API基础地址：
```javascript
const BASE_URL = 'http://45.149.92.22:8000'
```

## 🔧 核心API接口

### 认证接口
- `POST /simple-login` - 简化登录（测试用）
- `POST /auth/jwt/login` - JWT登录
- `GET /users/me` - 获取当前用户信息

### 考生管理
- `GET /candidates/` - 获取考生列表
- `POST /candidates/` - 创建考生
- `GET /candidates/{id}` - 获取考生详情
- `PUT /candidates/{id}` - 更新考生信息
- `DELETE /candidates/{id}` - 删除考生
- `POST /candidates/batch-import` - 批量导入考生

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
- `POST /schedules/scan-check-in` - 扫码签到

### 机构管理
- `GET /simple-institutions/` - 获取机构列表
- `POST /simple-institutions/` - 创建机构
- `GET /simple-institutions/{id}` - 获取机构详情
- `PUT /simple-institutions/{id}` - 更新机构
- `DELETE /simple-institutions/{id}` - 删除机构

## 🔐 认证说明

### 测试用简化登录
```json
POST /simple-login
{
  "username": "admin@exam.com",
  "email": "admin@exam.com",
  "password": "admin123"
}
```

### JWT认证流程
1. 调用登录接口获取token
2. 在后续请求的Header中添加: `Authorization: Bearer <token>`

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

## 🛠️ 测试命令

### 基础测试
```bash
# 测试根接口
curl http://45.149.92.22:8000/

# 测试简化登录
curl -X POST http://45.149.92.22:8000/simple-login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@exam.com","email":"admin@exam.com","password":"admin123"}'
```

## 📞 沟通流程

### 1. 主动同步进度
当完成一个模块的API时，主动在群里@前端：
```
@前端 机构管理的API已经可以使用了
- 获取机构列表: GET /simple-institutions/
- 创建机构: POST /simple-institutions/
- 更新机构: PUT /simple-institutions/{id}
- 删除机构: DELETE /simple-institutions/{id}
```

### 2. 清晰地响应问题
当前端反馈接口有问题时，第一时间让他提供：
- **请求的URL**: 完整的接口地址
- **请求参数**: 请求体、查询参数、请求头
- **Network面板里的响应内容**: 状态码、响应体、错误信息

### 3. 问题排查步骤
1. 检查FastAPI服务是否正常运行
2. 验证内网穿透是否正常工作
3. 确认请求格式是否正确
4. 检查数据库连接是否正常
5. 查看服务器日志获取详细错误信息

## 🚨 常见问题

### 1. 连接失败
- 检查FastAPI服务是否启动
- 确认防火墙设置
- 验证网络连接
- 检查内网穿透是否正常工作

### 2. 认证失败
- 检查token格式是否正确
- 确认token是否过期
- 验证请求头格式
- 确认用户权限

### 3. 数据格式错误
- 检查Content-Type是否为application/json
- 验证请求体JSON格式
- 确认必填字段是否完整
- 检查字段类型是否正确

## 📈 性能监控

### 接口响应时间
- 正常: < 500ms
- 警告: 500ms - 2s
- 异常: > 2s

### 错误率监控
- 正常: < 1%
- 警告: 1% - 5%
- 异常: > 5%

## 🎯 下一步行动

1. **配置路由器端口映射**（推荐）
   - 将外网端口映射到本机的8000端口
   - 这样前端就可以通过公网IP访问API

2. **开始API联调测试**
   - 先测试公开接口
   - 再测试认证接口
   - 最后测试业务接口

3. **主动同步进度**
   - 当完成一个模块的API时，主动在群里@前端
   - 告诉他"XX模块的API已经可以使用了"

4. **清晰地响应问题**
   - 当前端反馈接口有问题时，第一时间让他提供：
     - 请求的URL
     - 请求参数
     - Network面板里的响应内容
   - 这能帮你最快地定位问题

---

## 📄 相关文档
- [完整API文档](FRONTEND_COMMUNICATION_READY.md)
- [团队沟通指南](TEAM_COMMUNICATION_GUIDE.md)
- [快速启动指南](QUICK_START_TUNNEL.md)

**联系方式**
- 后端开发: [你的联系方式]
- 技术支持: [技术负责人联系方式]
- 项目文档: [项目文档地址] 