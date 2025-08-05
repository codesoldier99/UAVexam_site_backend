// API 工具函数
const app = getApp()

// 导入性能优化工具
const { cache } = require('./cache')
const { loading } = require('./loading')
const { perf } = require('./performance')

// API基础配置
const API_CONFIG = {
  baseURL: 'http://10.20.175.146:8000',
  timeout: 10000,
  retryCount: 3,
  retryDelay: 1000
}

// Token管理
const TokenManager = {
  // 获取存储的token
  getToken() {
    return wx.getStorageSync('access_token') || ''
  },
  
  // 存储token
  setToken(token) {
    wx.setStorageSync('access_token', token)
  },
  
  // 清除token
  clearToken() {
    wx.removeStorageSync('access_token')
  },
  
  // 检查token是否存在
  hasToken() {
    return !!this.getToken()
  }
}

// 增强的通用请求函数
function request(url, options = {}) {
  return new Promise(async (resolve, reject) => {
    const { 
      method = 'GET', 
      data = {}, 
      header = {}, 
      needAuth = true, 
      showLoading = true, 
      retryCount = 0,
      useCache = false,
      cacheLevel = 'short',
      loadingTitle = '加载中...'
    } = options

    // 生成缓存键
    const cacheKey = useCache ? `${method}_${url}_${JSON.stringify(data)}` : null
    
    // 尝试从缓存获取数据
    if (useCache && cacheKey) {
      const cachedData = cache.get('api', cacheKey)
      if (cachedData) {
        console.log('从缓存获取数据:', url)
        resolve(cachedData)
        return
      }
    }

    // 开始性能监控
    const perfId = perf.start(`api_${url.replace(/[^a-zA-Z0-9]/g, '_')}`, 'api')
    const startTime = Date.now()
    
    // 显示加载提示
    let loadingPromise = null
    if (showLoading) {
      loadingPromise = loading.show(loadingTitle, true)
    }

    // 构建请求头
    const requestHeader = {
      'Content-Type': 'application/json',
      ...header
    }

    // 添加认证token
    if (needAuth && TokenManager.hasToken()) {
      requestHeader['Authorization'] = `Bearer ${TokenManager.getToken()}`
    }

    wx.request({
      url: `${API_CONFIG.baseURL}${url}`,
      method,
      data,
      header: requestHeader,
      timeout: API_CONFIG.timeout,
      success: (res) => {
        const duration = Date.now() - startTime
        
        // 隐藏加载提示
        if (showLoading) {
          loading.hide()
        }
        
        // 记录API性能
        perf.recordAPI(url, method, duration, res.statusCode, JSON.stringify(res.data).length)
        perf.end(perfId, { statusCode: res.statusCode, dataSize: JSON.stringify(res.data).length })
        
        if (res.statusCode === 200) {
          // 缓存成功响应
          if (useCache && cacheKey && method === 'GET') {
            cache.set('api', cacheKey, res.data, { level: cacheLevel })
          }
          
          resolve(res.data)
        } else if (res.statusCode === 401) {
          // Token过期处理
          TokenManager.clearToken()
          loading.error('登录已过期，请重新登录')
          
          setTimeout(() => {
            wx.reLaunch({
              url: '/pages/index/index'
            })
          }, 1500)
          
          const error = new Error('登录已过期')
          perf.recordError(error, { url, method, statusCode: res.statusCode })
          reject(error)
        } else {
          console.error('API请求失败:', res)
          const error = new Error(res.data?.message || `请求失败: ${res.statusCode}`)
          perf.recordError(error, { url, method, statusCode: res.statusCode })
          reject(error)
        }
      },
      fail: (err) => {
        const duration = Date.now() - startTime
        
        // 隐藏加载提示
        if (showLoading) {
          loading.hide()
        }
        
        console.error('网络请求失败:', err)
        
        // 记录失败的API性能
        perf.recordAPI(url, method, duration, 0, 0)
        perf.end(perfId, { error: err.errMsg })
        perf.recordError(err, { url, method })
        
        // 重试机制
        if (retryCount < API_CONFIG.retryCount) {
          setTimeout(() => {
            request(url, { ...options, retryCount: retryCount + 1 })
              .then(resolve)
              .catch(reject)
          }, API_CONFIG.retryDelay * (retryCount + 1)) // 递增延迟
        } else {
          const error = new Error('网络请求失败，请检查网络连接')
          reject(error)
        }
      }
    })
  })
}

// 认证相关API
const authAPI = {
  // 考生身份证登录
  candidateLogin(idNumber) {
    return request('/wx/login-by-idcard', {
      method: 'POST',
      data: { id_card: idNumber },
      needAuth: false
    })
  },
  
  // 工作人员登录
  staffLogin(username, password) {
    return request('/auth/jwt/login', {
      method: 'POST',
      data: { username, password },
      needAuth: false
    })
  },
  
  // 获取当前用户信息
  getCurrentUser() {
    return request('/auth/users/me')
  }
}

// 考生相关API
const candidateAPI = {
  // 根据身份证号获取考生信息
  getCandidateInfo(idNumber) {
    return request(`/wx-miniprogram/candidate-info?id_number=${idNumber}`, {
      needAuth: false,
      useCache: true,
      cacheLevel: 'medium'
    })
  },
  
  // 获取考生详细信息
  getCandidateDetail(candidateId) {
    return request(`/wx/candidate-info/${candidateId}`, {
      useCache: true,
      cacheLevel: 'medium'
    })
  },
  
  // 获取考生考试安排
  getExamSchedule(candidateId) {
    return request(`/wx-miniprogram/exam-schedule?candidate_id=${candidateId}`, {
      useCache: true,
      cacheLevel: 'short'
    })
  },
  
  // 获取考生动态二维码
  getCandidateQRCode(candidateId) {
    return request(`/wx/my-qrcode/${candidateId}`, {
      useCache: false // 二维码需要实时生成
    })
  },
  
  // 获取考生签到历史
  getCheckinHistory(candidateId) {
    return request(`/wx-miniprogram/checkin-history?candidate_id=${candidateId}`, {
      useCache: true,
      cacheLevel: 'short'
    })
  }
}

