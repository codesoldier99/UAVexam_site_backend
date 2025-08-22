# UAV考试管理系统 API接口文档

## 📊 接口统计总览

**总接口数量**: 38个  
**接口分组**: 9个模块

## 🏗️ 接口分组详情

| 模块 | 接口数量 | 说明 |
|------|----------|------|
| 日程管理 | 10个 | 考试日程安排与管理 |
| 微信小程序 | 8个 | 移动端功能接口 |
| 考场管理 | 8个 | 考场信息与状态管理 |
| 机构管理 | 7个 | 考试机构CRUD操作 |
| 考试产品管理 | 6个 | 考试产品配置管理 |
| 认证 | 5个 | 用户登录认证与授权 |
| 系统 | 3个 | 系统健康检查与配置 |
| 考生管理 | 2个 | 考生信息管理 |
| 公共接口 | 1个 | 通用功能接口 |

---

## 🔐 第一部分：核心认证与系统 (8个接口)

### 1. 认证模块 (5个接口)

#### 1.1 用户登录获取JWT令牌
- **接口路径**: `POST /api/v1/auth/token`
- **功能描述**: 用户通过用户名和密码登录，获取访问令牌
- **请求参数**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **响应格式**:
  ```json
  {
    "access_token": "string",
    "token_type": "bearer",
    "expires_in": 3600
  }
  ```
- **使用场景**: 用户登录系统
- **权限要求**: 无（公开接口）

#### 1.2 用户注册
- **接口路径**: `POST /api/v1/auth/register`
- **功能描述**: 新用户注册账号
- **请求参数**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string",
    "full_name": "string"
  }
  ```
- **响应格式**:
  ```json
  {
    "id": "integer",
    "username": "string",
    "email": "string",
    "full_name": "string",
    "created_at": "datetime"
  }
  ```
- **使用场景**: 新用户注册
- **权限要求**: 无（公开接口）

#### 1.3 获取当前用户信息
- **接口路径**: `GET /api/v1/auth/me`
- **功能描述**: 获取当前登录用户的详细信息
- **请求参数**: 无
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "id": "integer",
    "username": "string",
    "email": "string",
    "full_name": "string",
    "role": "string",
    "institution_id": "integer",
    "created_at": "datetime",
    "last_login": "datetime"
  }
  ```
- **使用场景**: 获取用户个人信息
- **权限要求**: 需要有效JWT令牌

#### 1.4 用户登出
- **接口路径**: `POST /api/v1/auth/logout`
- **功能描述**: 用户登出系统，使当前令牌失效
- **请求参数**: 无
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "message": "Successfully logged out"
  }
  ```
- **使用场景**: 用户主动登出
- **权限要求**: 需要有效JWT令牌

#### 1.5 刷新访问令牌
- **接口路径**: `POST /api/v1/auth/refresh`
- **功能描述**: 使用刷新令牌获取新的访问令牌
- **请求参数**:
  ```json
  {
    "refresh_token": "string"
  }
  ```
- **响应格式**:
  ```json
  {
    "access_token": "string",
    "token_type": "bearer",
    "expires_in": 3600
  }
  ```
- **使用场景**: 访问令牌过期时自动刷新
- **权限要求**: 需要有效刷新令牌

### 2. 系统模块 (3个接口)

#### 2.1 系统健康检查
- **接口路径**: `GET /health`
- **功能描述**: 检查系统运行状态和基本健康信息
- **请求参数**: 无
- **响应格式**:
  ```json
  {
    "status": "healthy",
    "timestamp": "datetime",
    "version": "string",
    "uptime": "string"
  }
  ```
- **使用场景**: 系统监控、负载均衡健康检查
- **权限要求**: 无（公开接口）

#### 2.2 获取系统信息
- **接口路径**: `GET /api/v1/system/info`
- **功能描述**: 获取系统配置信息和运行状态
- **请求参数**: 无
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "system_name": "UAV考试管理系统",
    "version": "v1.0.0",
    "environment": "production",
    "database_status": "connected",
    "redis_status": "connected",
    "uptime": "string",
    "last_restart": "datetime"
  }
  ```
- **使用场景**: 系统管理员查看系统状态
- **权限要求**: 需要管理员权限

