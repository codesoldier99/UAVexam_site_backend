// pages/public/board/board.js
const app = getApp()

Page({
  data: {
    venues: [],
    updateTime: '',
    timer: null
  },

  onLoad() {
    this.getVenueStatus()
    // 设置定时刷新
    this.startAutoRefresh()
  },

  onUnload() {
    // 清除定时器
    this.stopAutoRefresh()
  },

  onShow() {
    this.getVenueStatus()
    this.startAutoRefresh()
  },

  onHide() {
    this.stopAutoRefresh()
  },

  getVenueStatus() {
    // 模拟数据
    const mockVenues = [
      {
        id: 1,
        name: '理论考场1',
        active: true,
        currentCandidate: '张*',
        waitingCount: 8,
        queueList: [
          { position: 1, name: '李*', scheduledTime: '09:15' },
          { position: 2, name: '王*', scheduledTime: '09:30' },
          { position: 3, name: '赵*', scheduledTime: '09:45' },
          { position: 4, name: '刘*', scheduledTime: '10:00' },
          { position: 5, name: '陈*', scheduledTime: '10:15' }
        ]
      },
      {
        id: 2,
        name: '实操场A',
        active: true,
        currentCandidate: '孙*',
        waitingCount: 12,
        queueList: [
          { position: 1, name: '周*', scheduledTime: '14:15' },
          { position: 2, name: '吴*', scheduledTime: '14:30' },
          { position: 3, name: '郑*', scheduledTime: '14:45' }
        ]
      },
      {
        id: 3,
        name: '实操场B',
        active: false,
        currentCandidate: null,
        waitingCount: 0,
        queueList: []
      },
      {
        id: 4,
        name: '理论考场2',
        active: true,
        currentCandidate: '马*',
        waitingCount: 3,
        queueList: [
          { position: 1, name: '徐*', scheduledTime: '10:00' },
          { position: 2, name: '冯*', scheduledTime: '10:15' }
        ]
      }
    ]
    
    this.setData({
      venues: mockVenues,
      updateTime: this.formatTime(new Date())
    })
    
    // 实际请求
    wx.request({
      url: `${app.globalData.baseUrl}/api/v1/public/venue-status`,
      success: (res) => {
        if (res.data) {
          this.setData({
            venues: res.data,
            updateTime: this.formatTime(new Date())
          })
        }
      }
    })
  },

  startAutoRefresh() {
    // 每15秒刷新一次
    this.data.timer = setInterval(() => {
      this.getVenueStatus()
    }, 15000)
  },

  stopAutoRefresh() {
    if (this.data.timer) {
      clearInterval(this.data.timer)
      this.setData({ timer: null })
    }
  },

  formatTime(date) {
    const hours = date.getHours().toString().padStart(2, '0')
    const minutes = date.getMinutes().toString().padStart(2, '0')
    const seconds = date.getSeconds().toString().padStart(2, '0')
    return `${hours}:${minutes}:${seconds}`
  }
})