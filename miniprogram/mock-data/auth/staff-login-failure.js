// 工作人员登录失败响应
module.exports = {
  success: false,
  message: "登录失败，用户名或密码错误",
  error_code: "LOGIN_FAILED",
  data: null,
  timestamp: "{{timestamp}}",
  details: {
    error_type: "authentication_error",
    retry_allowed: true,
    max_attempts: 5,
    lockout_duration: 300 // 5分钟锁定
  }
}