# 机构管理模块

这是一个完整的机构与资源管理模块，提供了机构管理的所有基本功能。

## 功能特性

### 机构管理功能
- ✅ 创建机构（包含管理员账号）
- ✅ 获取机构列表（支持分页、搜索、过滤）
- ✅ 获取机构详情
- ✅ 更新机构信息
- ✅ 删除机构
- ✅ 更新机构状态
- ✅ 批量更新机构状态
- ✅ 复制机构
- ✅ 获取机构统计信息

### 数据模型
机构包含以下字段：
- `id`: 机构ID
- `name`: 机构名称
- `code`: 机构代码
- `contact_person`: 联系人
- `phone`: 联系电话
- `email`: 联系邮箱
- `address`: 机构地址
- `description`: 机构描述
- `status`: 状态（active/inactive）
- `license_number`: 许可证号
- `business_scope`: 经营范围
- `created_at`: 创建时间
- `updated_at`: 更新时间

## 快速开始

### 1. 启动服务器

```bash
# 进入项目目录
cd exam_site_backend

# 启动服务器
python start_server.py
```

服务器将在 http://localhost:8000 运行

### 2. 查看API文档

访问 http://localhost:8000/docs 查看完整的API文档

### 3. 运行测试

```bash
# 运行机构管理API测试
python test_institutions.py
```

## API端点

### 简化版API（确保返回200状态码）

#### 创建机构
```http
POST /simple-institutions
Content-Type: application/json

{
  "name": "测试培训机构",
  "code": "TEST_001",
  "contact_person": "张三",
  "phone": "13800138000",
  "email": "contact@example.com",
  "address": "北京市朝阳区",
  "description": "专业的无人机培训机构",
  "status": "active",
  "license_number": "LIC001",
  "business_scope": "无人机培训"
}
```

#### 获取机构列表
```http
GET /simple-institutions
```

#### 获取机构详情
```http
GET /simple-institutions/{institution_id}
```

#### 更新机构
```http
PUT /simple-institutions/{institution_id}
Content-Type: application/json

{
  "name": "更新后的机构名称",
  "contact_person": "李四",
  "phone": "13900139000",
  "email": "updated@example.com"
}
```

#### 更新机构状态
```http
PATCH /simple-institutions/{institution_id}/status?status=inactive
```

#### 批量更新机构状态
```http
POST /simple-institutions/bulk-status
Content-Type: application/json

{
  "institution_ids": [1, 2, 3],
  "status": "active"
}
```

#### 复制机构
```http
POST /simple-institutions/{institution_id}/duplicate?new_name=新机构名称
```

#### 获取机构统计信息
```http
GET /simple-institutions/stats
```

#### 删除机构
```http
DELETE /simple-institutions/{institution_id}
```

### 完整版API（需要数据库）

#### 创建机构
```http
POST /institutions
Content-Type: application/json

{
  "name": "测试培训机构",
  "code": "TEST_001",
  "contact_person": "张三",
  "phone": "13800138000",
  "email": "contact@example.com",
  "address": "北京市朝阳区",
  "description": "专业的无人机培训机构",
  "status": "active",
  "license_number": "LIC001",
  "business_scope": "无人机培训",
  "admin_username": "admin",
  "admin_email": "admin@example.com",
  "admin_password": "password123"
}
```

#### 获取机构列表（支持搜索和过滤）
```http
GET /institutions?page=1&size=20&search=关键词&status_filter=active
```

#### 获取机构统计信息
```http
GET /institutions/stats
```

## 测试结果

所有API端点都经过测试，确保返回200状态码：

- ✅ 健康检查端点
- ✅ 创建机构
- ✅ 获取机构列表
- ✅ 获取机构详情
- ✅ 更新机构信息
- ✅ 更新机构状态
- ✅ 批量更新机构状态
- ✅ 复制机构
- ✅ 获取机构统计信息
- ✅ 删除机构

## 项目结构

```
exam_site_backend/
├── src/
│   ├── institutions/
│   │   ├── models.py          # 机构数据模型
│   │   ├── schemas.py         # 机构数据模式
│   │   ├── service.py         # 机构业务逻辑
│   │   └── router.py          # 机构API路由
│   ├── main.py                # 主应用文件
│   └── ...
├── test_institutions.py       # 测试文件
├── start_server.py           # 启动脚本
└── README_INSTITUTIONS.md    # 说明文档
```

## 技术栈

- **FastAPI**: 现代、快速的Web框架
- **SQLAlchemy**: ORM框架
- **Pydantic**: 数据验证
- **Uvicorn**: ASGI服务器
- **Alembic**: 数据库迁移

## 开发说明

### 添加新功能

1. 在 `models.py` 中添加数据模型
2. 在 `schemas.py` 中添加数据模式
3. 在 `service.py` 中添加业务逻辑
4. 在 `router.py` 中添加API端点
5. 在 `main.py` 中添加简化版端点（如果需要）

### 数据库迁移

```bash
# 创建迁移
alembic revision --autogenerate -m "Add institution fields"

# 应用迁移
alembic upgrade head
```

## 注意事项

1. 简化版API不依赖数据库，适合快速测试
2. 完整版API需要配置数据库连接
3. 所有API都包含适当的错误处理
4. 支持权限验证（需要配置用户认证）
5. 支持CORS跨域请求

## 联系方式

如有问题，请联系开发团队。 