# Mock Data Structure Design Document

## Overview
This document defines the data structure for all mock data files based on the existing API interfaces and the complete API documentation.

## API Interface Analysis

### 1. Authentication Module (authAPI)

#### 1.1 candidateLogin
- **Endpoint**: `/wx/login-by-idcard`
- **Method**: POST
- **Request**: `{ id_card: string }`
- **Response Structure**:
```json
{
  "success": true,
  "message": "登录成功",
  "data": {
    "access_token": "jwt_token_string",
    "token_type": "Bearer",
    "expires_in": 3600,
    "user_info": {
      "id": 1,
      "name": "张三",
      "id_number": "110101199001011234",
      "phone": "13800138001",
      "status": "active"
    }
  }
}
```

#### 1.2 staffLogin
- **Endpoint**: `/auth/jwt/login`
- **Method**: POST
- **Request**: `{ username: string, password: string }`
- **Response Structure**:
```json
{
  "success": true,
  "message": "登录成功",
  "data": {
    "access_token": "jwt_token_string",
    "token_type": "Bearer",
    "expires_in": 3600,
    "user_info": {
      "id": 1,
      "username": "staff001",
      "role": "examiner",
      "name": "李考官",
      "status": "active"
    }
  }
}
```

#### 1.3 getCurrentUser
- **Endpoint**: `/auth/users/me`
- **Method**: GET
- **Response Structure**:
```json
{
  "success": true,
  "message": "获取用户信息成功",
  "data": {
    "id": 1,
    "username": "staff001",
    "email": "staff001@example.com",
    "role": "examiner",
    "name": "李考官",
    "status": "active",
    "permissions": ["scan_qr", "manual_checkin", "view_dashboard"]
  }
}
```

### 2. Candidate Module (candidateAPI)

#### 2.1 getCandidateInfo
- **Endpoint**: `/wx-miniprogram/candidate-info`
- **Method**: GET
- **Query**: `?id_number={id_number}`
- **Response Structure**:
```json
{
  "success": true,
  "message": "获取考生信息成功",
  "data": {
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
}
```

#### 2.2 getCandidateDetail
- **Endpoint**: `/wx/candidate-info/{candidateId}`
- **Method**: GET
- **Response Structure**:
```json
{
  "success": true,
  "message": "获取考生详情成功",
  "data": {
    "id": 1,
    "name": "张三",
    "id_number": "110101199001011234",
    "phone": "13800138001",
    "gender": "男",
    "status": "待排期",
    "exam_product": {
      "id": 1,
      "name": "无人机驾驶员考试",
      "category": "理论+实操",
      "duration": 120
    },
    "institution": {
      "id": 1,
      "name": "北京航空培训中心",
      "contact_person": "张经理",
      "phone": "010-12345678"
    },
    "registration_date": "2025-08-01",
    "photo_url": "/images/candidates/candidate_1.jpg",
    "emergency_contact": {
      "name": "张父",
      "phone": "13900139001",
      "relationship": "父亲"
    }
  }
}
```

#### 2.3 getExamSchedule
- **Endpoint**: `/wx-miniprogram/exam-schedule`
- **Method**: GET
- **Query**: `?candidate_id={candidateId}`
- **Response Structure**:
```json
{
  "success": true,
  "message": "获取考试安排成功",
  "data": [
    {
      "id": 1,
      "exam_name": "无人机驾驶员理论考试",
      "exam_type": "理论",
      "exam_time": "2025-08-10T09:00:00",
      "end_time": "2025-08-10T11:00:00",
      "venue": "考场A101",
      "venue_id": 1,
      "status": "待签到",
      "requirements": ["身份证", "准考证"],
      "description": "无人机驾驶员资格理论考试",
      "duration": 120,
      "seat_number": "A001",
      "examiner": "李考官"
    }
  ]
}
```

#### 2.4 getCandidateQRCode
- **Endpoint**: `/wx/my-qrcode/{candidateId}`
- **Method**: GET
- **Response Structure**:
```json
{
  "success": true,
  "message": "生成二维码成功",
  "data": {
    "qr_content": "candidate_checkin_1_1733472000",
    "qr_url": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=candidate_checkin_1_1733472000",
    "expires_at": "2025-08-10T12:00:00",
    "candidate_info": {
      "id": 1,
      "name": "张三",
      "exam_name": "无人机驾驶员理论考试"
    }
  }
}
```

