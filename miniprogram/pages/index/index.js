// 首页 - 角色选择页面
const app = getApp()

Page({
  data: {
    userType: '',
    isLogin: false
  },

  onLoad() {
    console.log('首页加载')
  },

  onShow() {
    // 检查登录状态
    this.checkLoginStatus()
  },

  // 检查登录状态
  checkLoginStatus() {
    const candidateInfo = wx.getStorageSync('candidateInfo')
    const staffInfo = wx.getStorageSync('staffInfo')
    
    if (candidateInfo && candidateInfo.id) {
      // 考生已登录，跳转到二维码页面
      wx.switchTab({
        url: '/pages/candidate/qrcode/qrcode'
      })
    } else if (staffInfo && staffInfo.id) {
      // 考务人员已登录，跳转到扫码页面
      wx.navigateTo({
        url: '/pages/staff/scan/scan'
      })
    } else {
      // 未登录，显示角色选择
      this.setData({
        isLogin: false
      })
    }
  },

  // 选择考生登录
  selectCandidate() {
    wx.navigateTo({
      url: '/pages/candidate/login/login'
    })
  },

  // 选择考务人员登录
  selectStaff() {
    wx.navigateTo({
      url: '/pages/staff/login/login'
    })
  },

  // 查看公共看板
  viewDashboard() {
    wx.switchTab({
      url: '/pages/public/dashboard/dashboard'
    })
  }
})