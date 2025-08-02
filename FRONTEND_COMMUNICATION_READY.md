# 🎯 考试系统后端API - 前端联调信息

## 📋 当前状态
- ✅ FastAPI服务: 运行中
- 🌐 本地地址: http://localhost:8000
- 📚 API文档: http://localhost:8000/docs
- 🧪 测试接口: http://localhost:8000/test

## 🌐 内网穿透地址
**公网IP**: 45.149.92.22  
**访问地址**: http://45.149.92.22:8000

⚠️ **注意**: 需要配置路由器端口映射才能从外网访问

## 📱 微信小程序端配置
在微信开发者工具中设置服务器域名：
- **request合法域名**: http://45.149.92.22:8000
- **socket合法域名**: ws://45.149.92.22:8000

## 💻 前端端配置
在项目配置文件中设置API基础地址：
```javascript
// 前端配置文件
const BASE_URL = 'http://45.149.92.22:8000'
```

## 🔧 API接口清单

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

## 🚨 常见问题

### 1. 连接失败
- 检查FastAPI服务是否启动
- 确认防火墙设置
- 验证网络连接

### 2. 认证失败
- 检查token格式是否正确
- 确认token是否过期
- 验证请求头格式

### 3. 数据格式错误
- 检查Content-Type是否为application/json
- 验证请求体JSON格式
- 确认必填字段是否完整

## 📞 沟通渠道

### 即时沟通
- 微信群: 考试系统开发群
- 钉钉群: 考试系统后端联调群

### 文档共享
- API文档: http://localhost:8000/docs
- 项目文档: 项目根目录/docs
- 测试报告: 项目根目录/test_reports

### 问题反馈
1. 在群里@后端开发人员
2. 提供详细的错误信息
3. 附上请求和响应数据
4. 说明复现步骤

## 🔄 开发流程

### 1. 接口开发
- 后端开发新接口
- 编写测试用例
- 更新API文档
- 通知前端和小程序端

### 2. 联调测试
- 启动内网穿透
- 分享地址给队友
- 协助调试问题
- 记录问题和解决方案

### 3. 问题处理
- 及时响应队友问题
- 提供详细的错误信息
- 协助排查问题原因
- 更新相关文档

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

---

## 💡 下一步行动

1. **配置路由器端口映射**（推荐）
   - 将外网端口映射到本机的8000端口
   - 这样前端就可以通过公网IP访问API

2. **或使用内网穿透工具**
   - ngrok（需要注册获取token）
   - cpolar: https://www.cpolar.com/
   - frp: https://github.com/fatedier/frp
   - natapp: https://natapp.cn/

3. **开始API联调测试**
   - 先测试公开接口
   - 再测试认证接口
   - 最后测试业务接口

4. **主动同步进度**
   - 当完成一个模块的API时，主动在群里@前端
   - 告诉他"XX模块的API已经可以使用了"

5. **清晰地响应问题**
   - 当前端反馈接口有问题时，第一时间让他提供：
     - 请求的URL
     - 请求参数
     - Network面板里的响应内容
   - 这能帮你最快地定位问题

---

**联系方式**
- 后端开发: [你的联系方式]
- 技术支持: [技术负责人联系方式]
- 项目文档: [项目文档地址] 