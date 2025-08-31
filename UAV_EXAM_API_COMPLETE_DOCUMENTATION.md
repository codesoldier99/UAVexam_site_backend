# UAV考试系统 - 完整API接口文档

## 项目概述
UAV考试系统是一个基于FastAPI的无人机考试管理平台，支持考生管理、考场调度、考试产品管理等功能。

## 技术栈
- **后端框架**: FastAPI
- **数据库**: MySQL + SQLAlchemy ORM
- **认证**: JWT Token
- **API文档**: Swagger/OpenAPI

## 接口总览
系统共包含 **61个API接口**，分为9个功能模块：

---

## 1. 健康检查模块 (1个接口)

### 1.1 健康检查
- **接口**: `GET /health`
- **描述**: 检查系统运行状态
- **权限**: 无需认证
- **请求参数**: 无
- **响应格式**:
```json
{
  "status": "healthy",
  "timestamp": "2025-08-28T11:00:00Z",
  "version": "1.0.0"
}
```

---

## 2. 认证授权模块 (4个接口)

### 2.1 用户登录
- **接口**: `POST /auth/login`
- **描述**: 用户登录获取访问令牌
- **权限**: 无需认证
- **请求格式**:
```json
{
  "username": "string",
  "password": "string"
}
```
- **响应格式**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "username": "admin",
    "role": "ADMIN",
    "institution_id": 1
  }
}
```

### 2.2 用户登出
- **接口**: `POST /auth/logout`
- **描述**: 用户登出，使令牌失效
- **权限**: 需要认证
- **请求参数**: 无
- **响应格式**:
```json
{
  "message": "登出成功"
}
```

### 2.3 刷新令牌
- **接口**: `POST /auth/refresh`
- **描述**: 使用刷新令牌获取新的访问令牌
- **权限**: 需要刷新令牌
- **请求格式**:
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```
- **响应格式**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### 2.4 获取当前用户信息
- **接口**: `GET /auth/me`
- **描述**: 获取当前登录用户的详细信息
- **权限**: 需要认证
- **请求参数**: 无
- **响应格式**:
```json
{
  "id": 1,
  "username": "admin",
  "real_name": "管理员",
  "role": "ADMIN",
  "institution_id": 1,
  "institution_name": "总部",
  "is_active": true,
  "created_at": "2025-01-01T00:00:00Z",
  "last_login": "2025-08-28T10:30:00Z"
}
```

---

## 3. 系统管理模块 (4个接口)

### 3.1 获取系统信息
- **接口**: `GET /system/info`
- **描述**: 获取系统基本信息和配置
- **权限**: 需要认证
- **请求参数**: 无
- **响应格式**:
```json
{
  "system_name": "UAV考试系统",
  "version": "1.0.0",
  "environment": "production",
  "database_status": "connected",
  "uptime": "72h 30m 15s"
}
```

### 3.2 获取权限列表
- **接口**: `GET /system/permissions`
- **描述**: 获取系统所有权限定义
- **权限**: 管理员
- **请求参数**: 无
- **响应格式**:
```json
{
  "user_management": {
    "user_create": true,
    "user_read": true,
    "user_update": true,
    "user_delete": true
  },
  "exam_management": {
    "exam_create": true,
    "exam_read": true,
    "exam_update": true,
    "exam_delete": true
  }
}
```

### 3.3 获取角色列表
- **接口**: `GET /system/roles`
- **描述**: 获取系统角色定义
- **权限**: 管理员
- **请求参数**: 无
- **响应格式**:
```json
[
  {
    "role": "SUPER_ADMIN",
    "name": "超级管理员",
    "description": "系统最高权限"
  },
  {
    "role": "ADMIN",
    "name": "管理员",
    "description": "机构管理权限"
  },
  {
    "role": "OPERATOR",
    "name": "操作员",
    "description": "基础操作权限"
  },
  {
    "role": "CANDIDATE",
    "name": "考生",
    "description": "考生权限"
  }
]
```

### 3.4 获取仪表板数据
- **接口**: `GET /system/dashboard`
- **描述**: 获取系统仪表板统计数据
- **权限**: 需要认证
- **请求参数**: 无
- **响应格式**:
```json
{
  "total_candidates": 1250,
  "total_venues": 15,
  "today_exams": 45,
  "completed_exams": 38,
  "pending_exams": 7,
  "system_status": "normal"
}
```

---

## 4. 微信小程序模块 (11个接口)

### 4.1 根据身份证获取考生信息
- **接口**: `GET /wechat/candidate/{id_card}`
- **描述**: 通过身份证号获取考生基本信息和考试安排
- **权限**: 无需认证
- **路径参数**: 
  - `id_card`: 身份证号码
