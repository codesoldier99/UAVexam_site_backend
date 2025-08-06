// Mock数据加载器 - 微信小程序版本
// 直接导入所有mock数据模块

// 认证相关数据
const candidateLoginSuccess = require('./auth/candidate-login-success.js')
const candidateLoginFailure = require('./auth/candidate-login-failure.js')
const staffLoginSuccess = require('./auth/staff-login-success.js')
const staffLoginFailure = require('./auth/staff-login-failure.js')
const userInfo = require('./auth/user-info.js')

// 考生相关数据
const candidateInfo = require('./candidate/candidate-info.js')
const candidateDetail = require('./candidate/candidate-detail.js')
const examSchedule = require('./candidate/exam-schedule.js')
const candidateQrcode = require('./candidate/candidate-qrcode.js')
const checkinHistory = require('./candidate/checkin-history.js')
const examResults = require('./candidate/exam-results.js')

// 二维码相关数据
const scheduleQr = require('./qrcode/schedule-qr.js')
const scanCheckin = require('./qrcode/scan-checkin.js')
const scanCheckinFailure = require('./qrcode/scan-checkin-failure.js')
const checkinStatus = require('./qrcode/checkin-status.js')
const manualCheckin = require('./qrcode/manual-checkin.js')

// 实时状态数据
const realtimeStatus = require('./realtime/realtime-status.js')
const publicBoard = require('./realtime/public-board.js')
const venueStatus = require('./realtime/venue-status.js')
const systemStatus = require('./realtime/system-status.js')
const queueStatus = require('./realtime/queue-status.js')
const venueQueue = require('./realtime/venue-queue.js')
const notifications = require('./realtime/notifications.js')

class DataLoader {
  constructor() {
    this.cache = new Map()
    this.mockData = {
      // 认证数据
      'auth/candidate-login-success': candidateLoginSuccess,
      'auth/candidate-login-failure': candidateLoginFailure,
      'auth/staff-login-success': staffLoginSuccess,
      'auth/staff-login-failure': staffLoginFailure,
      'auth/user-info': userInfo,
      
      // 考生数据
      'candidate/candidate-info': candidateInfo,
      'candidate/candidate-detail': candidateDetail,
      'candidate/exam-schedule': examSchedule,
      'candidate/candidate-qrcode': candidateQrcode,
      'candidate/checkin-history': checkinHistory,
      'candidate/exam-results': examResults,
      
      // 二维码数据
      'qrcode/schedule-qr': scheduleQr,
      'qrcode/scan-checkin': scanCheckin,
      'qrcode/scan-checkin-failure': scanCheckinFailure,
      'qrcode/checkin-status': checkinStatus,
      'qrcode/manual-checkin': manualCheckin,
      
      // 实时状态数据
      'realtime/realtime-status': realtimeStatus,
      'realtime/public-board': publicBoard,
      'realtime/venue-status': venueStatus,
      'realtime/system-status': systemStatus,
      'realtime/queue-status': queueStatus,
      'realtime/venue-queue': venueQueue,
      'realtime/notifications': notifications
    }
  }
  
  // 加载Mock数据（支持.js和.json文件）
  loadJsonFile(filePath) {
    try {
      // 移除文件扩展名
      const cleanPath = filePath.replace(/\.(json|js)$/, '')
      
      // 检查缓存
      if (this.cache.has(cleanPath)) {
        return this.cache.get(cleanPath)
      }
      
      // 从预加载的数据中获取
      const data = this.mockData[cleanPath]
      
      if (!data) {
        console.warn(`Mock data not found for: ${filePath}`)
        return this.getDefaultErrorResponse()
      }
      
      // 缓存数据
      this.cache.set(cleanPath, data)
      
      return data
    } catch (error) {
      console.error(`Failed to load mock data file: ${filePath}`, error)
      return this.getDefaultErrorResponse()
    }
  }
  
  // 获取默认错误响应
  getDefaultErrorResponse() {
    return {
      success: false,
      message: "Mock数据加载失败",
      error_code: "MOCK_DATA_ERROR",
      data: null,
      timestamp: new Date().toISOString()
    }
  }
  
  // 清除缓存
  clearCache() {
    this.cache.clear()
  }
  
  // 重新加载文件（清除缓存后重新加载）
  reloadFile(filePath) {
    const cleanPath = filePath.replace('.json', '')
    this.cache.delete(cleanPath)
    return this.loadJsonFile(filePath)
  }
}

module.exports = new DataLoader()
