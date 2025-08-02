# 考试系统后端API接口文档

## 概述

考试系统后端API提供完整的考试管理功能，包括用户认证、考生管理、考试产品管理、场地管理、排期管理等核心功能。

### 基础信息

- **基础URL**: `http://localhost:8000`
- **API版本**: v1.0.0
- **认证方式**: Bearer Token (JWT)
- **内容类型**: application/json

### 认证

所有需要认证的API都需要在请求头中包含Bearer Token：

```
Authorization: Bearer <your_jwt_token>
```

## 1. 认证相关API

### 1.1 用户登录

**POST** `/login`

**请求参数:**
```json
{
  "username": "string",
  "password": "string"
}
```

**响应示例:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "status": "active",
    "role_id": 1,
    "institution_id": null,
    "last_login": "2024-01-01T10:00:00Z",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

### 1.2 获取当前用户信息

**GET** `/me`

**响应示例:**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "status": "active",
  "role_id": 1,
  "institution_id": null,
  "last_login": "2024-01-01T10:00:00Z",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### 1.3 简化注册

**POST** `/simple-register`

**请求参数:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

### 1.4 简化登录

**POST** `/simple-auth/login`

**请求参数:**
```json
{
  "username": "string",
  "password": "string"
}
```

## 2. 健康检查

### 2.1 健康检查

**GET** `/health`

