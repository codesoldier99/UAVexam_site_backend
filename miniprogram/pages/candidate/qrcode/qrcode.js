// pages/candidate/qrcode/qrcode.js
const app = getApp()
import drawQrcode from '../../../utils/qrcode'

Page({
  data: {
    userInfo: {},
    nextSchedule: null,
    qrCodeData: ''
  },

  onLoad() {
    this.getUserInfo()
    this.getNextSchedule()
  },

  onShow() {
    this.generateQRCode()
  },

  getUserInfo() {
    const userInfo = wx.getStorageSync('userInfo')
    if (userInfo) {
      this.setData({
        userInfo: {
          name: userInfo.name,
          idCard: this.maskIdCard(userInfo.idCard)
        }
      })
    }
  },

  maskIdCard(idCard) {
    if (!idCard || idCard.length < 18) return idCard
    return idCard.substring(0, 6) + '********' + idCard.substring(14)
  },

  getNextSchedule() {
    // 模拟获取下一场考试信息
    wx.request({
      url: `${app.globalData.baseUrl}/api/v1/schedules/my-next`,
      header: {
        'Authorization': `Bearer ${app.globalData.token}`
      },
      success: (res) => {
        if (res.data) {
          this.setData({
            nextSchedule: {
              activityName: res.data.activity_name,
              time: this.formatDateTime(res.data.exam_date, res.data.start_time),
              venue: res.data.venue_name,
              scheduleId: res.data.id
            }
          })
          this.generateQRCode()
        }
      }
    })
    
    // 模拟数据
    this.setData({
      nextSchedule: {
        activityName: '多旋翼视距内驾驶员理论考试',
        time: '2025-08-16 09:00',
        venue: '理论考场1',
        scheduleId: 12345
      }
    })
  },

  generateQRCode() {
    const scheduleId = this.data.nextSchedule?.scheduleId || 'NO_SCHEDULE'
    const qrData = JSON.stringify({
      type: 'candidate',
      scheduleId: scheduleId,
      timestamp: Date.now()
    })
    
    this.setData({ qrCodeData: qrData })
    
    // 生成二维码
    drawQrcode({
      width: 200,
      height: 200,
      canvasId: 'qrcode',
      text: qrData
    })
  },

  refreshQRCode() {
    wx.showLoading({
      title: '刷新中...'
    })
    
    setTimeout(() => {
      this.getNextSchedule()
      this.generateQRCode()
      wx.hideLoading()
      wx.showToast({
        title: '刷新成功',
        icon: 'success'
      })
    }, 500)
  },

  formatDateTime(date, time) {
    return `${date} ${time}`
  }
})