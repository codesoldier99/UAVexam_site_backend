# 🚁 CAAC无人机驾驶员考试产品API接口文档

## 📋 概述

本API基于中国民航局（CAAC）无人机驾驶员考试分类体系，提供完整的考试产品管理功能。系统涵盖种类、类型、类别、等级四个维度的分类管理。

## 🏗️ 数据模型

### 考试产品分类体系

#### 1. 考试种类（按飞行范围划分）
- `VLOS` - 视距内驾驶员考试
- `BVLOS` - 超视距驾驶员考试

#### 2. 考试类型（按无人机机型划分）
- `MULTIROTOR` - 多旋翼无人机考试
- `FIXED_WING` - 固定翼无人机考试
- `VTOL` - 垂直起降固定翼无人机考试

#### 3. 考试类别（按应用领域划分）
- `AGRICULTURE` - 农业植保类
- `POWER_INSPECTION` - 电力巡检类
- `FILM_PHOTOGRAPHY` - 影视航拍类
- `LOGISTICS` - 物流配送类

#### 4. 考试等级（按执照权限划分）
- `PILOT` - 视距内驾驶员
- `CAPTAIN` - 超视距驾驶员
- `INSTRUCTOR` - 教员等级

## 🔌 API接口

### 基础信息
- **Base URL**: `http://localhost:8000`
- **认证方式**: JWT Bearer Token
- **Content-Type**: `application/json`

### 1. 创建考试产品

**POST** `/exam-products`

**请求头**:
```
Authorization: Bearer {token}
Content-Type: application/json
```

**请求体**:
```json
{
  "name": "视距内多旋翼无人机驾驶员考试",
  "code": "VLOS-MULTI-001",
  "description": "在肉眼可见范围内操控多旋翼无人机，适用于航拍、短距离巡检等基础作业",
  "category": "VLOS",
  "exam_type": "MULTIROTOR",
  "exam_class": "FILM_PHOTOGRAPHY",
  "exam_level": "PILOT",
  "theory_pass_score": 70,
  "practical_pass_score": 80,
  "duration_minutes": 120,
  "training_hours": 44,
  "price": 7500.0,
  "training_price": 6800.0,
  "theory_content": "无人机法规、飞行原理、气象知识、应急处置",
  "practical_content": "GPS模式悬停、水平8字飞行、定点降落",
  "requirements": "年满16周岁，初中以上学历，无犯罪记录，矫正视力≥1.0",
  "is_active": true
}
```

