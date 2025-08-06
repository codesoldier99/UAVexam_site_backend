// 考生登录成功响应数据
module.exports = {
  "success": true,
  "message": "登录成功",
  "access_token": "mock_candidate_token_" + Date.now(),
  "token_type": "Bearer",
  "expires_in": 3600,
  "candidate_info": {
    "id": "CAND_" + Math.floor(Math.random() * 9000 + 1000),
    "name": "张三",
    "id_number": "110101199001011234",
    "phone": "13800138001",
    "status": "active",
    "user_type": "candidate",
    "exam_status": "scheduled",
    "venue_name": "北京考试中心",
    "exam_date": "2025-08-10",
    "exam_time": "09:00"
  },
  "timestamp": new Date().toISOString()
}