- **响应格式**:
```json
{
  "id": 5,
  "real_name": "张三",
  "id_card": "110101199001011234",
  "phone": "13800138000",
  "current_exam": {
    "schedule_id": 123,
    "venue_id": 1,
    "venue_name": "考场A",
    "exam_date": "2025-08-28",
    "start_time": "08:30:00",
    "end_time": "10:30:00",
    "exam_product": {
      "id": 1,
      "name": "无人机驾驶员理论考试",
      "exam_type": "理论考试"
    }
  }
}
```

### 4.2 刷新考生二维码
- **接口**: `POST /wechat/candidate/refresh-qr`
- **描述**: 为考生生成新的签到二维码
- **权限**: 需要JWT认证
- **请求头**: `Authorization: Bearer <token>`
- **请求参数**: 无
- **响应格式**:
```json
{
  "qr_code_data": "{\"candidate_id\":5,\"schedule_id\":123,\"venue_id\":1,\"timestamp\":1724821200,\"expires_at\":1724823000}",
  "expires_at": "2025-08-28T09:00:00Z",
  "message": "二维码已刷新"
}
```

### 4.3 考生签到
- **接口**: `POST /wechat/checkin`
- **描述**: 处理考生扫码签到
- **权限**: 无需认证
- **请求格式**:
```json
{
  "qr_code_data": "{\"candidate_id\":5,\"schedule_id\":123,\"venue_id\":1,\"timestamp\":1724821200,\"expires_at\":1724823000}"
}
```
- **响应格式**:
```json
{
  "success": true,
  "message": "签到成功",
  "checkin_time": "2025-08-28T08:45:00Z",
  "candidate_name": "张三",
  "venue_name": "考场A",
  "exam_info": {
    "exam_name": "无人机驾驶员理论考试",
    "start_time": "08:30:00",
    "end_time": "10:30:00"
  }
}
```

### 4.4 获取考生签到历史
- **接口**: `GET /wechat/candidate/{candidate_id}/checkin-history`
- **描述**: 获取考生的签到记录
- **权限**: 需要认证
- **路径参数**:
  - `candidate_id`: 考生ID
- **查询参数**:
  - `limit`: 记录数量限制 (默认10)
- **响应格式**:
```json
[
  {
    "id": 1,
    "checkin_time": "2025-08-28T08:45:00Z",
    "venue_name": "考场A",
    "exam_name": "无人机驾驶员理论考试",
    "status": "已签到"
  }
]
```

### 4.5 获取考生考试结果
- **接口**: `GET /wechat/candidate/{candidate_id}/exam-results`
- **描述**: 获取考生的考试成绩和结果
- **权限**: 需要认证
- **路径参数**:
  - `candidate_id`: 考生ID
- **响应格式**:
```json
[
  {
    "exam_name": "无人机驾驶员理论考试",
    "exam_date": "2025-08-28",
    "score": 85,
    "result": "合格",
    "venue_name": "考场A"
  }
]
```

### 4.6 获取排队位置
- **接口**: `GET /wechat/queue-position/{candidate_id}`
- **描述**: 获取考生在考场的排队位置
- **权限**: 需要认证
- **路径参数**:
  - `candidate_id`: 考生ID
- **响应格式**:
```json
{
  "position": 3,
  "total_queue": 15,
  "estimated_wait_time": "15分钟",
  "venue_name": "考场A"
}
```

### 4.7 获取看板数据
- **接口**: `GET /wechat/dashboard-data`
- **描述**: 获取考试看板显示数据
- **权限**: 需要认证
- **请求参数**: 无
- **响应格式**:
```json
{
  "current_time": "2025-08-28T11:00:00Z",
  "total_candidates_today": 45,
  "checked_in": 38,
  "in_progress": 12,
  "completed": 26,
  "venues_status": [
    {
      "venue_name": "考场A",
      "status": "进行中",
      "current_candidates": 8
    }
  ]
}
```

### 4.8 获取考场当前考试信息
- **接口**: `GET /wechat/venue/{venue_id}/current-exam`
- **描述**: 获取指定考场当前进行的考试信息
- **权限**: 需要认证
- **路径参数**:
  - `venue_id`: 考场ID
- **响应格式**:
```json
{
  "venue_name": "考场A",
  "current_exam": {
    "exam_name": "无人机驾驶员理论考试",
    "start_time": "08:30:00",
    "end_time": "10:30:00",
    "candidates_count": 8,
    "status": "进行中"
  }
}
```

