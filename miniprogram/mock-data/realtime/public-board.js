// 公共看板响应数据
module.exports = {
  "success": true,
  "message": "获取公共看板数据成功",
  "data": {
    "current_time": "{{timestamp}}",
    "exam_sessions": [
      {
        "session_id": "SESSION001",
        "exam_name": "无人机驾驶理论考试",
        "exam_time": "09:00-11:00",
        "venue": "北京考试中心 A101",
        "status": "进行中",
        "total_candidates": 50,
        "checked_in": 48,
        "progress": "96%"
      },
      {
        "session_id": "SESSION002",
        "exam_name": "航空法规考试",
        "exam_time": "14:00-16:00",
        "venue": "北京考试中心 A102",
        "status": "准备中",
        "total_candidates": 45,
        "checked_in": 0,
        "progress": "0%"
      }
    ],
    "announcements": [
      {
        "id": "ANN001",
        "title": "考试注意事项",
        "content": "请考生提前30分钟到达考场，携带身份证原件",
        "priority": "high",
        "publish_time": "{{timestamp}}"
      }
    ],
    "weather": {
      "temperature": "25°C",
      "condition": "晴",
      "humidity": "60%"
    }
  },
  "timestamp": "{{timestamp}}"
}