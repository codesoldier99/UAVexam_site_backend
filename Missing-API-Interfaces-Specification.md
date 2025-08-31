# 需要补充的4个关键API接口详细规范

## 概述

基于对小程序功能需求的深入分析，发现需要补充4个关键API接口来完善微信小程序的核心功能。以下是每个接口的详细设计规范。

---

## 🔴 **接口1: 根据身份证获取考生信息**

### **基本信息**
- **接口路径**: `GET /api/v1/wechat/candidate/info-by-idcard`
- **请求方法**: GET
- **权限要求**: 公开接口（无需认证）
- **优先级**: 🔴 **极高** - 登录功能的核心依赖

### **功能描述**
此接口用于考生在小程序中输入身份证号后，验证身份证号的有效性并获取对应的考生基本信息，是考生登录流程的第一步。

### **请求参数**
```http
GET /api/v1/wechat/candidate/info-by-idcard?id_card=110101199001011234
```

**查询参数:**
| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| id_card | string | 是 | 18位身份证号码 | 110101199001011234 |

### **响应格式**

**成功响应 (200):**
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

**失败响应 (404):**
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

**参数错误响应 (400):**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_ID_CARD",
    "message": "身份证号格式不正确",
    "details": {
      "id_card": "12345",
      "requirement": "请输入18位有效身份证号"
    }
  }
}
```

### **业务逻辑**
1. 验证身份证号格式（18位，符合身份证号规则）
2. 在考生数据库中查找匹配的记录
3. 检查考生状态（是否激活、是否有效）
4. 返回考生基本信息和考试状态
5. 记录查询日志（用于安全审计）

### **使用场景**
- 考生首次登录小程序时的身份验证
- 考生忘记登录状态后的快速身份确认
- 工作人员协助考生查询信息

---

## 🟡 **接口2: 二维码刷新接口**

### **基本信息**
- **接口路径**: `POST /api/v1/wechat/candidate/qrcode/refresh`
- **请求方法**: POST
- **权限要求**: 考生认证（需要考生JWT令牌）
- **优先级**: 🟡 **中** - 用户体验优化

### **功能描述**
当考生的动态二维码即将过期或已过期时，通过此接口生成新的二维码，确保考生能够正常进行签到操作。

### **请求参数**
```http
POST /api/v1/wechat/candidate/qrcode/refresh
Authorization: Bearer <candidate_jwt_token>
Content-Type: application/json
```

**请求体:**
```json
{
  "reason": "expired",
  "current_location": {
    "latitude": 39.9042,
    "longitude": 116.4074
  }
}
```

**参数说明:**
| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| reason | string | 否 | 刷新原因 | expired, manual, error |
| current_location | object | 否 | 当前位置信息 | 用于验证考生位置 |

### **响应格式**

**成功响应 (200):**
```json
{
  "success": true,
  "data": {
    "qrcode_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
    "qrcode_data": "candidate_123_20240115_143022_v2",
    "expires_at": "2024-01-15T15:30:22Z",
    "refresh_count": 2,
    "max_refresh_per_day": 10,
    "next_refresh_available_at": "2024-01-15T14:35:22Z"
  },
  "message": "二维码刷新成功"
}
```

**频率限制响应 (429):**
```json
{
  "success": false,
  "error": {
    "code": "REFRESH_RATE_LIMITED",
    "message": "二维码刷新过于频繁，请稍后再试",
    "details": {
      "current_count": 10,
      "max_per_day": 10,
      "reset_time": "2024-01-16T00:00:00Z",
      "next_available": "2024-01-15T15:00:00Z"
    }
  }
}
```

### **业务逻辑**
1. 验证考生身份和权限
2. 检查刷新频率限制（防止滥用）
3. 生成新的动态二维码
4. 使旧二维码失效
5. 记录刷新操作日志
6. 返回新二维码和相关信息

### **使用场景**
- 考生发现二维码已过期
- 考生误操作导致二维码显示异常
- 考生主动刷新获取最新二维码

---

## 🟢 **接口3: 考生签到历史**

### **基本信息**
- **接口路径**: `GET /api/v1/wechat/candidate/checkin-history`
- **请求方法**: GET
- **权限要求**: 考生认证（需要考生JWT令牌）
- **优先级**: 🟢 **低** - 信息查询功能

### **功能描述**
考生可以查看自己的历史签到记录，包括签到时间、考试信息、签到状态等，帮助考生了解自己的考试历程。

### **请求参数**
```http
GET /api/v1/wechat/candidate/checkin-history?page=1&size=10&date_from=2024-01-01&date_to=2024-01-31
Authorization: Bearer <candidate_jwt_token>
```

**查询参数:**
| 参数名 | 类型 | 必填 | 说明 | 默认值 |
|--------|------|------|------|--------|
| page | integer | 否 | 页码 | 1 |
| size | integer | 否 | 每页数量 | 10 |
| date_from | string | 否 | 开始日期 (YYYY-MM-DD) | 30天前 |
| date_to | string | 否 | 结束日期 (YYYY-MM-DD) | 今天 |
| status | string | 否 | 签到状态筛选 | all |

### **响应格式**

**成功响应 (200):**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "checkin_time": "2024-01-15T08:45:00Z",
        "exam_time": "2024-01-15T09:00:00Z",
        "status": "success",
        "method": "qrcode_scan",
        "venue": {
          "id": 1,
          "name": "多旋翼A号实操场",
          "location": "实训楼A区"
        },
        "exam_product": {
          "id": 1,
          "name": "多旋翼视距内驾驶员"
        },
        "staff_name": "李老师",
        "notes": "准时签到",
        "exam_result": {
          "status": "completed",
          "score": 85,
          "result": "pass"
        }
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

### **业务逻辑**
1. 验证考生身份
2. 根据查询条件筛选签到记录
3. 关联考试信息、考场信息、考试结果
4. 计算统计数据
5. 分页返回结果

### **使用场景**
- 考生查看自己的考试历史
- 考生确认某次考试的签到状态
- 考生了解自己的考试表现趋势

---

## 🟡 **接口4: 考生考试结果查询**

### **基本信息**
- **接口路径**: `GET /api/v1/wechat/candidate/exam-results`
- **请求方法**: GET
- **权限要求**: 考生认证（需要考生JWT令牌）
- **优先级**: 🟡 **中** - 核心查询功能

### **功能描述**
考生可以查询自己的考试成绩和结果，包括已完成的考试、待出成绩的考试、以及详细的成绩信息。

### **请求参数**
```http
GET /api/v1/wechat/candidate/exam-results?page=1&size=10&status=all&exam_product_id=1
Authorization: Bearer <candidate_jwt_token>
```

**查询参数:**
| 参数名 | 类型 | 必填 | 说明 | 默认值 |
|--------|------|------|------|--------|
| page | integer | 否 | 页码 | 1 |
| size | integer | 否 | 每页数量 | 10 |
| status | string | 否 | 结果状态 | all |
| exam_product_id | integer | 否 | 考试产品ID筛选 | null |
| date_from | string | 否 | 开始日期 | null |
| date_to | string | 否 | 结束日期 | null |

### **响应格式**

**成功响应 (200):**
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
        "exam_duration": 15,
        "actual_duration": 12,
        "created_at": "2024-01-15T09:15:00Z"
      },
      {
        "id": 2,    
        "exam_date": "2024-01-10T14:00:00Z",
        "exam_product": {
          "id": 2,
          "name": "多旋翼超视距驾驶员",
          "code": "MULTIROTOR_BVLOS"
        },
        "venue": {
          "id": 2,
          "name": "多旋翼B号实操场"
        },
        "status": "failed",
        "result": "fail",
        "score": 65,
        "max_score": 100,
        "pass_score": 70,
        "exam_duration": 15,
        "actual_duration": 18,
        "created_at": "2024-01-10T14:15:00Z"
      }
    ],
    "pagination": {
      "total": 2,
      "page": 1,
      "size": 10,
      "pages": 1
    },
    "summary": {
      "total_exams": 2,
      "passed_exams": 1,
      "failed_exams": 1,
      "pending_exams": 0,
      "pass_rate": 50.0,
      "average_score": 75.0
    }
  },
  "message": "考试结果获取成功"
}
```

