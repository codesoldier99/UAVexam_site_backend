// API 工具函数
const app = getApp()

// 导入性能优化工具
const { cache } = require('./cache')
const { loading } = require('./loading')
const { perf } = require('./performance')

// 导入Mock数据管理器
const mockManager = require('../mock-data/index.js')

// API基础配置
const API_CONFIG = {
  baseURL: 'http://127.0.0.1:8000', // 本地开发环境：需在微信开发者工具中关闭域名校验
  timeout: 10000, // 增加超时时间，给后端API更多响应时间
  retryCount: 2, // 增加重试次数
  retryDelay: 1000,
  // 开发环境配置
  enableMockFallback: false // 禁用Mock回退机制，直接使用真实API
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

// 增强的通用请求函数 - 集成Mock数据支持
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

    // 🔥 Mock数据集成 - 只在明确启用时才检查Mock数据
    if (API_CONFIG.enableMockFallback) {
      try {
        const mockResponse = await mockManager.getMockResponse(url, method, data, {
          needAuth,
          userId: TokenManager.hasToken() ? 'current_user' : null
        })
        
        if (mockResponse) {
          console.log(`[Mock API] ${method} ${url}`, mockResponse)
          
          // 模拟加载过程
          if (showLoading) {
            loading.show(loadingTitle, true)
            // 等待Mock延迟
            await new Promise(resolve => setTimeout(resolve, 100))
            loading.hide()
          }
          
          // 处理Mock认证逻辑
          if (mockResponse.data && mockResponse.data.access_token) {
            TokenManager.setToken(mockResponse.data.access_token)
          }
          
          resolve(mockResponse)
          return
        }
      } catch (mockError) {
        console.warn('Mock data error, falling back to real API:', mockError)
      }
    }

    // 🌐 真实API调用逻辑
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
      success: async (res) => {
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
          // Token过期处理 - 避免重复弹框
          console.warn('API认证失败，需要重新登录')
          console.warn('401错误详情:', { url, method, statusCode: res.statusCode, data: res.data })
          
          // 清除token
          console.warn('清除token，原因：401错误')
          TokenManager.clearToken()
          
          // 检查是否已经在处理401错误，避免重复弹框
          if (!global._handling401) {
            global._handling401 = true
            console.warn('开始处理401错误，显示登录过期弹框')
            
            wx.showModal({
              title: '登录已过期',
              content: '请重新登录',
              showCancel: false,
              success: () => {
                console.warn('用户确认登录过期，清除所有本地存储')
                // 清除所有本地存储的登录信息
                wx.removeStorageSync('userType')
                wx.removeStorageSync('candidateInfo')
                wx.removeStorageSync('candidateId')
                
                // 跳转到首页
                wx.reLaunch({
                  url: '/pages/index/index'
                })
                
                // 重置处理标志
                setTimeout(() => {
                  global._handling401 = false
                }, 1000)
              }
            })
          }
          
          const error = new Error('登录已过期，请重新登录')
          perf.recordError(error, { url, method, statusCode: res.statusCode })
          reject(error)
        } else {
          console.error('API请求失败:', res)
          console.error('错误详情:', res.data)
          const errorMessage = res.data?.message || res.data?.detail || `请求失败: ${res.statusCode}`
          const error = new Error(errorMessage)
          perf.recordError(error, { url, method, statusCode: res.statusCode })
          reject(error)
        }
      },
      fail: async (err) => {
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
        
        // 不使用Mock回退，直接报告网络错误
        console.error('真实API连接失败:', err)
        
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
  // 考生身份证登录 (修改为通用登录接口)
  candidateLogin(idCard, openid = null) {
    // 生成考生用户名和密码
    const username = `candidate_${idCard.slice(-6)}`
    const password = idCard.slice(-6)
    
    return request('/api/v1/auth/login', {
      method: 'POST',
      data: { 
        username: username,
        password: password
      },
      needAuth: false,
      showLoading: true,
      loadingTitle: '登录中...'
    })
  },
  
  // 工作人员登录 (更新为标准API路径)
  staffLogin(username, password) {
    return request('/api/v1/auth/login', {
      method: 'POST',
      data: { username, password },
      needAuth: false,
      showLoading: true,
      loadingTitle: '登录中...'
    })
  },
  
  // 获取当前用户信息 (适配后端直接返回用户对象的格式)
  getCurrentUser() {
    return request('/api/v1/auth/me', {
      showLoading: true,
      loadingTitle: '获取用户信息...'
    }).then(response => {
      // 适配后端直接返回用户对象的格式
      if (response && typeof response === 'object' && response.id) {
        // 后端直接返回用户对象，包装成统一格式
        return {
          success: true,
          data: response,
          message: '获取用户信息成功'
        }
      }
      // 如果已经是包装格式，直接返回
      return response
    }).catch(error => {
      console.warn('获取用户信息失败，使用Mock数据:', error)
      throw error
    })
  }
}

