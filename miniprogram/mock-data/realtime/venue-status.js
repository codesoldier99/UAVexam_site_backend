// 考场状态响应数据 - 返回考场数组
module.exports = {
  "success": true,
  "message": "获取考场状态成功",
  "data": [
    {
      "id": 1,
      "name": "A101考场",
      "capacity": 50,
      "checked_in_count": 48,
      "total_candidates": 50,
      "current_exam": "无人机驾驶理论考试",
      "exam_time": "2025-08-06T09:00:00.000Z",
      "next_exam_time": "2025-08-06T14:00:00.000Z",
      "status": "busy",
      "temperature": "22°C",
      "humidity": "55%",
      "venue_id": 1,
      "room_id": "A101"
    },
    {
      "id": 2,
      "name": "A102考场",
      "capacity": 45,
      "checked_in_count": 0,
      "total_candidates": 42,
      "current_exam": null,
      "exam_time": null,
      "next_exam_time": "2025-08-06T14:00:00.000Z",
      "status": "active",
      "temperature": "23°C",
      "humidity": "58%",
      "venue_id": 1,
      "room_id": "A102"
    },
    {
      "id": 3,
      "name": "B201考场",
      "capacity": 40,
      "checked_in_count": 35,
      "total_candidates": 38,
      "current_exam": "航空法规考试",
      "exam_time": "2025-08-06T10:30:00.000Z",
      "next_exam_time": null,
      "status": "busy",
      "temperature": "21°C",
      "humidity": "52%",
      "venue_id": 2,
      "room_id": "B201"
    },
    {
      "id": 4,
      "name": "B202考场",
      "capacity": 35,
      "checked_in_count": 0,
      "total_candidates": 0,
      "current_exam": null,
      "exam_time": null,
      "next_exam_time": null,
      "status": "inactive",
      "temperature": "24°C",
      "humidity": "60%",
      "venue_id": 2,
      "room_id": "B202"
    }
  ],
  "timestamp": "{{timestamp}}"
}
