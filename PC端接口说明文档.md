# PC端接口说明文档

## 概述

本文档详细说明了UAV考点运营管理系统PC端的所有接口，按照开发优先级和功能模块进行划分，包括请求方法、路径、参数格式和响应格式。

**基础信息：**
- 基础URL: `http://localhost:8000`
- 认证方式: JWT Bearer Token
- 内容类型: `application/json`

---

## 第一批：认证模块（最高优先级）

> **开发原因：** 这是所有功能的基础，必须先确保认证系统正常工作

### 1.1 PC端管理员登录

**接口地址：** `POST /api/v1/pc/auth/login`

**功能说明：** 管理员登录系统，获取访问令牌

**请求格式：**
```json
{
  "username": "beijing_admin",
  "password": "123456"
}
```

**返回格式：**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user_info": {
    "id": 2,
    "username": "beijing_admin",
    "real_name": "北京管理员",
    "role": "admin",
    "institution_id": 1
  }
}
```

### 1.2 PC端管理员登出

**接口地址：** `POST /api/v1/pc/auth/logout`

**功能说明：** 管理员登出系统，使Token失效

**请求头：**
```
Authorization: Bearer <token>
```

**返回格式：**
```json
{
  "message": "登出成功"
}
```

### 1.3 获取当前用户信息

**接口地址：** `GET /api/v1/pc/auth/profile`

**功能说明：** 获取当前登录用户的详细信息

**请求头：**
```
Authorization: Bearer <token>
```

**返回格式：**
```json
{
  "id": 2,
  "username": "beijing_admin",
  "email": "admin@beijing.com",
  "real_name": "北京管理员",
  "role": "admin",
  "institution_id": 1,
  "is_active": true,
  "created_at": "2025-08-31T10:00:00"
}
```

### 1.4 更新用户资料

**接口地址：** `PUT /api/v1/pc/auth/profile`

**功能说明：** 更新当前用户的个人资料信息

**请求头：**
```
Authorization: Bearer <token>
```

**请求格式：**
```json
{
  "real_name": "更新后的姓名",
  "email": "newemail@example.com",
  "phone": "13800138000"
}
```

**返回格式：**
```json
{
  "success": true,
  "message": "用户资料更新成功",
  "data": {
    "id": 2,
    "real_name": "更新后的姓名",
    "email": "newemail@example.com",
    "updated_at": "2025-08-31T10:30:00"
  }
}
```

### 1.5 Token管理和权限验证

**权限角色层级：**
1. `SUPER_ADMIN`: 超级管理员 - 所有权限
2. `ADMIN`: 管理员 - 机构内所有权限
3. `OPERATOR`: 操作员 - 基础操作权限
4. `EXAMINER`: 考官 - 考试相关权限
5. `CANDIDATE`: 考生 - 仅查看自己的信息

**Token使用规范：**
- 所有接口都需要在请求头中携带有效的JWT Token
- Token格式：`Authorization: Bearer <access_token>`
- Token有效期：3600秒（1小时）
- Token过期后需要重新登录获取新Token

**权限控制规则：**
- 超级管理员可以访问所有机构的数据
- 普通管理员只能访问自己机构的数据
- 操作员和考官有限制的操作权限

---

## 第二批：仪表板模块

> **开发原因：** 用户登录后首先看到的就是仪表板，需要有数据展示

### 2.1 获取系统概览数据

**接口地址：** `GET /api/v1/pc/dashboard/overview`

**功能说明：** 获取系统整体运营数据概览

**请求头：**
```
Authorization: Bearer <token>
```

**返回格式：**
```json
{
  "total_candidates": 1250,
  "total_venues": 15,
  "total_exams": 89,
  "active_schedules": 23,
  "today_checkins": 156,
  "pending_registrations": 45,
  "system_status": "正常",
  "last_updated": "2025-08-31T10:00:00"
}
```

### 2.2 获取统计数据

**接口地址：** `GET /api/v1/pc/dashboard/statistics`

**功能说明：** 获取详细的统计分析数据

**请求头：**
```
Authorization: Bearer <token>
```

**查询参数：**
- `period`: 统计周期 (day/week/month)
- `start_date`: 开始日期 (YYYY-MM-DD)
- `end_date`: 结束日期 (YYYY-MM-DD)

**返回格式：**
```json
{
  "exam_statistics": {
    "total_exams": 89,
    "passed_exams": 67,
    "failed_exams": 22,
    "pass_rate": 75.3
  },
  "checkin_statistics": {
    "total_checkins": 156,
    "on_time": 134,
    "late": 18,
    "absent": 4
  },
  "venue_utilization": [
    {
      "venue_name": "多旋翼A号实操场",
      "utilization_rate": 85.5,
      "total_sessions": 12,
      "completed_sessions": 10
    }
  ]
}
```

### 2.3 获取最近活动日志

**接口地址：** `GET /api/v1/pc/dashboard/recent-activities`

**功能说明：** 获取系统最近的操作活动记录

**请求头：**
```
Authorization: Bearer <token>
```

**查询参数：**
- `limit`: 返回记录数 (默认20)

**返回格式：**
```json
{
  "activities": [
    {
      "id": 1,
      "type": "checkin",
      "description": "考生张三完成签到",
      "user": "张三",
      "venue": "多旋翼A号实操场",
      "timestamp": "2025-08-31T09:45:00",
      "status": "success"
    },
    {
      "id": 2,
      "type": "registration",
      "description": "新考生李四完成报名",
      "user": "李四",
      "exam_product": "多旋翼无人机驾驶员",
      "timestamp": "2025-08-31T09:30:00",
      "status": "pending"
    }
  ]
}
```

---

## 第三批：核心业务模块

### 3.1 考试管理接口

#### 3.1.1 获取考试产品列表

**接口地址：** `GET /api/v1/pc/exam-products/`

**功能说明：** 获取所有考试产品列表，支持搜索和筛选

**请求头：**
```
Authorization: Bearer <token>
```

**查询参数：**
- `skip`: 跳过记录数 (默认0)
- `limit`: 限制记录数 (默认100)
- `search`: 搜索关键词
- `is_active`: 状态筛选 (true/false)

**返回格式：**
```json
[
  {
    "id": 1,
    "name": "多旋翼无人机驾驶员",
    "code": "UAV_MULTI_001",
    "description": "多旋翼无人机驾驶员资格考试",
    "duration_minutes": 120,
    "exam_type": "PRACTICAL",
    "is_active": true,
    "created_at": "2025-08-31T10:00:00",
    "updated_at": "2025-08-31T10:00:00"
  }
]
```

#### 3.1.2 创建考试产品

**接口地址：** `POST /api/v1/pc/exam-products/`

**功能说明：** 创建新的考试产品

**权限要求：** SUPER_ADMIN 或 ADMIN

**请求头：**
```
Authorization: Bearer <token>
```

**请求格式：**
```json
{
  "name": "无人机驾驶员测试",
  "code": "UAV_TEST_001",
  "description": "无人机驾驶员资格考试",
  "duration_minutes": 120,
  "exam_type": "PRACTICAL",
  "is_active": true,
  "requirements": ["身份证", "体检证明"],
  "max_score": 100,
  "pass_score": 80,
  "price": 500.00
}
```

**返回格式：**
```json
{
  "success": true,
  "message": "考试产品创建成功",
  "data": {
    "id": 3,
    "name": "无人机驾驶员测试",
    "code": "UAV_TEST_001",
    "created_at": "2025-08-31T10:00:00"
  }
}
```

#### 3.1.3 获取考试产品详情

**接口地址：** `GET /api/v1/pc/exam-products/{product_id}/`

**功能说明：** 获取指定考试产品的详细信息

**请求头：**
```
Authorization: Bearer <token>
```

**返回格式：**
```json
{
  "id": 1,
  "name": "多旋翼无人机驾驶员",
  "code": "UAV_MULTI_001",
  "description": "多旋翼无人机驾驶员资格考试",
  "duration_minutes": 120,
  "exam_type": "PRACTICAL",
  "is_active": true,
  "requirements": ["身份证", "体检证明", "培训证书"],
  "max_score": 100,
  "pass_score": 80,
  "price": 500.00,
  "registration_count": 678,
  "pass_rate": 85.2,
  "created_at": "2025-08-31T10:00:00",
  "updated_at": "2025-08-31T10:00:00"
}
```

#### 3.1.4 更新考试产品

**接口地址：** `PUT /api/v1/pc/exam-products/{product_id}/`

**功能说明：** 更新考试产品信息

**请求头：**
```
Authorization: Bearer <token>
```

**请求格式：**
```json
{
  "name": "更新后的考试产品名称",
  "description": "更新后的描述",
  "duration_minutes": 150,
  "price": 600.00,
  "pass_score": 85,
  "is_active": true
}
```

**返回格式：**
```json
{
  "success": true,
  "message": "考试产品更新成功",
  "data": {
    "id": 1,
    "name": "更新后的考试产品名称",
    "price": 600.00,
    "updated_at": "2025-08-31T10:30:00"
  }
}
```

#### 3.1.5 考试产品搜索

**接口地址：** `GET /api/v1/pc/exam-products/?search=无人机`

**功能说明：** 根据关键词搜索考试产品

**请求头：**
```
Authorization: Bearer <token>
```

**返回格式：**
```json
[
  {
    "id": 1,
    "name": "多旋翼无人机驾驶员",
    "code": "UAV_MULTI_001",
    "description": "多旋翼无人机驾驶员资格考试",
    "duration_minutes": 120,
    "exam_type": "PRACTICAL",
    "is_active": true
  }
]
```

#### 3.1.6 获取考试产品统计

**接口地址：** `GET /api/v1/pc/exam-products/statistics/`

**功能说明：** 获取考试产品统计数据

**请求头：**
```
Authorization: Bearer <token>
```

**返回格式：**
```json
{
  "total_products": 15,
  "active_products": 12,
  "inactive_products": 3,
  "exam_type_breakdown": {
    "PRACTICAL": 8,
    "THEORY": 4,
    "MIXED": 3
  },
  "registration_stats": {
    "total_registrations": 2456,
    "average_per_product": 163.7,
    "most_popular": {
      "id": 1,
      "name": "多旋翼无人机驾驶员",
      "registrations": 678
    }
  },
  "pass_rate_stats": {
    "overall_pass_rate": 82.5,
    "highest_pass_rate": 95.2,
    "lowest_pass_rate": 68.9
  }
}
```

### 3.2 人员管理接口

#### 3.2.1 获取考生列表

**接口地址：** `GET /api/v1/pc/candidates/`

**功能说明：** 获取考生列表，支持分页、搜索和筛选

**请求头：**
```
Authorization: Bearer <token>
```

**查询参数：**
- `page`: 页码 (默认1)
- `size`: 每页数量 (默认20)
- `search`: 搜索关键词
- `status`: 状态筛选
- `exam_product_id`: 考试产品ID筛选

**返回格式：**
```json
{
  "items": [
    {
      "id": 1,
      "real_name": "张三",
      "id_card": "110101199001011234",
      "phone": "13800138001",
      "email": "zhangsan@example.com",
      "exam_product_name": "多旋翼无人机驾驶员",
      "registration_status": "approved",
      "registration_time": "2025-08-30T14:30:00",
      "institution_name": "北京无人机培训中心",
      "created_at": "2025-08-30T14:30:00"
    }
  ],
  "total": 1250,
  "page": 1,
  "size": 20,
  "pages": 63
}
```

#### 3.2.2 创建考生记录

**接口地址：** `POST /api/v1/pc/candidates/`

**功能说明：** 创建新的考生记录

**请求头：**
```
Authorization: Bearer <token>
```

**请求格式：**
```json
{
  "real_name": "测试考生",
  "id_card": "110101199001011234",
  "phone": "13800138001",
  "email": "test@example.com",
  "exam_product_id": 1,
  "institution_id": 1
}
```

**返回格式：**
```json
{
  "success": true,
  "message": "考生创建成功",
  "data": {
    "id": 1251,
    "real_name": "测试考生",
    "id_card": "110101199001011234",
    "registration_number": "REG20250831001251",
    "created_at": "2025-08-31T10:00:00"
  }
}
```

#### 3.2.3 获取考生详情

**接口地址：** `GET /api/v1/pc/candidates/{candidate_id}`

**功能说明：** 获取指定考生的详细信息

**请求头：**
```
Authorization: Bearer <token>
```

**返回格式：**
```json
{
  "id": 1,
  "real_name": "张三",
  "id_card": "110101199001011234",
  "phone": "13800138001",
  "email": "zhangsan@example.com",
  "exam_product": {
    "id": 1,
    "name": "多旋翼无人机驾驶员",
    "code": "UAV_MULTI_001"
  },
  "institution": {
    "id": 1,
    "name": "北京无人机培训中心"
  },
  "registration_status": "approved",
  "registration_time": "2025-08-30T14:30:00",
  "schedules": [
    {
      "id": 1,
      "schedule_date": "2025-09-01",
      "start_time": "09:00:00",
      "venue_name": "多旋翼A号实操场",
      "status": "scheduled"
    }
  ],
  "created_at": "2025-08-30T14:30:00"
}
```

#### 3.2.4 更新考生信息

**接口地址：** `PUT /api/v1/pc/candidates/{candidate_id}`

**功能说明：** 更新考生信息

**请求头：**
```
Authorization: Bearer <token>
```

**请求格式：**
```json
{
  "phone": "13800138002",
  "email": "newemail@example.com",
  "notes": "更新备注信息"
}
```

**返回格式：**
```json
{
  "success": true,
  "message": "考生信息更新成功",
  "data": {
    "id": 1,
    "phone": "13800138002",
    "email": "newemail@example.com",
    "updated_at": "2025-08-31T10:30:00"
  }
}
```

#### 3.2.5 获取考生统计数据

**接口地址：** `GET /api/v1/pc/candidates/statistics`

**功能说明：** 获取考生统计分析数据

**请求头：**
```
Authorization: Bearer <token>
```

**返回格式：**
```json
{
  "total_candidates": 1250,
  "status_breakdown": {
    "pending": 45,
    "confirmed": 234,
    "approved": 856,
    "rejected": 89,
    "completed": 26
  },
  "exam_product_breakdown": [
    {
      "exam_product_name": "多旋翼无人机驾驶员",
      "count": 678
    },
    {
      "exam_product_name": "固定翼无人机驾驶员",
      "count": 572
    }
  ],
  "monthly_registrations": [
    {
      "month": "2025-08",
      "count": 156
    },
    {
      "month": "2025-07",
      "count": 189
    }
  ]
}
```

### 3.3 考场管理接口

#### 3.3.1 获取考场列表

**接口地址：** `GET /api/v1/pc/venues/`

**功能说明：** 获取考场列表，支持分页和搜索

**请求头：**
```
Authorization: Bearer <token>
```

**查询参数：**
- `skip`: 跳过记录数 (默认0)
- `limit`: 限制记录数 (默认100)
- `institution_id`: 机构ID筛选
- `search`: 搜索关键词

**返回格式：**
```json
[
  {
    "id": 1,
    "name": "多旋翼A号实操场",
    "code": "VENUE001",
    "description": "多旋翼无人机实操考试场地",
    "capacity": 20,
    "current_count": 5,
    "building": "A栋",
    "floor": "1楼",
    "room_number": "101",
    "equipment": ["投影仪", "音响", "监控"],
    "facilities": ["空调", "WiFi", "停车场"],
    "status": "AVAILABLE",
    "is_active": true,
    "institution_id": 1,
    "qr_code": "https://example.com/qr/venue1",
    "created_at": "2025-08-31T10:00:00",
    "updated_at": "2025-08-31T10:00:00"
  }
]
```

#### 3.3.2 创建考场

**接口地址：** `POST /api/v1/pc/venues/`

**功能说明：** 创建新的考场

**权限要求：** SUPER_ADMIN 或 ADMIN

**请求头：**
```
Authorization: Bearer <token>
```

**请求格式：**
```json
{
  "name": "测试考场001",
  "code": "TEST001",
  "description": "测试用考场",
  "capacity": 50,
  "building": "B栋",
  "floor": "2楼",
  "room_number": "201",
  "equipment": ["投影仪", "音响"],
  "facilities": ["空调", "WiFi"],
  "institution_id": 1,
  "contact_person": "张三",
  "contact_phone": "13800138000",
  "notes": "测试考场备注"
}
```

**返回格式：**
```json
{
  "success": true,
  "message": "考场创建成功",
  "data": {
    "id": 16,
    "name": "测试考场001",
    "code": "TEST001",
    "created_at": "2025-08-31T10:00:00"
  }
}
```

#### 3.3.3 获取考场详情

**接口地址：** `GET /api/v1/pc/venues/{venue_id}/`

**功能说明：** 获取指定考场的详细信息

**请求头：**
```
Authorization: Bearer <token>
```

**返回格式：**
```json
{
  "id": 1,
  "name": "多旋翼A号实操场",
  "code": "VENUE001",
  "description": "多旋翼无人机实操考试场地",
  "capacity": 20,
  "current_count": 5,
  "building": "A栋",
  "floor": "1楼",
  "room_number": "101",
  "equipment": ["投影仪", "音响", "监控"],
  "facilities": ["空调", "WiFi", "停车场"],
  "status": "AVAILABLE",
  "is_active": true,
  "institution_id": 1,
  "qr_code": "https://example.com/qr/venue1",
  "schedules": [
    {
      "id": 1,
      "schedule_date": "2025-08-31",
      "start_time": "09:00:00",
      "end_time": "11:00:00",
      "status": "scheduled"
    }
  ],
  "created_at": "2025-08-31T10:00:00",
  "updated_at": "2025-08-31T10:00:00"
}
```

#### 3.3.4 更新考场信息

**接口地址：** `PUT /api/v1/pc/venues/{venue_id}/`

**功能说明：** 更新考场信息

**请求头：**
```
Authorization: Bearer <token>
```

**请求格式：**
```json
{
  "name": "更新后的考场名称",
  "capacity": 25,
  "description": "更新后的描述",
  "equipment": ["投影仪", "音响", "监控", "录像设备"],
  "notes": "更新备注"
}
```

**返回格式：**
```json
{
  "success": true,
  "message": "考场更新成功",
  "data": {
    "id": 1,
    "name": "更新后的考场名称",
    "capacity": 25,
    "updated_at": "2025-08-31T10:30:00"
  }
}
```

#### 3.3.5 获取考场统计信息

**接口地址：** `GET /api/v1/pc/venues/statistics/`

**功能说明：** 获取考场统计数据

**请求头：**
```
Authorization: Bearer <token>
```

**返回格式：**
```json
{
  "total_venues": 15,
  "active_venues": 12,
  "inactive_venues": 3,
  "venue_types": {
    "practical": 8,
    "theory": 7
  },
  "utilization_stats": {
    "average_utilization": 78.5,
    "highest_utilization": 95.2,
    "lowest_utilization": 45.8
  }
}
```

---

## 第四批：辅助功能模块

### 4.1 考勤管理接口

#### 4.1.1 获取签到记录列表

**接口地址：** `GET /api/v1/pc/checkins/`

**功能说明：** 获取签到记录列表，支持分页和筛选

**请求头：**
```
Authorization: Bearer <token>
```

**查询参数：**
- `page`: 页码 (默认1)
- `size`: 每页数量 (默认20)
- `date_filter`: 日期筛选 (YYYY-MM-DD)
- `status_filter`: 状态筛选 (SUCCESS/LATE/FAILED)
- `venue_id`: 考场ID筛选

**返回格式：**
```json
{
  "items": [
    {
      "id": 1,
      "candidate_name": "张三",
      "candidate_id_card": "110101199001011234",
      "exam_type": "多旋翼无人机驾驶员",
      "venue_name": "多旋翼A号实操场",
      "scheduled_time": "2025-08-31T09:00:00",
      "checkin_time": "2025-08-31T08:55:00",
      "status": "SUCCESS",
      "checkin_method": "QR_CODE",
      "operator_info": "系统自动",
      "created_at": "2025-08-31T08:55:00"
    }
  ],
  "total": 156,
  "page": 1,
  "size": 20,
  "pages": 8
}
```

#### 4.1.2 手动签到查询

**接口地址：** `GET /api/v1/pc/checkins/manual-query/`

**功能说明：** 根据姓名和身份证查询考生信息，用于手动签到

**请求头：**
```
Authorization: Bearer <token>
```

**查询参数：**
- `real_name`: 考生真实姓名 (必填)
- `id_card`: 身份证号码 (必填)

**返回格式：**
```json
{
  "success": true,
  "candidate": {
    "id": 5,
    "real_name": "张三",
    "id_card": "110101199001011234",
    "phone": "13800138001"
  },
  "institution": {
    "id": 1,
    "name": "北京无人机培训中心"
  },
  "available_schedules": [
    {
      "id": 1,
      "schedule_date": "2025-08-31",
      "start_time": "09:00:00",
      "end_time": "11:00:00",
      "venue": {
        "id": 1,
        "name": "多旋翼A号实操场"
      },
      "exam_product": {
        "id": 1,
        "name": "多旋翼无人机驾驶员"
      },
      "can_checkin": true,
      "checkin_status": null
    }
  ]
}
```

#### 4.1.3 创建签到记录

**接口地址：** `POST /api/v1/pc/checkins/`

**功能说明：** 手动创建签到记录

**请求头：**
```
Authorization: Bearer <token>
```

**请求格式：**
```json
{
  "user_id": 5,
  "schedule_id": 1,
  "checkin_type": "MANUAL",
  "notes": "手动签到备注"
}
```

**返回格式：**
```json
{
  "success": true,
  "message": "签到记录创建成功",
  "data": {
    "id": 157,
    "user_id": 5,
    "schedule_id": 1,
    "checkin_type": "MANUAL",
    "notes": "手动签到备注",
    "created_at": "2025-08-31T10:00:00"
  }
}
```

#### 4.1.4 获取签到详情

**接口地址：** `GET /api/v1/pc/checkins/{checkin_id}/`

**功能说明：** 获取指定签到记录的详细信息

**请求头：**
```
Authorization: Bearer <token>
```

**返回格式：**
```json
{
  "id": 1,
  "candidate_name": "张三",
  "candidate_id_card": "110101199001011234",
  "exam_type": "多旋翼无人机驾驶员",
  "venue_name": "多旋翼A号实操场",
  "checkin_time": "2025-08-31T08:55:00",
  "status": "SUCCESS",
  "checkin_method": "QR_CODE",
  "location_info": {
    "latitude": 39.9042,
    "longitude": 116.4074,
    "address": "北京市朝阳区"
  },
  "device_info": "iPhone 13 Pro",
  "created_at": "2025-08-31T08:55:00"
}
```

#### 4.1.5 确认手动签到

**接口地址：** `POST /api/v1/pc/checkins/manual-confirm/`

**功能说明：** 确认手动签到操作

**请求头：**
```
Authorization: Bearer <token>
```

**请求格式：**
```json
{
  "candidate_id": 5,
  "schedule_id": 1
}
```

**返回格式：**
```json
{
  "success": true,
  "message": "手动签到确认成功",
  "data": {
    "checkin_id": 157,
    "candidate_name": "张三",
    "venue_name": "多旋翼A号实操场",
    "checkin_time": "2025-08-31T10:00:00",
    "operator": "北京管理员(admin)"
  }
}
```

#### 4.1.6 获取签到统计

**接口地址：** `GET /api/v1/pc/checkins/statistics`

**功能说明：** 获取签到统计数据

**请求头：**
```
Authorization: Bearer <token>
```

**查询参数：**
- `date_filter`: 日期筛选 (YYYY-MM-DD)

**返回格式：**
```json
{
  "total": 156,
  "success": 134,
  "late": 18,
  "failed": 4,
  "manual": 23,
  "qrcode": 133
}
```

### 4.2 系统设置接口

#### 4.2.1 获取机构列表

**接口地址：** `GET /api/v1/pc/institutions/`

**功能说明：** 获取机构列表，支持搜索和筛选

**权限要求：** SUPER_ADMIN 或 ADMIN

**请求头：**
```
Authorization: Bearer <token>
```

**查询参数：**
- `skip`: 跳过记录数 (默认0)
- `limit`: 限制记录数 (默认100)
- `search`: 搜索关键词
- `type`: 机构类型筛选
- `is_active`: 状态筛选

**返回格式：**
```json
[
  {
    "id": 1,
    "name": "北京无人机培训中心",
    "code": "BJ_UAV_001",
    "type": "TRAINING",
    "contact_person": "张主任",
    "contact_phone": "010-12345678",
    "contact_email": "contact@bjuav.com",
    "province": "北京市",
    "city": "北京市",
    "district": "朝阳区",
    "address": "朝阳区某某街道123号",
    "license_number": "BJ2023001",
    "is_active": true,
    "is_approved": true,
    "venue_count": 5,
    "candidate_count": 678,
    "created_at": "2025-08-31T10:00:00"
  }
]
```

#### 4.2.2 创建机构

**接口地址：** `POST /api/v1/pc/institutions/`

**功能说明：** 创建新机构

**权限要求：** 仅SUPER_ADMIN

**请求头：**
```
Authorization: Bearer <token>
```

**请求格式：**
```json
{
  "name": "上海无人机培训中心",
  "code": "SH_UAV_001",
  "type": "TRAINING",
  "contact_person": "李主任",
  "contact_phone": "021-12345678",
  "contact_email": "contact@shuav.com",
  "province": "上海市",
  "city": "上海市",
  "district": "浦东新区",
  "address": "浦东新区某某路456号",
  "license_number": "SH2023001",
  "business_license": "营业执照文件路径"
}
```

**返回格式：**
```json
{
  "success": true,
  "message": "机构创建成功",
  "data": {
    "id": 2,
    "name": "上海无人机培训中心",
    "code": "SH_UAV_001",
    "created_at": "2025-08-31T10:00:00"
  }
}
```

#### 4.2.3 获取机构详情

**接口地址：** `GET /api/v1/pc/institutions/{institution_id}/`

**功能说明：** 获取指定机构的详细信息

**请求头：**
```
Authorization: Bearer <token>
```

**返回格式：**
```json
{
  "id": 1,
  "name": "北京无人机培训中心",
  "code": "BJ_UAV_001",
  "type": "TRAINING",
  "contact_person": "张主任",
  "contact_phone": "010-12345678",
  "contact_email": "contact@bjuav.com",
  "province": "北京市",
  "city": "北京市",
  "district": "朝阳区",
  "address": "朝阳区某某街道123号",
  "license_number": "BJ2023001",
  "business_license": "营业执照文件路径",
  "is_active": true,
  "is_approved": true,
  "config": {
    "max_venues": 10,
    "max_candidates": 1000
  },
  "venues": [
    {
      "id": 1,
      "name": "多旋翼A号实操场",
      "status": "AVAILABLE"
    }
  ],
  "statistics": {
    "total_venues": 5,
    "total_candidates": 678,
    "total_exams": 234,
    "pass_rate": 85.2
  },
  "created_at": "2025-08-31T10:00:00",
  "updated_at": "2025-08-31T10:00:00"
}
```

#### 4.2.4 更新机构信息

**接口地址：** `PUT /api/v1/pc/institutions/{institution_id}/`

**功能说明：** 更新机构信息

**请求头：**
```
Authorization: Bearer <token>
```

**请求格式：**
```json
{
  "contact_person": "新联系人",
  "contact_phone": "010-87654321",
  "contact_email": "newcontact@bjuav.com",
  "address": "朝阳区新地址789号",
  "config": {
    "max_venues": 15,
    "max_candidates": 1500
  }
}
```

**返回格式：**
```json
{
  "success": true,
  "message": "机构信息更新成功",
  "data": {
    "id": 1,
    "contact_person": "新联系人",
    "contact_phone": "010-87654321",
    "updated_at": "2025-08-31T10:30:00"
  }
}
```

#### 4.2.5 获取机构统计信息

**接口地址：** `GET /api/v1/pc/institutions/statistics/`

**功能说明：** 获取机构统计数据

**请求头：**
```
Authorization: Bearer <token>
```

**返回格式：**
```json
{
  "total_institutions": 25,
  "active_institutions": 22,
  "pending_approval": 3,
  "type_breakdown": {
    "TRAINING": 18,
    "TESTING": 7
  },
  "regional_distribution": [
    {
      "province": "北京市",
      "count": 5
    },
    {
      "province": "上海市",
      "count": 4
    },
    {
      "province": "广东省",
      "count": 8
    }
  ],
  "performance_stats": {
    "average_venues_per_institution": 6.2,
    "average_candidates_per_institution": 456.8,
    "top_performing": {
      "id": 1,
      "name": "北京无人机培训中心",
      "candidate_count": 678
    }
  }
}
```

---

## 通用响应格式

### 成功响应
```json
{
  "success": true,
  "message": "操作成功",
  "data": {
    // 具体数据
  }
}
```

### 错误响应
```json
{
  "detail": "错误描述信息"
}
```

### 分页响应
```json
{
  "items": [
    // 数据列表
  ],
  "total": 总记录数,
  "page": 当前页码,
  "size": 每页数量,
  "pages": 总页数
}
```

---

## 状态码说明

- `200 OK`: 请求成功
- `201 Created`: 创建成功
- `400 Bad Request`: 请求参数错误
- `401 Unauthorized`: 未授权，需要登录
- `403 Forbidden`: 权限不足
- `404 Not Found`: 资源不存在
- `422 Unprocessable Entity`: 参数验证失败
- `500 Internal Server Error`: 服务器内部错误

---

## 开发优先级说明

### 第一批：认证模块（最高优先级）
**开发原因：** 这是所有功能的基础，必须先确保认证系统正常工作
- 登录/登出接口
- 用户信息获取
- 密码修改
- Token管理和权限验证

### 第二批：仪表板模块
**开发原因：** 用户登录后首先看到的就是仪表板，需要有数据展示
- 统计数据接口
- 最近考试列表
- 系统活动日志

### 第三批：核心业务模块
**开发原因：** 系统的主要业务功能，是用户的核心需求
- 考试管理接口
- 人员管理接口
- 考场管理接口

### 第四批：辅助功能模块
**开发原因：** 提升用户体验的辅助功能
- 考勤管理接口
- 系统设置接口

---

## 使用示例

### JavaScript/Axios示例
```javascript
// 登录
const loginResponse = await axios.post('/api/v1/pc/auth/login', {
  username: 'beijing_admin',
  password: '123456'
});

const token = loginResponse.data.access_token;

// 设置认证头
axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

// 获取考生列表
const candidatesResponse = await axios.get('/api/v1/pc/candidates/', {
  params: {
    page: 1,
    size: 20,
    search: '张三'
  }
});

console.log(candidatesResponse.data);
```

### Python/Requests示例
```python
import requests

# 登录
login_response = requests.post('http://localhost:8000/api/v1/pc/auth/login', 
    json={
        'username': 'beijing_admin',
        'password': '123456'
    }
)

token = login_response.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

# 获取考场列表
venues_response = requests.get('http://localhost:8000/api/v1/pc/venues/', 
    headers=headers,
    params={
        'limit': 50,
        'search': '实操'
    }
)

print(venues_response.json())
```

---

*文档版本: v1.0*  
*最后更新: 2025-08-31*