// 二维码相关API
const qrcodeAPI = {
  // 生成考试二维码
  generateScheduleQR(scheduleId) {
    return request(`/qrcode/generate-schedule-qr/${scheduleId}`)
  },
  
  // 扫码签到
  scanCheckin(qrContent, staffId) {
    return request('/qrcode/scan-checkin', {
      method: 'POST',
      data: {
        qr_content: qrContent,
        staff_id: staffId
      }
    })
  },
  
  // 获取签到状态
  getCheckinStatus(scheduleId) {
    return request(`/qrcode/checkin-status/${scheduleId}`)
  },
  
  // 手动签到
  manualCheckin(candidateId, scheduleId, staffId) {
    return request('/qrcode/manual-checkin', {
      method: 'POST',
      data: {
        candidate_id: candidateId,
        schedule_id: scheduleId,
        staff_id: staffId
      }
    })
  }
}

// 实时状态API
const realtimeAPI = {
  // 获取实时状态
  getRealtimeStatus() {
    return request('/realtime/status')
  },
  
  // 获取公共看板数据
  getPublicBoard() {
    return request('/realtime/public-board')
  },
  
  // 获取考场状态
  getVenueStatus(venueId) {
    if (venueId) {
      return request(`/realtime/venue-status?venue_id=${venueId}`)
    }
    return request('/realtime/venue-status')
  },
  
  // 获取系统状态
  getSystemStatus() {
    return request('/realtime/system-status')
  },
  
  // 获取排队状态
  getQueueStatus(candidateId) {
    return request(`/realtime/queue-status/${candidateId}`)
  },
  
  // 获取考场队列
  getVenueQueue(venueId) {
    return request(`/realtime/venue-queue/${venueId}`)
  },
  
  // 获取实时通知
  getNotifications(candidateId, venueId) {
    const params = new URLSearchParams()
    if (candidateId) params.append('candidate_id', candidateId)
    if (venueId) params.append('venue_id', venueId)
    
    const queryString = params.toString()
    return request(`/realtime/notifications${queryString ? '?' + queryString : ''}`)
  }
}

// 机构相关API
const institutionAPI = {
  // 获取机构列表
  getInstitutions(page = 1, size = 10) {
    return request(`/institutions?page=${page}&size=${size}`)
  },
  
  // 获取机构详情
  getInstitutionDetail(institutionId) {
    return request(`/institutions/${institutionId}`)
  }
}

// 考试产品API
const examProductAPI = {
  // 获取考试产品列表
  getExamProducts(page = 1, size = 10) {
    return request(`/exam-products?page=${page}&size=${size}`)
  },
  
  // 获取考试产品详情
  getExamProductDetail(productId) {
    return request(`/exam-products/${productId}`)
  }
}

// 场地相关API
const venueAPI = {
  // 获取场地列表
  getVenues(page = 1, size = 10) {
    return request(`/venues?page=${page}&size=${size}`)
  },
  
  // 获取场地详情
  getVenueDetail(venueId) {
    return request(`/venues/${venueId}`)
  }
}

// 排期相关API
const scheduleAPI = {
  // 获取排期列表
  getSchedules(page = 1, size = 10) {
    return request(`/schedules?page=${page}&size=${size}`)
  },
  
  // 获取增强版排期
  getEnhancedSchedules(page = 1, size = 10) {
    return request(`/schedule-enhanced?page=${page}&size=${size}`)
  }
}

// 工具函数
const utils = {
  // 身份证号格式验证
  validateIdNumber(idNumber) {
    if (!idNumber || idNumber.length !== 18) {
      return false
    }
    
    // 简单的身份证号格式验证
    const reg = /^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$/
    return reg.test(idNumber)
  },
  
  // 显示错误提示
  showError(message) {
    wx.showToast({
      title: message,
      icon: 'none',
      duration: 2000
    })
  },
  
  // 显示成功提示
  showSuccess(message) {
    wx.showToast({
      title: message,
      icon: 'success',
      duration: 2000
    })
  },
  
  // 格式化时间
  formatTime(dateString) {
    const date = new Date(dateString)
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const hour = String(date.getHours()).padStart(2, '0')
    const minute = String(date.getMinutes()).padStart(2, '0')
    
    return `${year}-${month}-${day} ${hour}:${minute}`
  },
  
  // 格式化日期
  formatDate(dateString) {
    const date = new Date(dateString)
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    
    return `${year}-${month}-${day}`
  },
  
  // 处理API错误
  handleError(error, defaultMessage = '操作失败') {
    console.error('API Error:', error)
    const message = error.message || defaultMessage
    this.showError(message)
    return Promise.reject(error)
  },
  
  // 检查网络状态
  checkNetworkStatus() {
    return new Promise((resolve) => {
      wx.getNetworkType({
        success: (res) => {
          resolve(res.networkType !== 'none')
        },
        fail: () => {
          resolve(false)
        }
      })
    })
  }
}

module.exports = {
  request,
  TokenManager,
  authAPI,
  candidateAPI,
  qrcodeAPI,
  realtimeAPI,
  institutionAPI,
  examProductAPI,
  venueAPI,
  scheduleAPI,
  utils
}