### 4.9 获取考场排队信息
- **接口**: `GET /wechat/venue/{venue_id}/queue`
- **描述**: 获取考场的排队情况
- **权限**: 需要认证
- **路径参数**:
  - `venue_id`: 考场ID
- **响应格式**:
```json
{
  "venue_name": "考场A",
  "queue_length": 15,
  "current_serving": 8,
  "estimated_wait_time": "20分钟"
}
```

### 4.10 获取考场统计信息
- **接口**: `GET /wechat/venue/{venue_id}/stats`
- **描述**: 获取考场的统计数据
- **权限**: 需要认证
- **路径参数**:
  - `venue_id`: 考场ID
- **响应格式**:
```json
{
  "venue_name": "考场A",
  "today_stats": {
    "total_scheduled": 45,
    "completed": 26,
    "in_progress": 12,
    "pending": 7
  },
  "utilization_rate": "85%"
}
```

### 4.11 获取考试日程详情
- **接口**: `GET /wechat/exam-schedule/{schedule_id}`
- **描述**: 获取指定日程的详细信息
- **权限**: 需要认证
- **路径参数**:
  - `schedule_id`: 日程ID
- **响应格式**:
```json
{
  "id": 123,
  "candidate_name": "张三",
  "exam_name": "无人机驾驶员理论考试",
  "venue_name": "考场A",
  "exam_date": "2025-08-28",
  "start_time": "08:30:00",
  "end_time": "10:30:00",
  "status": "已安排"
}
```

---

## 5. 考生管理模块 (6个接口)

### 5.1 获取考生列表
- **接口**: `GET /candidates/`
- **描述**: 分页获取考生列表
- **权限**: 需要认证
- **查询参数**:
  - `skip`: 跳过记录数 (默认0)
  - `limit`: 每页记录数 (默认20)
  - `search`: 搜索关键词
  - `institution_id`: 机构ID筛选
- **响应格式**:
```json
{
  "items": [
    {
      "id": 1,
      "username": "candidate_123456",
      "real_name": "张三",
      "id_card": "110101199001011234",
      "phone": "13800138000",
      "email": "zhangsan@example.com",
      "institution_name": "培训机构A",
      "exam_product_id": 1,
      "registrations": [
        {
          "id": 1,
          "exam_product_id": 1,
          "registration_number": "REG20250828001",
          "status": "APPROVED"
        }
      ]
    }
  ],
  "total": 1250,
  "skip": 0,
  "limit": 20
}
```

### 5.2 获取考生详情
- **接口**: `GET /candidates/{candidate_id}`
- **描述**: 获取指定考生的详细信息
- **权限**: 需要认证
- **路径参数**:
  - `candidate_id`: 考生ID
- **响应格式**:
```json
{
  "id": 1,
  "username": "candidate_123456",
  "real_name": "张三",
  "id_card": "110101199001011234",
  "phone": "13800138000",
  "email": "zhangsan@example.com",
  "institution_id": 1,
  "institution_name": "培训机构A",
  "exam_product_id": 1,
  "last_login": "2025-08-28T10:30:00Z",
  "registrations": [
    {
      "id": 1,
      "exam_product_id": 1,
      "registration_number": "REG20250828001",
      "status": "APPROVED",
      "created_at": "2025-08-20T00:00:00Z"
    }
  ]
}
```

### 5.3 创建考生
- **接口**: `POST /candidates/`
- **描述**: 创建新的考生账户
- **权限**: 管理员
- **请求格式**:
```json
{
  "real_name": "李四",
  "id_card": "110101199002021234",
  "phone": "13800138001",
  "email": "lisi@example.com",
  "institution_id": 1,
  "exam_product_id": 1
}
```
- **响应格式**:
```json
{
  "id": 2,
  "username": "candidate_021234",
  "real_name": "李四",
  "id_card": "110101199002021234",
  "phone": "13800138001",
  "email": "lisi@example.com",
  "institution_id": 1,
  "exam_product_id": 1,
  "registration_number": "REG20250828002",
  "message": "考生创建成功"
}
```

### 5.4 更新考生信息
- **接口**: `PUT /candidates/{candidate_id}`
- **描述**: 更新考生信息
- **权限**: 管理员
- **路径参数**:
  - `candidate_id`: 考生ID
- **请求格式**:
```json
{
  "real_name": "李四(更新)",
  "phone": "13800138002",
  "email": "lisi_new@example.com"
}
```
- **响应格式**:
```json
{
  "id": 2,
  "username": "candidate_021234",
  "real_name": "李四(更新)",
  "phone": "13800138002",
  "email": "lisi_new@example.com",
  "message": "考生信息更新成功"
}
```

