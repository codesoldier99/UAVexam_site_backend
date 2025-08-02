# 📱 扫码签到API文档

## 🎯 功能概述

扫码签到API为考试系统提供了安全、高效的签到功能，支持二维码扫描签到和批量签到操作。该API确保事务安全，正确更新Schedules和Candidates两个表的状态。

## 🔧 技术特性

- **事务安全**: 使用数据库事务确保数据一致性
- **并发控制**: 使用行锁防止重复签到
- **状态管理**: 自动更新排期和考生状态
- **迟到检测**: 自动判断是否迟到（超过开始时间15分钟）
- **批量操作**: 支持多个二维码同时签到

## 📋 API接口

### 1. 单个扫码签到

**POST** `/schedules/scan-check-in`

**功能**: 通过扫描二维码进行单个签到

**请求头**:
```
Authorization: Bearer {token}
Content-Type: application/json
```

**请求体**:
```json
{
  "qr_code": "SCHEDULE_123_1640995200_a1b2c3d4",
  "check_in_time": "2024-01-15T10:30:00",
  "notes": "考务人员备注信息"
}
```

**参数说明**:
- `qr_code`: 二维码内容（必填）
- `check_in_time`: 签到时间（可选，默认为当前时间）
- `notes`: 备注信息（可选）

**二维码格式**:
```
SCHEDULE_{schedule_id}_{timestamp}_{hash}
```

**响应示例** (200 OK):
```json
{
  "success": true,
  "message": "签到成功",
  "data": {
    "schedule_id": 123,
    "candidate_name": "张三",
    "exam_product_name": "视距内多旋翼无人机驾驶员考试",
    "check_in_time": "2024-01-15T10:30:00",
    "check_in_status": "已签到",
    "is_late": false,
    "notes": "考务人员备注信息",
    "operator": "admin@exam.com"
  }
}
```

**错误响应** (400 Bad Request):
```json
{
  "detail": "该考生已经签到"
}
```

### 2. 批量扫码签到

**POST** `/schedules/batch-scan-check-in`

**功能**: 批量处理多个二维码签到

**请求体**:
```json
{
  "qr_codes": [
    "SCHEDULE_123_1640995200_a1b2c3d4",
    "SCHEDULE_124_1640995300_b2c3d4e5",
    "SCHEDULE_125_1640995400_c3d4e5f6"
  ],
  "check_in_time": "2024-01-15T10:30:00",
  "notes": "批量签到备注"
}
```

**响应示例** (200 OK):
```json
{
  "success": true,
  "message": "批量签到完成，成功: 2，失败: 1",
  "summary": {
    "total": 3,
    "success_count": 2,
    "error_count": 1
  },
  "results": [
    {
      "qr_code": "SCHEDULE_123_1640995200_a1b2c3d4",
      "success": true,
      "data": {
        "schedule_id": 123,
        "candidate_name": "张三",
        "exam_product_name": "视距内多旋翼无人机驾驶员考试",
        "check_in_status": "已签到",
        "is_late": false
      }
    },
    {
      "qr_code": "SCHEDULE_124_1640995300_b2c3d4e5",
      "success": true,
      "data": {
        "schedule_id": 124,
        "candidate_name": "李四",
        "exam_product_name": "超视距固定翼无人机驾驶员考试",
        "check_in_status": "迟到",
        "is_late": true
      }
    },
    {
      "qr_code": "SCHEDULE_125_1640995400_c3d4e5f6",
      "success": false,
      "error": "该考生已经签到"
    }
  ]
}
```

### 3. 签到统计

**GET** `/schedules/check-in-stats`

**功能**: 获取签到统计信息

**查询参数**:
- `scheduled_date`: 排期日期（可选）
- `venue_id`: 考场ID（可选）

**响应示例** (200 OK):
```json
{
  "success": true,
  "data": {
    "total_schedules": 50,
    "checked_in_count": 35,
    "late_count": 5,
    "not_checked_in_count": 10,
    "check_in_rate": 80.0,
    "today_stats": {
      "total": 20,
      "checked_in": 15,
      "late": 2,
      "not_checked_in": 3
    },
    "date_filter": "2024-01-15",
    "venue_filter": 1
  }
}
```

## 🔒 事务安全机制

