// 全局应用配置
App({
  onLaunch(options) {
    console.log('考点运营管理小程序启动', options)
    
    // 检查用户登录状态
    this.checkLoginStatus()
  },

  onShow(options) {
    console.log('小程序显示', options)
  },

  onHide() {
    console.log('小程序隐藏')
  },

  // 检查登录状态
  checkLoginStatus() {
    const candidateInfo = wx.getStorageSync('candidateInfo')
    const staffInfo = wx.getStorageSync('staffInfo')
    
    if (candidateInfo && candidateInfo.id) {
      this.globalData.userType = 'candidate'
      this.globalData.userInfo = candidateInfo
      this.globalData.isLogin = true
    } else if (staffInfo && staffInfo.id) {
      this.globalData.userType = 'staff'
      this.globalData.userInfo = staffInfo
      this.globalData.isLogin = true
    } else {
      this.globalData.isLogin = false
    }
  },

  // 设置用户信息
  setUserInfo(userType, userInfo) {
    this.globalData.userType = userType
    this.globalData.userInfo = userInfo
    this.globalData.isLogin = true
    
    // 存储到本地
    if (userType === 'candidate') {
      wx.setStorageSync('candidateInfo', userInfo)
    } else if (userType === 'staff') {
      wx.setStorageSync('staffInfo', userInfo)
    }
  },

  // 退出登录
  logout() {
    this.globalData.isLogin = false
    this.globalData.userType = ''
    this.globalData.userInfo = null
    
    // 清除本地存储
    wx.removeStorageSync('candidateInfo')
    wx.removeStorageSync('staffInfo')
  },

  globalData: {
    isLogin: false,
    userType: '', // 'candidate' | 'staff'
    userInfo: null,
    apiBaseUrl: 'http://106.52.214.54'
  }
})