#### 2.5 getCheckinHistory
- **Endpoint**: `/wx-miniprogram/checkin-history`
- **Method**: GET
- **Query**: `?candidate_id={candidateId}`
- **Response Structure**:
```json
{
  "success": true,
  "message": "获取签到历史成功",
  "data": [
    {
      "id": 1,
      "exam_name": "无人机驾驶员理论考试",
      "checkin_time": "2025-08-10T08:45:00",
      "status": "success",
      "venue": "考场A101",
      "examiner": "李考官",
      "notes": "正常签到"
    }
  ]
}
```

### 3. QR Code Module (qrcodeAPI)

#### 3.1 generateScheduleQR
- **Endpoint**: `/qrcode/generate-schedule-qr/{scheduleId}`
- **Method**: GET
- **Response Structure**:
```json
{
  "success": true,
  "message": "考试安排二维码生成成功",
  "data": {
    "schedule_id": 1,
    "qr_data": {
      "type": "schedule_checkin",
      "schedule_id": 1,
      "timestamp": "2025-08-10T08:30:00",
      "valid_until": "2025-08-10T23:59:59"
    },
    "qr_url": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=schedule_checkin_1_1733472000",
    "scan_url": "/qrcode/scan/1",
    "instructions": "考生可扫描此二维码进行签到"
  }
}
```

#### 3.2 scanCheckin
- **Endpoint**: `/qrcode/scan-checkin`
- **Method**: POST
- **Request**: `{ qr_content: string, staff_id?: number }`
- **Response Structure**:
```json
{
  "success": true,
  "message": "签到成功",
  "data": {
    "schedule_id": 1,
    "candidate_id": 1,
    "candidate_name": "张三",
    "checkin_time": "2025-08-10T08:45:00",
    "status": "已签到",
    "examiner": "李考官"
  }
}
```

#### 3.3 getCheckinStatus
- **Endpoint**: `/qrcode/checkin-status/{scheduleId}`
- **Method**: GET
- **Response Structure**:
```json
{
  "success": true,
  "message": "获取签到状态成功",
  "data": {
    "schedule_id": 1,
    "total_candidates": 30,
    "checked_in": 25,
    "pending": 5,
    "checkin_rate": 83.33,
    "candidates": [
      {
        "id": 1,
        "name": "张三",
        "status": "已签到",
        "checkin_time": "2025-08-10T08:45:00"
      }
    ]
  }
}
```

#### 3.4 manualCheckin
- **Endpoint**: `/qrcode/manual-checkin`
- **Method**: POST
- **Request**: `{ candidate_id: number, schedule_id: number, staff_id: number }`
- **Response Structure**:
```json
{
  "success": true,
  "message": "手动签到成功",
  "data": {
    "checkin_id": 1,
    "candidate_id": 1,
    "candidate_name": "张三",
    "schedule_id": 1,
    "checkin_time": "2025-08-10T08:45:00",
    "method": "manual",
    "staff_id": 1,
    "staff_name": "李考官"
  }
}
```

### 4. Realtime Module (realtimeAPI)

#### 4.1 getRealtimeStatus
- **Endpoint**: `/realtime/status`
- **Method**: GET
- **Response Structure**:
```json
{
  "success": true,
  "message": "获取实时状态成功",
  "data": {
    "system_status": "healthy",
    "active_sessions": 156,
    "total_candidates": 300,
    "checked_in_today": 245,
    "active_exams": 8,
    "server_load": 65.5,
    "last_updated": "2025-08-10T09:15:00"
  }
}
```

#### 4.2 getPublicBoard
- **Endpoint**: `/realtime/public-board`
- **Method**: GET
- **Response Structure**:
```json
{
  "success": true,
  "message": "获取公共看板数据成功",
  "data": {
    "stats": {
      "total_candidates": 300,
      "checked_in": 245,
      "active_staff": 12,
      "active_venues": 6
    },
    "venues": [
      {
        "id": 1,
        "name": "考场A101",
        "status": "active",
        "capacity": 30,
        "checked_in": 28,
        "exam_name": "无人机驾驶员理论考试"
      }
    ],
    "recent_activities": [
      {
        "time": "2025-08-10T09:15:00",
        "type": "checkin",
        "message": "张三 签到成功 - 考场A101"
      }
    ]
  }
}
```

