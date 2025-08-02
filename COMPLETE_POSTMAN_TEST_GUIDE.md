# 🚀 Postman测试指南 - 考试系统后端API

## 📋 第一步：导入文件

### 导入集合文件
1. 打开Postman
2. 点击 "Import" 按钮
3. 选择 `exam_site_backend.postman_collection.json` 文件

### 导入环境文件
1. 再次点击 "Import" 按钮
2. 选择 `exam_site_backend.postman_environment.json` 文件
3. 在右上角选择 "Exam Site Backend Environment" 环境

## 🔧 第二步：环境配置

环境变量已自动配置：
- `base_url`: http://localhost:8000
- `admin_token`: (登录后自动设置)
- `user_token`: (登录后自动设置)
- `admin_email`: admin@exam.com
- `admin_password`: admin123

## 🚀 第三步：启动服务器

在开始测试前，请确保服务器已启动：

```bash
cd exam_site_backend
python start_dev.py
```

## 📝 第四步：开始测试

### 1. 认证测试

#### 1.1 管理员登录
**请求：**
```
POST {{base_url}}/auth/jwt/login
Content-Type: application/x-www-form-urlencoded

username={{admin_email}}&password={{admin_password}}
```

**预期响应：**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**测试脚本：**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has access token", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('access_token');
});

if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("admin_token", jsonData.access_token);
}
```

### 2. 机构管理测试

#### 2.1 创建机构
**请求：**
```
POST {{base_url}}/institutions
Authorization: Bearer {{admin_token}}
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

#### 2.2 获取机构列表
**请求：**
```
GET {{base_url}}/institutions?page=1&size=10
Authorization: Bearer {{admin_token}}
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

### 3. 考试产品测试

#### 3.1 创建考试产品
**请求：**
```
POST {{base_url}}/exam-products
Authorization: Bearer {{admin_token}}
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

### 4. 考场资源测试

#### 4.1 创建考场资源
**请求：**
```
POST {{base_url}}/venues
Authorization: Bearer {{admin_token}}
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

## ✅ 测试检查点

### 成功响应检查
- **状态码**: 200 (成功), 201 (创建成功)
- **响应格式**: JSON格式正确
- **数据完整性**: 返回数据包含必要字段

### 错误响应检查
- **401 Unauthorized**: Token无效或过期
- **403 Forbidden**: 权限不足
- **404 Not Found**: 资源不存在
- **422 Validation Error**: 数据验证失败

## 🔒 权限测试

### 测试无权限访问
使用普通用户token访问管理员接口
**预期响应：** 403 Forbidden

### 测试无效Token
使用错误的token
**预期响应：** 401 Unauthorized

## 📊 测试报告模板

| 功能模块 | 测试用例 | 状态 | 响应时间 | 备注 |
|----------|----------|------|----------|------|
| 认证管理 | 管理员登录 | ✅ | 200ms | 正常 |
| 机构管理 | 创建机构 | ✅ | 300ms | 正常 |
| 机构管理 | 查询列表 | ✅ | 150ms | 正常 |
| 考试产品 | 创建产品 | ✅ | 250ms | 正常 |
| 考场资源 | 创建资源 | ✅ | 280ms | 正常 |

## 🚨 常见问题解决

### 1. 连接错误
- 检查服务器是否启动：`python start_dev.py`
- 检查端口是否正确：`http://localhost:8000`
- 检查防火墙设置

### 2. 认证错误
- 确保先执行管理员登录
- 检查token格式：`Bearer YOUR_TOKEN`
- 验证token是否过期

### 3. 权限错误
- 确认用户角色和权限
- 检查接口权限要求
- 验证token中的权限信息

## 🎯 测试目标

### 功能完整性
- ✅ 所有CRUD操作正常
- ✅ 权限控制有效
- ✅ 数据验证正确

### 接口规范
- ✅ RESTful API设计
- ✅ 标准HTTP状态码
- ✅ 统一响应格式

### 安全性
- ✅ JWT认证有效
- ✅ 权限检查正确
- ✅ 数据保护到位

## 📋 测试前检查清单

开始测试前，请确保：
- ✅ 服务器已启动 (`python start_dev.py`)
- ✅ 数据库已初始化
- ✅ Postman已安装并导入文件
- ✅ 环境变量已配置

## 🚀 测试顺序建议

1. 🔐 **认证测试**
   - 管理员登录
   - 用户登录
   - Token验证

2. 🏢 **机构管理测试**
   - 创建机构
   - 查询机构列表
   - 更新机构信息
   - 删除机构

3. 📚 **考试产品测试**
   - 创建考试产品
   - 查询产品列表
   - 更新产品信息
   - 删除产品

4. 🏫 **考场资源测试**
   - 创建考场资源
   - 查询资源列表
   - 更新资源信息
   - 删除资源

5. 🔒 **权限测试**
   - 无权限访问测试
   - 无效Token测试
   - 过期Token测试

## 📞 技术支持

如果在测试过程中遇到问题，请检查：
1. 服务器日志输出
2. 数据库连接状态
3. 网络连接情况
4. Postman环境配置

现在您可以开始使用Postman进行测试了！如果遇到任何问题，请告诉我。 