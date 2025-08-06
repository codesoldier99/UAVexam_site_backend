// 签到状态响应数据
module.exports = {
  "success": true,
  "message": "获取签到状态成功",
  "data": {
    "schedule_id": "{{schedule_id}}",
    "total_candidates": 50,
    "checked_in": 35,
    "not_checked_in": 15,
    "checkin_rate": "70%",
    "exam_info": {
      "exam_name": "无人机驾驶理论考试",
      "exam_date": "2025-08-15",
      "exam_time": "09:00-11:00",
      "venue": "北京考试中心"
    },
    "recent_checkins": [
      {
        "candidate_name": "张三",
        "checkin_time": "2025-08-15T08:30:00",
        "seat_number": "A001"
      },
      {
        "candidate_name": "李四",
        "checkin_time": "2025-08-15T08:32:00",
        "seat_number": "A002"
      }
    ]
  },
  "timestamp": "{{timestamp}}"
}