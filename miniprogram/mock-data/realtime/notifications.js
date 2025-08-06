// 实时通知响应数据
module.exports = {
  "success": true,
  "message": "获取实时通知成功",
  "data": {
    "notifications": [
      {
        "id": "NOTIF001",
        "type": "exam_start",
        "title": "考试开始通知",
        "message": "无人机驾驶理论考试即将开始，请考生准备入场",
        "priority": "high",
        "venue_id": "VENUE001",
        "venue_name": "北京考试中心",
        "created_at": "{{timestamp}}",
        "read": false
      },
      {
        "id": "NOTIF002",
        "type": "checkin_reminder",
        "title": "签到提醒",
        "message": "请在考试开始前30分钟完成签到",
        "priority": "medium",
        "venue_id": "VENUE001",
        "venue_name": "北京考试中心",
        "created_at": "{{timestamp}}",
        "read": false
      },
      {
        "id": "NOTIF003",
        "type": "schedule_update",
        "title": "考试安排更新",
        "message": "您的考试时间已调整为14:00-16:00",
        "priority": "high",
        "venue_id": "VENUE002",
        "venue_name": "上海考试中心",
        "created_at": "{{timestamp}}",
        "read": true
      },
      {
        "id": "NOTIF004",
        "type": "checkin",
        "title": "考生签到",
        "message": "考生张三已完成签到",
        "priority": "low",
        "venue_id": "VENUE001",
        "venue_name": "北京考试中心",
        "created_at": "{{timestamp}}",
        "read": false
      },
      {
        "id": "NOTIF005",
        "type": "staff_login",
        "title": "工作人员登录",
        "message": "监考员李老师已登录系统",
        "priority": "low",
        "venue_id": "VENUE002",
        "venue_name": "上海考试中心",
        "created_at": "{{timestamp}}",
        "read": false
      }
    ]
  },
  "timestamp": "{{timestamp}}"
}
