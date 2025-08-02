# 🚀 简单API测试指南

## 📋 测试准备

### 1. 启动服务器
```bash
cd exam_site_backend
python start_dev.py
```

### 2. 检查服务器状态
访问：http://localhost:8000/docs

## 🔐 认证测试

### 1. 管理员登录
**请求：**
```
POST http://localhost:8000/auth/jwt/login
Content-Type: application/x-www-form-urlencoded

username=admin@exam.com&password=admin123
```

**预期响应：**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**测试要点：**
- 状态码：200
- 包含access_token字段
- token_type为"bearer"

### 2. 用户登录
**请求：**
```
POST http://localhost:8000/auth/jwt/login
Content-Type: application/x-www-form-urlencoded

username=user@exam.com&password=user123
```

**预期响应：**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## 🏢 机构管理测试

### 1. 创建机构
**请求：**
```
POST http://localhost:8000/institutions
Authorization: Bearer YOUR_ADMIN_TOKEN
Content-Type: application/json

{
  "name": "测试机构",
  "code": "TEST001",
  "contact_person": "张三",
  "phone": "13800138000",
  "email": "contact@test.com",
  "address": "北京市朝阳区",
  "description": "测试机构描述",
  "status": "active",
  "license_number": "LIC001",
  "business_scope": "考试服务",
  "admin_username": "admin_test",
  "admin_email": "admin@test.com",
  "admin_password": "password123"
}
```

**预期响应：**
```json
{
  "id": 1,
  "name": "测试机构",
  "code": "TEST001",
  "status": "active",
  "created_at": "2024-01-01T00:00:00Z"
}
```

**测试要点：**
- 状态码：201
- 返回机构ID
- 包含创建时间

### 2. 获取机构列表
**请求：**
```
GET http://localhost:8000/institutions?page=1&size=10
Authorization: Bearer YOUR_ADMIN_TOKEN
```

**预期响应：**
```json
{
  "items": [
    {
      "id": 1,
      "name": "测试机构",
      "code": "TEST001",
      "status": "active"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 10,
  "pages": 1
}
```

**测试要点：**
- 状态码：200
- 分页信息正确
- 数据格式正确

### 3. 获取机构详情
**请求：**
```
GET http://localhost:8000/institutions/1
Authorization: Bearer YOUR_ADMIN_TOKEN
```

**预期响应：**
```json
{
  "id": 1,
  "name": "测试机构",
  "code": "TEST001",
  "contact_person": "张三",
  "phone": "13800138000",
  "email": "contact@test.com",
  "address": "北京市朝阳区",
  "description": "测试机构描述",
  "status": "active",
  "license_number": "LIC001",
  "business_scope": "考试服务",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### 4. 更新机构信息
**请求：**
```
PUT http://localhost:8000/institutions/1
Authorization: Bearer YOUR_ADMIN_TOKEN
Content-Type: application/json

{
  "name": "更新后的机构名称",
  "contact_person": "李四",
  "phone": "13900139000",
  "email": "updated@test.com"
}
```

**预期响应：**
```json
{
  "id": 1,
  "name": "更新后的机构名称",
  "contact_person": "李四",
  "phone": "13900139000",
  "email": "updated@test.com",
  "status": "active"
}
```

### 5. 删除机构
**请求：**
```
DELETE http://localhost:8000/institutions/1
Authorization: Bearer YOUR_ADMIN_TOKEN
```

**预期响应：**
```json
{
  "message": "机构删除成功"
}
```

## 📚 考试产品测试

### 1. 创建考试产品
**请求：**
```
POST http://localhost:8000/exam-products
Authorization: Bearer YOUR_ADMIN_TOKEN
Content-Type: application/json