### 5.5 删除考生
- **接口**: `DELETE /candidates/{candidate_id}`
- **描述**: 删除考生账户
- **权限**: 管理员
- **路径参数**:
  - `candidate_id`: 考生ID
- **响应格式**:
```json
{
  "message": "考生删除成功"
}
```

### 5.6 获取考生日程
- **接口**: `GET /candidates/{candidate_id}/schedules`
- **描述**: 获取考生的考试日程安排
- **权限**: 需要认证
- **路径参数**:
  - `candidate_id`: 考生ID
- **响应格式**:
```json
[
  {
    "id": 123,
    "exam_name": "无人机驾驶员理论考试",
    "venue_name": "考场A",
    "exam_date": "2025-08-28",
    "start_time": "08:30:00",
    "end_time": "10:30:00",
    "status": "已安排",
    "registration_number": "REG20250828001"
  }
]
```

---

## 6. 考场管理模块 (9个接口)

### 6.1 获取考场列表
- **接口**: `GET /venues/`
- **描述**: 分页获取考场列表
- **权限**: 需要认证
- **查询参数**:
  - `skip`: 跳过记录数 (默认0)
  - `limit`: 每页记录数 (默认100)
  - `institution_id`: 机构ID筛选
  - `status`: 状态筛选
  - `venue_type`: 考场类型筛选
- **响应格式**:
```json
[
  {
    "id": 1,
    "name": "考场A",
    "code": "VENUE_A_001",
    "venue_type": "理论考场",
    "capacity": 30,
    "status": "AVAILABLE",
    "institution_id": 1,
    "institution_name": "培训机构A",
    "address": "北京市朝阳区xxx路xxx号",
    "equipment": "投影仪、音响、监控设备",
    "created_at": "2025-01-01T00:00:00Z"
  }
]
```

### 6.2 获取考场详情
- **接口**: `GET /venues/{venue_id}`
- **描述**: 获取指定考场的详细信息
- **权限**: 需要认证
- **路径参数**:
  - `venue_id`: 考场ID
- **响应格式**:
```json
{
  "id": 1,
  "name": "考场A",
  "code": "VENUE_A_001",
  "venue_type": "理论考场",
  "capacity": 30,
  "status": "AVAILABLE",
  "institution_id": 1,
  "institution_name": "培训机构A",
  "address": "北京市朝阳区xxx路xxx号",
  "equipment": "投影仪、音响、监控设备",
  "contact_person": "王老师",
  "contact_phone": "13800138000",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-08-28T10:00:00Z"
}
```

### 6.3 创建考场
- **接口**: `POST /venues/`
- **描述**: 创建新的考场
- **权限**: 管理员
- **请求格式**:
```json
{
  "name": "考场B",
  "code": "VENUE_B_001",
  "venue_type": "实操考场",
  "capacity": 20,
  "institution_id": 1,
  "address": "北京市朝阳区yyy路yyy号",
  "equipment": "无人机设备、安全防护设施",
  "contact_person": "李老师",
  "contact_phone": "13800138001"
}
```
- **响应格式**:
```json
{
  "id": 2,
  "name": "考场B",
  "code": "VENUE_B_001",
  "venue_type": "实操考场",
  "capacity": 20,
  "status": "AVAILABLE",
  "institution_id": 1,
  "message": "考场创建成功"
}
```

### 6.4 更新考场信息
- **接口**: `PUT /venues/{venue_id}`
- **描述**: 更新考场信息
- **权限**: 管理员
- **路径参数**:
  - `venue_id`: 考场ID
- **请求格式**:
```json
{
  "name": "考场B(更新)",
  "capacity": 25,
  "contact_person": "李老师(更新)",
  "contact_phone": "13800138002"
}
```
- **响应格式**:
```json
{
  "id": 2,
  "name": "考场B(更新)",
  "capacity": 25,
  "contact_person": "李老师(更新)",
  "contact_phone": "13800138002",
  "message": "考场信息更新成功"
}
```

### 6.5 删除考场
- **接口**: `DELETE /venues/{venue_id}`
- **描述**: 删除考场
- **权限**: 管理员
- **路径参数**:
  - `venue_id`: 考场ID
- **响应格式**:
```json
{
  "message": "考场删除成功"
}
```

### 6.6 切换考场状态
- **接口**: `POST /venues/{venue_id}/toggle-status`
- **描述**: 切换考场的可用/维护状态
- **权限**: 管理员
- **路径参数**:
  - `venue_id`: 考场ID
