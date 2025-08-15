// app.js
App({
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 登录
    this.checkLogin()
  },

  checkLogin() {
    // 检查是否已登录
    const token = wx.getStorageSync('token')
    const userInfo = wx.getStorageSync('userInfo')
    
    if (token && userInfo) {
      this.globalData.isLoggedIn = true
      this.globalData.userInfo = userInfo
      this.globalData.token = token
    }
  },

  login(idCard) {
    // 模拟登录
    return new Promise((resolve, reject) => {
      wx.request({
        url: `${this.globalData.baseUrl}/api/v1/miniprogram/login`,
        method: 'POST',
        data: {
          id_card: idCard,
          code: '' // 微信登录code
        },
        success: (res) => {
          if (res.data.success) {
            const { token, user } = res.data
            wx.setStorageSync('token', token)
            wx.setStorageSync('userInfo', user)
            this.globalData.isLoggedIn = true
            this.globalData.userInfo = user
            this.globalData.token = token
            resolve(res.data)
          } else {
            reject(res.data.message)
          }
        },
        fail: reject
      })
    })
  },

  logout() {
    wx.removeStorageSync('token')
    wx.removeStorageSync('userInfo')
    this.globalData.isLoggedIn = false
    this.globalData.userInfo = null
    this.globalData.token = null
  },

  globalData: {
    userInfo: null,
    token: null,
    isLoggedIn: false,
    baseUrl: 'http://localhost:8000', // 后端API地址
    userType: 'candidate' // candidate | staff
  }
})