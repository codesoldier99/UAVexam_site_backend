// 排队状态响应数据
module.exports = {
  "success": true,
  "message": "获取排队状态成功",
  "data": {
    "candidate_id": "{{candidate_id}}",
    "queue_position": 5,
    "estimated_wait_time": "15分钟",
    "queue_info": {
      "total_in_queue": 12,
      "processing_rate": "3人/小时",
      "current_serving": "A001"
    },
    "exam_info": {
      "exam_name": "无人机驾驶理论考试",
      "exam_time": "09:00-11:00",
      "venue": "北京考试中心",
      "room": "A101"
    },
    "status_updates": [
      {
        "time": "{{timestamp}}",
        "message": "您当前排在第5位，预计等待15分钟"
      },
      {
        "time": "2025-08-15T08:45:00",
        "message": "队伍前进，您现在排在第5位"
      }
    ]
  },
  "timestamp": "{{timestamp}}"
}