- **响应格式**:
```json
{
  "message": "考场状态已切换为MAINTENANCE",
  "venue": {
    "id": 1,
    "name": "考场A",
    "status": "MAINTENANCE"
  }
}
```

### 6.7 获取考场日程
- **接口**: `GET /venues/{venue_id}/schedules`
- **描述**: 获取考场的日程安排
- **权限**: 需要认证
- **路径参数**:
  - `venue_id`: 考场ID
- **查询参数**:
  - `date`: 日期筛选 (YYYY-MM-DD格式)
- **响应格式**:
```json
[
  {
    "id": 123,
    "candidate_name": "张三",
    "exam_name": "无人机驾驶员理论考试",
    "start_time": "08:30:00",
    "end_time": "10:30:00",
    "status": "已安排",
    "registration_number": "REG20250828001"
  }
]
```

### 6.8 获取考场当前状态
- **接口**: `GET /venues/{venue_id}/current-status`
- **描述**: 获取考场当前状态信息
- **权限**: 需要认证
- **路径参数**:
  - `venue_id`: 考场ID
- **响应格式**:
```json
{
  "venue_name": "考场A",
  "status": "AVAILABLE",
  "current_capacity": 8,
  "max_capacity": 30,
  "utilization_rate": "26.7%",
  "current_exam": {
    "exam_name": "无人机驾驶员理论考试",
    "start_time": "08:30:00",
    "end_time": "10:30:00",
    "candidates_count": 8
  }
}
```

---

## 7. 考试产品管理模块 (6个接口)

### 7.1 获取考试产品列表
- **接口**: `GET /exam-products/`
- **描述**: 分页获取考试产品列表
- **权限**: 需要认证
- **查询参数**:
  - `skip`: 跳过记录数 (默认0)
  - `limit`: 每页记录数 (默认100)
  - `is_active`: 是否启用筛选
  - `exam_type`: 考试类型筛选
- **响应格式**:
```json
[
  {
    "id": 1,
    "name": "无人机驾驶员理论考试",
    "code": "UAV_THEORY_001",
    "exam_type": "理论考试",
    "duration_minutes": 120,
    "total_score": 100,
    "pass_score": 70,
    "is_active": true,
    "description": "无人机驾驶员理论知识考试",
    "created_at": "2025-01-01T00:00:00Z"
  }
]
```

### 7.2 获取考试产品详情
- **接口**: `GET /exam-products/{product_id}`
- **描述**: 获取指定考试产品的详细信息
- **权限**: 需要认证
- **路径参数**:
  - `product_id`: 考试产品ID
- **响应格式**:
```json
{
  "id": 1,
  "name": "无人机驾驶员理论考试",
  "code": "UAV_THEORY_001",
  "exam_type": "理论考试",
  "duration_minutes": 120,
  "total_score": 100,
  "pass_score": 70,
  "is_active": true,
  "description": "无人机驾驶员理论知识考试",
  "exam_content": "包含法规、技术、安全等内容",
  "requirements": "需要完成培训课程",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-08-28T10:00:00Z"
}
```

### 7.3 创建考试产品
- **接口**: `POST /exam-products/`
- **描述**: 创建新的考试产品
- **权限**: 管理员
- **请求格式**:
```json
{
  "name": "无人机驾驶员实操考试",
  "code": "UAV_PRACTICAL_001",
  "exam_type": "实操考试",
  "duration_minutes": 60,
  "total_score": 100,
  "pass_score": 80,
  "description": "无人机驾驶员实际操作考试",
  "exam_content": "包含起飞、悬停、降落等操作",
  "requirements": "需要通过理论考试"
}
```
- **响应格式**:
```json
{
  "id": 2,
  "name": "无人机驾驶员实操考试",
  "code": "UAV_PRACTICAL_001",
  "exam_type": "实操考试",
  "duration_minutes": 60,
  "is_active": true,
  "message": "考试产品创建成功"
}
```

### 7.4 更新考试产品
- **接口**: `PUT /exam-products/{product_id}`
- **描述**: 更新考试产品信息
- **权限**: 管理员
- **路径参数**:
  - `product_id`: 考试产品ID
- **请求格式**:
```json
{
  "name": "无人机驾驶员实操考试(更新)",
  "duration_minutes": 90,
  "pass_score": 85,
  "description": "更新后的考试描述"
}
```
- **响应格式**:
```json
{
  "id": 2,
  "name": "无人机驾驶员实操考试(更新)",
  "duration_minutes": 90,
  "pass_score": 85,
  "message": "考试产品更新成功"
}
```