**响应** (201 Created):
```json
{
  "id": 3,
  "name": "视距内多旋翼无人机驾驶员考试",
  "code": "VLOS-MULTI-001",
  "description": "在肉眼可见范围内操控多旋翼无人机，适用于航拍、短距离巡检等基础作业",
  "category": "VLOS",
  "exam_type": "MULTIROTOR",
  "exam_class": "FILM_PHOTOGRAPHY",
  "exam_level": "PILOT",
  "theory_pass_score": 70,
  "practical_pass_score": 80,
  "duration_minutes": 120,
  "training_hours": 44,
  "price": 7500.0,
  "training_price": 6800.0,
  "theory_content": "无人机法规、飞行原理、气象知识、应急处置",
  "practical_content": "GPS模式悬停、水平8字飞行、定点降落",
  "requirements": "年满16周岁，初中以上学历，无犯罪记录，矫正视力≥1.0",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

### 2. 获取考试产品列表

**GET** `/exam-products`

**查询参数**:
- `page` (可选): 页码，默认1
- `size` (可选): 每页数量，默认10
- `category` (可选): 按考试种类筛选
- `exam_type` (可选): 按考试类型筛选
- `exam_class` (可选): 按考试类别筛选
- `exam_level` (可选): 按考试等级筛选

**请求头**:
```
Authorization: Bearer {token}
```

**响应** (200 OK):
```json
{
  "items": [
    {
      "id": 3,
      "name": "视距内多旋翼无人机驾驶员考试",
      "code": "VLOS-MULTI-001",
      "description": "在肉眼可见范围内操控多旋翼无人机，适用于航拍、短距离巡检等基础作业",
      "category": "VLOS",
      "exam_type": "MULTIROTOR",
      "exam_class": "FILM_PHOTOGRAPHY",
      "exam_level": "PILOT",
      "theory_pass_score": 70,
      "practical_pass_score": 80,
      "duration_minutes": 120,
      "training_hours": 44,
      "price": 7500.0,
      "training_price": 6800.0,
      "theory_content": "无人机法规、飞行原理、气象知识、应急处置",
      "practical_content": "GPS模式悬停、水平8字飞行、定点降落",
      "requirements": "年满16周岁，初中以上学历，无犯罪记录，矫正视力≥1.0",
      "is_active": true,
      "created_at": "2024-01-15T10:30:00",
      "updated_at": "2024-01-15T10:30:00"
    }
  ],
  "total": 3,
  "page": 1,
  "size": 10,
  "pages": 1
}
```

### 3. 获取考试产品详情

**GET** `/exam-products/{id}`

**请求头**:
```
Authorization: Bearer {token}
```

**响应** (200 OK):
```json
{
  "id": 3,
  "name": "视距内多旋翼无人机驾驶员考试",
  "code": "VLOS-MULTI-001",
  "description": "在肉眼可见范围内操控多旋翼无人机，适用于航拍、短距离巡检等基础作业",
  "category": "VLOS",
  "exam_type": "MULTIROTOR",
  "exam_class": "FILM_PHOTOGRAPHY",
  "exam_level": "PILOT",
  "theory_pass_score": 70,
  "practical_pass_score": 80,
  "duration_minutes": 120,
  "training_hours": 44,
  "price": 7500.0,
  "training_price": 6800.0,
  "theory_content": "无人机法规、飞行原理、气象知识、应急处置",
  "practical_content": "GPS模式悬停、水平8字飞行、定点降落",
  "requirements": "年满16周岁，初中以上学历，无犯罪记录，矫正视力≥1.0",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

### 4. 更新考试产品

**PUT** `/exam-products/{id}`

**请求头**:
```
Authorization: Bearer {token}
Content-Type: application/json
```

**请求体** (部分字段可选):
```json
{
  "name": "视距内多旋翼无人机驾驶员考试-高级版",
  "description": "更新后的考试产品描述",
  "price": 8000.0,
  "training_price": 7200.0,
  "is_active": true
}
```

**响应** (200 OK):
```json
{
  "id": 3,
  "name": "视距内多旋翼无人机驾驶员考试-高级版",
  "code": "VLOS-MULTI-001",
  "description": "更新后的考试产品描述",
  "category": "VLOS",
  "exam_type": "MULTIROTOR",
  "exam_class": "FILM_PHOTOGRAPHY",
  "exam_level": "PILOT",
  "theory_pass_score": 70,
  "practical_pass_score": 80,
  "duration_minutes": 120,
  "training_hours": 44,
  "price": 8000.0,
  "training_price": 7200.0,
  "theory_content": "无人机法规、飞行原理、气象知识、应急处置",
  "practical_content": "GPS模式悬停、水平8字飞行、定点降落",
  "requirements": "年满16周岁，初中以上学历，无犯罪记录，矫正视力≥1.0",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:35:00"
}
```

### 5. 删除考试产品

**DELETE** `/exam-products/{id}`

**请求头**:
```
Authorization: Bearer {token}
```

**响应** (204 No Content):
```
无响应体
```

## 📊 字段说明

### 必填字段
- `name`: 产品名称 (string, max 100字符)
- `code`: 产品代码 (string, max 50字符, 唯一)
- `category`: 考试种类 (enum: VLOS, BVLOS)
- `exam_type`: 考试类型 (enum: MULTIROTOR, FIXED_WING, VTOL)
- `exam_class`: 考试类别 (enum: AGRICULTURE, POWER_INSPECTION, FILM_PHOTOGRAPHY, LOGISTICS)
- `exam_level`: 考试等级 (enum: PILOT, CAPTAIN, INSTRUCTOR)
- `theory_pass_score`: 理论考试及格分数 (integer)
- `practical_pass_score`: 实操考试及格分数 (integer)
- `duration_minutes`: 考试时长（分钟）(integer)
- `training_hours`: 培训时长（小时）(integer)
- `price`: 考试费用 (float)

### 可选字段
- `description`: 产品描述 (text)
- `training_price`: 培训费用 (float)
- `theory_content`: 理论考试内容 (text)
- `practical_content`: 实操考试内容 (text)
- `requirements`: 报考要求 (text)
- `is_active`: 是否启用 (boolean, 默认true)

### 系统字段
- `id`: 主键ID (integer, 自动生成)
- `created_at`: 创建时间 (datetime, 自动生成)
- `updated_at`: 更新时间 (datetime, 自动更新)

## 🔐 权限要求

- **创建考试产品**: 需要超级管理员或考务管理员权限
- **查看考试产品**: 需要管理员权限
- **更新考试产品**: 需要超级管理员或考务管理员权限
- **删除考试产品**: 需要超级管理员权限

## 📝 使用示例

### 创建视距内多旋翼考试产品
```bash
curl -X POST "http://localhost:8000/exam-products" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "视距内多旋翼无人机驾驶员考试",
    "code": "VLOS-MULTI-001",
    "description": "在肉眼可见范围内操控多旋翼无人机",
    "category": "VLOS",
    "exam_type": "MULTIROTOR",
    "exam_class": "FILM_PHOTOGRAPHY",
    "exam_level": "PILOT",
    "theory_pass_score": 70,
    "practical_pass_score": 80,
    "duration_minutes": 120,
    "training_hours": 44,
    "price": 7500.0,
    "training_price": 6800.0,
    "theory_content": "无人机法规、飞行原理、气象知识、应急处置",
    "practical_content": "GPS模式悬停、水平8字飞行、定点降落",
    "requirements": "年满16周岁，初中以上学历，无犯罪记录，矫正视力≥1.0"
  }'
```

### 按分类筛选考试产品
```bash
# 筛选视距内考试
curl -X GET "http://localhost:8000/exam-products?category=VLOS" \
  -H "Authorization: Bearer {token}"

# 筛选多旋翼考试
curl -X GET "http://localhost:8000/exam-products?exam_type=MULTIROTOR" \
  -H "Authorization: Bearer {token}"

# 筛选农业植保类考试
curl -X GET "http://localhost:8000/exam-products?exam_class=AGRICULTURE" \
  -H "Authorization: Bearer {token}"
```

## 🎯 业务场景

### 1. 视距内多旋翼无人机考试
- **适用场景**: 航拍、短距离巡检、小型农业植保
- **考试内容**: 理论考试（70分及格）、GPS模式实操飞行
- **培训时长**: 44小时
- **费用范围**: 6800-8000元

### 2. 超视距固定翼无人机考试
- **适用场景**: 电力巡检、长距离测绘、物流配送
- **考试内容**: 理论考试（80分及格）、姿态模式实操、地面站操作
- **培训时长**: 56小时
- **费用范围**: 12000-15000元

### 3. 农业植保类考试
- **适用场景**: 大面积农田作业、果树植保
- **特殊要求**: 需掌握农药喷洒、播撒等专业操作
- **培训内容**: 农药知识、植保技术、安全操作、环保要求

## 🔧 错误处理

### 常见错误码
- `400 Bad Request`: 请求参数错误
- `401 Unauthorized`: 未认证或认证失败
- `403 Forbidden`: 权限不足
- `404 Not Found`: 考试产品不存在
- `422 Unprocessable Entity`: 数据验证失败
- `500 Internal Server Error`: 服务器内部错误

### 错误响应示例
```json
{
  "detail": [
    {
      "type": "enum",
      "loc": ["body", "category"],
      "msg": "Input should be 'VLOS' or 'BVLOS'",
      "input": "INVALID_CATEGORY"
    }
  ]
}
```

## 📈 数据统计

系统支持以下统计功能：
- 按考试种类统计产品数量
- 按考试类型统计产品数量
- 按考试类别统计产品数量
- 按考试等级统计产品数量
- 按价格区间统计产品数量

---

**注意**: 本API严格按照CAAC无人机驾驶员考试分类体系设计，确保与民航局标准保持一致。 