#### 4.3 getVenueStatus
- **Endpoint**: `/realtime/venue-status`
- **Method**: GET
- **Query**: `?venue_id={venueId}` (optional)
- **Response Structure**:
```json
{
  "success": true,
  "message": "获取考场状态成功",
  "data": [
    {
      "id": 1,
      "name": "考场A101",
      "status": "active",
      "capacity": 30,
      "checked_in": 28,
      "pending": 2,
      "exam_name": "无人机驾驶员理论考试",
      "start_time": "2025-08-10T09:00:00",
      "end_time": "2025-08-10T11:00:00",
      "examiner": "李考官",
      "progress": 85.5
    }
  ]
}
```

#### 4.4 getSystemStatus
- **Endpoint**: `/realtime/system-status`
- **Method**: GET
- **Response Structure**:
```json
{
  "success": true,
  "message": "获取系统状态成功",
  "data": {
    "server_status": "healthy",
    "database_status": "healthy",
    "api_response_time": 120,
    "active_connections": 156,
    "memory_usage": 65.5,
    "cpu_usage": 45.2,
    "disk_usage": 78.9,
    "last_backup": "2025-08-10T02:00:00"
  }
}
```

#### 4.5 getQueueStatus
- **Endpoint**: `/realtime/queue-status/{candidateId}`
- **Method**: GET
- **Response Structure**:
```json
{
  "success": true,
  "message": "获取排队状态成功",
  "data": {
    "candidate_id": 1,
    "queue_position": 3,
    "estimated_wait_time": 15,
    "venue": "考场A101",
    "exam_name": "无人机驾驶员理论考试",
    "status": "waiting",
    "alerts": [
      {
        "type": "info",
        "message": "请准备身份证和准考证",
        "time": "2025-08-10T08:30:00"
      }
    ]
  }
}
```

#### 4.6 getVenueQueue
- **Endpoint**: `/realtime/venue-queue/{venueId}`
- **Method**: GET
- **Response Structure**:
```json
{
  "success": true,
  "message": "获取考场队列成功",
  "data": {
    "venue_id": 1,
    "venue_name": "考场A101",
    "queue_length": 5,
    "average_wait_time": 12,
    "candidates": [
      {
        "id": 1,
        "name": "张三",
        "position": 1,
        "wait_time": 5,
        "status": "waiting"
      }
    ]
  }
}
```

#### 4.7 getNotifications
- **Endpoint**: `/realtime/notifications`
- **Method**: GET
- **Query**: `?candidate_id={candidateId}&venue_id={venueId}` (optional)
- **Response Structure**:
```json
{
  "success": true,
  "message": "获取通知成功",
  "data": [
    {
      "id": 1,
      "type": "info",
      "title": "考试提醒",
      "message": "您的考试将在30分钟后开始，请提前到达考场",
      "time": "2025-08-10T08:30:00",
      "read": false,
      "priority": "high"
    }
  ]
}
```

## Data File Structure Plan

Based on the above analysis, the mock data files will be organized as follows:

```
mock-data/
├── auth/
│   ├── candidate-login-success.json
│   ├── candidate-login-failure.json
│   ├── staff-login-success.json
│   ├── staff-login-failure.json
│   └── user-info.json
├── candidate/
│   ├── candidate-info.json
│   ├── candidate-detail.json
│   ├── exam-schedule.json
│   ├── qrcode-data.json
│   └── checkin-history.json
├── qrcode/
│   ├── generate-qr-success.json
│   ├── scan-checkin-success.json
│   ├── scan-checkin-failure.json
│   ├── checkin-status.json
│   └── manual-checkin.json
├── realtime/
│   ├── realtime-status.json
│   ├── public-board.json
│   ├── venue-status.json
│   ├── system-status.json
│   ├── queue-status.json
│   ├── venue-queue.json
│   └── notifications.json
├── institution/
│   └── institutions.json
├── exam/
│   ├── exam-products.json
│   └── venues.json
└── schedule/
    ├── schedules.json
    └── enhanced-schedules.json
```

## Error Response Structure

All APIs will follow a consistent error response format:

```json
{
  "success": false,
  "message": "错误描述",
  "error_code": "ERROR_CODE",
  "data": null,
  "timestamp": "2025-08-10T09:15:00"
}
```

## Next Steps

1. Create the mock-data directory structure
2. Generate JSON files with sample data for each interface
3. Implement data-loader.js utility
4. Create mock-api.js wrapper
5. Update api.js to support mock data mode

This completes Phase 1: Data Structure Design. The next phase will involve creating the actual mock data files based on this structure.