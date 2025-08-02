# 机构与资源管理API测试指南

## 📋 测试概述

本指南提供了三个独立的测试脚本，用于测试机构与资源管理的所有API端点：

1. **机构管理测试** - `test_institutions_only.py`
2. **考试产品管理测试** - `test_exam_products_only.py`  
3. **考场资源管理测试** - `test_venues_only.py`

## 🚀 快速开始

### 1. 启动服务器

首先确保API服务器正在运行：

```bash
# 启动数据库
docker-compose up -d db

# 等待数据库启动
Start-Sleep 15

# 运行数据库迁移
alembic upgrade head

# 启动API服务器
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 运行测试

#### 测试机构管理
```bash
python test_institutions_only.py
```

#### 测试考试产品管理
```bash
python test_exam_products_only.py
```

#### 测试考场资源管理
```bash
python test_venues_only.py
```

## 📊 API端点测试清单

### 3.1 机构管理 (Institutions)

| 功能 | 方法 | 路径 | 状态码 | 说明 |
|------|------|------|--------|------|
| 管理员登录 | POST | `/auth/jwt/login` | 200 | 获取JWT Token |
| 创建机构 | POST | `/institutions` | 201 | 创建新机构 |
| 查询机构列表 | GET | `/institutions?page=1&size=10` | 200 | 支持分页查询 |
| 查询机构详情 | GET | `/institutions/{id}` | 200 | 获取单个机构信息 |
| 更新机构信息 | PUT | `/institutions/{id}` | 200 | 更新机构基本信息 |
| 获取机构统计 | GET | `/institutions/stats` | 200 | 获取统计信息 |
| 删除机构 | DELETE | `/institutions/{id}` | 204 | 逻辑删除机构 |

### 3.2 考试产品管理 (Exam Products)

| 功能 | 方法 | 路径 | 状态码 | 说明 |
|------|------|------|--------|------|
| 创建考试产品 | POST | `/exam-products` | 201 | 创建新产品 |
| 查询产品列表 | GET | `/exam-products?page=1&size=10` | 200 | 支持分页查询 |
| 查询产品详情 | GET | `/exam-products/{id}` | 200 | 获取产品详细信息 |
| 更新产品信息 | PUT | `/exam-products/{id}` | 200 | 更新产品信息 |
| 删除产品 | DELETE | `/exam-products/{id}` | 204 | 删除产品 |

### 3.3 考场资源管理 (Venues)

| 功能 | 方法 | 路径 | 状态码 | 说明 |
|------|------|------|--------|------|
| 创建考场资源 | POST | `/venues` | 201 | 创建新考场 |
| 查询考场列表 | GET | `/venues?page=1&size=10` | 200 | 支持分页查询 |
| 查询考场详情 | GET | `/venues/{id}` | 200 | 获取考场详细信息 |
| 更新考场信息 | PUT | `/venues/{id}` | 200 | 更新考场信息 |
| 删除考场 | DELETE | `/venues/{id}` | 204 | 删除考场 |

## 🔐 权限说明

- **机构管理**: 仅"超级管理员"可操作
- **考试产品管理**: "超级管理员"或"考务管理员"可操作
- **考场资源管理**: "超级管理员"或"考务管理员"可操作

## 📝 测试数据示例

### 机构数据
```json
{
  "name": "测试机构A",
  "code": "TEST001",
  "contact_person": "张三",
  "phone": "13800138001",
  "email": "test@example.com",
  "address": "北京市朝阳区测试街道123号",
  "description": "这是一个测试机构",
  "status": "active"
}
```

### 考试产品数据
```json
{
  "name": "Python编程基础考试",
  "code": "PYTHON001",
  "description": "Python编程基础知识和技能测试",
  "duration_minutes": 120,
  "pass_score": 60,
  "max_score": 100,
  "price": 299.00,
  "status": "active",
  "category": "编程语言",
  "difficulty_level": "初级"
}
```

### 考场资源数据
```json
{
  "name": "北京朝阳考场",
  "code": "BJ001",
  "address": "北京市朝阳区建国路88号",
  "capacity": 100,
  "description": "现代化考场，设备齐全",
  "contact_person": "王五",
  "contact_phone": "010-12345678",
  "status": "active",
  "venue_type": "标准考场",
  "facilities": "电脑、投影仪、音响设备"
}
```

## 🧪 手动测试步骤

### 使用Postman测试

1. **导入环境变量**
   - 设置 `base_url` = `http://localhost:8000`
   - 设置 `admin_token` = 登录后获取的token

2. **登录获取Token**
   ```
   POST {{base_url}}/auth/jwt/login
   Content-Type: application/x-www-form-urlencoded
   
   username=admin@exam.com&password=admin123
   ```

3. **设置Authorization Header**
   ```
   Authorization: Bearer {{admin_token}}
   ```

4. **逐个测试API端点**

## 🔍 故障排除

### 常见问题

1. **连接错误**
   - 检查服务器是否启动
   - 确认端口8000是否可用

2. **认证失败**
   - 确认管理员账号存在
   - 检查密码是否正确

3. **数据库错误**
   - 检查Docker容器状态
   - 确认数据库迁移已执行

4. **权限错误**
   - 确认用户具有相应权限
   - 检查JWT Token是否有效

### 重置测试环境

```bash
# 重置数据库
docker-compose down
docker volume rm exam_site_backend_mysql_data
docker-compose up -d db
alembic upgrade head
python create_test_user.py
```

## 📈 测试结果解读

### 成功状态码
- `200` - 请求成功
- `201` - 创建成功
- `204` - 删除成功

### 错误状态码
- `400` - 请求参数错误
- `401` - 未授权访问
- `403` - 权限不足
- `404` - 资源不存在
- `500` - 服务器内部错误

## 🎯 下一步

完成API测试后，可以：

1. **前端开发** - 基于测试通过的API开发前端界面
2. **功能扩展** - 添加更多业务功能
3. **性能优化** - 优化API响应速度
4. **安全加固** - 增强安全防护措施 