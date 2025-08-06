// 考场队列响应数据
module.exports = {
  "success": true,
  "message": "获取考场队列成功",
  "data": {
    "venue_id": "{{venue_id}}",
    "venue_name": "北京考试中心",
    "current_time": "{{timestamp}}",
    "queue_summary": {
      "total_in_queue": 15,
      "average_wait_time": "12分钟",
      "processing_rate": "4人/小时"
    },
    "queue_list": [
      {
        "position": 1,
        "candidate_id": "CAND001",
        "candidate_name": "张三",
        "seat_number": "A001",
        "estimated_time": "2分钟",
        "status": "等待中"
      },
      {
        "position": 2,
        "candidate_id": "CAND002",
        "candidate_name": "李四",
        "seat_number": "A002",
        "estimated_time": "5分钟",
        "status": "等待中"
      },
      {
        "position": 3,
        "candidate_id": "CAND003",
        "candidate_name": "王五",
        "seat_number": "A003",
        "estimated_time": "8分钟",
        "status": "等待中"
      }
    ],
    "currently_serving": {
      "candidate_name": "赵六",
      "seat_number": "A000",
      "start_time": "2025-08-15T08:45:00",
      "estimated_completion": "2025-08-15T08:50:00"
    }
  },
  "timestamp": "{{timestamp}}"
}