// 考生签到历史响应数据
module.exports = {
  "success": true,
  "message": "获取签到历史成功",
  "data": [
    {
      "checkin_id": "CHECKIN001",
      "exam_name": "航空法规考试",
      "exam_date": "2025-07-20",
      "checkin_time": "2025-07-20T08:30:00",
      "checkin_method": "二维码扫描",
      "venue": "北京考试中心",
      "staff_name": "李考官",
      "status": "已签到"
    },
    {
      "checkin_id": "CHECKIN002",
      "exam_name": "无人机驾驶理论考试",
      "exam_date": "2025-08-15",
      "checkin_time": null,
      "checkin_method": null,
      "venue": "北京考试中心",
      "staff_name": null,
      "status": "未签到"
    }
  ],
  "timestamp": "{{timestamp}}"
}