#### 2.3 获取系统配置
- **接口路径**: `GET /api/v1/system/config`
- **功能描述**: 获取系统可配置参数和设置
- **请求参数**: 无
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "jwt_expire_minutes": 60,
    "max_login_attempts": 5,
    "session_timeout": 3600,
    "file_upload_max_size": "10MB",
    "allowed_file_types": ["jpg", "png", "pdf"],
    "maintenance_mode": false
  }
  ```
- **使用场景**: 前端获取系统配置参数
- **权限要求**: 需要有效JWT令牌

---

## 📋 第一部分总结

**核心认证与系统模块**包含了系统的基础功能：

### 🔑 认证功能
- 完整的JWT认证流程（登录、注册、令牌刷新、登出）
- 用户信息获取和权限验证
- 安全的令牌管理机制

### ⚙️ 系统功能  
- 系统健康状态监控
- 系统信息查询
- 配置参数管理

### 🛡️ 安全特性
- JWT令牌认证
- 角色权限控制
- 会话管理
- 安全登出机制

---

**接下来我们将整理第二部分：基础业务管理（机构管理、考试产品管理、考生管理）**

你希望我继续整理第二部分吗？

---

## 🏢 第二部分：基础业务管理 (15个接口)

### 1. 机构管理 (7个接口)

#### 1.1 获取机构列表
- **接口路径**: `GET /api/v1/institutions`
- **功能描述**: 分页获取考试机构列表，支持搜索和筛选
- **请求参数**:
  ```
  ?page=1&size=20&search=关键词&status=active
  ```
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "items": [
      {
        "id": "integer",
        "name": "string",
        "code": "string",
        "address": "string",
        "contact_person": "string",
        "contact_phone": "string",
        "email": "string",
        "status": "string",
        "created_at": "datetime"
      }
    ],
    "total": "integer",
    "page": "integer",
    "size": "integer",
    "pages": "integer"
  }
  ```
- **使用场景**: 管理员查看所有考试机构
- **权限要求**: 需要管理员权限

#### 1.2 获取机构详情
- **接口路径**: `GET /api/v1/institutions/{id}`
- **功能描述**: 根据ID获取指定机构的详细信息
- **请求参数**: 路径参数 `id`
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "id": "integer",
    "name": "string",
    "code": "string",
    "address": "string",
    "contact_person": "string",
    "contact_phone": "string",
    "email": "string",
    "description": "string",
    "status": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
  ```
- **使用场景**: 查看机构详细信息
- **权限要求**: 需要有效JWT令牌

#### 1.3 创建新机构
- **接口路径**: `POST /api/v1/institutions`
- **功能描述**: 创建新的考试机构
- **请求参数**:
  ```json
  {
    "name": "string",
    "code": "string",
    "address": "string",
    "contact_person": "string",
    "contact_phone": "string",
    "email": "string",
    "description": "string"
  }
  ```
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "id": "integer",
    "name": "string",
    "code": "string",
    "message": "机构创建成功"
  }
  ```
- **使用场景**: 管理员添加新考试机构
- **权限要求**: 需要管理员权限

#### 1.4 更新机构信息
- **接口路径**: `PUT /api/v1/institutions/{id}`
- **功能描述**: 更新指定机构的信息
- **请求参数**: 路径参数 `id`
- **请求体**:
  ```json
  {
    "name": "string",
    "address": "string",
    "contact_person": "string",
    "contact_phone": "string",
    "email": "string",
    "description": "string"
  }
  ```
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "message": "机构信息更新成功",
    "institution": {
      "id": "integer",
      "name": "string",
      "updated_at": "datetime"
    }
  }
  ```
- **使用场景**: 修改机构信息
- **权限要求**: 需要管理员权限

#### 1.5 删除机构
- **接口路径**: `DELETE /api/v1/institutions/{id}`
- **功能描述**: 删除指定的考试机构（软删除）
- **请求参数**: 路径参数 `id`
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "message": "机构删除成功"
  }
  ```
- **使用场景**: 移除不再使用的机构
- **权限要求**: 需要管理员权限

#### 1.6 获取机构考场列表
- **接口路径**: `GET /api/v1/institutions/{id}/venues`
- **功能描述**: 获取指定机构下的所有考场
- **请求参数**: 路径参数 `id`
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "institution_id": "integer",
    "institution_name": "string",
    "venues": [
      {
        "id": "integer",
        "name": "string",
        "capacity": "integer",
        "status": "string",
        "address": "string"
      }
    ]
  }
  ```
- **使用场景**: 查看机构下的考场分布
- **权限要求**: 需要有效JWT令牌

#### 1.7 获取机构统计信息
- **接口路径**: `GET /api/v1/institutions/{id}/stats`
- **功能描述**: 获取指定机构的统计信息（考场数量、考试次数等）
- **请求参数**: 路径参数 `id`
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "institution_id": "integer",
    "institution_name": "string",
    "total_venues": "integer",
    "total_exams": "integer",
    "total_candidates": "integer",
    "active_exams": "integer",
    "monthly_stats": [
      {
        "month": "string",
        "exams_count": "integer",
        "candidates_count": "integer"
      }
    ]
  }
  ```
