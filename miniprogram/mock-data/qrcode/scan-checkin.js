// 扫码签到响应数据
module.exports = {
  "success": true,
  "message": "签到成功",
  "data": {
    "checkin_id": "CHECKIN_{{timestamp}}",
    "candidate_info": {
      "id": "{{user_id}}",
      "name": "张三",
      "id_number": "{{id_number}}",
      "seat_number": "A001"
    },
    "exam_info": {
      "exam_name": "无人机驾驶理论考试",
      "exam_date": "2025-08-15",
      "exam_time": "09:00-11:00",
      "venue": "北京考试中心"
    },
    "checkin_time": "{{timestamp}}",
    "staff_info": {
      "id": "{{staff_id}}",
      "name": "李考官"
    }
  },
  "timestamp": "{{timestamp}}"
}