### 1. 数据库事务
```python
# 开始事务
db.begin()

# 使用行锁获取排期信息
schedule = db.query(Schedule).filter(Schedule.id == schedule_id).with_for_update().first()

# 更新排期状态
schedule.check_in_status = check_in_status
schedule.check_in_time = check_in_time

# 更新考生状态
if candidate.status == "PENDING":
    candidate.status = "ACTIVE"

# 提交事务
db.commit()
```

### 2. 状态检查
- 检查排期是否存在
- 检查排期状态（已完成/已取消）
- 检查是否已经签到
- 检查是否已标记为迟到

### 3. 迟到判断
```python
# 判断是否迟到（超过开始时间15分钟）
is_late = check_in_time > schedule.start_time + timedelta(minutes=15)
check_in_status = "迟到" if is_late else "已签到"
```

## 📊 状态更新规则

### Schedules表更新
- `check_in_status`: 更新为"已签到"或"迟到"
- `check_in_time`: 记录实际签到时间
- `notes`: 添加签到备注信息

### Candidates表更新
- 如果考生状态为"PENDING"，自动更新为"ACTIVE"
- `updated_at`: 更新修改时间

## 🚨 错误处理

### 常见错误码
- `400`: 请求参数错误或业务逻辑错误
- `403`: 权限不足
- `404`: 排期不存在
- `500`: 服务器内部错误

### 错误场景
1. **无效二维码**: 二维码格式错误或排期不存在
2. **重复签到**: 考生已经签到
3. **排期状态错误**: 排期已完成或已取消
4. **权限不足**: 非考务人员尝试签到

## 🧪 测试用例

### 1. 正常签到流程
```python
# 生成二维码
qr_code = "SCHEDULE_123_1640995200_a1b2c3d4"

# 执行签到
response = requests.post(
    f"{BASE_URL}/schedules/scan-check-in",
    json={"qr_code": qr_code}
)

# 验证结果
assert response.status_code == 200
assert response.json()["success"] == True
```

### 2. 重复签到测试
```python
# 第一次签到
response1 = requests.post(
    f"{BASE_URL}/schedules/scan-check-in",
    json={"qr_code": qr_code}
)

# 第二次签到（应该失败）
response2 = requests.post(
    f"{BASE_URL}/schedules/scan-check-in",
    json={"qr_code": qr_code}
)

assert response2.status_code == 400
```

### 3. 批量签到测试
```python
qr_codes = [
    "SCHEDULE_123_1640995200_a1b2c3d4",
    "SCHEDULE_124_1640995300_b2c3d4e5"
]

response = requests.post(
    f"{BASE_URL}/schedules/batch-scan-check-in",
    json={"qr_codes": qr_codes}
)

assert response.status_code == 200
result = response.json()
assert result["summary"]["total"] == 2
```

## 📱 二维码生成

### 二维码格式
```
SCHEDULE_{schedule_id}_{timestamp}_{hash}
```

### 生成示例
```python
import hashlib
import time

def generate_qr_code(schedule_id):
    timestamp = int(time.time())
    content = f"SCHEDULE_{schedule_id}_{timestamp}"
    hash_value = hashlib.md5(content.encode()).hexdigest()[:8]
    return f"{content}_{hash_value}"

# 生成二维码
qr_code = generate_qr_code(123)
# 输出: SCHEDULE_123_1640995200_a1b2c3d4
```

## 🔧 部署说明

### 1. 环境要求
- Python 3.8+
- FastAPI
- SQLAlchemy
- MySQL 8.0

### 2. 数据库配置
```env
DB_PORT=3307
DB_USER=root
DB_PASSWORD=a_secret_password
DB_NAME=exam_site_db_dev
```

### 3. 启动服务
```bash
# 启动数据库
docker-compose up -d db

# 运行迁移
alembic upgrade head

# 启动API服务
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## 📈 性能优化

### 1. 数据库优化
- 使用行锁防止并发冲突
- 合理设置索引
- 批量操作减少数据库交互

### 2. 缓存策略
- 缓存考生信息
- 缓存考试产品信息
- 使用Redis缓存热点数据

### 3. 监控指标
- 签到成功率
- 平均响应时间
- 并发处理能力
- 错误率统计

---

*扫码签到API已完全集成到考试系统中，支持事务安全和状态管理，确保数据一致性和操作可靠性。* 