- **使用场景**: 机构运营数据分析
- **权限要求**: 需要有效JWT令牌

### 2. 考试产品管理 (6个接口)

#### 2.1 获取考试产品列表
- **接口路径**: `GET /api/v1/exam-products`
- **功能描述**: 分页获取考试产品列表，支持搜索和筛选
- **请求参数**:
  ```
  ?page=1&size=20&search=关键词&status=active&institution_id=1
  ```
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "items": [
      {
        "id": "integer",
        "name": "string",
        "code": "string",
        "description": "string",
        "duration_minutes": "integer",
        "pass_score": "integer",
        "status": "string",
        "institution_id": "integer",
        "created_at": "datetime"
      }
    ],
    "total": "integer",
    "page": "integer",
    "size": "integer"
  }
  ```
- **使用场景**: 查看所有考试产品
- **权限要求**: 需要有效JWT令牌

#### 2.2 获取考试产品详情
- **接口路径**: `GET /api/v1/exam-products/{id}`
- **功能描述**: 根据ID获取指定考试产品的详细信息
- **请求参数**: 路径参数 `id`
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "id": "integer",
    "name": "string",
    "code": "string",
    "description": "string",
    "duration_minutes": "integer",
    "pass_score": "integer",
    "total_questions": "integer",
    "question_types": ["string"],
    "status": "string",
    "institution_id": "integer",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
  ```
- **使用场景**: 查看考试产品详细信息
- **权限要求**: 需要有效JWT令牌

#### 2.3 创建考试产品
- **接口路径**: `POST /api/v1/exam-products`
- **功能描述**: 创建新的考试产品
- **请求参数**:
  ```json
  {
    "name": "string",
    "code": "string",
    "description": "string",
    "duration_minutes": "integer",
    "pass_score": "integer",
    "total_questions": "integer",
    "question_types": ["string"],
    "institution_id": "integer"
  }
  ```
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "id": "integer",
    "name": "string",
    "code": "string",
    "message": "考试产品创建成功"
  }
  ```
- **使用场景**: 管理员添加新考试产品
- **权限要求**: 需要管理员权限

#### 2.4 更新考试产品
- **接口路径**: `PUT /api/v1/exam-products/{id}`
- **功能描述**: 更新指定考试产品的信息
- **请求参数**: 路径参数 `id`
- **请求体**:
  ```json
  {
    "name": "string",
    "description": "string",
    "duration_minutes": "integer",
    "pass_score": "integer",
    "total_questions": "integer",
    "question_types": ["string"]
  }
  ```
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "message": "考试产品更新成功",
    "product": {
      "id": "integer",
      "name": "string",
      "updated_at": "datetime"
    }
  }
  ```
- **使用场景**: 修改考试产品信息
- **权限要求**: 需要管理员权限

#### 2.5 删除考试产品
- **接口路径**: `DELETE /api/v1/exam-products/{id}`
- **功能描述**: 删除指定的考试产品（软删除）
- **请求参数**: 路径参数 `id`
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "message": "考试产品删除成功"
  }
  ```
- **使用场景**: 移除不再使用的考试产品
- **权限要求**: 需要管理员权限

#### 2.6 切换考试产品状态
- **接口路径**: `POST /api/v1/exam-products/{id}/toggle-status`
- **功能描述**: 启用或禁用考试产品
- **请求参数**: 路径参数 `id`
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "message": "状态切换成功",
    "product_id": "integer",
    "new_status": "string"
  }
  ```
- **使用场景**: 快速启用/禁用考试产品
- **权限要求**: 需要管理员权限

### 3. 考生管理 (2个接口)

