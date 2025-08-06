// 实时状态响应数据
module.exports = {
  "success": true,
  "message": "获取实时状态成功",
  "data": {
    "system_status": "正常",
    "current_time": "{{timestamp}}",
    "active_exams": 3,
    "total_candidates": 150,
    "checked_in_candidates": 120,
    "venues": [
      {
        "venue_id": "VENUE001",
        "venue_name": "北京考试中心",
        "status": "考试中",
        "capacity": 50,
        "current_candidates": 45,
        "checkin_rate": "90%"
      },
      {
        "venue_id": "VENUE002",
        "venue_name": "上海考试中心",
        "status": "准备中",
        "capacity": 60,
        "current_candidates": 55,
        "checkin_rate": "92%"
      }
    ],
    "schedules": [
      {
        "id": "SCH001",
        "exam_name": "无人机驾驶理论考试",
        "exam_date": "{{today}}",
        "exam_time": "09:00-11:00",
        "venue": "北京考试中心",
        "candidates_count": 45,
        "status": "in_progress"
      },
      {
        "id": "SCH002",
        "exam_name": "航空法规考试",
        "exam_date": "{{today}}",
        "exam_time": "14:00-16:00",
        "venue": "上海考试中心",
        "candidates_count": 55,
        "status": "scheduled"
      }
    ],
    "staff": [
      {
        "id": "STAFF001",
        "name": "李考官",
        "role": "主考官",
        "status": "online",
        "current_venue": "北京考试中心",
        "last_activity": "{{timestamp}}",
        "tasks_completed": 12
      },
      {
        "id": "STAFF002",
        "name": "王监考",
        "role": "监考员",
        "status": "active",
        "current_venue": "上海考试中心",
        "last_activity": "{{timestamp}}",
        "tasks_completed": 8
      }
    ],
    "exams": [
      {
        "id": "EXAM001",
        "name": "无人机驾驶理论考试",
        "venue": "北京考试中心",
        "start_time": "{{today}} 09:00:00",
        "end_time": "{{today}} 11:00:00",
        "status": "in_progress",
        "progress": 65,
        "total_candidates": 45,
        "checked_in": 43,
        "completed": 28
      },
      {
        "id": "EXAM002",
        "name": "航空法规考试",
        "venue": "上海考试中心",
        "start_time": "{{today}} 14:00:00",
        "end_time": "{{today}} 16:00:00",
        "status": "scheduled",
        "progress": 0,
        "total_candidates": 55,
        "checked_in": 0,
        "completed": 0
      }
    ],
    "alerts": [
      {
        "id": "ALERT001",
        "type": "candidate",
        "priority": "medium",
        "title": "考生迟到提醒",
        "message": "考场A101有考生迟到",
        "venue": "北京考试中心",
        "created_at": "{{timestamp}}",
        "resolved": false
      },
      {
        "id": "ALERT002",
        "type": "system",
        "priority": "low",
        "title": "设备检查",
        "message": "考场设备运行正常",
        "venue": "上海考试中心",
        "created_at": "{{timestamp}}",
        "resolved": true
      }
    ]
  },
  "timestamp": "{{timestamp}}"
}
