// API路径到Mock数据文件的映射
const apiMapping = {
  // 认证模块
  'POST /wx/login-by-idcard': {
    success: 'auth/candidate-login-success.js',
    failure: 'auth/candidate-login-failure.js'
  },
  'POST /auth/jwt/login': {
    success: 'auth/staff-login-success.js',
    failure: 'auth/staff-login-failure.js'
  },
  'GET /auth/users/me': {
    success: 'auth/user-info.js'
  },
  'GET /auth/user/info': {
    success: 'auth/user-info.js'
  },
  
  // 考生模块
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
  'GET /wx-miniprogram/exam-results': {
    success: 'candidate/exam-results.js'
  },
  
  // 二维码模块
  'GET /qrcode/generate-schedule-qr/:id': {
    success: 'qrcode/schedule-qr.js'
  },
  'POST /qrcode/scan-checkin': {
    success: 'qrcode/scan-checkin.js',
    failure: 'qrcode/scan-checkin-failure.js'
  },
  'GET /qrcode/checkin-status/:id': {
    success: 'qrcode/checkin-status.js'
  },
  'POST /qrcode/manual-checkin': {
    success: 'qrcode/manual-checkin.js'
  },
  
  // 实时数据模块
  'GET /realtime/status': {
    success: 'realtime/realtime-status.js'
  },
  'GET /realtime/public-board': {
    success: 'realtime/public-board.js'
  },
  'GET /realtime/venue-status': {
    success: 'realtime/venue-status.js'
  },
  'GET /realtime/system-status': {
    success: 'realtime/system-status.js'
  },
  'GET /realtime/queue-status/:id': {
    success: 'realtime/queue-status.js'
  },
  'GET /realtime/venue-queue/:id': {
    success: 'realtime/venue-queue.js'
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
    // 将 :id 等参数转换为正则表达式
    const regexPattern = pattern
      .replace(/:[^/]+/g, '[^/]+')  // :id -> [^/]+
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