#### 3.1 获取考生列表
- **接口路径**: `GET /api/v1/candidates`
- **功能描述**: 分页获取考生列表，支持搜索和筛选
- **请求参数**:
  ```
  ?page=1&size=20&search=关键词&institution_id=1&status=active
  ```
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "items": [
      {
        "id": "integer",
        "name": "string",
        "id_card": "string",
        "phone": "string",
        "email": "string",
        "institution_id": "integer",
        "status": "string",
        "created_at": "datetime"
    }
    ],
    "total": "integer",
    "page": "integer",
    "size": "integer"
  }
  ```
- **使用场景**: 查看所有考生信息
- **权限要求**: 需要有效JWT令牌

#### 3.2 获取考生详情
- **接口路径**: `GET /api/v1/candidates/{id}`
- **功能描述**: 根据ID获取指定考生的详细信息
- **请求参数**: 路径参数 `id`
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "id": "integer",
    "name": "string",
    "id_card": "string",
    "phone": "string",
    "email": "string",
    "gender": "string",
    "birth_date": "date",
    "address": "string",
    "institution_id": "integer",
    "institution_name": "string",
    "status": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
  ```
- **使用场景**: 查看考生详细信息
- **权限要求**: 需要有效JWT令牌

---

## 📋 第二部分总结

**基础业务管理模块**包含了系统的核心业务功能：

### 🏢 机构管理功能
- 完整的机构CRUD操作
- 机构考场关联查询
- 机构运营数据统计

### 📚 考试产品管理功能
- 考试产品全生命周期管理
- 产品状态快速切换
- 灵活的配置参数

### 👥 考生管理功能
- 考生信息查询
- 分页和筛选支持
- 机构关联管理

### 🔧 管理特性
- 分页查询支持
- 搜索和筛选功能
- 软删除机制
- 权限控制

---

**接下来我们将整理第三部分：考场与日程管理（考场管理8个接口、日程管理10个接口）**

你希望我继续整理第三部分吗？

---

## 🏫 第三部分：考场与日程管理 (18个接口)

### 1. 考场管理 (8个接口)

#### 1.1 获取考场列表
- **接口路径**: `GET /api/v1/venues`
- **功能描述**: 分页获取考场列表，支持搜索、筛选和排序
- **请求参数**:
  ```
  ?page=1&size=20&search=关键词&institution_id=1&status=active&sort_by=name&sort_order=asc
  ```
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "items": [
      {
        "id": "integer",
        "name": "string",
        "code": "string",
        "address": "string",
        "capacity": "integer",
        "status": "string",
        "institution_id": "integer",
        "institution_name": "string",
        "created_at": "datetime"
      }
    ],
    "total": "integer",
    "page": "integer",
    "size": "integer",
    "pages": "integer"
  }
  ```
- **使用场景**: 管理员查看所有考场
- **权限要求**: 需要有效JWT令牌

#### 1.2 获取考场详情
- **接口路径**: `GET /api/v1/venues/{id}`
- **功能描述**: 根据ID获取指定考场的详细信息
- **请求参数**: 路径参数 `id`
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "id": "integer",
    "name": "string",
    "code": "string",
    "address": "string",
    "capacity": "integer",
    "status": "string",
    "description": "string",
    "facilities": ["string"],
    "institution_id": "integer",
    "institution_name": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
  ```
- **使用场景**: 查看考场详细信息
- **权限要求**: 需要有效JWT令牌

#### 1.3 创建新考场
- **接口路径**: `POST /api/v1/venues`
- **功能描述**: 创建新的考场
- **请求参数**:
  ```json
  {
    "name": "string",
    "code": "string",
    "address": "string",
    "capacity": "integer",
    "description": "string",
    "facilities": ["string"],
    "institution_id": "integer"
  }
  ```
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "id": "integer",
    "name": "string",
    "code": "string",
    "message": "考场创建成功"
  }
  ```
- **使用场景**: 管理员添加新考场
- **权限要求**: 需要管理员权限

#### 1.4 更新考场信息
- **接口路径**: `PUT /api/v1/venues/{id}`
- **功能描述**: 更新指定考场的信息
- **请求参数**: 路径参数 `id`
- **请求体**:
  ```json
  {
    "name": "string",
    "address": "string",
    "capacity": "integer",
    "description": "string",
    "facilities": ["string"]
  }
  ```
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "message": "考场信息更新成功",
    "venue": {
      "id": "integer",
      "name": "string",
      "updated_at": "datetime"
    }
  }
  ```
- **使用场景**: 修改考场信息
- **权限要求**: 需要管理员权限