// 考生相关API
const candidateAPI = {
  // 根据身份证号获取考生信息 (新增 - 登录前验证)
  getCandidateInfoByIdCard(idCard) {
    return request(`/api/v1/wechat/candidate/info-by-idcard?id_card=${idCard}`, {
      method: 'GET',
      needAuth: false,
      useCache: false,
      showLoading: true,
      loadingTitle: '验证身份证信息...'
    }).then(response => {
      console.log('身份证验证响应:', response)
      
      // 处理后端直接返回用户对象的情况
      if (response && response.id) {
        // 后端直接返回用户对象，包装成统一格式
        return {
          success: true,
          data: response
        }
      }
      
      // 处理已包装的响应格式
      if (response && response.success && response.data) {
        return response
      }
      
      // 处理空响应或错误响应
      if (!response || (response.success === false)) {
        return {
          success: false,
          message: response?.message || '未找到该身份证号对应的考生信息'
        }
      }
      
      return response
    }).catch(error => {
      console.error('身份证验证请求失败:', error)
      throw error
    })
  },
  
  // 根据身份证号获取考生信息 (保留兼容)
  getCandidateInfo(idNumber) {
    return request(`/wx-miniprogram/candidate-info?id_number=${idNumber}`, {
      needAuth: false,
      useCache: true,
      cacheLevel: 'medium'
    })
  },
  
  // 获取考生详细信息 (修改为使用身份证号查询)
  getCandidateDetail(idCard) {
    // 使用现有的身份证验证接口来获取考生详细信息
    return this.getCandidateInfoByIdCard(idCard)
  },

  // 获取考生考试结果统计
  getExamResults(candidateId) {
    return request(`/api/v1/wechat/candidate/exam-results`, {
      method: 'GET',
      useCache: true,
      cacheLevel: 'short',
      showLoading: true,
      loadingTitle: '获取考试统计...'
    })
  },

  // 更新考生信息
  updateCandidateInfo(candidateId, data) {
    return request(`/api/v1/wechat/candidate/${candidateId}/update`, {
      method: 'PUT',
      data: data,
      useCache: false,
      showLoading: true,
      loadingTitle: '保存中...'
    })
  },
  
  // 获取考生考试安排 (更新为标准API路径)
  getExamSchedule() {
    return request('/api/v1/wechat/candidate/schedule', {
      useCache: true,
      cacheLevel: 'short',
      showLoading: true,
      loadingTitle: '获取考试日程...'
    })
  },
  
  // 获取考生动态二维码 (更新为标准API路径)
  getCandidateQRCode() {
    return request('/api/v1/wechat/candidate/qrcode', {
      useCache: false, // 二维码需要实时生成
      showLoading: true,
      loadingTitle: '生成二维码...'
    })
  },
  
  // 刷新考生二维码 (🆕 安全性提升 - 移除参数，直接从JWT获取用户身份)
  refreshCandidateQRCode() {
    return request('/api/v1/wechat/candidate/qrcode/refresh', {
      method: 'POST',
      // 🆕 不再需要传递任何参数，后端从JWT token中获取用户身份
      useCache: false,
      showLoading: true,
      loadingTitle: '刷新二维码...'
    })
  },
  
  // 获取考生签到历史 (修改为新的API路径，通过JWT自动识别考生)
  getCheckinHistory() {
    return request('/api/v1/wechat/candidate/checkin-history', {
      method: 'GET',
      useCache: true,
      cacheLevel: 'short',
      showLoading: true,
      loadingTitle: '获取签到历史...'
    })
  }
}

