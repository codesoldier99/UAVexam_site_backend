# 考试系统后端API完整接口文档

## 🏠 项目概述

**项目名称**: 考试系统后端API  
**版本**: 1.0.0-test  
**部署地址**: http://106.52.214.54/  
**GitHub仓库**: https://github.com/codesoldier99/UAVexam_site_backend  
**最后更新**: 2025-08-03

这是一个完整的考试管理系统后端API，主要用于无人机驾驶员等各类技能考试的管理。系统支持机构管理、考生管理、排期管理、二维码签到、批量操作等完整功能。

## 🚀 快速开始

### 基础信息
- **Base URL**: `http://106.52.214.54/`
- **API文档**: `http://106.52.214.54/docs`
- **ReDoc文档**: `http://106.52.214.54/redoc`

### 通用响应格式
```json
{
  "message": "操作描述",
  "data": {},
  "pagination": {
    "page": 1,
    "size": 10,
    "total": 100,
    "pages": 10
  }
}
```

### 通用查询参数
- `page`: 页码（默认1）
- `size`: 每页数量（默认10，最大100）

---

## 📋 API接口列表

### 1. 系统基础接口

#### 1.1 根路径
```http
GET /
```
**功能**: 系统欢迎信息  
**响应示例**:
```json
{
  "message": "欢迎使用考试系统后端API - 简化测试版本",
  "version": "1.0.0-test"
}
```

#### 1.2 健康检查
```http
GET /health
```
**功能**: 系统健康状态检查  
**响应示例**:
```json
{
  "status": "healthy",
  "timestamp": "2025-08-03T19:10:00",
  "version": "1.0.0-test",
  "service": "考试系统后端API - 简化测试版本"
}
```

#### 1.3 测试接口
```http
GET /test
```
**功能**: API连通性测试  
**响应示例**:
```json
{
  "message": "测试成功",
  "status": "ok",
  "timestamp": "2025-08-03T19:10:00"
}
```

---

### 2. 机构管理 `/institutions`

#### 2.1 获取机构列表
```http
GET /institutions
```
**查询参数**:
- `page`: 页码
- `size`: 每页数量
- `status`: 状态筛选 (active/inactive)
- `search`: 搜索关键词

**响应示例**:
```json
{
  "message": "机构列表",
  "data": [
    {
      "id": 1,
      "name": "北京航空培训中心",
      "contact_person": "张经理",
      "phone": "010-12345678",
      "status": "active",
      "created_at": "2025-08-01T10:00:00",
      "updated_at": "2025-08-01T10:00:00"
    }
  ],
  "pagination": {
    "page": 1,
    "size": 10,
    "total": 3,
    "pages": 1
  }
}
```

#### 2.2 获取机构详情
```http
GET /institutions/{institution_id}
```
**响应示例**:
```json
{
  "message": "机构详情",
  "data": {
    "id": 1,
    "name": "北京航空培训中心",
    "contact_person": "张经理",
    "phone": "010-12345678",
    "status": "active",
    "stats": {
      "total_candidates": 45,
      "active_schedules": 3
    }
  }
}
```

#### 2.3 创建机构
```http
POST /institutions
```
**请求体**:
```json
{
  "name": "机构名称",
  "contact_person": "联系人",
  "phone": "联系电话"
}
```

#### 2.4 更新机构
```http
PUT /institutions/{institution_id}
```

#### 2.5 删除机构
```http
DELETE /institutions/{institution_id}
```

---

### 3. 用户管理 `/users`

#### 3.1 获取用户列表
```http
GET /users
```
**查询参数**:
- `page`: 页码
- `size`: 每页数量
- `role`: 角色筛选 (admin/examiner/student/teacher)
- `status`: 状态筛选 (active/inactive)

**响应示例**:
```json
{
  "message": "用户列表接口 - 支持分页和筛选",
  "data": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "role": "admin",
      "status": "active",
      "created_at": "2025-01-01"
    }
  ],
  "pagination": {
    "page": 1,
    "size": 10,
    "total": 6,
    "pages": 1
  },
  "filters": {
    "role": null,
    "status": null
  }
}
```

#### 3.2 获取用户详情
```http
GET /users/{user_id}
```

---

### 4. 考生管理 `/candidates`

#### 4.1 获取考生列表
```http
GET /candidates
```
**查询参数**:
- `page`: 页码
- `size`: 每页数量
- `status`: 状态筛选 (待排期/已审核/已考试)
- `exam_type`: 考试类型筛选
- `gender`: 性别筛选 (男/女)
- `institution_id`: 机构ID筛选

