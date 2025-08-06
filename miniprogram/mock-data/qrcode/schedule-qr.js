// 考试排期二维码响应数据
module.exports = {
  "success": true,
  "message": "生成二维码成功",
  "data": {
    "qr_code": "{{qr_code}}",
    "qr_content": "SCHEDULE_{{schedule_id}}_{{timestamp}}",
    "schedule_id": "{{schedule_id}}",
    "expires_at": "{{expires_at}}",
    "schedule_info": {
      "exam_name": "无人机驾驶理论考试",
      "exam_date": "2025-08-15",
      "exam_time": "09:00-11:00",
      "venue": "北京考试中心",
      "room": "A101"
    }
  },
  "timestamp": "{{timestamp}}"
}