**响应示例:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T10:00:00Z",
  "version": "1.0.0"
}
```

### 2.2 根路径

**GET** `/`

**响应示例:**
```json
{
  "message": "考试系统后端API",
  "version": "1.0.0"
}
```

## 3. 考生管理API

### 3.1 创建考生

**POST** `/candidates/`

**请求参数:**
```json
{
  "name": "张三",
  "id_number": "110101199001011234",
  "phone": "13800138000",
  "email": "zhangsan@example.com",
  "gender": "male",
  "birth_date": "1990-01-01",
  "address": "北京市朝阳区",
  "emergency_contact": "李四",
  "emergency_phone": "13900139000",
  "target_exam_product_id": 1,
  "institution_id": 1,
  "exam_product_id": 1,
  "status": "active",
  "notes": "备注信息"
}
```

**响应示例:**
```json
{
  "id": 1,
  "name": "张三",
  "id_number": "110101199001011234",
  "phone": "13800138000",
  "email": "zhangsan@example.com",
  "gender": "male",
  "birth_date": "1990-01-01",
  "address": "北京市朝阳区",
  "emergency_contact": "李四",
  "emergency_phone": "13900139000",
  "target_exam_product_id": 1,
  "institution_id": 1,
  "exam_product_id": 1,
  "status": "active",
  "notes": "备注信息",
  "created_by": 1,
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

### 3.2 获取考生列表

**GET** `/candidates/`

**查询参数:**
- `page` (int): 页码，默认1
- `size` (int): 每页数量，默认10，最大100
- `institution_id` (int, 可选): 机构ID
- `status` (string, 可选): 状态筛选
- `search` (string, 可选): 搜索关键词

**响应示例:**
```json
[
  {
    "id": 1,
    "name": "张三",
    "id_number": "110101199001011234",
    "phone": "13800138000",
    "email": "zhangsan@example.com",
    "gender": "male",
    "birth_date": "1990-01-01",
    "address": "北京市朝阳区",
    "emergency_contact": "李四",
    "emergency_phone": "13900139000",
    "target_exam_product_id": 1,
    "institution_id": 1,
    "exam_product_id": 1,
    "status": "active",
    "notes": "备注信息",
    "created_by": 1,
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z"
  }
]
```

### 3.3 获取考生详情

**GET** `/candidates/{candidate_id}`

**响应示例:**
```json
{
  "id": 1,
  "name": "张三",
  "id_number": "110101199001011234",
  "phone": "13800138000",
  "email": "zhangsan@example.com",
  "gender": "male",
  "birth_date": "1990-01-01",
  "address": "北京市朝阳区",
  "emergency_contact": "李四",
  "emergency_phone": "13900139000",
  "target_exam_product_id": 1,
  "institution_id": 1,
  "exam_product_id": 1,
  "status": "active",
  "notes": "备注信息",
  "created_by": 1,
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

### 3.4 更新考生信息

**PUT** `/candidates/{candidate_id}`

**请求参数:**
```json
{
  "name": "张三",
  "phone": "13800138000",
  "email": "zhangsan@example.com",
  "status": "active",
  "notes": "更新后的备注信息"
}
```

### 3.5 删除考生

**DELETE** `/candidates/{candidate_id}`

**响应状态码:** 204 (无内容)

### 3.6 批量导入考生

**POST** `/candidates/batch-import`

**请求参数:**
- `file` (file): Excel文件
- `institution_id` (int): 机构ID
- `exam_product_id` (int): 考试产品ID

**响应示例:**
```json
{
  "success_count": 50,
  "failed_count": 2,
  "failed_items": [
    "身份证号 110101199001011234 已存在",
    "身份证号 110101199001011235 格式错误"
  ]
}
```

### 3.7 下载导入模板

**GET** `/candidates/batch-import/template`

**响应:** Excel文件下载

## 4. 考试产品管理API

### 4.1 创建考试产品

**POST** `/exam-products/`

**请求参数:**
```json
{
  "name": "计算机等级考试",
  "description": "全国计算机等级考试",
  "code": "NCRE_001",
  "category": "计算机类",
  "exam_type": "理论+实践",
  "exam_class": "等级考试",
  "exam_level": "一级",
  "duration_minutes": 120,
  "theory_pass_score": 60,
  "practical_pass_score": 60,
  "training_hours": 40,
  "price": 150.00,
  "training_price": 800.00,
  "theory_content": "计算机基础知识",
  "practical_content": "Office办公软件操作",
  "requirements": "无特殊要求"
}
```

**响应示例:**
```json
{
  "id": 1,
  "name": "计算机等级考试",
  "description": "全国计算机等级考试",
  "code": "NCRE_001",
  "category": "计算机类",
  "exam_type": "理论+实践",
  "exam_class": "等级考试",
  "exam_level": "一级",
  "duration_minutes": 120,
  "theory_pass_score": 60,
  "practical_pass_score": 60,
  "training_hours": 40,
  "price": 150.00,
  "training_price": 800.00,
  "theory_content": "计算机基础知识",
  "practical_content": "Office办公软件操作",
  "requirements": "无特殊要求",
  "status": "active",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

### 4.2 获取考试产品列表

**GET** `/exam-products/`

**查询参数:**
- `page` (int): 页码，默认1
- `size` (int): 每页数量，默认20，最大100

**响应示例:**
```json
[
  {
    "id": 1,
    "name": "计算机等级考试",
    "description": "全国计算机等级考试",
    "code": "NCRE_001",
    "category": "计算机类",
    "exam_type": "理论+实践",
    "exam_class": "等级考试",
    "exam_level": "一级",
    "duration_minutes": 120,
    "theory_pass_score": 60,
    "practical_pass_score": 60,
    "training_hours": 40,
    "price": 150.00,
    "training_price": 800.00,
    "theory_content": "计算机基础知识",
    "practical_content": "Office办公软件操作",
    "requirements": "无特殊要求",
    "status": "active",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z"
  }
]
```

### 4.3 获取考试产品详情

**GET** `/exam-products/{exam_product_id}`

### 4.4 更新考试产品

**PUT** `/exam-products/{exam_product_id}`

### 4.5 删除考试产品

**DELETE** `/exam-products/{exam_product_id}`

**响应状态码:** 204 (无内容)

## 5. 场地管理API

### 5.1 创建场地

**POST** `/venues/`

**请求参数:**
```json
{
  "name": "第一考场",
  "type": "理论考场"
}
```

**响应示例:**
```json
{
  "id": 1,
  "name": "第一考场",
  "type": "理论考场",
  "status": "active",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

### 5.2 获取场地列表

**GET** `/venues/`

**查询参数:**
- `page` (int): 页码，默认1
- `size` (int): 每页数量，默认20，最大100

**响应示例:**
```json
[
  {
    "id": 1,
    "name": "第一考场",
    "type": "理论考场",
    "status": "active",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z"
  }
]
```

### 5.3 获取场地详情

**GET** `/venues/{venue_id}`

### 5.4 更新场地信息

**PUT** `/venues/{venue_id}`

### 5.5 删除场地

**DELETE** `/venues/{venue_id}`

**响应状态码:** 204 (无内容)

## 6. 排期管理API

### 6.1 获取待排期考生

**GET** `/schedules/candidates-to-schedule`

**查询参数:**
- `scheduled_date` (datetime): 排期日期
- `institution_id` (int, 可选): 机构ID
- `exam_product_id` (int, 可选): 考试产品ID
- `status` (string, 可选): 状态筛选

**响应示例:**
```json
{
  "candidates": [
    {
      "id": 1,
      "name": "张三",
      "phone": "13800138000",
      "institution_name": "培训机构A",
      "target_exam_product_name": "计算机等级考试"
    }
  ]
}
```

### 6.2 批量创建排期

**POST** `/schedules/batch-create`

**请求参数:**
```json
{
  "scheduled_date": "2024-01-15",
  "start_time": "09:00:00",
  "end_time": "11:00:00",
  "venue_id": 1,
  "exam_product_id": 1,
  "candidate_ids": [1, 2, 3, 4, 5]
}
```

**响应示例:**
```json
{
  "message": "成功创建 5 个排期",
  "schedules": [
    {
      "id": 1,
      "candidate_id": 1,
      "exam_product_id": 1,
      "venue_id": 1,
      "schedule_type": "theory",
      "scheduled_date": "2024-01-15",
      "start_time": "09:00:00",
      "end_time": "11:00:00"
    }
  ]
}
```

### 6.3 获取考生排期列表

**GET** `/schedules/candidates/{candidate_id}/schedules`

**查询参数:**
- `page` (int): 页码，默认1
- `size` (int): 每页数量，默认10，最大100

### 6.4 获取排期列表

**GET** `/schedules/`

**查询参数:**
- `page` (int): 页码，默认1
- `size` (int): 每页数量，默认10，最大100
- `candidate_id` (int, 可选): 考生ID
- `status` (string, 可选): 状态筛选
- `scheduled_date` (datetime, 可选): 排期日期

### 6.5 获取排期详情

**GET** `/schedules/{schedule_id}`

### 6.6 更新排期

**PUT** `/schedules/{schedule_id}`

### 6.7 删除排期

**DELETE** `/schedules/{schedule_id}`

**响应状态码:** 204 (无内容)

### 6.8 签到功能

**POST** `/schedules/{schedule_id}/check-in`

**请求参数:**
```json
{
  "check_in_time": "2024-01-15T09:00:00Z",
  "notes": "考生按时到达"
}
```

### 6.9 扫码签到

**POST** `/schedules/scan-check-in`

**请求参数:**
```json
{
  "qr_code": "schedule_123_456",
  "check_in_time": "2024-01-15T09:00:00Z",
  "notes": "扫码签到"
}
```

### 6.10 批量扫码签到

**POST** `/schedules/batch-scan-check-in`

**请求参数:**
```json
{
  "qr_codes": ["schedule_123_456", "schedule_123_457"],
  "check_in_time": "2024-01-15T09:00:00Z",
  "notes": "批量扫码签到"
}
```

### 6.11 获取签到统计

**GET** `/schedules/check-in-stats`

**查询参数:**
- `scheduled_date` (datetime, 可选): 排期日期
- `venue_id` (int, 可选): 场地ID

**响应示例:**
```json
{
  "total_schedules": 100,
  "checked_in": 85,
  "not_checked_in": 15,
  "check_in_rate": 0.85
}
```

### 6.12 获取排队位置

**GET** `/schedules/{schedule_id}/queue-position`

**响应示例:**
```json
{
  "schedule_id": 1,
  "queue_position": 5,
  "total_in_queue": 20,
  "estimated_wait_time": 15
}
```

## 7. 公共API

### 7.1 获取考场状态

**GET** `/public/venues-status`

**响应示例:**
```json
{
  "timestamp": "2024-01-01T10:00:00Z",
  "venues": [
    {
      "id": 1,
      "name": "第一考场",
      "status": "active",
      "current_capacity": 30,
      "max_capacity": 50,
      "current_exam": "计算机等级考试"
    }
  ]
}
```

### 7.2 获取指定考场状态

**GET** `/public/venues/{venue_id}/status`

**响应示例:**
```json
{
  "venue_id": 1,
  "name": "第一考场",
  "status": "active",
  "current_capacity": 30,
  "max_capacity": 50,
  "current_exam": "计算机等级考试",
  "next_exam": "英语等级考试",
  "next_exam_time": "2024-01-01T14:00:00Z"
}
```

## 8. 机构管理API

### 8.1 创建机构

**POST** `/simple-institutions`

**请求参数:**
```json
{
  "name": "培训机构A",
  "code": "ORG_001",
  "contact_person": "张经理",
  "phone": "010-12345678",
  "email": "contact@orga.com",
  "address": "北京市朝阳区",
  "description": "专业培训机构",
  "status": "active",
  "license_number": "L123456789",
  "business_scope": "计算机培训"
}
```

### 8.2 获取机构列表

**GET** `/simple-institutions`

### 8.3 获取机构详情

**GET** `/simple-institutions/{institution_id}`

### 8.4 更新机构信息

**PUT** `/simple-institutions/{institution_id}`

### 8.5 删除机构

**DELETE** `/simple-institutions/{institution_id}`

### 8.6 更新机构状态

**PATCH** `/simple-institutions/{institution_id}/status`

**请求参数:**
```json
{
  "status": "inactive"
}
```

### 8.7 复制机构

**POST** `/simple-institutions/{institution_id}/duplicate`

**请求参数:**
```json
{
  "new_name": "培训机构A-副本"
}
```

### 8.8 获取机构统计

**GET** `/simple-institutions/stats`

**响应示例:**
```json
{
  "total_institutions": 50,
  "active_institutions": 45,
  "inactive_institutions": 5,
  "total_candidates": 1000
}
```

### 8.9 批量更新机构状态

**POST** `/simple-institutions/bulk-status`

**请求参数:**
```json
{
  "institution_ids": [1, 2, 3],
  "status": "active"
}
```

## 9. 错误码说明

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 204 | 删除成功，无返回内容 |
| 400 | 请求参数错误 |
| 401 | 未授权，需要登录 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 422 | 请求参数验证失败 |
| 500 | 服务器内部错误 |

## 10. 使用示例

### 10.1 完整流程示例

1. **用户登录**
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

2. **创建考试产品**
```bash
curl -X POST "http://localhost:8000/exam-products/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "计算机等级考试", "description": "全国计算机等级考试"}'
```

3. **创建考生**
```bash
curl -X POST "http://localhost:8000/candidates/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "张三", "id_number": "110101199001011234", "phone": "13800138000"}'
```

4. **创建排期**
```bash
curl -X POST "http://localhost:8000/schedules/batch-create" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"scheduled_date": "2024-01-15", "candidate_ids": [1]}'
```

## 11. 注意事项

1. 所有需要认证的API都需要在请求头中包含有效的Bearer Token
2. 文件上传接口使用multipart/form-data格式
3. 分页查询的页码从1开始
4. 时间格式统一使用ISO 8601格式
5. 批量操作建议控制单次请求的数据量，避免超时 