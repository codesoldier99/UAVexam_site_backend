// 工作人员扫码签到页面
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
    // 相机权限
    cameraAuth: false,
    flashEnabled: false,
    // 今日统计（简化数据结构）
    todayStats: {
      total: 0,      // 总扫描次数
      success: 0,    // 成功签到
      failed: 0      // 失败次数
    },
    // 手动输入
    showManualInput: false,
    manualCode: '',
    manualInput: '',
    // 错误处理
    lastError: null,
    retryCount: 0,
    maxRetries: 3,
    // UI状态
    showResult: false,
    resultType: 'success', // success, error
    resultMessage: '',
    // 手动签到相关（简化流程）
    showModal: false,
    manualCheckin: {
      step: 1, // 1: 输入信息, 2: 确认完成
      idCard: '',
      name: '',
      candidateInfo: null,
      isLoading: false
    },
    // 最近扫描记录
    recentScans: [],
    // 当前日期
    currentDate: ''
  },

  onLoad() {
    console.log('扫码签到页面加载')
    this.checkStaffLoginAndInit()
    this.setCurrentDate()
    this.checkCameraAuth()
  },

  // 检查相机权限
  checkCameraAuth() {
    const self = this
    wx.getSetting({
      success: function(res) {
        if (res.authSetting['scope.camera']) {
          self.setData({
            cameraAuth: true
          })
        }
      }
    })
  },

  onShow() {
    // 每次显示页面时刷新数据
    if (this.data.staffInfo) {
      this.loadTodayStats()
      this.loadRecentScans()
    }
    this.setCurrentDate()
  },

  onUnload() {
    // 页面卸载时清理资源
    this.resetScanState()
  },

  // 设置当前日期
  setCurrentDate() {
    const now = new Date()
    const year = now.getFullYear()
    const month = String(now.getMonth() + 1).padStart(2, '0')
    const day = String(now.getDate()).padStart(2, '0')
    
    this.setData({
      currentDate: `${year}-${month}-${day}`
    })
  },

  // 检查工作人员登录状态并初始化
  checkStaffLoginAndInit() {
    try {
      const staffInfo = wx.getStorageSync('staffInfo')
      
      if (!staffInfo || !staffInfo.id) {
        // 未登录，跳转到登录页面
        wx.showModal({
          title: '未登录',
          content: '请先登录工作人员账号',
          showCancel: false,
          success: () => {
            wx.navigateTo({
              url: '/pages/staff/login/login'
            })
          }
        })
        return
      }

      // 设置用户信息
      this.setData({
        staffInfo: {
          id: staffInfo.id || 1,
          name: staffInfo.name || staffInfo.full_name || '工作人员',
          department: staffInfo.department || '考务部门',
          role: staffInfo.role || 'Examiner'
        }
      })

      // 如果没有用户信息，使用模拟数据
      if (!this.data.staffInfo.name || this.data.staffInfo.name === '工作人员') {
        const mockStaff = {
          id: 1,
          name: '张考官',
          department: '考务一部',
          role: 'Examiner'
        }
        this.setData({
          staffInfo: mockStaff
        })
        wx.setStorageSync('staffInfo', mockStaff)
      }
    } catch (error) {
      console.error('Failed to load staff info:', error)
    }
  },

  // 检查网络连接
  checkNetworkConnection() {
    return new Promise((resolve, reject) => {
      wx.getNetworkType({
        success: (res) => {
          if (res.networkType === 'none') {
            reject(new Error('网络连接不可用，请检查网络设置'))
          } else {
            resolve(true)
          }
        },
        fail: () => {
          reject(new Error('无法检测网络状态'))
        }
      })
    })
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
      examInfo: null,
      showResult: false
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

    let parsedData  // 声明在外面，确保catch块中也能访问

    try {
      // 检查网络连接
      await this.checkNetworkConnection()

      // 解析二维码数据
      console.log('原始扫码数据:', scanData)
      console.log('扫码数据类型:', typeof scanData)
      
      // 解析扫码数据
      try {
        if (typeof scanData === 'string') {
          parsedData = JSON.parse(scanData)
        } else {
          parsedData = scanData
        }
      } catch (parseError) {
        console.error('JSON解析失败:', parseError)
        throw new Error('二维码数据格式错误')
      }

      console.log('解析后的数据:', parsedData)

      // 解码姓名字段（如果是URL编码的）
      if (parsedData.name && parsedData.name.includes('%')) {
        try {
          parsedData.name = decodeURIComponent(parsedData.name)
          console.log('解码后的姓名:', parsedData.name)
        } catch (decodeError) {
          console.warn('姓名解码失败:', decodeError)
        }
      }

      // 验证必要字段 - 支持多种字段名
      if (!parsedData) {
        throw new Error('二维码数据为空')
      }

      // 检查各种可能的考生ID字段名
      const candidateId = parsedData.candidateId || 
                         parsedData.candidate_id || 
                         parsedData.id || 
                         parsedData.userId || 
                         parsedData.user_id

      if (!candidateId) {
        console.error('缺少考生ID字段，当前数据:', parsedData)
        throw new Error('二维码缺少考生ID信息')
      }

      // 补充缺失的字段
      parsedData.candidateId = candidateId
      console.log('验证通过，考生ID:', candidateId)

      // 获取Token - 检查多种可能的存储键名
      const token = wx.getStorageSync('access_token') || 
                   wx.getStorageSync('token') || 
                   wx.getStorageSync('staffToken') ||
                   wx.getStorageSync('userToken')
      
      console.log('Token检查结果:', {
        access_token: wx.getStorageSync('access_token'),
        token: wx.getStorageSync('token'),
        staffToken: wx.getStorageSync('staffToken'),
        userToken: wx.getStorageSync('userToken'),
        finalToken: token
      })
      
      if (!token) {
        throw new Error('用户未登录，请先登录')
      }

      // 构建签到请求数据 - 按照后端API文档格式
      const qrCodeDataString = JSON.stringify(parsedData)
      
      console.log('二维码数据字符串:', qrCodeDataString)
      console.log('原始二维码数据字段:', Object.keys(parsedData))

      // 调用签到API - 使用正确的数据格式
      const response = await staffAPI.scanQRCode(qrCodeDataString)
      
      console.log('API响应:', response)
      console.log('响应类型:', typeof response)
      console.log('success字段:', response?.success)

      // 更宽松的成功判断 - 只要不是明确的失败就认为成功
      if (response && response.success !== false && !response.error) {
        console.log('判断为成功，开始处理')
        // 签到成功
        this.handleCheckInSuccess(response.data || response, parsedData)
        console.log('handleCheckInSuccess 执行完成')
        return // 成功后直接返回，避免进入catch块
      } else {
        console.log('判断为失败，抛出错误')
        throw new Error(response.message || '签到失败')
      }

    } catch (error) {
      console.error('处理扫码结果失败:', error)
      
      // 检查是否已经成功处理过（避免成功后的错误被误判为失败）
      if (this.data.checkInStatus === 'success') {
        console.log('签到已成功，忽略后续错误')
        return
      }
      
      // 特殊处理已签到的情况
      if (error.message && error.message.includes('已完成签到')) {
        this.handleAlreadyCheckedIn(error.message, parsedData)
      } else {
        this.handleScanError(error.message || '处理失败，请重试')
      }
    }
  },

  // 检查网络连接
  async checkNetworkConnection() {
    return new Promise((resolve, reject) => {
      wx.getNetworkType({
        success: (res) => {
          if (res.networkType === 'none') {
            reject(new Error('网络连接不可用，请检查网络设置'))
          } else {
            resolve(true)
          }
        },
        fail: () => {
          reject(new Error('无法检测网络状态'))
        }
      })
    })
  },

  // 处理已签到的情况
  handleAlreadyCheckedIn(message, qrData) {
    const candidateName = qrData.candidateName || qrData.name || '未知考生'
    
    // 解码姓名（如果是URL编码的）
    const decodedName = candidateName.includes('%') ? decodeURIComponent(candidateName) : candidateName
    
    wx.showModal({
      title: '签到提示',
      content: `考生 ${decodedName} ${message}`,
      showCancel: false,
      confirmText: '知道了',
      confirmColor: '#007aff'
    })
    
    // 记录已签到的扫码记录
    const record = {
      id: Date.now().toString(),
      candidateName: decodedName,
      scanTime: this.formatDateTime(new Date().toISOString()),
      status: 'already_checked',
      message: message,
      timestamp: new Date().toISOString()
    }
    
    this.addToRecentScans(record)
    this.updateStats('already_checked')
  },

  // 统一显示结果弹窗
  showResultModal(type, message) {
    try {
      if (type === 'success') {
        wx.showModal({
          title: '签到成功',
          content: message,
          showCancel: false,
          confirmText: '确定',
          confirmColor: '#07c160'
        })
      } else {
        wx.showModal({
          title: '签到失败',
          content: message,
          showCancel: false,
          confirmText: '确定',
          confirmColor: '#ff4444'
        })
      }
    } catch (modalError) {
      console.error('显示弹窗失败:', modalError)
      // 降级到 Toast 提示
      wx.showToast({
        title: message,
        icon: type === 'success' ? 'success' : 'none',
        duration: 3000
      })
    }
  },

  // 处理扫码错误
  handleScanError(errorMessage) {
    console.error('扫码错误:', errorMessage)
    
    this.setData({
      checkInStatus: 'failed',
      checkInMessage: errorMessage,
      showResult: true,
      resultType: 'error',
      resultMessage: errorMessage
    })

    // 更新失败统计
    this.updateStats('failed')

    // 添加失败记录
    this.addScanRecord({
      candidateName: '未知',
      status: 'failed',
      scanTime: new Date().toLocaleTimeString()
    })
  },

  // 处理签到成功
  handleCheckInSuccess(responseData, qrData) {
    const candidateName = qrData.candidateName || qrData.name || '未知考生'
    
    this.setData({
      checkInStatus: 'success',
      checkInMessage: '签到成功！',
      showResult: true,
      resultType: 'success',
      resultMessage: `${candidateName} 签到成功`
    })

    // 更新统计数据
    this.updateStats('success')

    // 添加到扫描记录
    this.addScanRecord({
      candidateName: candidateName,
      status: 'success',
      scanTime: new Date().toLocaleTimeString()
    })
  },

  // 添加到最近扫描记录
  addToRecentScans(record) {
    try {
      let recentScans = wx.getStorageSync('recentScans') || []
      
      // 添加新记录到数组开头
      recentScans.unshift(record)
      
      // 限制记录数量，只保留最近50条
      if (recentScans.length > 50) {
        recentScans = recentScans.slice(0, 50)
      }
      
      // 保存到本地存储
      wx.setStorageSync('recentScans', recentScans)
      
      // 更新页面数据
      this.setData({
        recentScans: recentScans
      })
      
      console.log('添加扫码记录成功:', record)
    } catch (error) {
      console.error('添加扫码记录失败:', error)
    }
  },

  // 加载最近扫描记录
  loadRecentScans() {
    try {
      const recentScans = wx.getStorageSync('recentScans') || []
      this.setData({
        recentScans: recentScans
      })
    } catch (error) {
      console.error('Failed to load recent scans:', error)
    }
  },

  // 加载今日统计
  loadTodayStats() {
    try {
      const todayStats = wx.getStorageSync('todayStats') || {
        totalScans: 0,
        successfulCheckins: 0,
        failedCheckins: 0,
        scanned: 0,
        success: 0,
        failed: 0
      }
      this.setData({
        todayStats: todayStats
      })
    } catch (error) {
      console.error('Failed to load today stats:', error)
    }
  },

  // 格式化日期时间
  formatDateTime(dateString) {
    const date = new Date(dateString)
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    
    return `${year}-${month}-${day} ${hours}:${minutes}`
  },

  // 显示/隐藏历史记录
  toggleHistory() {
    this.setData({
      showHistory: !this.data.showHistory
    })
  },

  // 手动输入处理
  onManualInput(e) {
    const value = e.detail.value
    this.setData({
      manualInput: value
    })
  },

  // 显示手动签到模态框
  showManualCheckinModal() {
    this.setData({
      showModal: true,
      'manualCheckin.step': 1,
      'manualCheckin.name': '',
      'manualCheckin.idCard': '',
      'manualCheckin.candidateInfo': null,
      'manualCheckin.isLoading': false
    })
  },

  // 关闭手动签到模态框
  hideManualCheckinModal() {
    this.setData({
      showModal: false
    })
  },

  // 手动签到 - 姓名输入
  onManualNameInput(e) {
    this.setData({
      'manualCheckin.name': e.detail.value
    })
  },

  // 手动签到 - 身份证输入
  onManualIdCardInput(e) {
    this.setData({
      'manualCheckin.idCard': e.detail.value
    })
  },

  // 手动签到 - 下一步
  nextManualStep() {
    const { name, idCard } = this.data.manualCheckin
    if (!name || !idCard) {
      wx.showToast({
        title: '请填写完整信息',
        icon: 'none'
      })
      return
    }
    
    this.setData({
      'manualCheckin.step': 2
    })
  },

  // 手动签到 - 上一步
  prevManualStep() {
    this.setData({
      'manualCheckin.step': 1
    })
  },

  // 手动签到 - 下一步
  nextManualStep() {
    const { name, idCard } = this.data.manualCheckin
    if (!name || !idCard) {
      wx.showToast({
        title: '请填写完整信息',
        icon: 'none'
      })
      return
    }
    
    // 直接进入第二步确认
    this.setData({
      'manualCheckin.step': 2
    })
  },

  // 手动签到 - 上一步
  prevManualStep() {
    this.setData({
      'manualCheckin.step': 1
    })
  },

  // 确认手动签到
  async confirmManualCheckin() {
    const { name, idCard } = this.data.manualCheckin
    
    this.setData({
      'manualCheckin.isLoading': true
    })

    try {
      // 先查询考生信息
      console.log('开始查询考生信息:', { name, idCard })
      const queryResult = await staffAPI.queryManualCheckin(name, idCard)
      console.log('查询结果:', queryResult)

      // 检查查询结果
      if (queryResult && queryResult.success !== false) {
        // 检查是否有考试安排
        const examSchedules = queryResult.exam_schedules || []
        
        if (examSchedules.length === 0) {
          // 没有考试安排
          throw new Error(queryResult.message || '该考生今日无考试安排，无法签到')
        }
        
        // 有考试安排，检查是否可以签到
        const availableSchedules = examSchedules.filter(schedule => 
          schedule.status === 'can_checkin' || schedule.status === 'pending'
        )
        
        if (availableSchedules.length === 0) {
          throw new Error('该考生的考试尚未到签到时间或已完成签到')
        }
        
        // 可以签到，调用签到API
        const candidateInfo = queryResult.candidate_info
        const scheduleToCheckin = availableSchedules[0] // 使用第一个可签到的考试
        
        console.log('开始执行签到:', {
          candidateId: candidateInfo.id,
          scheduleId: scheduleToCheckin.schedule_id
        })
        
        const checkinResult = await staffAPI.confirmManualCheckin(
          candidateInfo.id,
          scheduleToCheckin.schedule_id,
          '手动签到'
        )
        
        console.log('签到结果:', checkinResult)
        
        // 检查签到结果
        if (checkinResult && checkinResult.success !== false) {
          // 签到成功
          this.setData({
            showModal: false,
            showResult: true,
            resultType: 'success',
            resultMessage: `${name} 签到成功！`
          })
          
          // 更新统计数据
          this.updateStats('success')
          
          // 添加到扫描记录
          this.addScanRecord({
            candidateName: name,
            status: 'success',
            scanTime: new Date().toLocaleTimeString()
          })

          // 添加到最近扫描记录
          const record = {
            id: Date.now().toString(),
            candidateName: name,
            scanTime: this.formatDateTime(new Date().toISOString()),
            status: 'success',
            message: '手动签到成功',
            timestamp: new Date().toISOString()
          }
          this.addToRecentScans(record)
        } else {
          throw new Error(checkinResult.message || '签到失败')
        }

      } else {
        throw new Error(queryResult.message || '未找到考生信息')
      }
    } catch (error) {
      console.error('手动签到失败:', error)
      this.setData({
        showModal: false,
        showResult: true,
        resultType: 'error',
        resultMessage: error.message || '签到失败，请重试'
      })
      
      this.updateStats('failed')
    } finally {
      this.setData({
        'manualCheckin.isLoading': false
      })
    }
  },

  // 阻止事件冒泡
  stopPropagation() {
    // 空方法，用于阻止事件冒泡
  },

  // 切换历史记录显示
  toggleHistory() {
    this.setData({
      showHistory: !this.data.showHistory
    })
  },

  // 隐藏结果弹窗
  hideResult() {
    this.setData({
      showResult: false
    })
  },

  // 更新统计数据
  updateStats(type) {
    const stats = this.data.todayStats
    if (type === 'success') {
      this.setData({
        'todayStats.total': stats.total + 1,
        'todayStats.success': stats.success + 1
      })
    } else if (type === 'failed') {
      this.setData({
        'todayStats.total': stats.total + 1,
        'todayStats.failed': stats.failed + 1
      })
    }
  },

  // 添加扫描记录
  addScanRecord(record) {
    const records = this.data.recentScans
    records.unshift({
      id: Date.now(),
      ...record
    })
    
    // 只保留最近20条记录
    if (records.length > 20) {
      records.splice(20)
    }
    
    this.setData({
      recentScans: records
    })
  },


  // 保存最近扫描记录
  saveRecentScan(result) {
    try {
      const recentScans = this.data.recentScans || []
      const newScan = {
        id: Date.now(),
        timestamp: result.timestamp || new Date().toISOString(),
        candidateInfo: result.candidateInfo,
        success: result.success,
        type: 'manual' // 标记为手动签到
      }
      
      // 添加到最近记录，保持最新的10条
      const updatedScans = [newScan, ...recentScans].slice(0, 10)
      
      this.setData({
        recentScans: updatedScans
      })
      
      // 保存到本地存储
      wx.setStorageSync('recentScans', updatedScans)
      
      console.log('保存扫描记录成功:', newScan)
    } catch (error) {
      console.error('保存扫描记录失败:', error)
    }
  },

  // 格式化日期时间
  formatDateTime(dateString) {
    try {
      const date = new Date(dateString)
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const hour = String(date.getHours()).padStart(2, '0')
      const minute = String(date.getMinutes()).padStart(2, '0')
      const second = String(date.getSeconds()).padStart(2, '0')
      
      return `${year}-${month}-${day} ${hour}:${minute}:${second}`
    } catch (error) {
      console.error('日期格式化失败:', error)
      return new Date().toLocaleString()
    }
  },

  // 手动签到 - 输入身份证号
  onIdCardInput(e) {
    this.setData({
      'manualCheckin.idCard': e.detail.value
    })
  },

  // 手动签到 - 输入姓名
  onNameInput(e) {
    this.setData({
      'manualCheckin.name': e.detail.value
    })
  },

  // 手动签到 - 查询考生
  async searchCandidate() {
    const { idCard, name } = this.data.manualCheckin
    
    if (!idCard.trim()) {
      wx.showToast({
        title: '请输入身份证号',
        icon: 'none'
      })
      return
    }

    this.setData({
      'manualCheckin.isLoading': true
    })

    try {
      // 模拟API调用
      const mockResponse = {
        success: true,
        data: {
          candidate: {
            id: 'C001',
            name: name || '张三',
            id_number: idCard,
            phone: '138****5678'
          },
          schedules: [
            {
              id: 'S001',
              exam_name: '计算机等级考试',
              exam_time: '2025-08-28 09:00',
              venue: '考场A101',
              status: 'can_checkin'
            }
          ]
        }
      }

      if (mockResponse.success) {
        this.setData({
          'manualCheckin.candidateInfo': mockResponse.data.candidate,
          'manualCheckin.schedules': mockResponse.data.schedules,
          'manualCheckin.step': 2
        })
      } else {
        throw new Error('未找到考生信息')
      }
    } catch (error) {
      wx.showToast({
        title: error.message || '查询失败',
        icon: 'error'
      })
    } finally {
      this.setData({
        'manualCheckin.isLoading': false
      })
    }
  },

  // 手动签到 - 选择考试安排
  selectSchedule(e) {
    const scheduleId = e.currentTarget.dataset.id
    const schedule = this.data.manualCheckin.schedules.find(s => s.id === scheduleId)
    
    this.setData({
      'manualCheckin.selectedSchedule': schedule,
      'manualCheckin.step': 3
    })
  },


  // 手动签到 - 返回上一步
  goBackStep() {
    const currentStep = this.data.manualCheckin.step
    if (currentStep > 1) {
      this.setData({
        'manualCheckin.step': currentStep - 1
      })
    }
  },

  // 快速测试功能
  quickTest() {
    const mockCandidate = {
      id: 'C001',
      name: '张三',
      idNumber: '110101199001011234'
    }
    
    const validTimestamp = Date.now()
    const mockQrData = {
      candidateId: mockCandidate.id,
      candidateName: mockCandidate.name,
      scheduleId: 'S001',
      examId: 'E001',
      timestamp: validTimestamp,
      type: 'candidate_checkin'
    }
    
    const qrCodeString = JSON.stringify(mockQrData)
    console.log('快速测试二维码数据:', mockQrData)
    this.processScanResult(qrCodeString)
  },

  // 继续扫码
  continueScan() {
    this.setData({
      showResult: false
    })
    // 可选择自动开始新的扫码
    setTimeout(() => {
      this.startScan()
    }, 500)
  },

  // 切换快捷操作显示
  toggleQuickActions() {
    this.setData({
      showQuickActions: !this.data.showQuickActions
    })
  },

  // 切换最近记录显示
  toggleRecentRecords() {
    this.setData({
      showRecentRecords: !this.data.showRecentRecords
    })
  },

  // 切换闪光灯
  toggleFlash() {
    this.setData({
      flashOn: !this.data.flashOn
    })
  },

  // 退出登录
  logout() {
    wx.showModal({
      title: '确认退出',
      content: '确定要退出登录吗？',
      success: (res) => {
        if (res.confirm) {
          // 清除本地存储的用户信息
          wx.removeStorageSync('userInfo')
          wx.removeStorageSync('staffInfo')
          wx.removeStorageSync('token')
          
          // 跳转到登录页面
          wx.reLaunch({
            url: '/pages/staff/login/login'
          })
        }
      }
    })
  },

  // 申请相机权限
  requestCameraAuth() {
    const self = this
    
    wx.getSetting({
      success: function(res) {
        if (res.authSetting['scope.camera']) {
          self.setData({
            cameraAuth: true
          })
        } else {
          wx.authorize({
            scope: 'scope.camera',
            success: function() {
              self.setData({
                cameraAuth: true
              })
            },
            fail: function() {
              wx.showModal({
                title: '需要相机权限',
                content: '扫描二维码需要使用相机，请在设置中开启相机权限',
                showCancel: false
              })
            }
          })
        }
      }
    })
  },


  // 相机事件处理
  onCameraError(error) {
    console.error('Camera error:', error)
    wx.showToast({
      title: '相机启动失败',
      icon: 'error'
    })
  },

  onCameraStop() {
    console.log('Camera stopped')
  },

  onCameraReady() {
    console.log('Camera ready')
  },

  // 关闭结果弹窗
  closeResult() {
    this.setData({
      showResult: false
    })
  },

  // 查看扫描详情
  viewScanDetail(e) {
    const scan = e.currentTarget.dataset.scan
    wx.showModal({
      title: '扫描详情',
      content: `考生：${scan.candidateName}\n时间：${scan.scanTime}\n状态：${scan.status === 'success' ? '成功' : '失败'}`,
      showCancel: false
    })
  },

  // 查看全部记录
  viewAllRecords() {
    wx.showModal({
      title: '功能提示',
      content: '全部记录页面正在开发中，敬请期待！\n\n当前可以查看最近10条扫描记录。',
      showCancel: false,
      confirmText: '知道了'
    })
  },

  // 手动输入处理
  onManualInput(e) {
    const value = e.detail.value
    this.setData({
      manualInput: value
    })
  },

  // 处理手动输入
  handleManualInput() {
    this.showManualCheckinModal()
    
    // 如果已经输入了身份证号，自动填充
    const idCard = this.data.manualInput.trim()
    if (idCard) {
      this.setData({
        'manualCheckin.idCard': idCard,
        'manualInput': ''
      })
    }
  },

  // 手动签到相关方法
  onManualNameInput(e) {
    this.setData({
      'manualCheckin.name': e.detail.value
    })
  },

  onManualIdCardInput(e) {
    this.setData({
      'manualCheckin.idCard': e.detail.value
    })
  },

  // 手动输入处理（通用）
  onManualInput(e) {
    this.setData({
      manualInput: e.detail.value
    })
  },

  onSelectSchedule(e) {
    const scheduleId = parseInt(e.currentTarget.dataset.id)
    this.setData({
      'manualCheckin.selectedScheduleId': scheduleId
    })
  },

  // 查询考生信息
  async queryCandidate() {
    const { name, idCard } = this.data.manualCheckin
    
    // 验证输入
    if (!name.trim()) {
      wx.showToast({
        title: '请输入考生姓名',
        icon: 'none'
      })
      return
    }
    
    if (!idCard.trim()) {
      wx.showToast({
        title: '请输入身份证号',
        icon: 'none'
      })
      return
    }
    
    this.setData({
      processing: true
    })
    
    try {
      // 调用真实API
      console.log('查询考生信息:', { name, idCard })
      const response = await staffAPI.queryManualCheckin(name, idCard)
      console.log('API返回数据:', response)

      // 处理不同的响应格式
      let candidateInfo, examSchedules
      
      if (response.success !== false) {
        // 情况1: 直接返回数据对象
        if (response.candidate_info && response.exam_schedules) {
          candidateInfo = response.candidate_info
          examSchedules = response.exam_schedules
        }
        // 情况2: 包装在data字段中
        else if (response.data) {
          candidateInfo = response.data.candidate_info
          examSchedules = response.data.exam_schedules
        }
        // 情况3: 直接是考生信息
        else if (response.id || response.real_name) {
          candidateInfo = response
          examSchedules = response.exam_schedules || []
        }
        
        if (candidateInfo) {
          this.setData({
            'manualCheckin.candidateInfo': candidateInfo,
            'manualCheckin.examSchedules': examSchedules || [],
            'manualCheckin.step': 2,
            'manualCheckin.selectedScheduleId': examSchedules?.[0]?.schedule_id
          })
          console.log('设置考生信息成功')
        } else {
          throw new Error('返回数据格式不正确')
        }
      } else {
        throw new Error(response.message || '未找到考生信息')
      }
    } catch (error) {
      console.error('查询考生信息失败:', error)
      wx.showToast({
        title: error.message || '查询失败',
        icon: 'none'
      })
    } finally {
      this.setData({
        processing: false
      })
    }
  },

  // 确认签到
  async confirmCheckin() {
    const { candidateInfo, selectedScheduleId } = this.data.manualCheckin
    
    console.log('确认签到参数:', { candidateInfo, selectedScheduleId })
    
    if (!selectedScheduleId) {
      wx.showToast({
        title: '请选择要签到的考试',
        icon: 'none'
      })
      return
    }
    
    this.setData({
      processing: true
    })
    
    try {
      // 调用真实API
      console.log('调用签到API:', {
        candidateId: candidateInfo.id,
        scheduleId: selectedScheduleId,
        operatorInfo: '手动签到'
      })
      
      const response = await staffAPI.confirmManualCheckin(
        candidateInfo.id, 
        selectedScheduleId, 
        '手动签到'
      )
      
      console.log('签到API返回:', response)

      // 处理不同的响应格式
      let checkinInfo
      let success = false
      
      if (response.success !== false) {
        // 情况1: 直接返回签到信息
        if (response.checkin_info) {
          checkinInfo = response.checkin_info
          success = true
        }
        // 情况2: 包装在data字段中
        else if (response.data && response.data.checkin_info) {
          checkinInfo = response.data.checkin_info
          success = true
        }
        // 情况3: 直接是签到结果
        else if (response.candidate_name || response.checkin_time) {
          checkinInfo = response
          success = true
        }
        // 情况4: 简单成功响应
        else if (response.message && response.message.includes('成功')) {
          checkinInfo = {
            candidate_name: candidateInfo.name || candidateInfo.real_name,
            exam_name: '考试',
            venue_name: '考场',
            checkin_time: new Date().toISOString()
          }
          success = true
        }
      }

      if (success && checkinInfo) {
        this.setData({
          'manualCheckin.checkinResult': checkinInfo,
          'manualCheckin.step': 3
        })
        
        // 更新统计和记录
        this.updateStats()
        
        const result = {
          success: true,
          candidateInfo: {
            name: checkinInfo.candidate_name || candidateInfo.name || candidateInfo.real_name,
            examName: checkinInfo.exam_name || '考试',
            venue: checkinInfo.venue_name || '考场',
            checkInTime: this.formatDateTime(checkinInfo.checkin_time || new Date().toISOString())
          },
          timestamp: checkinInfo.checkin_time || new Date().toISOString()
        }
        
        this.saveRecentScan(result)
        
        wx.showToast({
          title: '签到成功',
          icon: 'success'
        })
        
        console.log('签到处理成功')
      } else {
        throw new Error(response.message || '签到失败')
      }
    } catch (error) {
      console.error('签到失败:', error)
      
      // 特殊处理时间相关错误
      if (error.message && error.message.includes('签到时间已过')) {
        wx.showModal({
          title: '签到时间已过',
          content: error.message,
          showCancel: false,
          confirmText: '知道了'
        })
      } else {
        wx.showToast({
          title: error.message || '签到失败',
          icon: 'none',
          duration: 3000
        })
      }
      
      // 更新失败统计
      const todayStats = this.data.todayStats
      this.setData({
        'todayStats.failedCheckins': todayStats.failedCheckins + 1,
        'todayStats.failed': todayStats.failed + 1,
        'todayStats.totalScans': todayStats.totalScans + 1
      })
    } finally {
      this.setData({
        processing: false
      })
    }
  },

  // 返回上一步
  goBackManualCheckin() {
    const currentStep = this.data.manualCheckin.step
    if (currentStep > 1) {
      this.setData({
        'manualCheckin.step': currentStep - 1
      })
    }
  },

  // 重置手动签到
  resetManualCheckin() {
    this.setData({
      'manualCheckin.step': 1,
      'manualCheckin.name': '',
      'manualCheckin.idCard': '',
      'manualCheckin.candidateInfo': null,
      'manualCheckin.examSchedules': [],
      'manualCheckin.selectedScheduleId': null,
      'manualCheckin.checkinResult': null
    })
  },

})
