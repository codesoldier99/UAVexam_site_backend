
# 考试系统后端API文档

## 基础信息
- 开发环境: FastAPI + SQLAlchemy + MySQL
- 认证方式: JWT Token
- 数据格式: JSON

## 主要接口

### 1. 认证接口
- `POST /auth/jwt/login` - JWT登录
- `POST /simple-login` - 简化登录（测试用）
- `GET /users/me` - 获取当前用户信息

### 2. 考生管理
- `GET /candidates/` - 获取考生列表
- `POST /candidates/` - 创建考生
- `GET /candidates/{id}` - 获取考生详情
- `PUT /candidates/{id}` - 更新考生信息
- `DELETE /candidates/{id}` - 删除考生
- `POST /candidates/batch-import` - 批量导入考生
- `GET /candidates/template` - 下载导入模板

### 3. 考试产品管理
- `GET /exam-products/` - 获取考试产品列表
- `POST /exam-products/` - 创建考试产品
- `GET /exam-products/{id}` - 获取考试产品详情
- `PUT /exam-products/{id}` - 更新考试产品
- `DELETE /exam-products/{id}` - 删除考试产品

### 4. 排期管理
- `GET /schedules/` - 获取排期列表
- `POST /schedules/` - 创建排期
- `GET /schedules/{id}` - 获取排期详情
- `PUT /schedules/{id}` - 更新排期
- `DELETE /schedules/{id}` - 删除排期
- `GET /schedules/candidates-to-schedule` - 获取待排期考生
- `POST /schedules/batch-create` - 批量创建排期
- `POST /schedules/scan-check-in` - 扫码签到
- `POST /schedules/batch-scan-check-in` - 批量扫码签到
- `GET /schedules/check-in-stats` - 获取签到统计

### 5. 机构管理
- `GET /simple-institutions/` - 获取机构列表
- `POST /simple-institutions/` - 创建机构
- `GET /simple-institutions/{id}` - 获取机构详情
- `PUT /simple-institutions/{id}` - 更新机构
- `DELETE /simple-institutions/{id}` - 删除机构

### 6. 微信小程序接口
- `POST /wx-miniprogram/login` - 微信登录
- `GET /wx-miniprogram/user-info` - 获取用户信息
- `POST /wx-miniprogram/check-in` - 微信签到

## 数据模型

### 考生 (Candidate)
```json
{
  "id": 1,
  "name": "张三",
  "phone": "13800138000",
  "id_card": "110101199001011234",
  "email": "zhangsan@example.com",
  "institution_id": 1,
  "target_exam_product_id": 1,
  "status": "pending",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### 考试产品 (ExamProduct)
```json
{
  "id": 1,
  "name": "无人机驾驶员理论考试",
  "code": "UAV_THEORY",
  "description": "无人机驾驶员理论考试",
  "category": "VLOS",
  "exam_type": "MULTIROTOR",
  "exam_class": "AGRICULTURE",
  "exam_level": "PILOT",
  "theory_pass_score": 80,
  "practical_pass_score": 85,
  "duration_minutes": 120,
  "training_hours": 40,
  "price": 1000.0,
  "is_active": true
}
```

### 排期 (Schedule)
```json
{
  "id": 1,
  "candidate_id": 1,
  "exam_product_id": 1,
  "venue_id": 1,
  "scheduled_date": "2024-01-01",
  "start_time": "09:00:00",
  "end_time": "11:00:00",
  "schedule_type": "theory",
  "status": "scheduled",
  "check_in_time": null,
  "notes": "测试排期"
}
```

## 认证说明

### JWT认证
1. 调用登录接口获取token
2. 在后续请求的Header中添加: `Authorization: Bearer <token>`

### 权限说明
- 机构用户: 只能访问本机构的考生和排期
- 超级管理员: 可以访问所有数据
- 微信用户: 只能访问自己的信息

## 错误码说明
- 200: 成功
- 201: 创建成功
- 400: 请求参数错误
- 401: 未认证
- 403: 权限不足
- 404: 资源不存在
- 422: 数据验证失败
- 500: 服务器内部错误

## 测试接口
- `GET /` - 根接口
- `GET /test` - 测试接口
- `GET /docs` - API文档
- `GET /redoc` - 另一种API文档格式

## 联调建议
1. 使用Postman或类似工具测试接口
2. 先测试公开接口（如 `/` 和 `/test`）
3. 再测试需要认证的接口
4. 注意请求格式和认证方式
5. 遇到问题及时沟通
