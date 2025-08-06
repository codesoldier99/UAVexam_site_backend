// 考生二维码响应数据
module.exports = {
  "success": true,
  "message": "获取二维码成功",
  "data": {
    "qr_code": "{{qr_code}}",
    "qr_content": "CANDIDATE_{{user_id}}_{{timestamp}}",
    "expires_at": "{{expires_at}}",
    "refresh_interval": 30,
    "candidate_info": {
      "id": "{{user_id}}",
      "name": "张三",
      "id_number": "{{id_number}}",
      "exam_schedule": {
        "exam_name": "无人机驾驶理论考试",
        "exam_date": "2025-08-15",
        "exam_time": "09:00",
        "venue": "北京考试中心",
        "seat_number": "A001"
      }
    }
  },
  "timestamp": "{{timestamp}}"
}