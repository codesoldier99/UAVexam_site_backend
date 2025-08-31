// 工作人员扫码页面
const { staffAPI, qrcodeAPI, utils } = require('../../../utils/api')
const app = getApp()

Page({
  data: {
    staffInfo: null,
    isScanning: false,
    scanResult: null,
    candidateInfo: null,
    examInfo: null,
    checkInStatus: 'idle', // idle, scanning, processing, success, failed
    checkInMessage: '',
    scanHistory: [],
    showHistory: false,
    // 扫码统计
    todayStats: {
      totalScans: 0,
      successfulCheckins: 0,
      failedCheckins: 0
    },
    // 手动输入
    showManualInput: false,
    manualCode: '',
    // 错误处理
    lastError: null,
    retryCount: 0,
    maxRetries: 3
  },

  onLoad() {
    console.log('Scanner page loaded')
    this.checkStaffLoginAndInit()
    
    // 设置自定义tabBar的选中状态
    if (typeof this.getTabBar === 'function' && this.getTabBar()) {
      this.getTabBar().setData({
        selected: 1 // 扫码是第2个tab，索引为1
      })
    }
  },

  onShow() {
    // 每次显示页面时刷新数据
    if (this.data.staffInfo) {
      this.loadTodayStats()
      this.loadScanHistory()
    }
  },

  onUnload() {
    // 页面卸载时清理资源
    this.resetScanState()
  },

  // 检查工作人员登录状态并初始化
  checkStaffLoginAndInit() {
    const staffInfo = wx.getStorageSync('staffInfo')
    
    if (!staffInfo || !staffInfo.id) {
      // 未登录，跳转到登录页面
      wx.redirectTo({
        url: '/pages/staff/login/login'
      })
      return
    }

    // 检查扫码权限
    if (!this.hasPermission(staffInfo, 'scan_qr')) {
      wx.showModal({
        title: '权限不足',
        content: '您没有扫码签到的权限，请联系管理员',
        showCancel: false,
        success: () => {
          wx.navigateBack()
        }
      })
      return
    }

    this.setData({
      staffInfo: staffInfo
    })

    // 加载初始数据
    this.loadTodayStats()
    this.loadScanHistory()
  },

  // 检查权限
  hasPermission(staffInfo, permission) {
    return staffInfo.permissions && staffInfo.permissions.includes(permission)
  },

  // 加载今日统计
  async loadTodayStats() {
    try {
      const response = await staffAPI.getTodayStats(this.data.staffInfo.id)
      
      if (response && response.success && response.data) {
        this.setData({
          todayStats: response.data
        })
      }
    } catch (error) {
      console.error('加载今日统计失败:', error)
    }
  },

  // 加载扫码历史
  async loadScanHistory() {
    try {
      const response = await staffAPI.getScanHistory(this.data.staffInfo.id)
      
      if (response && response.success && response.data) {
        this.setData({
          scanHistory: response.data.slice(0, 10) // 只显示最近10条
        })
      }
    } catch (error) {
      console.error('加载扫码历史失败:', error)
    }
  },

  // 开始扫码
  startScan() {
    if (this.data.isScanning) return
    
    this.setData({
      isScanning: true,
      checkInStatus: 'scanning',
      checkInMessage: '请对准考生二维码...',
      scanResult: null,
      candidateInfo: null,
      examInfo: null
    })

    // 调用微信扫码API
    wx.scanCode({
      success: (res) => {
        console.log('扫码成功:', res)
        this.processScanResult(res.result)
      },
      fail: (err) => {
        console.error('扫码失败:', err)
        this.handleScanError('扫码失败，请重试')
      },
      complete: () => {
        this.setData({
          isScanning: false
        })
      }
    })
  },

  // 处理扫码结果
  async processScanResult(scanData) {
    this.setData({
      checkInStatus: 'processing',
      checkInMessage: '正在处理扫码结果...'
    })

    try {
      // 1. 解析二维码数据
      const qrData = this.parseQRCode(scanData)
      
      if (!qrData) {
        throw new Error('无效的二维码格式')
      }

      // 2. 验证二维码
      const validationResult = await this.validateQRCode(qrData)
      
      if (!validationResult.success) {
        throw new Error(validationResult.message || '二维码验证失败')
      }

      // 3. 获取考生和考试信息
      const candidateInfo = validationResult.data.candidate
      const examInfo = validationResult.data.exam

      this.setData({
        scanResult: qrData,
        candidateInfo: candidateInfo,
        examInfo: examInfo,
        checkInMessage: '验证成功，请确认签到信息'
      })

      // 4. 显示确认对话框
      this.showCheckInConfirmation()

    } catch (error) {
      console.error('处理扫码结果失败:', error)
      this.handleScanError(error.message || '处理失败，请重试')
    }
  },

  // 解析二维码数据
  parseQRCode(scanData) {
    try {
      // 尝试解析JSON格式的二维码
      const qrData = JSON.parse(scanData)
      
      // 验证必要字段
      if (qrData.t === 'CHK' && qrData.c && qrData.s && qrData.ts && qrData.exp) {
        return {
          type: qrData.t,
          candidateId: qrData.c,
          scheduleId: qrData.s,
          timestamp: qrData.ts,
          expires: qrData.exp
        }
      }
    } catch (e) {
      // 如果不是JSON格式，尝试其他格式
      console.log('非JSON格式二维码，尝试其他解析方式')
    }

    // 尝试解析其他格式（如简单字符串格式）
    if (typeof scanData === 'string' && scanData.includes('CANDIDATE_')) {
      const parts = scanData.split('_')
      if (parts.length >= 3) {
        return {
          type: 'CHK',
          candidateId: parts[1],
          scheduleId: parts[2] || 'UNKNOWN',
          timestamp: Date.now(),
          expires: Date.now() + 2 * 60 * 60 * 1000 // 2小时后过期
        }
      }
    }

    return null
  },

  // 验证二维码
  async validateQRCode(qrData) {
    try {
      // 1. 检查过期时间
      if (qrData.expires && Date.now() > qrData.expires) {
        return {
          success: false,
          message: '二维码已过期，请考生刷新后重试'
        }
      }

      // 2. 调用后端验证API
      const response = await qrcodeAPI.validateQRCode({
        qr_data: qrData,
        staff_id: this.data.staffInfo.id,
        scan_time: new Date().toISOString()
      })

      return response

    } catch (error) {
      console.error('验证二维码失败:', error)
      return {
        success: false,
        message: '验证失败，请检查网络连接'
      }
    }
  },

  // 显示签到确认对话框
  showCheckInConfirmation() {
    const { candidateInfo, examInfo } = this.data
    
    wx.showModal({
      title: '确认签到',
      content: `考生：${candidateInfo.name}\n身份证：${candidateInfo.id_number}\n考试：${examInfo.exam_name}\n时间：${examInfo.exam_time}`,
      confirmText: '确认签到',
      cancelText: '取消',
      success: (res) => {
        if (res.confirm) {
          this.performCheckIn()
        } else {
          this.resetScanState()
        }
      }
    })
  },

  // 执行签到
  async performCheckIn() {
    this.setData({
      checkInStatus: 'processing',
      checkInMessage: '正在签到...'
    })

    try {
      const checkInData = {
        qr_code: JSON.stringify(this.data.scanResult),
        candidate_id: this.data.candidateInfo.id,
        schedule_id: this.data.examInfo.schedule_id,
        staff_id: this.data.staffInfo.id,
        checkin_time: new Date().toISOString(),
        location: '考试现场', // 可以通过GPS获取
        notes: ''
      }

      const response = await qrcodeAPI.performCheckIn(checkInData)

      if (response && response.success) {
        // 签到成功
        this.handleCheckInSuccess(response.data)
      } else {
        throw new Error(response.message || '签到失败')
      }

    } catch (error) {
      console.error('签到失败:', error)
      this.handleCheckInError(error.message || '签到失败，请重试')
    }
  },

  // 处理签到成功
  handleCheckInSuccess(checkInData) {
    this.setData({
      checkInStatus: 'success',
      checkInMessage: '签到成功！'
    })

    // 显示成功提示
    wx.showToast({
      title: '签到成功',
      icon: 'success',
      duration: 2000
    })

    // 更新统计数据
    this.updateStats('success')

    // 添加到历史记录
    this.addToHistory(checkInData)

    // 3秒后重置状态
    setTimeout(() => {
      this.resetScanState()
    }, 3000)
  },

  // 处理签到错误
  handleCheckInError(errorMessage) {
    this.setData({
      checkInStatus: 'failed',
      checkInMessage: errorMessage,
      lastError: errorMessage
    })

    // 更新统计数据
    this.updateStats('failed')

    // 显示错误提示
    wx.showToast({
      title: errorMessage,
      icon: 'error',
      duration: 3000
    })
  },

  // 处理扫码错误
  handleScanError(errorMessage) {
    this.setData({
      checkInStatus: 'failed',
      checkInMessage: errorMessage,
      lastError: errorMessage
    })

    wx.showToast({
      title: errorMessage,
      icon: 'error',
      duration: 2000
    })
  },

  // 重置扫码状态
  resetScanState() {
    this.setData({
      isScanning: false,
      scanResult: null,
      candidateInfo: null,
      examInfo: null,
      checkInStatus: 'idle',
      checkInMessage: '',
      lastError: null,
      retryCount: 0
    })
  },

  // 更新统计数据
  updateStats(result) {
    const stats = { ...this.data.todayStats }
    stats.totalScans += 1
    
    if (result === 'success') {
      stats.successfulCheckins += 1
    } else if (result === 'failed') {
      stats.failedCheckins += 1
    }

    this.setData({
      todayStats: stats
    })
  },

  // 添加到历史记录
  addToHistory(checkInData) {
    const history = [...this.data.scanHistory]
    const newRecord = {
      id: Date.now().toString(),
      candidate_name: this.data.candidateInfo.name,
      exam_name: this.data.examInfo.exam_name,
      checkin_time: new Date().toISOString(),
      status: 'success',
      ...checkInData
    }
    
    history.unshift(newRecord)
    
    this.setData({
      scanHistory: history.slice(0, 10) // 只保留最近10条
    })
  },

  // 重试扫码
  retryScan() {
    if (this.data.retryCount < this.data.maxRetries) {
      this.setData({
        retryCount: this.data.retryCount + 1
      })
      this.startScan()
    } else {
      wx.showModal({
        title: '重试次数过多',
        content: '请检查二维码是否清晰，或联系技术支持',
        showCancel: false
      })
    }
  },

  // 显示/隐藏历史记录
  toggleHistory() {
    this.setData({
      showHistory: !this.data.showHistory
    })
  },

  // 显示/隐藏手动输入
  toggleManualInput() {
    this.setData({
      showManualInput: !this.data.showManualInput,
      manualCode: ''
    })
  },

  // 手动输入签到码
  onManualCodeInput(e) {
    this.setData({
      manualCode: e.detail.value
    })
  },

  // 提交手动签到码
  submitManualCode() {
    const code = this.data.manualCode.trim()
    
    if (!code) {
      wx.showToast({
        title: '请输入签到码',
        icon: 'none'
      })
      return
    }

    if (code.length !== 6) {
      wx.showToast({
        title: '签到码应为6位数字',
        icon: 'none'
      })
      return
    }

    // 处理手动签到码
    this.processManualCode(code)
  },

  // 处理手动签到码
  async processManualCode(code) {
    this.setData({
      checkInStatus: 'processing',
      checkInMessage: '正在验证签到码...'
    })

    try {
      const response = await qrcodeAPI.validateManualCode({
        checkin_code: code,
        staff_id: this.data.staffInfo.id,
        scan_time: new Date().toISOString()
      })

      if (response && response.success) {
        // 验证成功，显示考生信息
        this.setData({
          candidateInfo: response.data.candidate,
          examInfo: response.data.exam,
          checkInMessage: '验证成功，请确认签到信息'
        })
        
        this.showCheckInConfirmation()
      } else {
        throw new Error(response.message || '签到码无效')
      }

    } catch (error) {
      console.error('验证签到码失败:', error)
      this.handleScanError(error.message || '验证失败，请重试')
    }
  },

  // 清除错误状态
  clearError() {
    this.setData({
      lastError: null,
      checkInStatus: 'idle',
      checkInMessage: ''
    })
  },

  // 退出登录
  logout() {
    wx.showModal({
      title: '确认退出',
      content: '确定要退出登录吗？',
      success: (res) => {
        if (res.confirm) {
          app.logout()
          wx.redirectTo({
            url: '/pages/index/index'
          })
        }
      }
    })
  }
})