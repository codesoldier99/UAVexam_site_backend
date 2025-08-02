# 🎯 考试系统后端API - 修正版信息

## 📋 当前状态
- ✅ **FastAPI服务**: 运行中 (http://localhost:8000)
- ✅ **API文档**: 可用 (http://localhost:8000/docs)
- ✅ **测试接口**: 可用 (http://localhost:8000/test)
- 🌐 **公网IP**: 45.149.92.22

## 🔧 正确的API接口清单

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

### 机构管理（修正版）
- `GET /institutions/` - 获取机构列表
- `POST /institutions/` - 创建机构
- `GET /institutions/{id}` - 获取机构详情
- `PUT /institutions/{id}` - 更新机构
- `DELETE /institutions/{id}` - 删除机构
- `PATCH /institutions/{id}/status` - 更新机构状态
- `POST /institutions/bulk-status` - 批量更新机构状态

### 场地管理
- `GET /venues/` - 获取场地列表
- `POST /venues/` - 创建场地
- `GET /venues/{id}` - 获取场地详情
- `PUT /venues/{id}` - 更新场地
- `DELETE /venues/{id}` - 删除场地

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

## 📱 前端配置信息

### 微信小程序端配置
在微信开发者工具中设置服务器域名：
- **request合法域名**: http://45.149.92.22:8000
- **socket合法域名**: ws://45.149.92.22:8000

### 前端端配置
在项目配置文件中设置API基础地址：
```javascript
const BASE_URL = 'http://45.149.92.22:8000'
```

## 🚨 重要说明

### 机构API路由说明
- **正式API**: `/institutions/*` - 完整功能，有权限控制
- **简化API**: `/simple-institutions/*` - 测试用，简化版本

**建议使用正式API**: `/institutions/*`

### 权限要求
- 机构管理需要相应的权限
- 考生管理需要相应的权限
- 考试产品管理需要相应的权限
- 排期管理需要相应的权限

## 📞 沟通流程

### 1. 主动同步进度
当完成一个模块的API时，主动在群里@前端：
```
@前端 机构管理模块的API已经可以使用了！

📋 可用接口：
- GET /institutions/ - 获取机构列表
- POST /institutions/ - 创建机构
- GET /institutions/{id} - 获取机构详情
- PUT /institutions/{id} - 更新机构
- DELETE /institutions/{id} - 删除机构
- PATCH /institutions/{id}/status - 更新机构状态

🧪 测试数据格式：
创建机构:
{
  "name": "测试机构",
  "code": "TEST001",
  "contact_person": "联系人",
  "phone": "13800138000",
  "email": "test@example.com",
  "address": "测试地址",
  "description": "测试描述",
  "license_number": "LIC001",
  "business_scope": "考试培训"
}

请测试一下，有问题及时反馈！
```

### 2. 清晰地响应问题
当前端反馈接口有问题时，第一时间让他提供：
- **请求的URL**: 完整的接口地址
- **请求参数**: 请求体、查询参数、请求头
- **Network面板里的响应内容**: 状态码、响应体、错误信息

## 💡 下一步行动

1. **配置路由器端口映射**（推荐）
2. **使用正确的API地址**: `/institutions/*`
3. **开始API联调测试**
4. **主动同步每个模块的进度**

---

**感谢你的提醒！** 使用正确的API地址很重要。🎯 