### 7.5 删除考试产品
- **接口**: `DELETE /exam-products/{product_id}`
- **描述**: 删除考试产品
- **权限**: 管理员
- **路径参数**:
  - `product_id`: 考试产品ID
- **响应格式**:
```json
{
  "message": "考试产品删除成功"
}
```

### 7.6 切换考试产品状态
- **接口**: `POST /exam-products/{product_id}/toggle-status`
- **描述**: 切换考试产品的启用/禁用状态
- **权限**: 管理员
- **路径参数**:
  - `product_id`: 考试产品ID
- **响应格式**:
```json
{
  "message": "考试产品状态已切换为禁用",
  "product": {
    "id": 2,
    "name": "无人机驾驶员实操考试",
    "is_active": false
  }
}
```

---

## 8. 机构管理模块 (8个接口)

### 8.1 获取机构列表
- **接口**: `GET /institutions/`
- **描述**: 分页获取机构列表
- **权限**: 需要认证
- **查询参数**:
  - `skip`: 跳过记录数 (默认0)
  - `limit`: 每页记录数 (默认20)
  - `search`: 搜索关键词
  - `is_active`: 是否启用筛选
- **响应格式**:
```json
{
  "items": [
    {
      "id": 1,
      "name": "培训机构A",
      "code": "INST_A_001",
      "type": "培训机构",
      "contact_person": "张经理",
      "contact_phone": "13800138000",
      "contact_email": "contact@institution-a.com",
      "address": "北京市朝阳区xxx路xxx号",
      "is_active": true,
      "is_approved": true,
      "created_at": "2025-01-01T00:00:00Z"
    }
  ],
  "total": 50,
  "skip": 0,
  "limit": 20
}
```

### 8.2 获取机构详情
- **接口**: `GET /institutions/{institution_id}`
- **描述**: 获取指定机构的详细信息
- **权限**: 需要认证
- **路径参数**:
  - `institution_id`: 机构ID
- **响应格式**:
```json
{
  "id": 1,
  "name": "培训机构A",
  "code": "INST_A_001",
  "type": "培训机构",
  "contact_person": "张经理",
  "contact_phone": "13800138000",
  "contact_email": "contact@institution-a.com",
  "address": "北京市朝阳区xxx路xxx号",
  "is_active": true,
  "is_approved": true,
  "description": "专业的无人机培训机构",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-08-28T10:00:00Z"
}
```

### 8.3 创建机构
- **接口**: `POST /institutions/`
- **描述**: 创建新机构
- **权限**: 管理员
- **请求参数**:
  - `name`: 机构名称
  - `code`: 机构代码
  - `type`: 机构类型 (默认"培训机构")
  - `contact_person`: 联系人
  - `contact_phone`: 联系电话
  - `contact_email`: 联系邮箱
  - `address`: 地址
- **响应格式**:
```json
{
  "id": 2,
  "name": "培训机构B",
  "code": "INST_B_001",
  "type": "培训机构",
  "contact_person": "李经理",
  "is_active": true,
  "message": "机构创建成功"
}
```

### 8.4 更新机构信息
- **接口**: `PUT /institutions/{institution_id}`
- **描述**: 更新机构信息
- **权限**: 管理员
- **路径参数**:
  - `institution_id`: 机构ID
- **请求参数**:
  - `name`: 机构名称
  - `type`: 机构类型
  - `contact_person`: 联系人
  - `contact_phone`: 联系电话
  - `contact_email`: 联系邮箱
  - `address`: 地址
  - `is_active`: 是否启用
  - `is_approved`: 是否审批通过
- **响应格式**:
```json
{
  "id": 2,
  "name": "培训机构B(更新)",
  "contact_person": "李经理(更新)",
  "is_active": true,
  "message": "机构信息更新成功"
}
```

### 8.5 删除机构
- **接口**: `DELETE /institutions/{institution_id}`
- **描述**: 删除机构
- **权限**: 超级管理员
- **路径参数**:
  - `institution_id`: 机构ID
- **响应格式**:
```json
{
  "message": "机构删除成功"
}
```

### 8.6 获取机构考场列表
- **接口**: `GET /institutions/{institution_id}/venues`
- **描述**: 获取指定机构的考场列表
- **权限**: 需要认证
- **路径参数**:
  - `institution_id`: 机构ID
- **查询参数**:
  - `skip`: 跳过记录数 (默认0)
  - `limit`: 每页记录数 (默认20)
