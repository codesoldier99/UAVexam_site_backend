// 工作人员登录成功响应数据
// 注意：这个API应该直接返回token信息，而不是包装在data字段中
module.exports = {
  "access_token": "mock_staff_token_" + Date.now(),
  "token_type": "Bearer", 
  "expires_in": 3600,
  "refresh_token": "mock_refresh_token_" + Date.now(),
  "scope": "staff",
  "user_type": "staff"
}
