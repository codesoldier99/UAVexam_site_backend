// 考生考试安排响应数据
module.exports = {
  "success": true,
  "message": "获取考试安排成功",
  "data": [
    {
      "schedule_id": "SCH001",
      "exam_id": "EXAM001",
      "exam_name": "无人机驾驶理论考试",
      "exam_date": "2025-08-15",
      "exam_time": "09:00-11:00",
      "venue": {
        "id": "VENUE001",
        "name": "北京考试中心",
        "address": "北京市朝阳区xxx路xxx号",
        "room": "A101",
        "seat_number": "A001"
      },
      "status": "confirmed",
      "checkin_time": null,
      "checkin_status": "未签到",
      "requirements": [
        "携带身份证原件",
        "提前30分钟到达考场",
        "禁止携带电子设备"
      ]
    }
  ],
  "timestamp": "{{timestamp}}"
}