- **响应格式**:
```json
{
  "items": [
    {
      "id": 1,
      "name": "考场A",
      "code": "VENUE_A_001",
      "venue_type": "理论考场",
      "capacity": 30,
      "status": "AVAILABLE"
    }
  ],
  "skip": 0,
  "limit": 20
}
```

### 8.7 获取机构统计信息
- **接口**: `GET /institutions/{institution_id}/stats`
- **描述**: 获取机构的统计信息
- **权限**: 需要认证
- **路径参数**:
  - `institution_id`: 机构ID
- **响应格式**:
```json
{
  "institution_name": "培训机构A",
  "total_venues": 5,
  "total_candidates": 120,
  "total_exams_today": 15,
  "completed_exams": 12,
  "pending_exams": 3,
  "pass_rate": "85%"
}
```

---

## 9. 日程管理模块 (12个接口)

### 9.1 获取日程列表
- **接口**: `GET /schedules/`
- **描述**: 分页获取日程列表
- **权限**: 需要认证
- **查询参数**:
  - `skip`: 跳过记录数 (默认0)
  - `limit`: 每页记录数 (默认100)
  - `venue_id`: 考场ID筛选
  - `date`: 日期筛选 (YYYY-MM-DD格式)
  - `status`: 状态筛选
  - `institution_id`: 机构ID筛选
- **响应格式**:
```json
[
  {
    "id": 123,
    "registration_id": 1,
    "venue_id": 1,
    "venue_name": "考场A",
    "candidate_name": "张三",
    "exam_name": "无人机驾驶员理论考试",
    "start_time": "2025-08-28T08:30:00Z",
    "end_time": "2025-08-28T10:30:00Z",
    "status": "SCHEDULED",
    "registration_number": "REG20250828001"
  }
]
```

### 9.2 获取日程详情
- **接口**: `GET /schedules/{schedule_id}`
- **描述**: 获取指定日程的详细信息
- **权限**: 需要认证
- **路径参数**:
  - `schedule_id`: 日程ID
- **响应格式**:
```json
{
  "id": 123,
  "registration_id": 1,
  "venue_id": 1,
  "venue_name": "考场A",
  "venue_address": "北京市朝阳区xxx路xxx号",
  "candidate_name": "张三",
  "candidate_phone": "13800138000",
  "exam_name": "无人机驾驶员理论考试",
  "exam_type": "理论考试",
  "start_time": "2025-08-28T08:30:00Z",
  "end_time": "2025-08-28T10:30:00Z",
  "status": "SCHEDULED",
  "registration_number": "REG20250828001",
  "created_at": "2025-08-20T00:00:00Z"
}
```

### 9.3 创建日程
- **接口**: `POST /schedules/`
- **描述**: 创建新的考试日程
- **权限**: 管理员
- **请求格式**:
```json
{
  "registration_id": 1,
  "venue_id": 1,
  "start_time": "2025-08-29T08:30:00Z",
  "end_time": "2025-08-29T10:30:00Z"
}
```
- **响应格式**:
```json
{
  "id": 124,
  "registration_id": 1,
  "venue_id": 1,
  "start_time": "2025-08-29T08:30:00Z",
  "end_time": "2025-08-29T10:30:00Z",
  "status": "SCHEDULED",
  "message": "日程创建成功"
}
```

### 9.4 批量创建日程
- **接口**: `POST /schedules/batch`
- **描述**: 批量创建考试日程安排
- **权限**: 管理员
- **请求格式**:
```json
{
  "registration_ids": [1, 2, 3],
  "exam_product_id": 1,
  "venue_id": 1,
  "start_time": "2025-08-29T08:30:00Z",
  "duration_minutes": 120
}
```
- **响应格式**:
```json
{
  "message": "成功创建 3 个日程",
  "schedules": [
    {
      "id": 124,
      "registration_id": 1,
      "venue_id": 1,
      "start_time": "2025-08-29T08:30:00Z",
      "end_time": "2025-08-29T10:30:00Z"
    },
    {
      "id": 125,
      "registration_id": 2,
      "venue_id": 1,
      "start_time": "2025-08-29T10:30:00Z",
      "end_time": "2025-08-29T12:30:00Z"
    }
  ]
}
```

### 9.5 更新日程
- **接口**: `PUT /schedules/{schedule_id}`
- **描述**: 更新日程信息
- **权限**: 管理员
- **路径参数**:
  - `schedule_id`: 日程ID
- **请求格式**:
```json
{
  "venue_id": 2,
  "start_time": "2025-08-29T09:00:00Z",
  "end_time": "2025-08-29T11:00:00Z"
}
```
- **响应格式**:
```json
{
  "id": 124,
  "venue_id": 2,
  "start_time": "2025-08-29T09:00:00Z",
  "end_time": "2025-08-29T11:00:00Z",
  "message": "日程更新成功"
}
```

