// pages/login/login.js
const app = getApp()

Page({
  data: {
    idCard: ''
  },

  onIdCardInput(e) {
    this.setData({
      idCard: e.detail.value
    })
  },

  handleLogin() {
    const { idCard } = this.data
    
    // 验证身份证格式
    if (!this.validateIdCard(idCard)) {
      wx.showToast({
        title: '身份证号格式不正确',
        icon: 'none'
      })
      return
    }

    wx.showLoading({
      title: '登录中...'
    })

    // 获取微信登录code
    wx.login({
      success: (res) => {
        if (res.code) {
          // 调用后端登录接口
          this.doLogin(idCard, res.code)
        }
      },
      fail: () => {
        wx.hideLoading()
        wx.showToast({
          title: '登录失败',
          icon: 'none'
        })
      }
    })
  },

  doLogin(idCard, code) {
    // 模拟登录请求
    setTimeout(() => {
      wx.hideLoading()
      
      // 保存登录信息
      wx.setStorageSync('userInfo', {
        name: '张三',
        idCard: idCard,
        type: 'candidate'
      })
      wx.setStorageSync('token', 'mock-token-123')
      
      app.globalData.isLoggedIn = true
      app.globalData.userType = 'candidate'
      
      wx.showToast({
        title: '登录成功',
        icon: 'success'
      })
      
      // 跳转到首页
      setTimeout(() => {
        wx.switchTab({
          url: '/pages/candidate/home/home'
        })
      }, 1500)
    }, 1000)
  },

  validateIdCard(idCard) {
    // 简单的身份证格式验证
    const reg = /^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$/
    return reg.test(idCard)
  },

  goToStaffLogin() {
    wx.navigateTo({
      url: '/pages/staff/scan/scan'
    })
  }
})