{
  "name": "无人机驾驶员考试",
  "description": "无人机驾驶员理论考试",
  "category": "无人机",
  "duration": 120,
  "pass_score": 80,
  "status": "active"
}
```

**预期响应：**
```json
{
  "id": 1,
  "name": "无人机驾驶员考试",
  "category": "无人机",
  "status": "active",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### 2. 获取考试产品列表
**请求：**
```
GET http://localhost:8000/exam-products?page=1&size=10
Authorization: Bearer YOUR_ADMIN_TOKEN
```

**预期响应：**
```json
{
  "items": [
    {
      "id": 1,
      "name": "无人机驾驶员考试",
      "category": "无人机",
      "status": "active"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 10,
  "pages": 1
}
```

### 3. 获取考试产品详情
**请求：**
```
GET http://localhost:8000/exam-products/1
Authorization: Bearer YOUR_ADMIN_TOKEN
```

### 4. 更新考试产品
**请求：**
```
PUT http://localhost:8000/exam-products/1
Authorization: Bearer YOUR_ADMIN_TOKEN
Content-Type: application/json

{
  "name": "更新后的考试产品",
  "description": "更新后的描述",
  "duration": 150,
  "pass_score": 85
}
```

### 5. 删除考试产品
**请求：**
```
DELETE http://localhost:8000/exam-products/1
Authorization: Bearer YOUR_ADMIN_TOKEN
```

## 🏫 考场资源测试

### 1. 创建考场资源
**请求：**
```
POST http://localhost:8000/venues
Authorization: Bearer YOUR_ADMIN_TOKEN
Content-Type: application/json

{
  "name": "考场A",
  "location": "北京市朝阳区",
  "address": "朝阳区某某街道123号",
  "capacity": 50,
  "equipment": "电脑、投影仪",
  "status": "active",
  "description": "标准考场"
}
```

**预期响应：**
```json
{
  "id": 1,
  "name": "考场A",
  "location": "北京市朝阳区",
  "capacity": 50,
  "status": "active",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### 2. 获取考场资源列表
**请求：**
```
GET http://localhost:8000/venues?page=1&size=10
Authorization: Bearer YOUR_ADMIN_TOKEN
```

### 3. 获取考场资源详情
**请求：**
```
GET http://localhost:8000/venues/1
Authorization: Bearer YOUR_ADMIN_TOKEN
```

### 4. 更新考场资源
**请求：**
```
PUT http://localhost:8000/venues/1
Authorization: Bearer YOUR_ADMIN_TOKEN
Content-Type: application/json

{
  "name": "更新后的考场名称",
  "capacity": 60,
  "equipment": "电脑、投影仪、监控设备"
}
```

### 5. 删除考场资源
**请求：**
```
DELETE http://localhost:8000/venues/1
Authorization: Bearer YOUR_ADMIN_TOKEN
```

## 🔒 权限测试

### 1. 无权限访问测试
**请求：**
```
GET http://localhost:8000/institutions
Authorization: Bearer invalid_token
```

**预期响应：**
```json
{
  "detail": "Could not validate credentials"
}
```

**测试要点：**
- 状态码：401
- 返回认证错误信息

### 2. 无Token访问测试
**请求：**
```
GET http://localhost:8000/institutions
```

**预期响应：**
```json
{
  "detail": "Not authenticated"
}
```

**测试要点：**
- 状态码：401
- 返回未认证错误

### 3. 普通用户访问管理员接口
**请求：**
```
POST http://localhost:8000/institutions
Authorization: Bearer USER_TOKEN
Content-Type: application/json

{
  "name": "测试机构"
}
```

**预期响应：**
```json
{
  "detail": "权限不足"
}
```

**测试要点：**
- 状态码：403
- 返回权限不足错误

## 📊 测试检查清单

### 认证测试
- [ ] 管理员登录成功
- [ ] 用户登录成功
- [ ] 无效凭据返回401
- [ ] Token格式正确

### 机构管理测试
- [ ] 创建机构成功
- [ ] 获取机构列表成功
- [ ] 获取机构详情成功
- [ ] 更新机构信息成功
- [ ] 删除机构成功

### 考试产品测试
- [ ] 创建考试产品成功
- [ ] 获取产品列表成功
- [ ] 获取产品详情成功
- [ ] 更新产品信息成功
- [ ] 删除考试产品成功

### 考场资源测试
- [ ] 创建考场资源成功
- [ ] 获取资源列表成功
- [ ] 获取资源详情成功
- [ ] 更新资源信息成功
- [ ] 删除考场资源成功

### 权限测试
- [ ] 无Token访问返回401
- [ ] 无效Token返回401
- [ ] 权限不足返回403
- [ ] 管理员权限正常

## 🚨 常见问题

### 1. 连接错误
- 检查服务器是否启动
- 确认端口8000可用
- 检查防火墙设置

### 2. 认证错误
- 确认用户凭据正确
- 检查数据库是否初始化
- 验证JWT配置

### 3. 权限错误
- 确认用户角色设置
- 检查接口权限要求
- 验证Token格式

## 📝 测试记录模板

| 接口 | 方法 | 状态码 | 响应时间 | 结果 | 备注 |
|------|------|--------|----------|------|------|
| 管理员登录 | POST | 200 | ___ms | ✅/❌ | |
| 创建机构 | POST | 201 | ___ms | ✅/❌ | |
| 获取机构列表 | GET | 200 | ___ms | ✅/❌ | |
| 创建考试产品 | POST | 201 | ___ms | ✅/❌ | |
| 创建考场资源 | POST | 201 | ___ms | ✅/❌ | |

现在您可以一个一个手动测试这些API了！每个接口都可以独立测试，不需要依赖Postman集合。 