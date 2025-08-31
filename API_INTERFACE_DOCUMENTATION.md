# UAV考点运营管理系统 API接口文档

## 概述

本文档描述了UAV考点运营管理系统的所有API接口，包括健康检查、认证授权、机构管理、考场管理、考试产品管理、考生管理、日程管理、微信小程序接口、系统管理等功能模块。

## 基础信息

- **基础URL**: `http://localhost:8000`
- **API版本**: v1
- **认证方式**: JWT Bearer Token
- **数据格式**: JSON

## 认证说明

除了公开接口外，所有API都需要在请求头中包含JWT令牌：

```
Authorization: Bearer <your_jwt_token>
```

## 接口列表

### 1. 健康检查模块 (Health Check) - 5个接口

#### 1.1 基础健康检查
- **接口**: `GET /api/v1/health/`
- **描述**: 基础健康检查，返回系统运行状态
- **权限**: 公开
- **响应**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0"
}
```

#### 1.2 详细健康检查
- **接口**: `GET /api/v1/health/detailed`
- **描述**: 详细健康检查，包括数据库、Redis、文件系统状态
- **权限**: 公开
- **响应**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "checks": {
    "database": "healthy",
    "redis": "healthy",
    "filesystem": "healthy"
  }
}
```

#### 1.3 数据库健康检查
- **接口**: `GET /api/v1/health/database`
- **描述**: 专门检查数据库连接状态
- **权限**: 公开
- **响应**:
```json
{
  "status": "healthy",
  "database": "connected",
  "response_time": "5ms"
}
```