#### 1.5 删除考场
- **接口路径**: `DELETE /api/v1/venues/{id}`
- **功能描述**: 删除指定的考场（软删除）
- **请求参数**: 路径参数 `id`
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "message": "考场删除成功"
  }
  ```
- **使用场景**: 移除不再使用的考场
- **权限要求**: 需要管理员权限

#### 1.6 获取考场状态
- **接口路径**: `GET /api/v1/venues/{id}/status`
- **功能描述**: 获取指定考场的实时状态信息
- **请求参数**: 路径参数 `id`
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "venue_id": "integer",
    "venue_name": "string",
    "current_status": "string",
    "current_capacity": "integer",
    "max_capacity": "integer",
    "current_exam": {
      "id": "integer",
      "name": "string",
      "start_time": "datetime",
      "end_time": "datetime"
    },
    "last_updated": "datetime"
  }
  ```
- **使用场景**: 查看考场实时状态
- **权限要求**: 需要有效JWT令牌

#### 1.7 更新考场状态
- **接口路径**: `PUT /api/v1/venues/{id}/status`
- **功能描述**: 更新考场的状态（可用、维护中、已满等）
- **请求参数**: 路径参数 `id`
- **请求体**:
  ```json
  {
    "status": "string",
    "reason": "string"
  }
  ```
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "message": "考场状态更新成功",
    "venue_id": "integer",
    "new_status": "string",
    "updated_at": "datetime"
  }
  ```
- **使用场景**: 管理员更新考场状态
- **权限要求**: 需要管理员权限

#### 1.8 获取考场统计信息
- **接口路径**: `GET /api/v1/venues/{id}/stats`
- **功能描述**: 获取指定考场的使用统计信息
- **请求参数**: 路径参数 `id`
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "venue_id": "integer",
    "venue_name": "string",
    "total_exams": "integer",
    "total_candidates": "integer",
    "utilization_rate": "float",
    "monthly_stats": [
      {
        "month": "string",
        "exams_count": "integer",
        "candidates_count": "integer",
        "utilization_rate": "float"
      }
    ]
  }
  ```
- **使用场景**: 考场使用效率分析
- **权限要求**: 需要有效JWT令牌

### 2. 日程管理 (10个接口)

#### 2.1 获取考试日程列表
- **接口路径**: `GET /api/v1/schedules`
- **功能描述**: 分页获取考试日程列表，支持多种筛选条件
- **请求参数**:
  ```
  ?page=1&size=20&institution_id=1&venue_id=1&exam_product_id=1&date_from=2024-01-01&date_to=2024-12-31&status=upcoming
  ```
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "items": [
      {
        "id": "integer",
        "exam_name": "string",
        "exam_product_id": "integer",
        "venue_id": "integer",
        "venue_name": "string",
        "start_time": "datetime",
        "end_time": "datetime",
        "max_candidates": "integer",
        "current_candidates": "integer",
        "status": "string",
        "created_at": "datetime"
      }
    ],
    "total": "integer",
    "page": "integer",
    "size": "integer"
  }
  ```
- **使用场景**: 查看所有考试日程
- **权限要求**: 需要有效JWT令牌

#### 2.2 获取考试日程详情
- **接口路径**: `GET /api/v1/schedules/{id}`
- **功能描述**: 根据ID获取指定考试日程的详细信息
- **请求参数**: 路径参数 `id`
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "id": "integer",
    "exam_name": "string",
    "exam_product_id": "integer",
    "exam_product_name": "string",
    "venue_id": "integer",
    "venue_name": "string",
    "venue_address": "string",
    "start_time": "datetime",
    "end_time": "datetime",
    "max_candidates": "integer",
    "current_candidates": "integer",
    "status": "string",
    "description": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
  ```
- **使用场景**: 查看考试日程详细信息
- **权限要求**: 需要有效JWT令牌

#### 2.3 创建考试日程
- **接口路径**: `POST /api/v1/schedules`
- **功能描述**: 创建新的考试日程
- **请求参数**:
  ```json
  {
    "exam_name": "string",
    "exam_product_id": "integer",
    "venue_id": "integer",
    "start_time": "datetime",
    "end_time": "datetime",
    "max_candidates": "integer",
    "description": "string"
  }
  ```
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "id": "integer",
    "exam_name": "string",
    "message": "考试日程创建成功"
  }
  ```
- **使用场景**: 管理员安排新考试
- **权限要求**: 需要管理员权限

#### 2.4 更新考试日程
- **接口路径**: `PUT /api/v1/schedules/{id}`
- **功能描述**: 更新指定考试日程的信息
- **请求参数**: 路径参数 `id`
- **请求体**:
  ```json
  {
    "exam_name": "string",
    "venue_id": "integer",
    "start_time": "datetime",
    "end_time": "datetime",
    "max_candidates": "integer",
    "description": "string"
  }
  ```
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "message": "考试日程更新成功",
    "schedule": {
      "id": "integer",
      "exam_name": "string",
      "updated_at": "datetime"
    }
  }
  ```
