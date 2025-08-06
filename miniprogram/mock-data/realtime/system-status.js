// 系统状态响应数据
module.exports = {
  "success": true,
  "message": "获取系统状态成功",
  "data": {
    "system_health": "正常",
    "current_time": "{{timestamp}}",
    "uptime": "99.9%",
    "services": [
      {
        "service_name": "认证服务",
        "status": "正常",
        "response_time": "120ms",
        "last_check": "{{timestamp}}"
      },
      {
        "service_name": "数据库服务",
        "status": "正常",
        "response_time": "50ms",
        "last_check": "{{timestamp}}"
      },
      {
        "service_name": "二维码服务",
        "status": "正常",
        "response_time": "80ms",
        "last_check": "{{timestamp}}"
      }
    ],
    "statistics": {
      "total_users": 1250,
      "active_sessions": 156,
      "api_calls_today": 8520,
      "error_rate": "0.1%"
    },
    "alerts": [
      {
        "level": "info",
        "message": "系统运行正常",
        "time": "{{timestamp}}"
      }
    ]
  },
  "timestamp": "{{timestamp}}"
}