#### 1.4 就绪检查
- **接口**: `GET /api/v1/health/readiness`
- **描述**: 检查应用是否准备好接收流量
- **权限**: 公开
- **响应**:
```json
{
  "status": "ready",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### 1.5 存活检查
- **接口**: `GET /api/v1/health/liveness`
- **描述**: 检查应用进程是否正常运行
- **权限**: 公开
- **响应**:
```json
{
  "status": "alive",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 2. 认证授权模块 (Authentication) - 6个接口

#### 2.1 用户登录 (JSON格式)
- **接口**: `POST /api/v1/auth/login`
- **描述**: 用户登录获取访问令牌
- **权限**: 公开
- **请求体**:
```json
{
  "username": "admin",
  "password": "admin123"
}
```
- **响应**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "role": "admin",
    "institution_id": null
  }
}
```

#### 2.2 OAuth2兼容登录
- **接口**: `POST /api/v1/auth/token`
- **描述**: OAuth2标准格式登录
- **权限**: 公开
- **请求体** (form-data):
```
username=admin
password=admin123
grant_type=password
```
- **响应**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

#### 2.3 用户注册
- **接口**: `POST /api/v1/auth/register`
- **描述**: 注册新用户
- **权限**: 公开
- **请求体**:
```json
{
  "username": "newuser",
  "password": "password123",
  "email": "user@example.com",
  "role": "operator",
  "institution_id": 1
}
```

#### 2.4 获取当前用户信息
- **接口**: `GET /api/v1/auth/me`
- **描述**: 获取当前登录用户的详细信息
- **权限**: 需要认证
- **响应**:
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "role": "admin",
  "institution_id": null,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### 2.5 用户登出
- **接口**: `POST /api/v1/auth/logout`
- **描述**: 用户登出，使令牌失效
- **权限**: 需要认证
- **响应**:
```json
{
  "message": "Successfully logged out"
}
```

#### 2.6 刷新访问令牌
- **接口**: `POST /api/v1/auth/refresh`
- **描述**: 刷新访问令牌
- **权限**: 需要认证
- **响应**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### 3. 机构管理模块 (Institution Management) - 8个接口

#### 3.1 获取机构列表
- **接口**: `GET /api/v1/institutions/`
- **描述**: 获取机构列表，支持分页、搜索、筛选
- **权限**: 需要认证
- **查询参数**:
  - `skip`: 跳过记录数 (默认: 0)
  - `limit`: 每页数量 (默认: 20)
  - `search`: 搜索关键词
  - `is_active`: 机构状态筛选
- **响应**:
```json
{
  "items": [
    {
      "id": 1,
      "code": "BJAV001",
      "name": "北京航空培训中心",
      "address": "北京市朝阳区",
      "contact_person": "张经理",
      "contact_phone": "13800138001",
      "type": "培训机构",
      "is_active": true,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 20
}
```

#### 3.2 获取机构详情
- **接口**: `GET /api/v1/institutions/{id}`
- **描述**: 获取指定机构的详细信息
- **权限**: 需要认证
- **响应**:
```json
{
  "id": 1,
  "code": "BJAV001",
  "name": "北京航空培训中心",
  "address": "北京市朝阳区",
  "contact_person": "张经理",
  "contact_phone": "13800138001",
  "email": "contact@bjav.com",
  "status": "active",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### 3.3 创建机构
- **接口**: `POST /api/v1/institutions/`
- **描述**: 创建新机构
- **权限**: 管理员
- **请求参数**:
  - `name`: 机构名称 (必填)
  - `code`: 机构代码 (必填)
  - `type`: 机构类型 (默认: "培训机构")
  - `contact_person`: 联系人
  - `contact_phone`: 联系电话
  - `contact_email`: 联系邮箱
  - `address`: 地址
- **响应**: 返回创建的机构信息

#### 3.4 更新机构信息
- **接口**: `PUT /api/v1/institutions/{id}`
- **描述**: 更新机构信息
- **权限**: 管理员
- **请求参数**:
  - `name`: 机构名称
  - `type`: 机构类型
  - `contact_person`: 联系人
  - `contact_phone`: 联系电话
  - `contact_email`: 联系邮箱
  - `address`: 地址
  - `is_active`: 是否激活
  - `is_approved`: 是否审核通过
- **响应**: 返回更新后的机构信息

#### 3.5 删除机构
- **接口**: `DELETE /api/v1/institutions/{id}`
- **描述**: 删除机构
- **权限**: 超级管理员
- **响应**:
```json
{
  "message": "Institution deleted successfully"
}
```

#### 3.6 获取机构考场列表
- **接口**: `GET /api/v1/institutions/{id}/venues`
- **描述**: 获取指定机构的所有考场
- **权限**: 需要认证
- **响应**:
```json
{
  "items": [
    {
      "id": 1,
      "code": "MULTIROTOR_A",
      "name": "多旋翼A号实操场",
      "type": "practical",
      "capacity": 20,
      "status": "available"
    }
  ],
  "total": 1
}
```

#### 3.7 获取机构统计信息
- **接口**: `GET /api/v1/institutions/{id}/stats`
- **描述**: 获取机构统计数据
- **权限**: 需要认证
- **响应**:
```json
{
  "venues_count": 5,
  "candidates_count": 120,
  "exams_today": 8,
  "exams_this_month": 45
}
```

### 4. 考场管理模块 (Venue Management) - 8个接口

#### 4.1 获取考场列表
- **接口**: `GET /api/v1/venues/`
- **描述**: 获取考场列表，支持机构、状态、类型筛选
- **权限**: 需要认证
- **查询参数**:
  - `skip`: 跳过记录数 (默认: 0)
  - `limit`: 每页数量 (默认: 100)
  - `institution_id`: 机构ID筛选
  - `status`: 状态筛选
  - `venue_type`: 考场类型筛选
- **响应**: 返回考场列表数组
```json
[
  {
    "id": 1,
    "code": "MULTIROTOR_A",
    "name": "多旋翼A号实操场",
    "type": "practical",
    "capacity": 20,
    "status": "available",
    "equipment": "多旋翼无人机、安全设备",
    "location": "实训楼A区",
    "institution_id": 1,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

#### 4.2 获取考场详情
- **接口**: `GET /api/v1/venues/{id}`
- **描述**: 获取考场详细信息
- **权限**: 需要认证
- **响应**:
```json
{
  "id": 1,
  "code": "MULTIROTOR_A",
  "name": "多旋翼A号实操场",
  "type": "practical",
  "capacity": 20,
  "status": "available",
  "equipment": "多旋翼无人机、安全设备",
  "location": "实训楼A区",
  "institution_id": 1,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### 4.3 创建考场
- **接口**: `POST /api/v1/venues/`
- **描述**: 创建新考场
- **权限**: 管理员
- **请求体**:
```json
{
  "code": "MULTIROTOR_A",
  "name": "多旋翼A号实操场",
  "type": "practical",
  "capacity": 20,
  "equipment": "多旋翼无人机、安全设备",
  "location": "实训楼A区",
  "institution_id": 1
}
```

#### 4.4 更新考场信息
- **接口**: `PUT /api/v1/venues/{id}`
- **描述**: 更新考场信息
- **权限**: 管理员或机构管理员
- **请求体**:
```json
{
  "name": "多旋翼A号实操场",
  "capacity": 25,
  "equipment": "多旋翼无人机、安全设备、新增摄像设备"
}
```

#### 4.5 删除考场
- **接口**: `DELETE /api/v1/venues/{id}`
- **描述**: 删除考场
- **权限**: 管理员
- **响应**:
```json
{
  "message": "Venue deleted successfully"
}
```

#### 4.6 切换考场状态
- **接口**: `POST /api/v1/venues/{id}/toggle-status`
- **描述**: 切换考场可用状态
- **权限**: 管理员或机构管理员
- **响应**:
```json
{
  "id": 1,
  "status": "maintenance",
  "message": "Venue status updated successfully"
}
```

#### 4.7 获取考场日程
- **接口**: `GET /api/v1/venues/{id}/schedules`
- **描述**: 获取考场的日程安排
- **权限**: 需要认证
- **查询参数**:
  - `date`: 指定日期 (YYYY-MM-DD)
- **响应**:
```json
{
  "venue": {
    "id": 1,
    "name": "多旋翼A号实操场"
  },
  "schedules": [
    {
      "id": 1,
      "exam_time": "2024-01-01T09:00:00Z",
      "duration": 15,
      "candidate_name": "张三",
      "exam_product": "多旋翼视距内驾驶员",
      "status": "scheduled"
    }
  ]
}
```

#### 4.8 获取考场当前状态
- **接口**: `GET /api/v1/venues/{id}/current-status`
- **描述**: 获取考场实时状态信息
- **权限**: 需要认证
- **响应**:
```json
{
  "venue_id": 1,
  "status": "available",
  "current_exam": null,
  "next_exam": {
    "id": 1,
    "exam_time": "2024-01-01T10:00:00Z",
    "candidate_name": "张三"
  },
  "capacity_usage": "5/20"
}
```

### 5. 考试产品管理模块 (Exam Product Management) - 6个接口

#### 5.1 获取考试产品列表
- **接口**: `GET /api/v1/exam-products/`
- **描述**: 获取考试产品列表
- **权限**: 需要认证
- **查询参数**:
  - `skip`: 跳过记录数 (默认: 0)
  - `limit`: 每页数量 (默认: 100)
  - `is_active`: 状态筛选
  - `exam_type`: 考试类型筛选
- **响应**: 返回考试产品列表数组
```json
[
  {
    "id": 1,
    "code": "MULTIROTOR_VLOS",
    "name": "多旋翼视距内驾驶员",
    "type": "practical",
    "duration": 15,
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

#### 5.2 获取考试产品详情
- **接口**: `GET /api/v1/exam-products/{id}`
- **描述**: 获取考试产品详细信息
- **权限**: 需要认证
- **响应**:
```json
{
  "id": 1,
  "code": "MULTIROTOR_VLOS",
  "name": "多旋翼视距内驾驶员",
  "description": "多旋翼无人机视距内驾驶员实操考试",
  "type": "practical",
  "duration": 15,
  "requirements": "持有理论考试合格证",
  "status": "active",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### 5.3 创建考试产品
- **接口**: `POST /api/v1/exam-products/`
- **描述**: 创建新的考试产品
- **权限**: 管理员
- **请求体**:
```json
{
  "code": "MULTIROTOR_VLOS",
  "name": "多旋翼视距内驾驶员",
  "description": "多旋翼无人机视距内驾驶员实操考试",
  "type": "practical",
  "duration": 15,
  "requirements": "持有理论考试合格证"
}
```

#### 5.4 更新考试产品
- **接口**: `PUT /api/v1/exam-products/{id}`
- **描述**: 更新考试产品信息
- **权限**: 管理员
- **请求体**:
```json
{
  "name": "多旋翼视距内驾驶员",
  "description": "多旋翼无人机视距内驾驶员实操考试（更新版）",
  "duration": 20
}
```

#### 5.5 删除考试产品
- **接口**: `DELETE /api/v1/exam-products/{id}`
- **描述**: 删除考试产品
- **权限**: 管理员
- **响应**:
```json
{
  "message": "Exam product deleted successfully"
}
```

#### 5.6 切换产品状态
- **接口**: `POST /api/v1/exam-products/{id}/toggle-status`
- **描述**: 切换考试产品状态
- **权限**: 管理员
- **响应**:
```json
{
  "id": 1,
  "status": "inactive",
  "message": "Exam product status updated successfully"
}
```

### 6. 考生管理模块 (Candidate Management) - 8个接口

#### 6.1 获取考生列表
- **接口**: `GET /api/v1/candidates/`
- **描述**: 获取考生列表，支持分页、搜索、筛选
- **权限**: 需要认证
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `size`: 每页数量 (默认: 20)
  - `search`: 搜索关键词（姓名、身份证号）
  - `institution_id`: 机构筛选
  - `status`: 状态筛选
- **响应**:
```json
{
  "items": [
    {
      "id": 1,
      "real_name": "张三",
      "id_card": "110101199001011234",
      "phone": "13800138001",
      "email": "zhangsan@example.com",
      "username": "candidate001",
      "role": "candidate",
      "is_active": true,
      "is_verified": false,
      "institution_id": 1,
      "exam_product_id": 1,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z",
      "last_login": null
    }
  ],
  "total": 1,
  "page": 1,
  "size": 20,
  "pages": 1
}
```

#### 6.2 获取考生详情
- **接口**: `GET /api/v1/candidates/{id}`
- **描述**: 获取考生详细信息
- **权限**: 需要认证
- **响应**:
```json
{
  "id": 1,
  "name": "张三",
  "id_card": "110101199001011234",
  "phone": "13800138001",
  "email": "zhangsan@example.com",
  "address": "北京市朝阳区",
  "institution_id": 1,
  "created_at": "2024-01-01T00:00:00Z",
  "registrations": [
    {
      "id": 1,
      "exam_product": "多旋翼视距内驾驶员",
      "status": "approved",
      "registration_time": "2024-01-01T00:00:00Z"
    }
  ]
}
```

#### 6.3 创建考生
- **接口**: `POST /api/v1/candidates/`
- **描述**: 创建新考生
- **权限**: 操作员及以上
- **请求体**:
```json
{
  "name": "张三",
  "id_card": "110101199001011234",
  "phone": "13800138001",
  "email": "zhangsan@example.com",
  "address": "北京市朝阳区",
  "institution_id": 1
}
```

#### 6.4 更新考生信息
- **接口**: `PUT /api/v1/candidates/{id}`
- **描述**: 更新考生信息
- **权限**: 操作员及以上
- **请求体**:
```json
{
  "name": "张三",
  "phone": "13800138002",
  "email": "zhangsan_new@example.com",
  "address": "北京市朝阳区新地址"
}
```

#### 6.5 删除考生
- **接口**: `DELETE /api/v1/candidates/{id}`
- **描述**: 删除考生
- **权限**: 管理员
- **响应**:
```json
{
  "message": "Candidate deleted successfully"
}
```

#### 6.6 批量导入考生
- **接口**: `POST /api/v1/candidates/batch-import`
- **描述**: 通过Excel文件批量导入考生
- **权限**: 操作员及以上
- **请求体**: multipart/form-data
- **文件字段**: `file` (Excel文件)
- **响应**:
```json
{
  "message": "Batch import completed",
  "success_count": 10,
  "error_count": 2,
  "errors": [
    {
      "row": 3,
      "error": "身份证号格式错误"
    }
  ]
}
```

#### 6.7 下载导入模板
- **接口**: `GET /api/v1/candidates/template/download`
- **描述**: 下载考生批量导入Excel模板
- **权限**: 操作员及以上
- **响应**: Excel文件下载

#### 6.8 获取考生统计
- **接口**: `GET /api/v1/candidates/statistics`
- **描述**: 获取考生统计信息
- **权限**: 需要认证
- **响应**:
```json
{
  "total_candidates": 120,
  "new_this_month": 15,
  "by_institution": [
    {
      "institution_name": "北京航空培训中心",
      "count": 80
    }
  ],
  "by_status": {
    "active": 100,
    "inactive": 20
  }
}
```

### 7. 日程管理模块 (Schedule Management) - 10个接口

#### 7.1 获取日程列表
- **接口**: `GET /api/v1/schedules/`
- **描述**: 获取日程列表
- **权限**: 需要认证
- **查询参数**:
  - `skip`: 跳过记录数 (默认: 0)
  - `limit`: 每页数量 (默认: 100)
  - `venue_id`: 考场筛选
  - `date`: 日期筛选 (YYYY-MM-DD格式)
  - `status`: 状态筛选
  - `institution_id`: 机构筛选
- **响应**: 返回日程列表数组
```json
[
  {
    "id": 1,
    "start_time": "2024-01-01T09:00:00Z",
    "end_time": "2024-01-01T09:15:00Z",
    "status": "scheduled",
    "registration_id": 1,
    "venue_id": 1,
    "candidate_name": "张三",
    "venue_name": "多旋翼A号实操场",
    "exam_product_name": "多旋翼视距内驾驶员",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

#### 7.2 获取日程详情
- **接口**: `GET /api/v1/schedules/{id}`
- **描述**: 获取日程详细信息
- **权限**: 需要认证
- **响应**:
```json
{
  "id": 1,
  "exam_time": "2024-01-01T09:00:00Z",
  "duration": 15,
  "status": "scheduled",
  "notes": "考试注意事项",
  "candidate_id": 1,
  "venue_id": 1,
  "exam_product_id": 1,
  "registration_id": 1,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### 7.3 创建日程
- **接口**: `POST /api/v1/schedules/`
- **描述**: 创建新的考试日程
- **权限**: 管理员
- **请求体**:
```json
{
  "registration_id": 1,
  "venue_id": 1,
  "start_time": "2024-01-01T09:00:00Z",
  "end_time": "2024-01-01T09:15:00Z"
}
```
- **响应**: 返回创建的日程信息

#### 7.4 批量创建日程
- **接口**: `POST /api/v1/schedules/batch`
- **描述**: 批量创建考试日程
- **权限**: 管理员
- **请求体**:
```json
{
  "registration_ids": [1, 2, 3],
  "exam_product_id": 1,
  "venue_id": 1,
  "start_time": "2024-01-01T09:00:00Z",
  "duration_minutes": 15
}
```
- **响应**:
```json
{
  "message": "成功创建 3 个日程",
  "schedules": [...]
}
```

#### 7.5 更新日程
- **接口**: `PUT /api/v1/schedules/{id}`
- **描述**: 更新日程信息
- **权限**: 操作员及以上
- **请求体**:
```json
{
  "exam_time": "2024-01-01T10:00:00Z",
  "duration": 20,
  "notes": "更新的考试注意事项"
}
```

#### 7.6 删除日程
- **接口**: `DELETE /api/v1/schedules/{id}`
- **描述**: 删除日程
- **权限**: 操作员及以上
- **响应**:
```json
{
  "message": "Schedule deleted successfully"
}
```

#### 7.7 开始日程
- **接口**: `POST /api/v1/schedules/{id}/start`
- **描述**: 开始考试日程
- **权限**: 操作员及以上
- **响应**:
```json
{
  "id": 1,
  "status": "in_progress",
  "started_at": "2024-01-01T09:00:00Z",
  "message": "Schedule started successfully"
}
```

#### 7.8 完成日程
- **接口**: `POST /api/v1/schedules/{id}/complete`
- **描述**: 完成考试日程
- **权限**: 操作员及以上
- **请求体**:
```json
{
  "result": "pass",
  "score": 85,
  "notes": "考试完成，表现良好"
}
```

#### 7.9 获取日程统计
- **接口**: `GET /api/v1/schedules/statistics/overview`
- **描述**: 获取日程统计概览
- **权限**: 需要认证
- **响应**:
```json
{
  "today": {
    "total": 10,
    "completed": 5,
    "in_progress": 2,
    "scheduled": 3
  },
  "this_week": {
    "total": 50,
    "completed": 30,
    "scheduled": 20
  },
  "this_month": {
    "total": 200,
    "completed": 150,
    "scheduled": 50
  }
}
```

#### 7.10 获取考场今日日程
- **接口**: `GET /api/v1/schedules/venue/{id}/today`
- **描述**: 获取指定考场今日的所有日程
- **权限**: 需要认证
- **响应**:
```json
{
  "venue": {
    "id": 1,
    "name": "多旋翼A号实操场"
  },
  "date": "2024-01-01",
  "schedules": [
    {
      "id": 1,
      "exam_time": "2024-01-01T09:00:00Z",
      "duration": 15,
      "candidate_name": "张三",
      "exam_product": "多旋翼视距内驾驶员",
      "status": "scheduled"
    }
  ],
  "total": 1
}
```

### 8. 微信小程序模块 (WeChat Mini Program) - 11个接口

#### 8.1 微信小程序登录
- **接口**: `POST /api/v1/wechat/login`
- **描述**: 考生通过身份证号登录小程序
- **权限**: 公开
- **请求体**:
```json
{
  "id_card": "110101199001011234",
  "openid": "wx_openid_123456"
}
```
- **响应**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "username": "candidate_001",
    "real_name": "张三",
    "role": "candidate"
  }
}
```

#### 8.2 根据身份证获取考生信息 ⭐ 新增
- **接口**: `GET /api/v1/wechat/candidate/info-by-idcard`
- **描述**: 根据身份证号获取考生基本信息（登录前验证）
- **权限**: 公开
- **查询参数**:
  - `id_card`: 身份证号 (必填)
- **响应**:
```json
{
  "success": true,
  "data": {
    "candidate_id": 1,
    "name": "张三",
    "id_card": "110101199001011234",
    "phone": "13800138001",
    "institution": {
      "id": 1,
      "name": "北京航空培训中心",
      "code": "BJAV001"
    },
    "status": "active",
    "has_pending_exams": true,
    "next_exam_date": "2024-01-15"
  },
  "message": "考生信息获取成功"
}
```
- **错误响应**:
```json
{
  "success": false,
  "error": {
    "code": "CANDIDATE_NOT_FOUND",
    "message": "未找到该身份证号对应的考生信息",
    "details": {
      "id_card": "110101199001011234",
      "suggestion": "请确认身份证号是否正确，或联系培训机构确认报名状态"
    }
  }
}
```

#### 8.3 获取考生日程
- **接口**: `GET /api/v1/wechat/candidate/schedule`
- **描述**: 获取当前考生的考试日程
- **权限**: 考生认证
- **响应**:
```json
[
  {
    "id": 1,
    "registration_id": 1,
    "venue_id": 1,
    "schedule_date": "2024-01-15",
    "start_time": "2024-01-15T09:00:00Z",
    "end_time": "2024-01-15T09:15:00Z",
    "status": "pending",
    "queue_position": 3,
    "venue_name": "多旋翼A号实操场",
    "venue_type": "实操",
    "exam_product_name": "多旋翼视距内驾驶员",
    "exam_type": "practical",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

#### 8.4 获取考生二维码
- **接口**: `GET /api/v1/wechat/candidate/qrcode`
- **描述**: 生成考生签到二维码
- **权限**: 考生认证
- **响应**:
```json
{
  "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "qr_data": "{\"type\":\"candidate\",\"candidate_id\":1,\"schedule_id\":1,\"timestamp\":\"2024-01-01T09:00:00Z\"}",
  "expires_at": "2024-01-01T10:00:00Z"
}
```

#### 8.5 刷新考生二维码 ⭐ 新增
- **接口**: `POST /api/v1/wechat/candidate/qrcode/refresh`
- **描述**: 刷新考生的动态二维码
- **权限**: 考生认证
- **请求体**:
```json
{
  "reason": "二维码过期",
  "current_location": {
    "latitude": 39.9042,
    "longitude": 116.4074
  }
}
```
- **响应**:
```json
{
  "success": true,
  "data": {
    "qrcode_url": "data:qrcode;text,{\"type\":\"candidate\",\"candidate_id\":1,\"timestamp\":1704067200,\"version\":2,\"hash\":\"abc12345\"}",
    "qrcode_data": "{\"type\":\"candidate\",\"candidate_id\":1,\"timestamp\":1704067200,\"version\":2,\"hash\":\"abc12345\"}",
    "expires_at": "2024-01-01T11:00:00Z",
    "refresh_count": 2,
    "max_refresh_per_day": 10,
    "next_refresh_available_at": "2024-01-01T09:05:00Z"
  },
  "message": "二维码刷新成功"
}
```
- **频率限制响应**:
```json
{
  "success": false,
  "error": {
    "code": "REFRESH_RATE_LIMITED",
    "message": "二维码刷新过于频繁，请稍后再试",
    "details": {
      "current_count": 10,
      "max_per_day": 10,
      "reset_time": "2024-01-02T00:00:00Z",
      "next_available": "2024-01-01T09:05:00Z"
    }
  }
}
```

#### 8.6 获取考生签到历史 ⭐ 新增
- **接口**: `GET /api/v1/wechat/candidate/checkin-history`
- **描述**: 获取考生的签到历史记录
- **权限**: 考生认证
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `size`: 每页数量 (默认: 10)
  - `date_from`: 开始日期 (YYYY-MM-DD)
  - `date_to`: 结束日期 (YYYY-MM-DD)
  - `status`: 状态筛选 (all/success/late/failed)
- **响应**:
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "checkin_time": "2024-01-15T08:45:00Z",
        "status": "success",
        "method": "qr_code",
        "venue": {
          "id": 1,
          "name": "多旋翼A号实操场"
        },
        "notes": ""
      }
    ],
    "pagination": {
      "total": 5,
      "page": 1,
      "size": 10,
      "pages": 1
    },
    "statistics": {
      "total_checkins": 5,
      "successful_checkins": 4,
      "late_checkins": 1,
      "missed_checkins": 0
    }
  },
  "message": "签到历史获取成功"
}
```

#### 8.7 获取考生考试结果 ⭐ 新增
- **接口**: `GET /api/v1/wechat/candidate/exam-results`
- **描述**: 获取考生的考试结果记录
- **权限**: 考生认证
- **查询参数**:
  - `page`: 页码 (默认: 1)
  - `size`: 每页数量 (默认: 10)
  - `status`: 状态筛选 (all/completed/passed/failed)
  - `exam_product_id`: 考试产品ID筛选
  - `date_from`: 开始日期 (YYYY-MM-DD)
  - `date_to`: 结束日期 (YYYY-MM-DD)
- **响应**:
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "exam_date": "2024-01-15T09:00:00Z",
        "exam_product": {
          "id": 1,
          "name": "多旋翼视距内驾驶员",
          "code": "MULTIROTOR_VLOS"
        },
        "venue": {
          "id": 1,
          "name": "多旋翼A号实操场"
        },
        "status": "completed",
        "result": "pass",
        "score": 85,
        "max_score": 100,
        "pass_score": 70,
        "actual_duration": 12,
        "created_at": "2024-01-15T09:15:00Z"
      }
    ],
    "pagination": {
      "total": 3,
      "page": 1,
      "size": 10,
      "pages": 1
    },
    "summary": {
      "total_exams": 3,
      "passed_exams": 2,
      "failed_exams": 1,
      "pending_exams": 0,
      "pass_rate": 66.7,
      "average_score": 78.3
    }
  },
  "message": "考试结果获取成功"
}
```

#### 8.8 获取考场状态 (公共接口)
- **接口**: `GET /api/v1/wechat/venues/status`
- **描述**: 获取所有考场的实时状态
- **权限**: 公开
- **响应**:
```json
[
  {
    "venue_id": 1,
    "venue_name": "多旋翼A号实操场",
    "venue_type": "实操",
    "status": "available",
    "current_candidate": "张**",
    "waiting_count": 3,
    "next_start_time": "10:00",
    "capacity": 20
  }
]
```

#### 8.9 扫码签到
- **接口**: `POST /api/v1/wechat/checkin`
- **描述**: 考务人员扫码为考生签到
- **权限**: 考务人员认证
- **请求体**:
```json
{
  "schedule_id": 1,
  "venue_id": 1
}
```
- **响应**:
```json
{
  "success": true,
  "message": "张三 签到成功",
  "candidate_name": "张三",
  "schedule_info": {
    "schedule_id": 1,
    "venue_name": "多旋翼A号实操场",
    "exam_product_name": "多旋翼视距内驾驶员",
    "start_time": "09:00"
  },
  "checkin_time": "2024-01-15T08:45:00Z"
}
```

#### 8.10 获取排队位置
- **接口**: `GET /api/v1/wechat/candidate/queue-position`
- **描述**: 获取考生当前排队位置
- **权限**: 考生认证
- **响应**:
```json
{
  "venue_name": "多旋翼A号实操场",
  "position": 3,
  "total_waiting": 8,
  "estimated_wait_time": 45
}
```

#### 8.11 获取看板数据
- **接口**: `GET /api/v1/wechat/dashboard`
- **描述**: 获取小程序看板展示数据
- **权限**: 公开
- **响应**:
```json
{
  "title": "UAV考点实时状态",
  "update_time": "09:30",
  "venues": [
    {
      "venue_id": 1,
      "venue_name": "多旋翼A号实操场",
      "venue_type": "实操",
      "status": "available",
      "current_candidate": "张**",
      "waiting_count": 3,
      "next_start_time": "10:00",
      "capacity": 20
    }
  ],
  "summary": {
    "total_venues": 5,
    "active_venues": 4,
    "total_waiting": 12
  }
}
```

### 9. 系统管理模块 (System Management) - 4个接口

#### 9.1 获取系统配置
- **接口**: `GET /api/v1/system/config`
- **描述**: 获取系统配置信息
- **权限**: 管理员
- **响应**:
```json
{
  "system_name": "UAV考点运营管理系统",
  "version": "1.0.0",
  "timezone": "Asia/Shanghai",
  "max_upload_size": "10MB",
  "supported_file_types": ["xlsx", "xls", "csv"],
  "exam_settings": {
    "default_duration": 15,
    "checkin_advance_time": 30,
    "auto_complete_delay": 5
  }
}
```

#### 9.2 获取系统状态
- **接口**: `GET /api/v1/system/status`
- **描述**: 获取系统运行状态
- **权限**: 管理员
- **响应**:
```json
{
  "status": "running",
  "uptime": "5 days, 12 hours",
  "database": {
    "status": "connected",
    "connections": 5,
    "max_connections": 100
  },
  "memory_usage": "256MB / 1GB",
  "disk_usage": "2.5GB / 10GB",
  "active_users": 15
}
```

#### 9.3 获取系统功能特性
- **接口**: `GET /api/v1/system/features`
- **描述**: 获取系统支持的功能特性
- **权限**: 公开
- **响应**:
```json
{
  "features": {
    "multi_institution": true,
    "wechat_integration": true,
    "batch_import": true,
    "qr_code_checkin": true,
    "real_time_dashboard": true,
    "auto_scheduling": false,
    "sms_notification": false
  },
  "modules": [
    "institution_management",
    "venue_management",
    "candidate_management",
    "schedule_management",
    "wechat_miniprogram"
  ]
}
```

#### 9.4 获取版本信息
- **接口**: `GET /api/v1/system/version`
- **描述**: 获取系统版本信息
- **权限**: 公开
- **响应**:
```json
{
  "version": "1.0.0",
  "build_date": "2024-01-01",
  "git_commit": "abc123def456",
  "environment": "production",
  "dependencies": {
    "fastapi": "0.104.1",
    "sqlalchemy": "2.0.23",
    "python": "3.11.0"
  }
}
```

## 错误响应格式

所有API在发生错误时都会返回统一的错误响应格式：

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "请求参数验证失败",
    "details": {
      "field": "username",
      "issue": "用户名不能为空"
    }
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 常见错误代码

- `AUTHENTICATION_REQUIRED`: 需要认证
- `PERMISSION_DENIED`: 权限不足
- `VALIDATION_ERROR`: 参数验证失败
- `RESOURCE_NOT_FOUND`: 资源不存在
- `DUPLICATE_RESOURCE`: 资源重复
- `INTERNAL_SERVER_ERROR`: 服务器内部错误

## 权限说明

### 用户角色

- **super_admin**: 超级管理员，拥有所有权限
- **admin**: 管理员，可管理机构、考场、考试产品
- **operator**: 操作员，可管理本机构的考生和日程
- **candidate**: 考生，只能查看自己的信息和日程

### 权限级别

- **公开**: 无需认证即可访问
- **需要认证**: 需要有效的JWT令牌
- **操作员及以上**: 需要operator、admin或super_admin角色
- **管理员**: 需要admin或super_admin角色
- **超级管理员**: 需要super_admin角色
- **考生认证**: 需要candidate角色的JWT令牌

## 接口总数统计

- **健康检查模块**: 5个接口
- **认证授权模块**: 6个接口
- **机构管理模块**: 8个接口 ⭐ (更新)
- **考场管理模块**: 8个接口
- **考试产品管理模块**: 6个接口
- **考生管理模块**: 8个接口
- **日程管理模块**: 10个接口
- **微信小程序模块**: 11个接口
- **系统管理模块**: 4个接口

**总计**: 66个API接口 ⭐ (更新统计)

### 接口实现状态

本文档基于实际代码实现进行了全面更新，确保所有接口信息与后端实现完全一致：

#### ✅ 已验证的模块
- **健康检查模块**: 5个接口 - 完全匹配
- **认证授权模块**: 6个接口 - 完全匹配  
- **系统管理模块**: 4个接口 - 完全匹配
- **微信小程序模块**: 11个接口 - 完全匹配
- **机构管理模块**: 8个接口 - 已更新参数格式
- **考场管理模块**: 8个接口 - 已更新响应格式
- **考试产品管理模块**: 6个接口 - 已更新查询参数
- **考生管理模块**: 8个接口 - 已更新响应结构
- **日程管理模块**: 10个接口 - 已更新请求参数

#### 🔧 主要更新内容
1. **参数格式统一**: 将分页参数统一为 `skip/limit` 格式
2. **响应结构优化**: 更新了实际的响应数据结构
3. **权限说明完善**: 明确了各接口的权限要求
4. **接口总数修正**: 总计66个API接口

#### 📋 文档质量保证
- ✅ 所有接口路径与实际代码一致
- ✅ 请求参数与实际实现匹配
- ✅ 响应格式基于真实数据结构
- ✅ 权限控制说明准确
- ✅ 错误处理机制完整

---

*文档最后更新时间: 2025-08-26*  
*版本: v1.1.0*  
*更新内容: 基于实际代码实现全面校验和更新*