- **使用场景**: 修改考试日程安排
- **权限要求**: 需要管理员权限

#### 2.5 删除考试日程
- **接口路径**: `DELETE /api/v1/schedules/{id}`
- **功能描述**: 删除指定的考试日程（软删除）
- **请求参数**: 路径参数 `id`
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "message": "考试日程删除成功"
  }
  ```
- **使用场景**: 取消已安排的考试
- **权限要求**: 需要管理员权限

#### 2.6 获取考场可用时间
- **接口路径**: `GET /api/v1/venues/{id}/available-times`
- **功能描述**: 获取指定考场在指定日期范围内的可用时间段
- **请求参数**: 路径参数 `id`
- **查询参数**: `?date_from=2024-01-01&date_to=2024-01-31`
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "venue_id": "integer",
    "venue_name": "string",
    "date_from": "date",
    "date_to": "date",
    "available_slots": [
      {
        "date": "date",
        "available_times": [
          {
            "start_time": "time",
            "end_time": "time",
            "duration_minutes": "integer"
          }
        ]
      }
    ]
  }
  ```
- **使用场景**: 安排考试时选择合适时间
- **权限要求**: 需要有效JWT令牌

#### 2.7 获取考试产品可用时间
- **接口路径**: `GET /api/v1/exam-products/{id}/available-times`
- **功能描述**: 获取指定考试产品在指定日期范围内的可用时间段
- **请求参数**: 路径参数 `id`
- **查询参数**: `?date_from=2024-01-01&date_to=2024-01-31&venue_id=1`
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "exam_product_id": "integer",
    "exam_product_name": "string",
    "date_from": "date",
    "date_to": "date",
    "venue_id": "integer",
    "available_slots": [
      {
        "date": "date",
        "available_times": [
          {
            "start_time": "time",
            "end_time": "time",
            "duration_minutes": "integer"
          }
        ]
      }
    ]
  }
  ```
- **使用场景**: 安排特定考试产品的时间
- **权限要求**: 需要有效JWT令牌

#### 2.8 获取日程冲突检查
- **接口路径**: `POST /api/v1/schedules/check-conflicts`
- **功能描述**: 检查新考试日程是否与现有日程冲突
- **请求参数**:
  ```json
  {
    "venue_id": "integer",
    "start_time": "datetime",
    "end_time": "datetime",
    "exclude_schedule_id": "integer"
  }
  ```
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "has_conflicts": "boolean",
    "conflicts": [
      {
        "schedule_id": "integer",
        "exam_name": "string",
        "start_time": "datetime",
        "end_time": "datetime",
        "conflict_type": "string"
      }
    ]
  }
  ```
- **使用场景**: 创建日程前检查时间冲突
- **权限要求**: 需要有效JWT令牌

#### 2.9 获取日程统计信息
- **接口路径**: `GET /api/v1/schedules/stats`
- **功能描述**: 获取考试日程的统计信息
- **请求参数**:
  ```
  ?institution_id=1&venue_id=1&date_from=2024-01-01&date_to=2024-12-31
  ```
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "total_schedules": "integer",
    "upcoming_schedules": "integer",
    "completed_schedules": "integer",
    "cancelled_schedules": "integer",
    "total_candidates": "integer",
    "monthly_stats": [
      {
        "month": "string",
        "schedules_count": "integer",
        "candidates_count": "integer"
      }
    ]
  }
  ```
- **使用场景**: 考试日程数据分析
- **权限要求**: 需要有效JWT令牌

#### 2.10 批量更新日程状态
- **接口路径**: `POST /api/v1/schedules/batch-update-status`
- **功能描述**: 批量更新多个考试日程的状态
- **请求参数**:
  ```json
  {
    "schedule_ids": ["integer"],
    "new_status": "string",
    "reason": "string"
  }
  ```
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "message": "批量更新成功",
    "updated_count": "integer",
    "failed_count": "integer",
    "failed_ids": ["integer"]
  }
  ```