**响应示例**:
```json
{
  "message": "考生列表",
  "data": [
    {
      "id": 1,
      "name": "张三",
      "id_number": "110101199001011234",
      "phone": "13800138001",
      "gender": "男",
      "status": "待排期",
      "exam_product_id": 1,
      "exam_product_name": "无人机驾驶员考试",
      "institution_id": 1,
      "institution_name": "北京航空培训中心",
      "registration_date": "2025-08-01"
    }
  ]
}
```

#### 4.2 获取考生详情
```http
GET /candidates/{candidate_id}
```

#### 4.3 创建考生
```http
POST /candidates
```
**请求体**:
```json
{
  "name": "考生姓名",
  "id_number": "身份证号",
  "phone": "联系电话",
  "gender": "性别",
  "exam_product_id": 1,
  "institution_id": 1
}
```

#### 4.4 导出考生数据
```http
GET /candidates/export
```
**功能**: 导出Excel格式的考生数据

---

### 5. 考试产品管理 `/exam-products`

#### 5.1 获取考试产品列表
```http
GET /exam-products
```
**查询参数**:
- `page`: 页码
- `size`: 每页数量
- `category`: 考试类别筛选 (理论/实操/理论+实操)
- `status`: 状态筛选 (active/inactive)
- `difficulty`: 难度筛选 (简单/中等/困难)

**响应示例**:
```json
{
  "message": "考试产品列表接口 - 支持分页和筛选",
  "data": [
    {
      "id": 1,
      "name": "无人机驾驶员考试",
      "description": "民用无人机驾驶员资格考试",
      "category": "理论+实操",
      "duration": 120,
      "status": "active",
      "difficulty": "中等",
      "price": 500.0
    }
  ]
}
```

#### 5.2 获取考试产品详情
```http
GET /exam-products/{product_id}
```

---

### 6. 场地管理 `/venues`

#### 6.1 获取场地列表
```http
GET /venues
```

#### 6.2 获取场地详情
```http
GET /venues/{venue_id}
```

---

### 7. 排期管理 `/schedules`

#### 7.1 获取排期列表
```http
GET /schedules
```

#### 7.2 创建排期
```http
POST /schedules
```

#### 7.3 增强版排期管理
```http
GET /schedule-enhanced
POST /schedule-enhanced/batch
PUT /schedule-enhanced/{schedule_id}
```

---

### 8. 批量操作 `/batch`

#### 8.1 下载考生导入模板
```http
GET /batch/candidates/template
```
**功能**: 下载Excel格式的考生导入模板  
**响应**: Excel文件下载

**模板格式**:
- 考生姓名
- 身份证号
- 联系电话
- 考试产品名称

#### 8.2 批量导入考生
```http
POST /batch/candidates/import
```
**请求**: 上传Excel文件  
**响应示例**:
```json
{
  "message": "批量导入考生完成",
  "result": {
    "total_rows": 10,
    "success_count": 8,
    "failed_count": 2,
    "success_items": [...],
    "failed_items": [...],
    "import_time": "2025-08-03T19:10:00"
  }
}
```

#### 8.3 批量排期
```http
POST /batch/schedules
```
**请求体**:
```json
{
  "candidate_ids": [1, 2, 3],
  "exam_date": "2025-08-10",
  "start_time": "09:00:00",
  "venue_id": 1,
  "activity_name": "无人机驾驶员考试",
  "duration_minutes": 15
}
```

#### 8.4 批量导出数据
```http
GET /batch/export/candidates
GET /batch/export/schedules
GET /batch/export/results
```

---

### 9. 二维码与签到 `/qrcode`

#### 9.1 健康检查
```http
GET /qrcode/health
```
**响应示例**:
```json
{
  "status": "healthy",
  "service": "二维码和签到服务",
  "version": "1.0.0",
  "features": ["二维码生成", "扫码签到", "考生查询", "签到管理"]
}
```

#### 9.2 生成考试二维码
```http
GET /qrcode/generate-schedule-qr/{schedule_id}
```
**响应示例**:
```json
{
  "message": "考试安排 1 二维码生成成功",
  "schedule_id": 1,
  "qr_data": {
    "type": "schedule_checkin",
    "schedule_id": 1,
    "timestamp": "2025-08-03T19:10:00",
    "valid_until": "2025-08-03T23:59:59"
  },
  "qr_url": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=1",
  "scan_url": "/qrcode/scan/1",
  "instructions": "考生可扫描此二维码进行签到"
}
```

