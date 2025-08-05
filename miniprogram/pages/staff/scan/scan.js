// miniprogram/pages/staff/scan/scan.js
const { staffAPI } = require('../../../utils/api.js')

Page({
  data: {
    staffInfo: {
      name: '',
      id: '',
      department: '',
      role: ''
    },
    // Camera and scanning
    cameraAuthorized: false,
    scanning: false,
    processing: false,
    manualInput: '',
    
    // Scan results and history
    showResult: false,
    resultData: null,
    recentScans: [],
    
    // Statistics
    todayStats: {
      scanned: 0,
      checkedIn: 0,
      failed: 0
    },
    
    // Mock data for demonstration
    mockCandidates: [
      {
        id: 'C001',
        name: '张三',
        examName: '计算机二级考试',
        examTime: '2025-01-08 09:00',
        venue: '考场A101',
        status: 'registered',
        qrCode: 'EXAM_C001_20250108'
      },
      {
        id: 'C002', 
        name: '李四',
        examName: '英语四级考试',
        examTime: '2025-01-08 14:00',
        venue: '考场B201',
        status: 'registered',
        qrCode: 'EXAM_C002_20250108'
      },
      {
        id: 'C003',
        name: '王五',
        examName: '数学竞赛',
        examTime: '2025-01-08 10:30',
        venue: '考场C301',
        status: 'checked_in',
        qrCode: 'EXAM_C003_20250108'
      }
    ]
  },

  onLoad: function(options) {
    this.loadStaffInfo()
    this.loadRecentScans()
    this.loadTodayStats()
    this.requestCameraAuth()
  },

  onShow: function() {
    this.loadRecentScans()
    this.loadTodayStats()
  },

  // Load staff information
  loadStaffInfo: function() {
    try {
      const staffInfo = wx.getStorageSync('staffInfo')
      if (staffInfo) {
        this.setData({
          staffInfo: {
            ...staffInfo,
            role: staffInfo.role || 'Examiner'
          }
        })
      } else {
        // Use mock data for demonstration
        const mockStaff = {
          id: 'S001',
          name: '监考老师',
          department: '教务处',
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

  // Request camera authorization
  requestCameraAuth: function() {
    const self = this
    
    wx.getSetting({
      success: function(res) {
        if (res.authSetting['scope.camera']) {
          self.setData({
            cameraAuthorized: true
          })
        } else {
          wx.authorize({
            scope: 'scope.camera',
            success: function() {
              self.setData({
                cameraAuthorized: true
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

  // Camera event handlers
  onCameraError: function(error) {
    console.error('Camera error:', error)
    wx.showToast({
      title: '相机启动失败',
      icon: 'error'
    })
  },

  onCameraStop: function() {
    console.log('Camera stopped')
  },

  onCameraReady: function() {
    console.log('Camera ready')
  },

  // Start scanning
  startScan: function() {
    if (this.data.scanning || this.data.processing) {
      return
    }

    const self = this
    this.setData({
      scanning: true
    })

    wx.scanCode({
      onlyFromCamera: true,
      scanType: ['qrCode'],
      success: function(res) {
        console.log('Scan result:', res.result)
        self.processScanResult(res.result)
      },
      fail: function(error) {
        console.error('Scan failed:', error)
        wx.showToast({
          title: '扫描失败',
          icon: 'error'
        })
      },
      complete: function() {
        self.setData({
          scanning: false
        })
      }
    })
  },

  // Process scan result
  processScanResult: async function(qrCode) {
    if (this.data.processing) {
      return
    }

    this.setData({
      processing: true
    })

    try {
      // Check network status
      const networkStatus = await new Promise((resolve) => {
        wx.getNetworkType({
          success: (res) => resolve(res.networkType !== 'none'),
          fail: () => resolve(false)
        });
      });

      if (!networkStatus) {
        throw new Error('网络连接不可用，请检查网络设置');
      }

      // Call real API to scan QR code
      const response = await staffAPI.scanQRCode(qrCode);
      
      if (response.success) {
        const result = {
          success: true,
          message: response.message || '签到成功！',
          candidateInfo: {
            name: response.data.candidate_name || response.data.name,
            examName: response.data.exam_name || response.data.examName,
            examTime: response.data.exam_time || response.data.examTime,
            venue: response.data.venue || response.data.location,
            checkInTime: this.formatDateTime(response.data.check_in_time || new Date().toISOString())
          },
          timestamp: response.data.check_in_time || new Date().toISOString()
        }
        
        this.showScanResult(result)
        this.updateScanHistory(result)
        this.updateTodayStats('success')
      } else {
        // Failed scan
        const result = {
          success: false,
          message: response.message || '扫描失败',
          timestamp: new Date().toISOString()
        }
        this.showScanResult(result)
        this.updateTodayStats('failed')
      }
    } catch (error) {
      console.error('Scan processing failed:', error)
      
      let errorMessage = '扫描处理失败，请重试';
      if (error.message.includes('网络')) {
        errorMessage = error.message;
      } else if (error.message.includes('token')) {
        errorMessage = '登录已过期，请重新登录';
        setTimeout(() => {
          wx.reLaunch({
            url: '/pages/staff/login/login'
          });
        }, 2000);
      }
      
      const result = {
        success: false,
        message: errorMessage,
        timestamp: new Date().toISOString()
      }
      this.showScanResult(result)
      this.updateTodayStats('failed')
    } finally {
      this.setData({
        processing: false
      })
    }
  },

  // Find candidate by QR code
  findCandidateByQR: function(qrCode) {
    return this.data.mockCandidates.find(candidate => 
      candidate.qrCode === qrCode || 
      candidate.id === qrCode ||
      qrCode.includes(candidate.id)
    )
  },

  // Show scan result modal
  showScanResult: function(result) {
    this.setData({
      resultData: result,
      showResult: true
    })
  },

  // Close result modal
  closeResult: function() {
    this.setData({
      showResult: false,
      resultData: null
    })
  },

  // Continue scanning
  continueScan: function() {
    this.closeResult()
    // Auto start next scan after a short delay
    setTimeout(() => {
      this.startScan()
    }, 500)
  },

  // Handle manual input
  onManualInput: function(e) {
    this.setData({
      manualInput: e.detail.value
    })
  },

  // Handle manual input submission
  handleManualInput: function() {
    const input = this.data.manualInput.trim()
    if (!input) {
      wx.showToast({
        title: '请输入内容',
        icon: 'error'
      })
      return
    }

    this.setData({
      manualInput: ''
    })
    
    this.processScanResult(input)
  },

  // Update scan history
  updateScanHistory: function(result) {
    let recentScans = [...this.data.recentScans]
    
    const scanRecord = {
      id: Date.now(),
      candidateName: result.candidateInfo ? result.candidateInfo.name : '未知',
      scanTime: this.formatTime(result.timestamp),
      status: result.success ? 'success' : 'failed',
      statusIcon: result.success ? '✅' : '❌',
      statusText: result.success ? '成功' : '失败',
      fullData: result
    }
    
    recentScans.unshift(scanRecord)
    
    // Keep only last 10 records
    if (recentScans.length > 10) {
      recentScans = recentScans.slice(0, 10)
    }

    this.setData({
      recentScans: recentScans.slice(0, 5) // Show only 5 in UI
    })

    // Save to storage
    try {
      wx.setStorageSync('recentScans', recentScans)
    } catch (error) {
      console.error('Failed to save recent scans:', error)
    }
  },

  // Load recent scans
  loadRecentScans: function() {
    try {
      const recentScans = wx.getStorageSync('recentScans') || []
      this.setData({
        recentScans: recentScans.slice(0, 5)
      })
    } catch (error) {
      console.error('Failed to load recent scans:', error)
    }
  },

  // Update today's statistics
  updateTodayStats: function(type) {
    const stats = { ...this.data.todayStats }
    
    stats.scanned += 1
    if (type === 'success') {
      stats.checkedIn += 1
    } else if (type === 'failed') {
      stats.failed += 1
    }

    this.setData({
      todayStats: stats
    })

    // Save to storage
    try {
      const today = new Date().toDateString()
      wx.setStorageSync(`todayStats_${today}`, stats)
    } catch (error) {
      console.error('Failed to save today stats:', error)
    }
  },

  // Load today's statistics
  loadTodayStats: function() {
    try {
      const today = new Date().toDateString()
      const stats = wx.getStorageSync(`todayStats_${today}`) || {
        scanned: 0,
        checkedIn: 0,
        failed: 0
      }
      this.setData({
        todayStats: stats
      })
    } catch (error) {
      console.error('Failed to load today stats:', error)
    }
  },

  // View scan detail
  viewScanDetail: function(e) {
    const scanData = e.currentTarget.dataset.scan
    if (scanData && scanData.fullData) {
      this.showScanResult(scanData.fullData)
    }
  },

  // Logout
  logout: function() {
    wx.showModal({
      title: '确认退出',
      content: '确定要退出登录吗？',
      success: (res) => {
        if (res.confirm) {
          try {
            wx.removeStorageSync('staffInfo')
            wx.removeStorageSync('staffToken')
            wx.redirectTo({
              url: '/pages/staff/login/login'
            })
          } catch (error) {
            console.error('Logout failed:', error)
            wx.showToast({
              title: '退出失败',
              icon: 'error'
            })
          }
        }
      }
    })
  },

  // Utility functions
  formatTime: function(timestamp) {
    const date = new Date(timestamp)
    const hours = date.getHours().toString().padStart(2, '0')
    const minutes = date.getMinutes().toString().padStart(2, '0')
    return `${hours}:${minutes}`
  },

  formatDateTime: function(timestamp) {
    const date = new Date(timestamp)
    const month = (date.getMonth() + 1).toString().padStart(2, '0')
    const day = date.getDate().toString().padStart(2, '0')
    const hours = date.getHours().toString().padStart(2, '0')
    const minutes = date.getMinutes().toString().padStart(2, '0')
    return `${month}/${day} ${hours}:${minutes}`
  }
})
