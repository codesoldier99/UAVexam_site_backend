// 考生登录成功Mock数据 - 临时回退用
module.exports = {
  success: true,
  message: '登录成功',
  data: {
    access_token: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.{{token_suffix}}',
    token_type: 'bearer',
    expires_in: 3600,
    user: {
      id: 1,
      username: 'candidate_001',
      real_name: '张三',
      role: 'candidate'
    }
  },
  timestamp: '{{timestamp}}'
}