// 考生信息响应数据
module.exports = {
  "success": true,
  "message": "获取考生信息成功",
  "data": {
    "id": "{{user_id}}",
    "name": "张三",
    "id_number": "{{id_number}}",
    "phone": "13800138001",
    "email": "zhangsan@example.com",
    "status": "active",
    "registration_date": "2025-07-15",
    "exam_info": {
      "exam_type": "无人机驾驶理论考试",
      "exam_date": "2025-08-15",
      "exam_time": "09:00",
      "venue": "北京考试中心",
      "seat_number": "A001"
    },
    "documents": {
      "id_card_verified": true,
      "photo_verified": true,
      "medical_certificate": true
    }
  },
  "timestamp": "{{timestamp}}"
}