- **使用场景**: 批量操作考试日程
- **权限要求**: 需要管理员权限

---

## 📋 第三部分总结

**考场与日程管理模块**包含了系统的核心运营功能：

### 🏫 考场管理功能
- 完整的考场CRUD操作
- 实时状态监控
- 使用效率统计
- 设施管理

### 📅 日程管理功能
- 考试日程全生命周期管理
- 智能时间冲突检测
- 可用时间段查询
- 批量操作支持

### 🔧 管理特性
- 多维度筛选查询
- 实时状态更新
- 冲突检测机制
- 统计分析功能

---

**接下来我们将整理第四部分：移动端与公共接口（微信小程序8个接口、公共接口1个接口）**

你希望我继续整理第四部分吗？

---

## 📱 第四部分：移动端与公共接口 (9个接口)

### 1. 微信小程序 (8个接口)

#### 1.1 小程序登录
- **接口路径**: `POST /api/v1/wechat/login`
- **功能描述**: 微信小程序用户登录，获取用户信息和访问令牌
- **请求参数**:
  ```json
  {
    "code": "string",
    "encrypted_data": "string",
    "iv": "string"
  }
  ```
- **请求头**: 无
- **响应格式**:
  ```json
  {
    "access_token": "string",
    "token_type": "bearer",
    "user_info": {
      "openid": "string",
      "nickname": "string",
      "avatar_url": "string",
      "gender": "integer"
    },
    "expires_in": 3600
  }
  ```
- **使用场景**: 小程序用户首次登录
- **权限要求**: 无（公开接口）

#### 1.2 获取考生考试日程
- **接口路径**: `GET /api/v1/wechat/candidate/schedule`
- **功能描述**: 获取指定考生的考试日程信息
- **请求参数**: 查询参数 `?candidate_id=1&date_from=2024-01-01&date_to=2024-12-31`
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "candidate_id": "integer",
    "candidate_name": "string",
    "schedules": [
      {
        "id": "integer",
        "exam_name": "string",
        "exam_product_name": "string",
        "venue_name": "string",
        "venue_address": "string",
        "start_time": "datetime",
        "end_time": "datetime",
        "status": "string",
        "checkin_status": "string"
      }
    ]
  }
  ```
- **使用场景**: 考生查看自己的考试安排
- **权限要求**: 需要有效JWT令牌

#### 1.3 生成考生二维码
- **接口路径**: `POST /api/v1/wechat/candidate/qrcode`
- **功能描述**: 为指定考生生成考试签到二维码
- **请求参数**:
  ```json
  {
    "candidate_id": "integer",
    "schedule_id": "integer",
    "expire_minutes": "integer"
  }
  ```
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "qrcode_url": "string",
    "qrcode_data": "string",
    "expire_time": "datetime",
    "candidate_id": "integer",
    "schedule_id": "integer"
  }
  ```
- **使用场景**: 考生生成签到二维码
- **权限要求**: 需要有效JWT令牌

#### 1.4 获取考场状态
- **接口路径**: `GET /api/v1/wechat/venues/status`
- **功能描述**: 获取所有考场的实时状态信息
- **请求参数**: 查询参数 `?institution_id=1&status=active`
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "venues": [
      {
        "id": "integer",
        "name": "string",
        "address": "string",
        "current_status": "string",
        "current_capacity": "integer",
        "max_capacity": "integer",
        "current_exam": {
          "name": "string",
          "start_time": "datetime",
          "end_time": "datetime"
        }
      }
    ]
  }
  ```
- **使用场景**: 查看考场实时状态
- **权限要求**: 需要有效JWT令牌

#### 1.5 扫码签到
- **接口路径**: `POST /api/v1/wechat/checkin/scan`
- **功能描述**: 考生通过扫描二维码进行考试签到
- **请求参数**:
  ```json
  {
    "qrcode_data": "string",
    "candidate_id": "integer",
    "location": {
      "latitude": "float",
      "longitude": "float",
      "accuracy": "float"
    }
  }
  ```
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "message": "签到成功",
    "checkin_id": "integer",
    "checkin_time": "datetime",
    "venue_name": "string",
    "exam_name": "string",
    "start_time": "datetime"
  }
  ```
- **使用场景**: 考生考试签到
- **权限要求**: 需要有效JWT令牌

