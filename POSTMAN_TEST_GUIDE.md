# Postman 测试指南

## 🚀 快速开始

### 1. 环境配置

#### 创建环境变量
在Postman中创建新环境，添加以下变量：

| 变量名 | 初始值 | 描述 |
|--------|--------|------|
| `base_url` | `http://localhost:8000` | API基础URL |
| `admin_token` | (空) | 管理员访问令牌 |
| `user_token` | (空) | 普通用户访问令牌 |

### 2. 认证流程

#### 步骤1：管理员登录
```
POST {{base_url}}/auth/jwt/login
Content-Type: application/x-www-form-urlencoded

username=admin@exam.com&password=admin123
```

**响应示例：**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 步骤2：设置环境变量
在响应中添加脚本：
```javascript
pm.environment.set("admin_token", pm.response.json().access_token);
```

## 📋 测试集合

### 1. 机构管理测试

#### 1.1 获取机构列表
```
GET {{base_url}}/institutions?page=1&size=10
Authorization: Bearer {{admin_token}}
```

#### 1.2 创建新机构
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

#### 1.3 获取机构详情
```
GET {{base_url}}/institutions/1
Authorization: Bearer {{admin_token}}
```

#### 1.4 更新机构信息
```
PUT {{base_url}}/institutions/1
Authorization: Bearer {{admin_token}}
Content-Type: application/json

{
  "name": "更新后的机构名称",
  "contact_person": "李四",
  "phone": "13900139000",
  "email": "updated@test.com"
}
```

#### 1.5 删除机构
```
DELETE {{base_url}}/institutions/1
Authorization: Bearer {{admin_token}}
```

#### 1.6 获取机构统计信息
```
GET {{base_url}}/institutions/stats
Authorization: Bearer {{admin_token}}
```

### 2. 考试产品管理测试

#### 2.1 获取考试产品列表
```
GET {{base_url}}/exam-products?page=1&size=10
Authorization: Bearer {{admin_token}}
```

#### 2.2 创建考试产品
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

#### 2.3 获取考试产品详情
```
GET {{base_url}}/exam-products/1
Authorization: Bearer {{admin_token}}
```

#### 2.4 更新考试产品
```
PUT {{base_url}}/exam-products/1
Authorization: Bearer {{admin_token}}
Content-Type: application/json

{
  "name": "更新后的考试产品",
  "description": "更新后的描述",
  "duration": 150,
  "pass_score": 85
}
```

#### 2.5 删除考试产品
```
DELETE {{base_url}}/exam-products/1
Authorization: Bearer {{admin_token}}
```

### 3. 考场资源管理测试

#### 3.1 获取考场资源列表
```
GET {{base_url}}/venues?page=1&size=10
Authorization: Bearer {{admin_token}}
```

#### 3.2 创建考场资源
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

#### 3.3 获取考场资源详情
```
GET {{base_url}}/venues/1
Authorization: Bearer {{admin_token}}
```

#### 3.4 更新考场资源
```
PUT {{base_url}}/venues/1
Authorization: Bearer {{admin_token}}
Content-Type: application/json

{
  "name": "更新后的考场名称",
  "capacity": 60,
  "equipment": "电脑、投影仪、监控设备"
}
```

#### 3.5 删除考场资源
```
DELETE {{base_url}}/venues/1
Authorization: Bearer {{admin_token}}
```

### 4. 用户认证测试

#### 4.1 用户注册
```
POST {{base_url}}/auth/register
Content-Type: application/json

{
  "email": "test@example.com",
  "username": "testuser",
  "password": "testpass123"
}
```

#### 4.2 用户登录
```
POST {{base_url}}/auth/jwt/login
Content-Type: application/x-www-form-urlencoded

username=test@example.com&password=testpass123
```

#### 4.3 获取当前用户信息
```
GET {{base_url}}/users/me
Authorization: Bearer {{user_token}}
```

#### 4.4 获取用户列表
```
GET {{base_url}}/users
Authorization: Bearer {{admin_token}}
```

## 🔧 测试脚本

### 自动设置Token脚本
在登录请求的Tests标签页中添加：

```javascript
// 检查响应状态
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// 检查响应包含token
pm.test("Response has access token", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('access_token');
});

// 自动设置环境变量
if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("admin_token", jsonData.access_token);
}
```

### 权限测试脚本
在需要权限的请求中添加：

```javascript
// 检查权限响应
pm.test("Permission check", function () {
    if (pm.response.code === 403) {
        pm.expect(pm.response.json()).to.have.property('detail');
        console.log("权限不足: " + pm.response.json().detail);
    }
});
```

## 📊 测试用例

### 正常流程测试
1. ✅ 管理员登录
2. ✅ 创建机构
3. ✅ 创建考试产品
4. ✅ 创建考场资源
5. ✅ 查询列表
6. ✅ 更新信息
7. ✅ 删除资源

### 权限测试
1. ✅ 无权限访问（403错误）
2. ✅ 无效token（401错误）
3. ✅ 过期token处理

### 数据验证测试
1. ✅ 必填字段验证
2. ✅ 数据格式验证
3. ✅ 唯一性约束验证

## 🚨 常见问题

### 1. 连接错误
- 检查服务器是否启动：`python start_dev.py`
- 检查端口是否正确：`http://localhost:8000`

### 2. 认证错误
- 确保token格式正确：`Bearer YOUR_TOKEN`
- 检查token是否过期
- 验证用户权限

### 3. 数据验证错误
- 检查请求体格式
- 验证必填字段
- 确认数据格式正确

## 📝 测试报告模板

### 测试结果记录
| 功能模块 | 测试用例 | 状态 | 备注 |
|----------|----------|------|------|
| 机构管理 | 创建机构 | ✅ | 正常 |
| 机构管理 | 查询列表 | ✅ | 正常 |
| 考试产品 | 创建产品 | ✅ | 正常 |
| 考场资源 | 创建资源 | ✅ | 正常 |

### 性能测试
- 响应时间：< 500ms
- 并发用户：10
- 错误率：< 1%

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

---

**开始测试前，请确保：**
1. 服务器已启动
2. 数据库已初始化
3. 环境变量已配置
4. Postman已安装

**测试顺序建议：**
1. 认证测试
2. 机构管理测试
3. 考试产品测试
4. 考场资源测试
5. 权限测试 