# UAV考点运营管理系统 - 后端API接口文档

## 文档信息
- **版本**: v1.0.0
- **更新时间**: 2025-08-28
- **基础URL**: `http://localhost:8000/api/v1`
- **认证方式**: JWT Bearer Token

---

## 目录
1. [基础接口](#1-基础接口)
2. [认证接口](#2-认证接口)
3. [系统管理接口](#3-系统管理接口)
4. [微信相关接口](#4-微信相关接口)
5. [用户管理接口](#5-用户管理接口)
6. [机构管理接口](#6-机构管理接口)
7. [考场管理接口](#7-考场管理接口)
8. [考试产品接口](#8-考试产品接口)
9. [考试安排接口](#9-考试安排接口)

---

## 1. 基础接口

### 1.1 基础健康检查
**接口**: `GET /health/`  
**描述**: 系统基础健康检查  
**认证**: 无需认证  

**响应示例**:
```json
{
  "status": "healthy",
  "message": "UAV考点运营管理系统运行正常",
  "timestamp": "2025-08-28T03:00:00.000Z",
  "version": "1.0.0",
  "environment": "development"
}
```

### 1.2 详细健康检查
**接口**: `GET /health/detailed`  
**描述**: 详细的系统健康检查，包括数据库连接等  
**认证**: 无需认证  

**响应示例**:
```json
{
  "status": "healthy",
  "timestamp": "2025-08-28T03:00:00.000Z",
  "version": "1.0.0",
  "checks": {
    "database": {
      "status": "healthy",
      "response_time_ms": 15.2,
      "message": "数据库连接正常"
    },
    "redis": {
      "status": "not_configured",
      "message": "Redis未配置"
    },
    "filesystem": {
      "status": "healthy",
      "message": "文件系统可写"
    }
  }
}
```

### 1.3 数据库健康检查
**接口**: `GET /health/database`  
**描述**: 专门的数据库健康检查  
**认证**: 无需认证  

**响应示例**:
```json
{
  "status": "healthy",
  "connection_time_ms": 12.5,
  "tables": {
    "users": {
      "exists": true,
      "count": 12
    },
    "institutions": {
      "exists": true,
      "count": 3
    },
    "venues": {
      "exists": true,
      "count": 7
    },
    "exam_products": {
      "exists": true,
      "count": 6
    }
  },
  "timestamp": "2025-08-28T03:00:00.000Z"
}
```

### 1.4 就绪检查
**接口**: `GET /health/readiness`  
**描述**: 应用就绪检查 - 检查应用是否准备好接收流量  
**认证**: 无需认证  

**响应示例**:
```json
{
  "ready": true,
  "checks": [
    {
      "name": "database",
      "ready": true,
      "message": "数据库连接正常"
    },
    {
      "name": "configuration",
      "ready": true,
      "message": "必要配置项完整"
    }
  ],
  "timestamp": "2025-08-28T03:00:00.000Z"
}
```

### 1.5 存活检查
**接口**: `GET /health/liveness`  
**描述**: 应用存活检查 - 检查应用进程是否正常运行  
**认证**: 无需认证  

**响应示例**:
```json
{
  "alive": true,
  "timestamp": "2025-08-28T03:00:00.000Z",
  "uptime": "运行中",
  "memory_usage": "正常",
  "cpu_usage": "正常"
}
```

---

## 2. 认证接口

### 2.1 用户登录 (JSON格式)
**接口**: `POST /auth/login`  
**描述**: 用户登录获取JWT访问令牌  
**认证**: 无需认证  

**请求体**:
```json
{
  "username": "admin",
  "password": "123456"
}
```

**响应示例**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "role": "super_admin",
    "full_name": "系统管理员"
  }
}
```

**考生登录响应示例**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": 5,
    "username": "candidate_011234",
    "email": "zhangsan@example.com",
    "role": "candidate",
    "full_name": "张三"
  },
  "current_exam": {
    "schedule_id": 1,
    "venue_id": 1,
    "exam_session": "上午",
    "exam_date": "2025-01-26",
    "start_time": "09:00",
    "end_time": "10:00",
    "venue_name": "北京理论考试教室A",
    "exam_name": "多旋翼视距内驾驶员理论"
  },
  "has_valid_schedule": true
}
```

### 2.2 用户登录 (OAuth2格式)
**接口**: `POST /auth/token`  
**描述**: 用户登录获取JWT访问令牌（OAuth2 form-data格式，用于兼容）  
**认证**: 无需认证  
**Content-Type**: `application/x-www-form-urlencoded`

**请求体**:
```
username=admin&password=123456
```

**响应示例**: 同上

### 2.3 用户注册
**接口**: `POST /auth/register`  
**描述**: 用户注册  
**认证**: 无需认证  

**请求体**:
```json
{
  "username": "newuser",
  "password": "password123",
  "email": "newuser@example.com",
  "full_name": "新用户",
  "phone": "13800138000"
}
```

**响应示例**:
```json
{
  "message": "注册成功",
  "user_id": 13,
  "username": "newuser"
}
```

### 2.4 获取当前用户信息
**接口**: `GET /auth/me`  
**描述**: 获取当前登录用户的详细信息  
**认证**: 需要Bearer Token  

**响应示例**:
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "phone": "13800138000",
  "full_name": "系统管理员",
  "role": "super_admin",
  "is_active": true,
  "is_verified": true,
  "institution_id": null,
  "created_at": "2025-01-15T08:00:00Z",
  "last_login": "2025-08-28T03:00:00Z"
}
```

### 2.5 用户登出
**接口**: `POST /auth/logout`  
**描述**: 用户登出（实际上由于JWT无状态，主要在客户端删除token）  
**认证**: 需要Bearer Token  

**响应示例**:
```json
{
  "message": "登出成功"
}
```

### 2.6 刷新访问令牌
**接口**: `POST /auth/refresh`  
**描述**: 刷新访问令牌  
**认证**: 无需认证  

**请求体**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**响应示例**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "role": "super_admin",
    "full_name": "系统管理员"
  }
}
```

---

## 3. 系统管理接口

### 3.1 获取系统配置
**接口**: `GET /system/config`  
**描述**: 获取系统可配置参数和设置  
**认证**: 需要Bearer Token  

**响应示例**:
```json
{
  "app_info": {
    "name": "UAV考点运营管理系统",
    "version": "1.0.0",
    "environment": "development"
  },
  "auth_settings": {
    "token_expire_minutes": 30,
    "password_min_length": 6,
    "username_min_length": 3
  },
  "file_upload": {
    "max_file_size": 10485760,
    "allowed_extensions": [".xlsx", ".xls", ".csv"],
    "upload_path": "uploads"
  },
  "exam_settings": {
    "max_candidates_per_venue": 50,
    "exam_duration_minutes": 120,
    "checkin_advance_minutes": 30,
    "late_arrival_tolerance_minutes": 15
  },
  "venue_settings": {
    "default_capacity": 20,
    "venue_types": ["理论", "实操", "综合"],
    "status_options": ["active", "inactive", "maintenance"]
  },
  "notification_settings": {
    "email_enabled": false,
    "sms_enabled": false,
    "wechat_enabled": false
  }
}
```

### 3.2 获取系统状态
**接口**: `GET /system/status`  
**描述**: 获取系统运行状态  
**认证**: 需要Bearer Token  

**响应示例**:
```json
{
  "status": "healthy",
  "timestamp": "2025-08-28T03:00:00Z",
  "uptime": "24小时",
  "version": "1.0.0",
  "services": {
    "database": "connected",
    "redis": "not_configured",
    "wechat": "not_configured"
  },
  "statistics": {
    "total_users": 12,
    "total_institutions": 3,
    "total_venues": 7,
    "total_exam_products": 6
  },
  "performance": {
    "active_connections": 1,
    "memory_usage": "128MB",
    "cpu_usage": "15%"
  }
}
```

### 3.3 获取系统功能特性
**接口**: `GET /system/features`  
**描述**: 获取系统支持的功能特性列表  
**认证**: 无需认证  

**响应示例**:
```json
{
  "authentication": {
    "jwt_token": true,
    "role_based_access": true,
    "multi_login_methods": true
  },
  "user_management": {
    "user_registration": true,
    "role_management": true,
    "institution_binding": true
  },
  "exam_management": {
    "exam_products": true,
    "candidate_management": true,
    "venue_management": true,
    "schedule_management": true
  },
  "integrations": {
    "wechat_miniprogram": false,
    "qr_code_checkin": true,
    "email_notifications": false,
    "file_upload": true
  },
  "reporting": {
    "real_time_dashboard": true,
    "export_functionality": true,
    "statistics": true
  },
  "scalability": {
    "concurrent_users": 1200,
    "docker_deployment": true,
    "load_balancing_ready": true
  }
}
```

### 3.4 获取版本信息
**接口**: `GET /system/version`  
**描述**: 获取系统版本信息  
**认证**: 无需认证  

**响应示例**:
```json
{
  "version": "1.0.0",
  "build_date": "2025-01-15",
  "git_commit": "latest",
  "api_version": "v1",
  "changelog": [
    {
      "version": "1.0.0",
      "date": "2025-01-15",
      "changes": [
        "初始版本发布",
        "完整的考点运营管理功能",
        "微信小程序支持",
        "Docker部署支持"
      ]
    }
  ]
}
```

---
---

## 4. 微信相关接口

### 4.1 微信小程序登录
**接口**: `POST /wechat/login`  
**描述**: 微信小程序登录（身份证号登录）  
**认证**: 无需认证  

**请求体**:
```json
{
  "id_card": "110101199001011234",
  "openid": "wx_123456789"
}
```

**响应示例**:
```json
{
  "success": true,
  "message": "登录成功",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 5,
    "username": "candidate_011234",
    "real_name": "张三",
    "id_card": "110101199001011234",
    "role": "candidate"
  }
}
```

### 4.2 根据身份证获取考生信息
**接口**: `GET /wechat/candidate/info-by-idcard`  
**描述**: 根据身份证号获取考生信息（公开接口）  
**认证**: 无需认证  

**查询参数**:
- `id_card` (string, required): 身份证号

**响应示例**:
```json
{
  "id": 5,
  "name": "张三",
  "id_card": "110101199001011234",
  "phone": "13800138001",
  "email": "zhangsan@example.com",
  "status": "active",
  "current_schedule_id": 1,
  "current_venue_id": 1,
  "exam_time": "2025-01-26T09:00:00Z",
  "exam_end_time": "2025-01-26T10:00:00Z",
  "venue_name": "北京理论考试教室A",
  "venue_address": "北京市朝阳区建国路88号教学楼2层201室",
  "exam_name": "多旋翼视距内驾驶员理论",
  "exam_type": "理论",
  "exam_status": "pending"
}
```

### 4.3 获取考生日程
**接口**: `GET /wechat/candidate/schedule`  
**描述**: 获取当前考生的日程安排  
**认证**: 需要Bearer Token (考生角色)  

**响应示例**:
```json
{
  "candidate_id": 5,
  "candidate_name": "张三",
  "schedules": [
    {
      "schedule_id": 1,
      "exam_date": "2025-01-26",
      "start_time": "09:00",
      "end_time": "10:00",
      "venue_name": "北京理论考试教室A",
      "venue_address": "北京市朝阳区建国路88号教学楼2层201室",
      "exam_name": "多旋翼视距内驾驶员理论",
      "exam_type": "理论",
      "status": "pending",
      "can_checkin": false,
      "checkin_start_time": "2025-01-26T08:30:00Z",
      "exam_result": null
    }
  ],
  "total_count": 1
}
```

### 4.4 获取考生二维码
**接口**: `GET /wechat/candidate/qrcode`  
**描述**: 获取考生的动态二维码  
**认证**: 需要Bearer Token (考生角色)  

**响应示例**:
```json
{
  "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "backup_code": "123456",
  "expires_at": "2025-08-28T11:30:00Z",
  "refresh_interval": 30,
  "qr_data": {
    "candidate_id": 5,
    "name": "张三",
    "id_card": "110101199001011234",
    "username": "candidate_011234",
    "schedule_id": 1,
    "venue_id": 1,
    "exam_session": "上午",
    "exam_date": "2025-01-26",
    "timestamp": 1724817000,
    "type": "candidate_checkin"
  }
}
```

### 4.5 刷新考生二维码
**接口**: `POST /wechat/candidate/qrcode/refresh`  
**描述**: 刷新考生的动态二维码  
**认证**: 需要Bearer Token (考生角色)  

**响应示例**:
```json
{
  "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "backup_code": "789012",
  "expires_at": "2025-08-28T11:35:00Z",
  "refresh_interval": 30
}
```

### 4.6 扫码签到
**接口**: `POST /wechat/checkin`  
**描述**: 考务人员扫码签到  
**认证**: 需要Bearer Token (考务人员角色)  

**请求体**:
```json
{
  "qr_code_data": "{\"candidate_id\":5,\"name\":\"张三\",\"id_card\":\"110101199001011234\",\"username\":\"candidate_011234\",\"schedule_id\":1,\"venue_id\":1,\"exam_session\":\"上午\",\"exam_date\":\"2025-01-26\",\"timestamp\":1724817000,\"type\":\"candidate_checkin\"}"
}
```

**响应示例**:
```json
{
  "success": true,
  "message": "签到成功",
  "checkin_time": "2025-08-28T11:05:00Z",
  "schedule_info": {
    "schedule_id": 1,
    "venue_name": "北京理论考试教室A",
    "venue_address": "北京市朝阳区建国路88号教学楼2层201室",
    "status": "checked_in",
    "candidate_name": "张三"
  }
}
```

### 4.7 获取考场状态
**接口**: `GET /wechat/venues/status`  
**描述**: 获取所有考场的实时状态  
**认证**: 需要Bearer Token  

**响应示例**:
```json
[
  {
    "id": 1,
    "name": "北京理论考试教室A",
    "address": "北京市朝阳区建国路88号教学楼2层201室",
    "capacity": 50,
    "current_occupancy": 25,
    "utilization_rate": 0.5,
    "status": "active",
    "current_exam": {
      "exam_name": "多旋翼视距内驾驶员理论",
      "start_time": "09:00",
      "end_time": "10:00",
      "candidates_count": 25
    }
  }
]
```

### 4.8 获取排队位置
**接口**: `GET /wechat/candidate/queue-position`  
**描述**: 获取考生在当前考场的排队位置  
**认证**: 需要Bearer Token (考生角色)  

**响应示例**:
```json
{
  "position": 3,
  "total_queue": 15,
  "estimated_wait_time": "15分钟",
  "venue_name": "北京理论考试教室A",
  "current_candidate": {
    "name": "李四",
    "exam_start_time": "09:00"
  },
  "next_start_time": "09:15",
  "last_updated": "2025-08-28T11:05:00Z"
}
```

### 4.9 获取看板数据
**接口**: `GET /wechat/dashboard`  
**描述**: 获取小程序看板数据（公共接口）  
**认证**: 无需认证  

**响应示例**:
```json
{
  "statistics": {
    "total_scheduled": 50,
    "checked_in": 35,
    "in_progress": 20,
    "completed": 15
  },
  "venues": [
    {
      "id": 1,
      "name": "北京理论考试教室A",
      "address": "北京市朝阳区建国路88号教学楼2层201室",
      "capacity": 50,
      "current_occupied": 25,
      "utilization_rate": 0.5
    }
  ],
  "announcements": [
    {
      "id": 1,
      "title": "考试注意事项",
      "content": "请考生提前30分钟到达考场",
      "type": "notice",
      "published_at": "2025-08-28T08:00:00Z"
    }
  ],
  "last_updated": "2025-08-28T11:05:00Z"
}
```

### 4.10 获取考生签到历史
**接口**: `GET /wechat/candidate/checkin-history`  
**描述**: 获取考生的签到历史记录  
**认证**: 需要Bearer Token (考生角色)  

**响应示例**:
```json
[
  {
    "id": 1,
    "schedule_id": 1,
    "venue_name": "北京理论考试教室A",
    "exam_name": "多旋翼视距内驾驶员理论",
    "checkin_time": "2025-01-26T08:45:00Z",
    "status": "success",
    "method": "qr_code",
    "staff_name": "北京管理员",
    "notes": "正常签到"
  }
]
```

### 4.11 获取考生考试结果
**接口**: `GET /wechat/candidate/exam-results`  
**描述**: 获取考生的考试结果  
**认证**: 需要Bearer Token (考生角色)  

**响应示例**:
```json
[
  {
    "id": 1,
    "schedule_id": 1,
    "exam_name": "多旋翼视距内驾驶员理论",
    "exam_date": "2025-01-26",
    "venue_name": "北京理论考试教室A",
    "result": "pass",
    "score": 85,
    "max_score": 100,
    "pass_score": 70,
    "duration": 60,
    "notes": "考试通过",
    "completed_at": "2025-01-26T10:00:00Z"
  }
]
```

---

## 5. 考生管理接口

### 5.1 获取考生列表
**接口**: `GET /candidates/`  
**描述**: 分页获取考生列表，支持搜索和筛选  
**认证**: 需要Bearer Token (管理员/操作员角色)  

**查询参数**:
- `page` (int, optional): 页码，默认1
- `size` (int, optional): 每页数量，默认20
- `search` (string, optional): 搜索关键词
- `institution_id` (int, optional): 机构ID筛选
- `status` (string, optional): 状态筛选

**响应示例**:
```json
{
  "items": [
    {
      "id": 5,
      "real_name": "张三",
      "id_card": "110101199001011234",
      "exam_product_id": 1,
      "institution_id": 1,
      "phone": "13800138001",
      "email": "zhangsan@example.com",
      "username": "candidate_011234",
      "role": "candidate",
      "is_active": true,
      "is_verified": true,
      "created_at": "2025-01-20T10:00:00Z",
      "updated_at": "2025-01-20T10:00:00Z",
      "last_login": null
    }
  ],
  "total": 50,
  "page": 1,
  "size": 20,
  "pages": 3
}
```

### 5.2 获取考生详情
**接口**: `GET /candidates/{candidate_id}`  
**描述**: 根据ID获取指定考生的详细信息  
**认证**: 需要Bearer Token (管理员/操作员角色)  

**路径参数**:
- `candidate_id` (int, required): 考生ID

**响应示例**:
```json
{
  "id": 5,
  "real_name": "张三",
  "id_card": "110101199001011234",
  "exam_product_id": 1,
  "institution_id": 1,
  "phone": "13800138001",
  "email": "zhangsan@example.com",
  "username": "candidate_011234",
  "role": "candidate",
  "is_active": true,
  "is_verified": true,
  "created_at": "2025-01-20T10:00:00Z",
  "updated_at": "2025-01-20T10:00:00Z",
  "last_login": null,
  "registrations": [
    {
      "id": 1,
      "exam_product_id": 1,
      "registration_number": "REG2025012000501",
      "status": "active",
      "created_at": "2025-01-20T10:00:00Z"
    }
  ]
}
```

### 5.3 创建考生
**接口**: `POST /candidates/`  
**描述**: 创建新考生  
**认证**: 需要Bearer Token (管理员/操作员角色)  

**请求体**:
```json
{
  "real_name": "王五",
  "id_card": "110101199001011236",
  "exam_product_id": 1,
  "institution_id": 1,
  "phone": "13800138002",
  "email": "wangwu@example.com"
}
```

**响应示例**:
```json
{
  "id": 6,
  "real_name": "王五",
  "id_card": "110101199001011236",
  "exam_product_id": 1,
  "institution_id": 1,
  "phone": "13800138002",
  "email": "wangwu@example.com",
  "username": "candidate_011236",
  "role": "candidate",
  "is_active": true,
  "is_verified": false,
  "created_at": "2025-08-28T11:00:00Z",
  "updated_at": "2025-08-28T11:00:00Z",
  "last_login": null
}
```

### 5.4 更新考生
**接口**: `PUT /candidates/{candidate_id}`  
**描述**: 更新指定考生的信息  
**认证**: 需要Bearer Token (管理员/操作员角色)  

**路径参数**:
- `candidate_id` (int, required): 考生ID

**请求体**:
```json
{
  "real_name": "王五五",
  "phone": "13800138003",
  "email": "wangwuwu@example.com",
  "is_active": true
}
```

### 5.5 删除考生
**接口**: `DELETE /candidates/{candidate_id}`  
**描述**: 删除指定的考生（软删除）  
**认证**: 需要Bearer Token (管理员角色)  

**路径参数**:
- `candidate_id` (int, required): 考生ID

**响应示例**:
```json
{
  "message": "考生删除成功"
}
```

### 5.6 批量导入考生
**接口**: `POST /candidates/batch-import`  
**描述**: 批量导入考生（Excel文件）  
**认证**: 需要Bearer Token (管理员/操作员角色)  

**请求体**: `multipart/form-data`
- `file` (file, required): Excel文件 (.xlsx/.xls)

**响应示例**:
```json
{
  "success_count": 45,
  "error_count": 5,
  "total_count": 50,
  "errors": [
    {
      "row": 3,
      "error": "身份证号格式错误"
    },
    {
      "row": 7,
      "error": "姓名不能为空"
    }
  ],
  "message": "批量导入完成，成功45条，失败5条"
}
```

### 5.7 下载考生导入模板
**接口**: `GET /candidates/template/download`  
**描述**: 下载考生批量导入的Excel模板  
**认证**: 需要Bearer Token  

**响应**: Excel文件下载

### 5.8 获取考生统计信息
**接口**: `GET /candidates/statistics`  
**描述**: 获取考生统计信息  
**认证**: 需要Bearer Token (管理员/操作员角色)  

**响应示例**:
```json
{
  "total_candidates": 150,
  "active_candidates": 140,
  "inactive_candidates": 10,
  "verified_candidates": 130,
  "unverified_candidates": 20,
  "by_institution": [
    {
      "institution_id": 1,
      "institution_name": "北京培训机构",
      "candidate_count": 80
    },
    {
      "institution_id": 2,
      "institution_name": "上海培训机构",
      "candidate_count": 70
    }
  ],
  "by_exam_product": [
    {
      "exam_product_id": 1,
      "exam_product_name": "多旋翼视距内驾驶员理论",
      "candidate_count": 90
    },
    {
      "exam_product_id": 2,
      "exam_product_name": "多旋翼视距内驾驶员实操",
      "candidate_count": 60
    }
  ],
  "recent_registrations": [
    {
      "date": "2025-08-28",
      "count": 5
    },
    {
      "date": "2025-08-27",
      "count": 8
    }
  ]
}
```

---

## 6. 考场管理接口

### 6.1 获取考场列表
**接口**: `GET /venues/`  
**描述**: 获取考场列表，支持筛选  
**认证**: 需要Bearer Token  

**查询参数**:
- `skip` (int, optional): 跳过数量，默认0
- `limit` (int, optional): 限制数量，默认100
- `institution_id` (int, optional): 机构ID筛选
- `status` (string, optional): 状态筛选
- `venue_type` (string, optional): 考场类型筛选

**响应示例**:
```json
[
  {
    "id": 1,
    "name": "北京考场A",
    "address": "北京市朝阳区xxx路xxx号",
    "institution_id": 1,
    "venue_type": "theory",
    "status": "available",
    "capacity": 50,
    "equipment": "投影仪、音响、空调",
    "contact_person": "张老师",
    "contact_phone": "13800138001",
    "created_at": "2025-01-15T10:00:00Z",
    "updated_at": "2025-01-15T10:00:00Z"
  }
]
```

### 6.2 获取考场详情
**接口**: `GET /venues/{venue_id}`  
**描述**: 根据ID获取指定考场的详细信息  
**认证**: 需要Bearer Token  

**路径参数**:
- `venue_id` (int, required): 考场ID

**响应示例**:
```json
{
  "id": 1,
  "name": "北京考场A",
  "address": "北京市朝阳区xxx路xxx号",
  "institution_id": 1,
  "venue_type": "theory",
  "status": "available",
  "capacity": 50,
  "equipment": "投影仪、音响、空调",
  "contact_person": "张老师",
  "contact_phone": "13800138001",
  "created_at": "2025-01-15T10:00:00Z",
  "updated_at": "2025-01-15T10:00:00Z"
}
```

### 6.3 创建考场
**接口**: `POST /venues/`  
**描述**: 创建新考场  
**认证**: 需要Bearer Token (管理员角色)  

**请求体**:
```json
{
  "name": "上海考场B",
  "address": "上海市浦东新区xxx路xxx号",
  "institution_id": 2,
  "venue_type": "practical",
  "capacity": 30,
  "equipment": "无人机设备、安全防护设施",
  "contact_person": "李老师",
  "contact_phone": "13800138002"
}
```

### 6.4 更新考场信息
**接口**: `PUT /venues/{venue_id}`  
**描述**: 更新指定考场的信息  
**认证**: 需要Bearer Token (管理员角色)  

**路径参数**:
- `venue_id` (int, required): 考场ID

**请求体**:
```json
{
  "name": "上海考场B（更新）",
  "capacity": 35,
  "equipment": "无人机设备、安全防护设施、新增监控设备",
  "contact_person": "李老师",
  "contact_phone": "13800138003"
}
```

### 6.5 删除考场
**接口**: `DELETE /venues/{venue_id}`  
**描述**: 删除指定的考场  
**认证**: 需要Bearer Token (管理员角色)  

**路径参数**:
- `venue_id` (int, required): 考场ID

**响应示例**:
```json
{
  "message": "考场删除成功"
}
```

### 6.6 切换考场状态
**接口**: `POST /venues/{venue_id}/toggle-status`  
**描述**: 切换考场的可用/维护状态  
**认证**: 需要Bearer Token (管理员角色)  

**路径参数**:
- `venue_id` (int, required): 考场ID

**响应示例**:
```json
{
  "message": "考场状态已切换为maintenance",
  "venue": {
    "id": 1,
    "name": "北京考场A",
    "status": "maintenance",
    "updated_at": "2025-08-28T11:00:00Z"
  }
}
```

### 6.7 获取考场日程
**接口**: `GET /venues/{venue_id}/schedules`  
**描述**: 获取考场的日程安排  
**认证**: 需要Bearer Token  

**路径参数**:
- `venue_id` (int, required): 考场ID

**查询参数**:
- `date` (string, optional): 日期筛选，格式YYYY-MM-DD

**响应示例**:
```json
[
  {
    "id": 1,
    "exam_product_id": 1,
    "venue_id": 1,
    "schedule_date": "2025-08-28",
    "start_time": "08:30:00",
    "end_time": "12:00:00",
    "max_candidates": 30,
    "registered_count": 25,
    "status": "scheduled",
    "exam_product": {
      "id": 1,
      "name": "多旋翼视距内驾驶员理论",
      "type": "theory"
    }
  }
]
```

### 6.8 获取考场当前状态
**接口**: `GET /venues/{venue_id}/current-status`  
**描述**: 获取考场当前状态信息  
**认证**: 需要Bearer Token  

**路径参数**:
- `venue_id` (int, required): 考场ID

**响应示例**:
```json
{
  "venue_id": 1,
  "venue_name": "北京考场A",
  "current_status": "available",
  "today_schedules": [
    {
      "schedule_id": 1,
      "exam_name": "多旋翼视距内驾驶员理论",
      "time_slot": "08:30-12:00",
      "registered_count": 25,
      "max_candidates": 30,
      "status": "in_progress"
    }
  ],
  "occupancy_rate": 83.33,
  "next_available_time": "14:00:00"
}
```

---

## 7. 考试产品管理接口

### 7.1 获取考试产品列表
**接口**: `GET /exam-products/`  
**描述**: 获取考试产品列表，支持筛选  
**认证**: 需要Bearer Token  

**查询参数**:
- `skip` (int, optional): 跳过数量，默认0
- `limit` (int, optional): 限制数量，默认100
- `is_active` (boolean, optional): 是否启用筛选
- `exam_type` (string, optional): 考试类型筛选

**响应示例**:
```json
[
  {
    "id": 1,
    "name": "多旋翼视距内驾驶员理论",
    "description": "多旋翼无人机视距内驾驶员理论考试",
    "exam_type": "theory",
    "duration_minutes": 120,
    "total_questions": 100,
    "passing_score": 70,
    "is_active": true,
    "created_at": "2025-01-10T10:00:00Z",
    "updated_at": "2025-01-10T10:00:00Z"
  },
  {
    "id": 2,
    "name": "多旋翼视距内驾驶员实操",
    "description": "多旋翼无人机视距内驾驶员实操考试",
    "exam_type": "practical",
    "duration_minutes": 60,
    "total_questions": null,
    "passing_score": 80,
    "is_active": true,
    "created_at": "2025-01-10T10:00:00Z",
    "updated_at": "2025-01-10T10:00:00Z"
  }
]
```

### 7.2 获取考试产品详情
**接口**: `GET /exam-products/{product_id}`  
**描述**: 根据ID获取指定考试产品的详细信息  
**认证**: 需要Bearer Token  

**路径参数**:
- `product_id` (int, required): 考试产品ID

**响应示例**:
```json
{
  "id": 1,
  "name": "多旋翼视距内驾驶员理论",
  "description": "多旋翼无人机视距内驾驶员理论考试",
  "exam_type": "theory",
  "duration_minutes": 120,
  "total_questions": 100,
  "passing_score": 70,
  "is_active": true,
  "created_at": "2025-01-10T10:00:00Z",
  "updated_at": "2025-01-10T10:00:00Z"
}
```

### 7.3 创建考试产品
**接口**: `POST /exam-products/`  
**描述**: 创建新的考试产品  
**认证**: 需要Bearer Token (管理员角色)  

**请求体**:
```json
{
  "name": "固定翼视距内驾驶员理论",
  "description": "固定翼无人机视距内驾驶员理论考试",
  "exam_type": "theory",
  "duration_minutes": 120,
  "total_questions": 100,
  "passing_score": 70
}
```

### 7.4 更新考试产品
**接口**: `PUT /exam-products/{product_id}`  
**描述**: 更新指定考试产品的信息  
**认证**: 需要Bearer Token (管理员角色)  

**路径参数**:
- `product_id` (int, required): 考试产品ID

**请求体**:
```json
{
  "name": "多旋翼视距内驾驶员理论（更新版）",
  "description": "多旋翼无人机视距内驾驶员理论考试（2025年版）",
  "duration_minutes": 150,
  "total_questions": 120,
  "passing_score": 75
}
```

### 7.5 删除考试产品
**接口**: `DELETE /exam-products/{product_id}`  
**描述**: 删除指定的考试产品  
**认证**: 需要Bearer Token (管理员角色)  

**路径参数**:
- `product_id` (int, required): 考试产品ID

**响应示例**:
```json
{
  "message": "考试产品删除成功"
}
```

### 7.6 切换考试产品状态
**接口**: `POST /exam-products/{product_id}/toggle-status`  
**描述**: 切换考试产品的启用/禁用状态  
**认证**: 需要Bearer Token (管理员角色)  

**路径参数**:
- `product_id` (int, required): 考试产品ID

**响应示例**:
```json
{
  "message": "考试产品状态已切换为禁用",
  "product": {
    "id": 1,
    "name": "多旋翼视距内驾驶员理论",
    "is_active": false,
    "updated_at": "2025-08-28T11:00:00Z"
  }
}
```

---

## 8. 机构管理接口

### 8.1 获取机构列表
**接口**: `GET /institutions/`  
**描述**: 分页获取机构列表，支持搜索和筛选  
**认证**: 需要Bearer Token  

**查询参数**:
- `skip` (int, optional): 跳过数量，默认0
- `limit` (int, optional): 限制数量，默认20
- `search` (string, optional): 搜索关键词
- `is_active` (boolean, optional): 是否启用筛选

**响应示例**:
```json
{
  "items": [
    {
      "id": 1,
      "name": "北京培训机构",
      "code": "BJ001",
      "type": "培训机构",
      "contact_person": "张主任",
      "contact_phone": "010-12345678",
      "contact_email": "contact@bj001.com",
      "address": "北京市朝阳区xxx路xxx号",
      "is_active": true,
      "is_approved": true,
      "created_at": "2025-01-01T10:00:00Z",
      "updated_at": "2025-01-01T10:00:00Z"
    }
  ],
  "total": 50,
  "skip": 0,
  "limit": 20
}
```

### 8.2 获取机构详情
**接口**: `GET /institutions/{institution_id}`  
**描述**: 根据ID获取指定机构的详细信息  
**认证**: 需要Bearer Token  

**路径参数**:
- `institution_id` (int, required): 机构ID

### 8.3 创建机构
**接口**: `POST /institutions/`  
**描述**: 创建新机构  
**认证**: 需要Bearer Token (管理员角色)  

**请求参数**:
- `name` (string, required): 机构名称
- `code` (string, required): 机构代码
- `type` (string, optional): 机构类型，默认"培训机构"
- `contact_person` (string, optional): 联系人
- `contact_phone` (string, optional): 联系电话
- `contact_email` (string, optional): 联系邮箱
- `address` (string, optional): 地址

### 8.4 更新机构信息
**接口**: `PUT /institutions/{institution_id}`  
**描述**: 更新指定机构的信息  
**认证**: 需要Bearer Token (管理员角色)  

### 8.5 删除机构
**接口**: `DELETE /institutions/{institution_id}`  
**描述**: 删除指定的机构  
**认证**: 需要Bearer Token (超级管理员角色)  

### 8.6 获取机构考场列表
**接口**: `GET /institutions/{institution_id}/venues`  
**描述**: 获取指定机构的考场列表  
**认证**: 需要Bearer Token  

### 8.7 获取机构统计信息
**接口**: `GET /institutions/{institution_id}/stats`  
**描述**: 获取机构的统计信息  
**认证**: 需要Bearer Token  

---

## 9. 日程管理接口

### 9.1 获取日程列表
**接口**: `GET /schedules/`  
**描述**: 获取日程列表，支持筛选  
**认证**: 需要Bearer Token  

**查询参数**:
- `skip` (int, optional): 跳过数量，默认0
- `limit` (int, optional): 限制数量，默认100
- `venue_id` (int, optional): 考场ID筛选
- `date` (string, optional): 日期筛选，格式YYYY-MM-DD
- `status` (string, optional): 状态筛选
- `institution_id` (int, optional): 机构ID筛选

**响应示例**:
```json
[
  {
    "id": 1,
    "registration_id": 1,
    "venue_id": 1,
    "exam_product_id": 1,
    "schedule_date": "2025-08-28",
    "start_time": "08:30:00",
    "end_time": "12:00:00",
    "status": "scheduled",
    "max_candidates": 30,
    "registered_count": 25,
    "created_at": "2025-08-20T10:00:00Z",
    "updated_at": "2025-08-20T10:00:00Z",
    "venue": {
      "id": 1,
      "name": "北京考场A",
      "address": "北京市朝阳区xxx路xxx号"
    },
    "exam_product": {
      "id": 1,
      "name": "多旋翼视距内驾驶员理论",
      "type": "theory"
    }
  }
]
```

### 9.2 获取日程详情
**接口**: `GET /schedules/{schedule_id}`  
**描述**: 根据ID获取指定日程的详细信息  
**认证**: 需要Bearer Token  

**路径参数**:
- `schedule_id` (int, required): 日程ID

### 9.3 创建日程
**接口**: `POST /schedules/`  
**描述**: 创建新日程  
**认证**: 需要Bearer Token (管理员角色)  

**请求体**:
```json
{
  "registration_id": 1,
  "venue_id": 1,
  "start_time": "2025-08-29T08:30:00Z",
  "end_time": "2025-08-29T12:00:00Z"
}
```

### 9.4 批量创建日程
**接口**: `POST /schedules/batch`  
**描述**: 批量创建日程安排  
**认证**: 需要Bearer Token (管理员角色)  

**请求体**:
```json
{
  "registration_ids": [1, 2, 3, 4, 5],
  "exam_product_id": 1,
  "venue_id": 1,
  "start_time": "2025-08-29T08:30:00Z",
  "duration_minutes": 120
}
```

**响应示例**:
```json
{
  "message": "成功创建 5 个日程",
  "schedules": [
    {
      "id": 1,
      "registration_id": 1,
      "venue_id": 1,
      "start_time": "2025-08-29T08:30:00Z",
      "end_time": "2025-08-29T10:30:00Z"
    }
  ]
}
```

### 9.5 更新日程
**接口**: `PUT /schedules/{schedule_id}`  
**描述**: 更新指定日程的信息  
**认证**: 需要Bearer Token (管理员角色)  

### 9.6 删除日程
**接口**: `DELETE /schedules/{schedule_id}`  
**描述**: 删除指定的日程  
**认证**: 需要Bearer Token (管理员角色)  

### 9.7 开始日程
**接口**: `POST /schedules/{schedule_id}/start`  
**描述**: 开始执行日程  
**认证**: 需要Bearer Token  

**响应示例**:
```json
{
  "message": "日程已开始",
  "schedule": {
    "id": 1,
    "status": "in_progress",
    "updated_at": "2025-08-28T11:00:00Z"
  }
}
```

### 9.8 完成日程
**接口**: `POST /schedules/{schedule_id}/complete`  
**描述**: 完成日程  
**认证**: 需要Bearer Token  

**响应示例**:
```json
{
  "message": "日程已完成",
  "schedule": {
    "id": 1,
    "status": "completed",
    "updated_at": "2025-08-28T11:00:00Z"
  }
}
```

### 9.9 获取日程统计
**接口**: `GET /schedules/statistics/overview`  
**描述**: 获取日程统计信息  
**认证**: 需要Bearer Token  

**查询参数**:
- `date` (string, optional): 日期筛选，格式YYYY-MM-DD

**响应示例**:
```json
{
  "total_schedules": 150,
  "scheduled": 80,
  "in_progress": 20,
  "completed": 45,
  "cancelled": 5,
  "by_venue": [
    {
      "venue_id": 1,
      "venue_name": "北京考场A",
      "schedule_count": 60
    }
  ],
  "by_exam_product": [
    {
      "exam_product_id": 1,
      "exam_product_name": "多旋翼视距内驾驶员理论",
      "schedule_count": 90
    }
  ]
}
```

### 9.10 获取考场今日日程
**接口**: `GET /schedules/venue/{venue_id}/today`  
**描述**: 获取指定考场今日的日程安排  
**认证**: 需要Bearer Token  

**路径参数**:
- `venue_id` (int, required): 考场ID

---

## 10. 接口总结

### 10.1 路由模块概览
根据 `backend/app/routes/__init__.py` 文件，系统包含以下9个主要路由模块：

1. **健康检查模块** (`health.py`) - 系统状态监控
2. **认证模块** (`auth.py`) - 用户登录、注册、权限管理
3. **系统管理模块** (`system.py`) - 系统配置、权限检查
4. **微信模块** (`wechat.py`) - 微信小程序相关功能
5. **考生管理模块** (`candidates.py`) - 考生信息管理
6. **考场管理模块** (`venues.py`) - 考场信息管理
7. **考试产品管理模块** (`exam_products.py`) - 考试产品配置
8. **机构管理模块** (`institutions.py`) - 培训机构管理
9. **日程管理模块** (`schedules.py`) - 考试日程安排

### 10.2 接口统计
- **总接口数量**: 约66个API接口
- **认证要求**: 除健康检查外，所有接口都需要Bearer Token认证
- **权限控制**: 
  - 管理员权限：创建、更新、删除操作
  - 操作员权限：查看本机构数据
  - 考生权限：查看个人信息和考试相关数据

### 10.3 核心业务流程
1. **考生注册流程**: 身份证验证 → 创建账户 → 生成报名记录
2. **考试安排流程**: 创建考试产品 → 分配考场 → 安排日程 → 考生签到
3. **签到流程**: 生成二维码 → 扫码签到 → 验证时间窗口 → 记录签到状态

### 10.4 数据模型关系
- **用户(User)** ↔ **机构(Institution)**: 多对一关系
- **用户(User)** ↔ **报名记录(ExamRegistration)**: 一对多关系
- **报名记录(ExamRegistration)** ↔ **日程(Schedule)**: 一对一关系
- **日程(Schedule)** ↔ **考场(Venue)**: 多对一关系
- **日程(Schedule)** ↔ **签到记录(CheckIn)**: 一对多关系

### 10.5 安全特性
- JWT Token认证机制
- 基于角色的访问控制(RBAC)
- 二维码30分钟过期机制
- 考试时间窗口验证
- 机构数据隔离

### 10.6 技术栈
- **后端框架**: FastAPI
- **数据库**: MySQL + SQLAlchemy ORM
- **认证**: JWT (JSON Web Tokens)
- **API文档**: 自动生成的OpenAPI/Swagger文档
- **部署**: Docker容器化部署

---

**文档版本**: v1.0  
**最后更新**: 2025-08-28  
**维护者**: UAV考试系统开发团队

*注：本文档涵盖了UAV考试管理系统的所有后端API接口。如有疑问或需要更新，请联系开发团队。*
