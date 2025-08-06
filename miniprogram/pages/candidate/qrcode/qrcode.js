// 考生二维码页面
const { candidateAPI, qrcodeAPI, utils } = require('../../../utils/api')
const app = getApp()

Page({
  data: {
    candidateInfo: null,
    qrCodeUrl: '',
    qrData: null,
    nextSchedule: null,
    isLoading: false,
    refreshing: false,
    autoRefreshTimer: null
  },

  onLoad() {
    console.log('QRCode page loaded')
    this.loadCandidateData()
    
    // 设置自定义tabBar的选中状态
    if (typeof this.getTabBar === 'function' && this.getTabBar()) {
      this.getTabBar().setData({
        selected: 0 // 二维码是第1个tab，索引为0
      })
    }
  },

  onShow() {
    // 每次显示页面时刷新二维码
    if (this.data.candidateInfo) {
      this.refreshQRCode()
      this.startAutoRefresh()
    }
  },

  onHide() {
    // 页面隐藏时停止自动刷新
    this.stopAutoRefresh()
  },

  onUnload() {
    // 页面卸载时停止自动刷新
    this.stopAutoRefresh()
  },

  // 检查登录状态并初始化
  checkLoginAndInit() {
    const candidateInfo = wx.getStorageSync('candidateInfo')
    
    if (!candidateInfo || !candidateInfo.id) {
      // 未登录，跳转到登录页面
      wx.redirectTo({
        url: '/pages/candidate/login/login'
      })
      return
    }

    this.setData({
      candidateInfo: candidateInfo
    })

    // 获取考生日程并生成二维码
    this.loadScheduleAndQRCode()
  },

  // 加载日程并生成二维码
  async loadScheduleAndQRCode() {
    this.setData({ isLoading: true })

    try {
      // 获取考生的考试安排
      const scheduleResponse = await candidateAPI.getExamSchedule(this.data.candidateInfo.id)
      
      if (scheduleResponse && scheduleResponse.data && scheduleResponse.data.length > 0) {
        // 找到下一个待签到的日程
        const nextSchedule = this.findNextSchedule(scheduleResponse.data)
        
        if (nextSchedule) {
          this.setData({ nextSchedule })
          await this.generateQRCode(nextSchedule.id)
        } else {
          // 没有待进行的日程
          this.setData({
            nextSchedule: null,
            qrCodeUrl: '',
            qrData: null
          })
        }
      } else {
        // 没有日程安排
        this.setData({
          nextSchedule: null,
          qrCodeUrl: '',
          qrData: null
        })
      }
    } catch (error) {
      console.error('加载日程失败:', error)
      utils.showError('加载日程失败，请重试')
    } finally {
      this.setData({ isLoading: false })
    }
  },

  // 查找下一个待签到的日程
  findNextSchedule(schedules) {
    // 筛选出状态为"待签到"的日程，按时间排序
    const waitingSchedules = schedules
      .filter(schedule => schedule.status === '待签到' || schedule.status === 'waiting')
      .sort((a, b) => new Date(a.exam_time) - new Date(b.exam_time))
    
    return waitingSchedules.length > 0 ? waitingSchedules[0] : null
  },

  // 生成二维码
  async generateQRCode(scheduleId) {
    try {
      const qrResponse = await qrcodeAPI.generateScheduleQR(scheduleId)
      
      if (qrResponse && qrResponse.qr_url) {
        this.setData({
          qrCodeUrl: qrResponse.qr_url,
          qrData: qrResponse.qr_data
        })
      } else {
        utils.showError('生成二维码失败')
      }
    } catch (error) {
      console.error('生成二维码失败:', error)
      utils.showError('生成二维码失败，请重试')
    }
  },

  // 手动刷新二维码
  async refreshQRCode() {
    if (this.data.refreshing) return
    
    this.setData({ refreshing: true })
    await this.loadScheduleAndQRCode()
    this.setData({ refreshing: false })
  },

  // 开始自动刷新
  startAutoRefresh() {
    this.stopAutoRefresh() // 先停止之前的定时器
    
    // 每30秒自动刷新一次
    this.data.autoRefreshTimer = setInterval(() => {
      this.refreshQRCode()
    }, 30000)
  },

  // 停止自动刷新
  stopAutoRefresh() {
    if (this.data.autoRefreshTimer) {
      clearInterval(this.data.autoRefreshTimer)
      this.data.autoRefreshTimer = null
    }
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.refreshQRCode().then(() => {
      wx.stopPullDownRefresh()
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