#### 9.3 扫码签到
```http
POST /qrcode/scan-checkin
```
**查询参数**:
- `qr_content`: 扫描的二维码内容
- `staff_id`: 考务人员ID (可选)

**响应示例**:
```json
{
  "message": "签到成功",
  "checkin_data": {
    "schedule_id": 1,
    "candidate_id": 1,
    "candidate_name": "张三",
    "checkin_time": "2025-08-03T09:15:00",
    "status": "已签到"
  }
}
```

#### 9.4 考生查询接口
```http
GET /qrcode/candidates/search
```
**查询参数**:
- `query`: 搜索关键词 (姓名/身份证/手机号)

#### 9.5 签到状态管理
```http
GET /qrcode/checkin-status/{schedule_id}
POST /qrcode/manual-checkin
PUT /qrcode/checkin/{checkin_id}/update
```

---

### 10. 微信小程序接口 `/wx-miniprogram`

#### 10.1 小程序健康检查
```http
GET /wx-miniprogram/health
```

#### 10.2 考生信息查询
```http
GET /wx-miniprogram/candidate-info
```
**查询参数**:
- `id_number`: 身份证号

#### 10.3 考试安排查询
```http
GET /wx-miniprogram/exam-schedule
```

#### 10.4 签到记录查询
```http
GET /wx-miniprogram/checkin-history
```

---

### 11. 权限管理

#### 11.1 角色管理 `/roles`
```http
GET /roles
POST /roles
PUT /roles/{role_id}
DELETE /roles/{role_id}
```

#### 11.2 权限管理 `/permissions`
```http
GET /permissions
POST /permissions
PUT /permissions/{permission_id}
```

#### 11.3 RBAC权限控制 `/rbac`
```http
GET /rbac/user-permissions/{user_id}
POST /rbac/assign-role
POST /rbac/assign-permission
```

---

### 12. 实时功能 `/realtime`

#### 12.1 实时状态查询
```http
GET /realtime/status
```

#### 12.2 实时通知
```http
GET /realtime/notifications
POST /realtime/send-notification
```

#### 12.3 WebSocket连接
```http
WS /realtime/ws/{user_id}
```

---

## 🔧 部署和配置

### 环境要求
- Python 3.8+
- FastAPI
- SQLAlchemy
- PostgreSQL/MySQL
- Redis (可选，用于缓存)

### 启动命令
```bash
# 本地开发
python start_server.py

# Docker部署
docker-compose up -d
```

### 环境变量
```bash
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key
DEBUG=True
```

## 📊 数据模型

### 考生模型
```python
{
  "id": "考生ID",
  "name": "考生姓名",
  "id_number": "身份证号",
  "phone": "联系电话",
  "gender": "性别",
  "status": "状态",
  "exam_product_id": "考试产品ID",
  "institution_id": "机构ID",
  "registration_date": "报名日期"
}
```

### 机构模型
```python
{
  "id": "机构ID",
  "name": "机构名称",
  "contact_person": "联系人",
  "phone": "联系电话",
  "status": "状态",
  "created_at": "创建时间",
  "updated_at": "更新时间"
}
```

## 🧪 测试说明

### API测试文件
- `api_full_test.py`: 完整API测试套件
- `test_core_features.py`: 核心功能测试
- `comprehensive_api_test.py`: 综合API测试

### 运行测试
```bash
python api_full_test.py
python test_core_features.py
```

## 📝 更新日志

### v1.0.0-test (2025-08-03)
- ✅ 完整的机构管理模块
- ✅ 批量操作功能 (Excel导入导出)
- ✅ 二维码签到功能
- ✅ RBAC权限控制系统
- ✅ 实时通信功能
- ✅ 增强的排期管理
- ✅ 微信小程序接口
- ✅ 完整的API测试套件

## 🔗 相关链接

- **GitHub仓库**: https://github.com/codesoldier99/UAVexam_site_backend
- **云服务器**: http://106.52.214.54/
- **API文档**: http://106.52.214.54/docs
- **Postman集合**: `exam_site_backend.postman_collection.json`

## 📞 技术支持

如有问题请通过以下方式联系：
- GitHub Issues
- 邮箱联系
- 技术文档查阅

---
*最后更新: 2025-08-03 19:10:00*