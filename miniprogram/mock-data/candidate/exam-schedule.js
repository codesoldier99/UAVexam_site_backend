// 考生考试安排响应数据
module.exports = {
  "success": true,
  "message": "获取考试安排成功",
  "data": [
    {
      "id": "SCH001",
      "schedule_id": "SCH001",
      "exam_id": "EXAM001",
      "exam_name": "无人机驾驶理论考试",
      "examName": "无人机驾驶理论考试",
      "exam_type": "理论考试",
      "examType": "理论考试",
      "exam_date": "2025-08-15",
      "exam_time": "2025-08-15T09:00:00.000Z",
      "startTime": "2025-08-15T09:00:00.000Z",
      "endTime": "2025-08-15T11:00:00.000Z",
      "end_time": "2025-08-15T11:00:00.000Z",
      "venue": "北京考试中心 A101",
      "location": "北京考试中心 A101",
      "venue_info": {
        "id": "VENUE001",
        "name": "北京考试中心",
        "address": "北京市朝阳区xxx路xxx号",
        "room": "A101",
        "seat_number": "A001"
      },
      "status": "confirmed",
      "checkin_time": null,
      "checkin_status": "未签到",
      "duration": 120,
      "total_marks": 100,
      "totalMarks": 100,
      "description": "无人机驾驶员理论知识考试，包含航空法规、飞行原理、气象知识等内容",
      "requirements": [
        "携带身份证原件",
        "提前30分钟到达考场",
        "禁止携带电子设备"
      ]
    },
    {
      "id": "SCH002",
      "schedule_id": "SCH002",
      "exam_id": "EXAM002",
      "exam_name": "无人机驾驶实操考试",
      "examName": "无人机驾驶实操考试",
      "exam_type": "实操考试",
      "examType": "实操考试",
      "exam_date": "2025-08-20",
      "exam_time": "2025-08-20T14:00:00.000Z",
      "startTime": "2025-08-20T14:00:00.000Z",
      "endTime": "2025-08-20T17:00:00.000Z",
      "end_time": "2025-08-20T17:00:00.000Z",
      "venue": "北京考试中心 实操场地",
      "location": "北京考试中心 实操场地",
      "venue_info": {
        "id": "VENUE002",
        "name": "北京考试中心",
        "address": "北京市朝阳区xxx路xxx号",
        "room": "实操场地",
        "seat_number": "B001"
      },
      "status": "待签到",
      "checkin_time": null,
      "checkin_status": "未签到",
      "duration": 180,
      "total_marks": 100,
      "totalMarks": 100,
      "description": "无人机驾驶员实际操作考试，包含起飞、悬停、降落等基本操作",
      "requirements": [
        "携带身份证原件",
        "提前30分钟到达考场",
        "穿着合适的服装"
      ]
    },
    {
      "id": "SCH003",
      "schedule_id": "SCH003",
      "exam_id": "EXAM003",
      "exam_name": "航空法规考试",
      "examName": "航空法规考试",
      "exam_type": "理论考试",
      "examType": "理论考试",
      "exam_date": "2025-07-25",
      "exam_time": "2025-07-25T10:00:00.000Z",
      "startTime": "2025-07-25T10:00:00.000Z",
      "endTime": "2025-07-25T12:00:00.000Z",
      "end_time": "2025-07-25T12:00:00.000Z",
      "venue": "北京考试中心 B201",
      "location": "北京考试中心 B201",
      "venue_info": {
        "id": "VENUE003",
        "name": "北京考试中心",
        "address": "北京市朝阳区xxx路xxx号",
        "room": "B201",
        "seat_number": "C001"
      },
      "status": "已完成",
      "checkin_time": "2025-07-25T09:30:00.000Z",
      "checkin_status": "已签到",
      "duration": 120,
      "total_marks": 100,
      "totalMarks": 100,
      "score": 88,
      "grade": "优秀",
      "description": "航空法规相关知识考试，涵盖民航法规、飞行安全等内容",
      "requirements": [
        "携带身份证原件",
        "提前30分钟到达考场",
        "禁止携带电子设备"
      ]
    }
  ],
  "timestamp": "{{timestamp}}"
}