#### 1.6 获取排队位置
- **接口路径**: `GET /api/v1/wechat/queue/position`
- **功能描述**: 获取考生在考试排队中的位置信息
- **请求参数**: 查询参数 `?candidate_id=1&schedule_id=1`
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "candidate_id": "integer",
    "schedule_id": "integer",
    "venue_name": "string",
    "queue_position": "integer",
    "estimated_wait_time": "integer",
    "total_in_queue": "integer",
    "last_updated": "datetime"
  }
  ```
- **使用场景**: 考生查看排队状态
- **权限要求**: 需要有效JWT令牌

#### 1.7 获取看板数据
- **接口路径**: `GET /api/v1/wechat/dashboard`
- **功能描述**: 获取考试看板的实时数据
- **请求参数**: 查询参数 `?institution_id=1&venue_id=1`
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "institution_id": "integer",
    "institution_name": "string",
    "current_time": "datetime",
    "today_stats": {
      "total_exams": "integer",
      "total_candidates": "integer",
      "checked_in": "integer",
      "in_progress": "integer",
      "completed": "integer"
    },
    "venue_status": [
      {
        "venue_id": "integer",
        "venue_name": "string",
        "status": "string",
        "current_exam": "string",
        "candidates_count": "integer"
      }
    ]
  }
  ```
- **使用场景**: 显示考试看板信息
- **权限要求**: 需要有效JWT令牌

#### 1.8 获取考试通知
- **接口路径**: `GET /api/v1/wechat/notifications`
- **功能描述**: 获取考生的考试相关通知消息
- **请求参数**: 查询参数 `?candidate_id=1&type=all&page=1&size=20`
- **请求头**: `Authorization: Bearer {token}`
- **响应格式**:
  ```json
  {
    "notifications": [
      {
        "id": "integer",
        "title": "string",
        "content": "string",
        "type": "string",
        "is_read": "boolean",
        "created_at": "datetime",
        "related_schedule_id": "integer"
      }
    ],
    "total": "integer",
    "page": "integer",
    "size": "integer"
  }
  ```
- **使用场景**: 考生查看考试通知
- **权限要求**: 需要有效JWT令牌

### 2. 公共接口 (1个接口)

#### 2.1 获取系统公告
- **接口路径**: `GET /api/v1/public/announcements`
- **功能描述**: 获取系统公告信息，无需认证
- **请求参数**: 查询参数 `?type=all&page=1&size=10`
- **请求头**: 无
- **响应格式**:
  ```json
  {
    "announcements": [
      {
        "id": "integer",
        "title": "string",
        "content": "string",
        "type": "string",
        "priority": "string",
        "start_date": "date",
        "end_date": "date",
        "created_at": "datetime"
      }
    ],
    "total": "integer",
    "page": "integer",
    "size": "integer"
  }
  ```
- **使用场景**: 显示系统公告
- **权限要求**: 无（公开接口）

---

## 📋 第四部分总结

**移动端与公共接口模块**包含了系统的移动端功能和公共访问功能：

### 📱 微信小程序功能
- 用户登录认证
- 考试日程查询
- 二维码签到
- 考场状态监控
- 排队位置查询
- 看板数据展示
- 通知消息管理

### 🌐 公共接口功能
- 系统公告展示
- 无需认证访问

### 🔧 移动端特性
- 微信生态集成
- 地理位置服务
- 实时状态更新
- 推送通知支持

---

## 🎉 完整API接口文档总结

我已经完成了整个UAV考试管理系统的API接口文档整理，总共包含**38个接口**，分为四个主要部分：

### 📊 接口统计总览
- **第一部分**: 核心认证与系统 (8个接口)
- **第二部分**: 基础业务管理 (15个接口)  
- **第三部分**: 考场与日程管理 (18个接口)
- **第四部分**: 移动端与公共接口 (9个接口)

### 🏆 系统功能亮点
1. **完整的认证体系** - JWT令牌管理、用户权限控制
2. **全面的业务管理** - 机构、产品、考生全生命周期管理
3. **智能的日程管理** - 冲突检测、可用时间查询、批量操作
4. **移动端友好** - 微信小程序集成、实时状态更新
5. **数据驱动** - 丰富的统计分析和报表功能

### 📱 技术架构特点
- RESTful API设计
- 分层架构（routes/services/models）
- 统一的错误处理和响应格式
- 完善的权限控制机制
- 支持分页、搜索、筛选等高级查询

这份文档为开发者和系统管理员提供了完整的API使用指南，涵盖了系统的所有核心功能！
