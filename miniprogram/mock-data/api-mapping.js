// API路径到Mock数据文件的映射 - 更新为标准API路径
const apiMapping = {
  // 工作人员登录
  'POST /api/v1/auth/login': {
    success: 'auth/staff-login-success',
    failure: 'auth/staff-login-failure'
  },
  
  // 考生认证 (回退支持)
  'GET /api/v1/candidate/info/by-idcard/:id': {
    success: 'candidate/candidate-info-by-idcard'
  },
  'POST /api/v1/auth/candidate/login': {
    success: 'auth/candidate-login-success'
  },
  'GET /api/v1/auth/me': {
    success: 'auth/user-info.js'
  },
  'POST /api/v1/auth/refresh': {
    success: 'auth/token-refresh.js'
  },
  
  // 兼容旧路径 (逐步废弃)
  'POST /auth/jwt/login': {
    success: 'auth/staff-login-success.js',
    failure: 'auth/staff-login-failure.js'
  },
  'GET /auth/users/me': {
    success: 'auth/user-info.js'
  },
  
  // 微信小程序模块 - 标准路径
  'GET /api/v1/wechat/candidate/schedule': {
    success: 'candidate/exam-schedule.js'
  },
  'GET /api/v1/wechat/candidate/qrcode': {
    success: 'candidate/candidate-qrcode.js'
  },
  'GET /api/v1/wechat/venues/status': {
    success: 'realtime/venue-status.js'
  },
  'POST /api/v1/wechat/checkin': {
    success: 'qrcode/scan-checkin.js',
    failure: 'qrcode/scan-checkin-failure.js'
  },
  'POST /api/v1/wechat/manual-checkin': {
    success: 'qrcode/scan-checkin.js',
    failure: 'qrcode/scan-checkin-failure.js'
  },
  'GET /api/v1/staff/stats': {
    success: 'staff/staff-stats.js'
  },
  'GET /api/v1/staff/checkin-history': {
    success: 'staff/checkin-history.js'
  },
  
  // 工作人员扫码相关API
  'GET /api/v1/staff/today-stats': {
    success: 'staff/staff-stats.js'
  },
  'GET /api/v1/staff/scan-history': {
    success: 'staff/checkin-history.js'
  },
  
  // 二维码验证和签到API
  'POST /api/v1/qrcode/validate': {
    success: 'staff/scan-validation.js',
    failure: 'staff/scan-validation.js'
  },
  'POST /api/v1/qrcode/manual-validate': {
    success: 'staff/scan-validation.js',
    failure: 'staff/scan-validation.js'
  },
  'POST /api/v1/checkin/perform': {
    success: 'staff/checkin-operations.js',
    failure: 'staff/checkin-operations.js'
  },
  'GET /api/v1/wechat/candidate/queue-position': {
    success: 'realtime/queue-status.js'
  },
  'GET /api/v1/wechat/dashboard': {
    success: 'realtime/public-board.js'
  },
  'POST /api/v1/wechat/candidate/qrcode/refresh': {
    success: 'candidate/candidate-qrcode.js'
  },
  'GET /api/v1/wechat/candidate/checkin-history': {
    success: 'candidate/checkin-history.js'
  },
  'GET /api/v1/wechat/candidate/*/exam-results': {
    success: 'candidate/exam-results.js'
  },
  'PUT /api/v1/wechat/candidate/*/update': {
    success: 'candidate/update-candidate-info.js'
  },
  
  // 考生管理模块 - 标准路径
  'GET /api/v1/candidates/': {
    success: 'candidate/candidates-list.js'
  },
  'GET /api/v1/candidates/:id': {
    success: 'candidate/candidate-detail.js'
  },
  'GET /api/v1/candidates/statistics': {
    success: 'candidate/candidates-statistics.js'
  },
  
  // 日程管理模块 - 标准路径
  'GET /api/v1/schedules/': {
    success: 'schedule/schedules-list.js'
  },
  'POST /api/v1/schedules/:id/start': {
    success: 'schedule/schedule-start.js'
  },
  'POST /api/v1/schedules/:id/complete': {
    success: 'schedule/schedule-complete.js'
  },
  'GET /api/v1/schedules/venue/:id/today': {
    success: 'schedule/venue-today-schedules.js'
  },
  
  // 考场管理模块 - 标准路径
  'GET /api/v1/venues/': {
    success: 'venue/venues-list.js'
  },
  'GET /api/v1/venues/:id': {
    success: 'venue/venue-detail.js'
  },
  'GET /api/v1/venues/:id/current-status': {
    success: 'venue/venue-current-status.js'
  },
  
  // 兼容旧路径 (逐步废弃)
  'GET /wx-miniprogram/candidate-info': {
    success: 'candidate/candidate-info.js'
  },
  'GET /wx/candidate-info/:id': {
    success: 'candidate/candidate-detail.js'
  },
  'GET /wx-miniprogram/exam-schedule': {
    success: 'candidate/exam-schedule.js'
  },
  'GET /wx/my-qrcode/:id': {
    success: 'candidate/candidate-qrcode.js'
  },
  'GET /wx-miniprogram/checkin-history': {
    success: 'candidate/checkin-history.js'
  },
  'GET /realtime/status': {
    success: 'realtime/realtime-status.js'
  },
  'GET /realtime/public-board': {
    success: 'realtime/public-board.js'
  },
  'GET /realtime/venue-status': {
    success: 'realtime/venue-status.js'
  },
  'GET /realtime/queue-status/:id': {
    success: 'realtime/queue-status.js'
  },
  'GET /realtime/notifications': {
    success: 'realtime/notifications.js'
  }
}

// 路径匹配工具
const pathMatcher = {
  // 标准化API路径
  normalizePath(method, url) {
    // 移除查询参数
    const cleanUrl = url.split('?')[0]
    return `${method.toUpperCase()} ${cleanUrl}`
  },
  
  // 匹配API路径（支持参数路径）
  matchPath(method, url) {
    const normalizedPath = this.normalizePath(method, url)
    
    // 直接匹配
    if (apiMapping[normalizedPath]) {
      return apiMapping[normalizedPath]
    }
    
    // 参数路径匹配
    for (const [pattern, mapping] of Object.entries(apiMapping)) {
      if (this.isPatternMatch(normalizedPath, pattern)) {
        return mapping
      }
    }
    
    return null
  },
  
  // 检查路径模式匹配
  isPatternMatch(path, pattern) {
    // 将 :id 等参数和 * 通配符转换为正则表达式
    const regexPattern = pattern
      .replace(/:[^/]+/g, '[^/]+')  // :id -> [^/]+
      .replace(/\*/g, '[^/]+')      // * -> [^/]+
      .replace(/\//g, '\\/')        // / -> \/
    
    const regex = new RegExp(`^${regexPattern}$`)
    return regex.test(path)
  },
  
  // 提取路径参数
  extractParams(path, pattern) {
    const pathParts = path.split('/')
    const patternParts = pattern.split('/')
    const params = {}
    
    for (let i = 0; i < patternParts.length; i++) {
      if (patternParts[i].startsWith(':')) {
        const paramName = patternParts[i].substring(1)
        params[paramName] = pathParts[i]
      }
    }
    
    return params
  }
}

module.exports = {
  apiMapping,
  pathMatcher
}