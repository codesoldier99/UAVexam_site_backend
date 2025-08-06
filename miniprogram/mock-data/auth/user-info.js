// 用户信息响应数据
module.exports = {
  "success": true,
  "message": "获取用户信息成功",
  "data": {
    "id": "STAFF_" + Math.floor(Math.random() * 9000 + 1000),
    "username": "admin",
    "email": "admin@example.com",
    "role": "staff",
    "name": "系统管理员",
    "status": "active",
    "permissions": ["scan_qr", "manual_checkin", "view_dashboard", "manage_system"],
    "department": "系统管理部",
    "phone": "13900139001",
    "last_login": new Date().toISOString()
  },
  "timestamp": new Date().toISOString()
}
