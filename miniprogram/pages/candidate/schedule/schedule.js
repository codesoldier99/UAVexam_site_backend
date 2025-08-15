// pages/candidate/schedule/schedule.js
const app = getApp()

Page({
  data: {
    schedules: []
  },

  onLoad() {
    this.getSchedules()
  },

  onPullDownRefresh() {
    this.getSchedules()
  },

  getSchedules() {
    wx.showLoading({
      title: '加载中...'
    })
    
    // 实际请求
    wx.request({
      url: `${app.globalData.baseUrl}/api/v1/schedules/my-schedules`,
      header: {
        'Authorization': `Bearer ${app.globalData.token}`
      },
      success: (res) => {
        if (res.data) {
          const schedules = res.data.map(item => ({
            ...item,
            dateTime: this.formatDateTime(item.exam_date, item.start_time),
            statusText: this.getStatusText(item.status),
            statusType: this.getStatusType(item.status)
          }))
          this.setData({ schedules })
        }
      },
      complete: () => {
        wx.hideLoading()
        wx.stopPullDownRefresh()
      }
    })
    
    // 模拟数据
    const mockSchedules = [
      {
        id: 1,
        activityName: '多旋翼视距内驾驶员理论考试',
        exam_date: '2025-08-16',
        start_time: '09:00',
        venue: '理论考场1',
        status: 'pending',
        queuePosition: null
      },
      {
        id: 2,
        activityName: '多旋翼视距内驾驶员实操考试',
        exam_date: '2025-08-16',
        start_time: '14:00',
        venue: '实操场A',
        status: 'pending',
        queuePosition: 5
      },
      {
        id: 3,
        activityName: '理论补考',
        exam_date: '2025-08-15',
        start_time: '10:00',
        venue: '理论考场2',
        status: 'completed',
        queuePosition: null
      }
    ]
    
    const schedules = mockSchedules.map(item => ({
      ...item,
      dateTime: this.formatDateTime(item.exam_date, item.start_time),
      statusText: this.getStatusText(item.status),
      statusType: this.getStatusType(item.status)
    }))
    
    this.setData({ schedules })
    wx.hideLoading()
    wx.stopPullDownRefresh()
  },

  formatDateTime(date, time) {
    return `${date} ${time}`
  },

  getStatusText(status) {
    const statusMap = {
      'pending': '待签到',
      'checked_in': '已签到',
      'in_progress': '进行中',
      'completed': '已完成',
      'no_show': '缺考',
      'cancelled': '已取消'
    }
    return statusMap[status] || status
  },

  getStatusType(status) {
    const typeMap = {
      'pending': 'warning',
      'checked_in': 'primary',
      'in_progress': 'primary',
      'completed': 'success',
      'no_show': 'danger',
      'cancelled': 'info'
    }
    return typeMap[status] || 'info'
  },

  showQRCode(e) {
    const scheduleId = e.currentTarget.dataset.id
    wx.switchTab({
      url: '/pages/candidate/qrcode/qrcode'
    })
  }
})