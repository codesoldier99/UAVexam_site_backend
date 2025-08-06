// 手动签到响应数据
module.exports = {
  "success": true,
  "message": "手动签到成功",
  "data": {
    "checkin_id": "MANUAL_CHECKIN_{{timestamp}}",
    "candidate_info": {
      "id": "{{candidate_id}}",
      "name": "张三",
      "id_number": "{{id_number}}",
      "seat_number": "A001"
    },
    "exam_info": {
      "schedule_id": "{{schedule_id}}",
      "exam_name": "无人机驾驶理论考试",
      "exam_date": "2025-08-15",
      "exam_time": "09:00-11:00",
      "venue": "北京考试中心"
    },
    "checkin_time": "{{timestamp}}",
    "checkin_method": "手动签到",
    "staff_info": {
      "id": "{{staff_id}}",
      "name": "李考官"
    },
    "notes": "考生二维码无法扫描，手动确认身份后签到"
  },
  "timestamp": "{{timestamp}}"
}