// 二维码相关API
const qrcodeAPI = {
  // 生成考试二维码
  generateScheduleQR(scheduleId) {
    return request(`/qrcode/generate-schedule-qr/${scheduleId}`)
  },
  
  // 扫码签到 (更新为标准API路径)
  scanCheckin(scheduleId, venueId) {
    return request('/api/v1/wechat/checkin', {
      method: 'POST',
      data: {
        schedule_id: scheduleId,
        venue_id: venueId
      },
      showLoading: true,
      loadingTitle: '签到中...'
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

// 工作人员相关API
const staffAPI = {
  // 扫描二维码 (更新为标准API路径)
  scanQRCode(qrCode) {
    return request('/api/v1/wechat/checkin', {
      method: 'POST',
      data: {
        qr_code_data: qrCode
      },
      needAuth: true,
      showLoading: true,
      loadingTitle: '处理签到...'
    })
  },
  
  // 扫描二维码 - 支持复杂数据格式
  scanQRCodeWithData(data) {
    return request('/api/v1/wechat/checkin', {
      method: 'POST',
      data: data,
      needAuth: true,
      showLoading: true,
      loadingTitle: '处理签到...'
    })
  },
  
  // 手动签到查询 - 第一步：查询考生信息和考试安排
  queryManualCheckin(realName, idCard) {
    return request('/api/v1/wechat/manual-checkin/query', {
      method: 'POST',
      data: {
        real_name: realName,
        id_card: idCard
      },
      needAuth: true,
      showLoading: true,
      loadingTitle: '查询考生信息...'
    })
  },
  
  // 手动签到确认 - 第二步：确认签到
  confirmManualCheckin(candidateId, scheduleId, operatorInfo = '') {
    return request('/api/v1/wechat/manual-checkin/confirm', {
      method: 'POST',
      data: {
        candidate_id: candidateId,
        schedule_id: scheduleId,
        operator_info: operatorInfo || undefined
      },
      needAuth: true,
      showLoading: true,
      loadingTitle: '处理签到...'
    })
  },
  
  // 旧版手动签到 (保留兼容)
  manualCheckin(candidateId, reason = '手动签到') {
    return request('/api/v1/wechat/manual-checkin', {
      method: 'POST',
      data: {
        candidate_id: candidateId,
        reason: reason
      },
      showLoading: true,
      loadingTitle: '处理签到...'
    })
  },
  
  // 获取工作人员统计信息
  getStaffStats() {
    return request('/api/v1/staff/stats', {
      useCache: true,
      cacheLevel: 'short',
      showLoading: true,
      loadingTitle: '获取统计信息...'
    })
  },
  
  // 获取签到历史
  getCheckinHistory(page = 1, size = 20) {
    return request(`/api/v1/staff/checkin-history?page=${page}&size=${size}`, {
      useCache: true,
      cacheLevel: 'short',
      showLoading: true,
      loadingTitle: '获取签到历史...'
    })
  }
}

// 实时状态API
const realtimeAPI = {
  // 获取实时状态
  getRealtimeStatus() {
    return request('/realtime/status')
  },
  
  // 获取公共看板数据 (更新为标准API路径)
  getPublicBoard() {
    return request('/api/v1/wechat/dashboard', {
      useCache: true,
      cacheLevel: 'short',
      showLoading: true,
      loadingTitle: '获取看板数据...'
    })
  },
  
  // 获取考场状态 (更新为标准API路径)
  getVenueStatus(venueId) {
    return request('/api/v1/wechat/venues/status', {
      useCache: true,
      cacheLevel: 'short',
      showLoading: true,
      loadingTitle: '获取考场状态...'
    })
  },
  
  // 获取排队状态 (更新为标准API路径)
  getQueueStatus() {
    return request('/api/v1/wechat/candidate/queue-position', {
      useCache: true,
      cacheLevel: 'short',
      showLoading: true,
      loadingTitle: '获取排队信息...'
    })
  },
  
  // 获取系统状态
  getSystemStatus() {
    return request('/realtime/system-status')
  },
  
  // 获取考场队列
  getVenueQueue(venueId) {
    return request(`/realtime/venue-queue/${venueId}`)
  },
  
  // 获取实时通知
  getNotifications(candidateId, venueId) {
    // 微信小程序兼容的查询参数构建
    const params = []
    if (candidateId) params.push(`candidate_id=${candidateId}`)
    if (venueId) params.push(`venue_id=${venueId}`)
    
    const queryString = params.join('&')
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
  staffAPI,
  realtimeAPI,
  institutionAPI,
  examProductAPI,
  venueAPI,
  scheduleAPI,
  utils
}

// 处理API错误
function handleError(error, defaultMessage = '操作失败') {
  console.error('API Error:', error)
  const message = error.message || defaultMessage
  wx.showToast({
    title: message,
    icon: 'none'
  })
  return Promise.reject(error)
}

// 检查网络状态
function checkNetworkStatus() {
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

module.exports = {
  request,
  TokenManager,
  authAPI,
  candidateAPI,
  qrcodeAPI,
  staffAPI,
  realtimeAPI,
  institutionAPI,
  examProductAPI,
  venueAPI,
  scheduleAPI,
  utils
}