### 9.6 删除日程
- **接口**: `DELETE /schedules/{schedule_id}`
- **描述**: 删除日程
- **权限**: 管理员
- **路径参数**:
  - `schedule_id`: 日程ID
- **响应格式**:
```json
{
  "message": "日程删除成功"
}
```

### 9.7 开始日程
- **接口**: `POST /schedules/{schedule_id}/start`
- **描述**: 开始执行日程
- **权限**: 需要认证
- **路径参数**:
  - `schedule_id`: 日程ID
- **响应格式**:
```json
{
  "message": "日程已开始",
  "schedule": {
    "id": 124,
    "status": "IN_PROGRESS",
    "start_time": "2025-08-29T09:00:00Z"
  }
}
```

### 9.8 完成日程
- **接口**: `POST /schedules/{schedule_id}/complete`
- **描述**: 完成日程
- **权限**: 需要认证
- **路径参数**:
  - `schedule_id`: 日程ID
- **响应格式**:
```json
{
  "message": "日程已完成",
  "schedule": {
    "id": 124,
    "status": "COMPLETED",
    "end_time": "2025-08-29T11:00:00Z"
  }
}
```

### 9.9 获取日程统计
- **接口**: `GET /schedules/statistics/overview`
- **描述**: 获取日程统计信息
- **权限**: 需要认证
- **查询参数**:
  - `date`: 日期筛选 (YYYY-MM-DD格式)
- **响应格式**:
```json
{
  "date": "2025-08-28",
  "total_schedules": 45,
  "scheduled": 7,
  "in_progress": 12,
  "completed": 26,
  "cancelled": 0,
  "venues_utilization": [
    {
      "venue_name": "考场A",
      "utilization_rate": "85%",
      "total_capacity": 30,
      "used_capacity": 25
    }
  ]
}
```

### 9.10 获取考场今日日程
- **接口**: `GET /schedules/venue/{venue_id}/today`
- **描述**: 获取指定考场今日的日程安排
- **权限**: 需要认证
- **路径参数**:
  - `venue_id`: 考场ID
- **响应格式**:
```json
[
  {
    "id": 123,
    "candidate_name": "张三",
    "exam_name": "无人机驾驶员理论考试",
    "start_time": "08:30:00",
    "end_time": "10:30:00",
    "status": "COMPLETED",
    "registration_number": "REG20250828001"
  },
  {
    "id": 124,
    "candidate_name": "李四",
    "exam_name": "无人机驾驶员理论考试",
    "start_time": "10:30:00",
    "end_time": "12:30:00",
    "status": "IN_PROGRESS",
    "registration_number": "REG20250828002"
  }
]
```

---

## 错误响应格式

所有接口在发生错误时都会返回统一的错误格式：

```json
{
  "detail": "错误描述信息"
}
```

常见HTTP状态码：
- `200`: 请求成功
- `201`: 创建成功
- `400`: 请求参数错误
- `401`: 未认证
- `403`: 权限不足
- `404`: 资源不存在
- `422`: 数据验证失败
- `500`: 服务器内部错误

---

## 认证说明

### JWT Token认证
大部分接口需要在请求头中携带JWT Token：

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### 权限级别
- **无需认证**: 健康检查、部分微信接口
- **需要认证**: 基础查询接口
- **管理员**: 创建、更新、删除操作
- **超级管理员**: 删除机构等高级操作

---

## 数据模型说明

### 用户角色 (UserRole)
- `SUPER_ADMIN`: 超级管理员
- `ADMIN`: 管理员  
- `OPERATOR`: 操作员
- `CANDIDATE`: 考生

### 考场状态 (VenueStatus)
- `AVAILABLE`: 可用
- `MAINTENANCE`: 维护中
- `OCCUPIED`: 占用中

### 日程状态 (ScheduleStatus)
- `SCHEDULED`: 已安排
- `IN_PROGRESS`: 进行中
- `COMPLETED`: 已完成
- `CANCELLED`: 已取消

### 报名状态 (RegistrationStatus)
- `PENDING`: 待审核
- `APPROVED`: 已通过
- `REJECTED`: 已拒绝

---

## 更新日志

- **v1.0.0** (2025-08-28): 初始版本，包含61个API接口
- 支持考生管理、考场调度、考试产品管理等核心功能
- 集成微信小程序接口，支持扫码签到
- 完整的权限控制和JWT认证机制

---

*文档最后更新时间: 2025-08-28 11:00:00*