**无结果响应 (200):**
```json
{
  "success": true,
  "data": {
    "items": [],
    "pagination": {
      "total": 0,
      "page": 1,
      "size": 10,
      "pages": 0
    },
    "summary": {
      "total_exams": 0,
      "passed_exams": 0,
      "failed_exams": 0,
      "pending_exams": 0,
      "pass_rate": 0,
      "average_score": 0,
      "certificates_earned": 0
    }
  },
  "message": "暂无考试结果"
}
```

### **业务逻辑**
1. 验证考生身份
2. 查询考生的所有考试记录
3. 关联考试产品、考场、考官信息
4. 计算统计数据和通过率
5. 处理证书信息（如果有）
6. 分页返回结果

### **使用场景**
- 考生查看考试成绩
- 考生下载电子证书
- 考生了解重考要求和时间
- 考生查看详细的评分标准

---

## 📋 **实施优先级和依赖关系**

### **实施顺序建议:**

1. **第一优先级** 🔴
   - **接口1**: 根据身份证获取考生信息
   - **原因**: 登录功能的核心依赖，必须首先实现

2. **第二优先级** 🟡
   - **接口4**: 考生考试结果查询
   - **原因**: 核心业务功能，考生关注度高

3. **第三优先级** 🟡
   - **接口2**: 二维码刷新接口
   - **原因**: 用户体验优化，提升操作便利性

4. **第四优先级** 🟢
   - **接口3**: 考生签到历史
   - **原因**: 信息查询功能，可以后续完善

### **技术依赖:**
- 所有接口都需要JWT认证机制（除接口1）
- 接口2需要二维码生成服务
- 接口3和4需要完善的数据关联查询
- 所有接口都需要统一的错误处理和日志记录

### **数据库设计考虑:**
- 考生表需要包含身份证号索引
- 签到记录表需要时间范围查询优化
- 考试结果表需要支持复杂的统计查询
- 二维码表需要过期时间和刷新次数字段

---

## 🔧 **开发和测试建议**

### **开发注意事项:**
1. **安全性**: 身份证号等敏感信息需要加密存储和传输
2. **性能**: 历史查询接口需要考虑分页和缓存策略
3. **容错性**: 二维码刷新需要防止频繁调用
4. **一致性**: 所有接口的响应格式需要保持统一

### **测试用例:**
1. **正常流程测试**: 各种正常参数的功能验证
2. **异常处理测试**: 无效参数、权限不足、数据不存在等场景
3. **性能测试**: 大量数据查询的响应时间
4. **安全测试**: SQL注入、XSS攻击等安全漏洞检查

---

*文档版本: v1.0*
*创建时间: 2024-01-01*
*最后更新: 2024-01-01*