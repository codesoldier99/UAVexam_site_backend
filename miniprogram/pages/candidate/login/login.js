// 考生登录页面
const { authAPI, candidateAPI, utils, TokenManager } = require('../../../utils/api')
const app = getApp()

Page({
  data: {
    idNumber: '',
    isLoading: false
  },

  onLoad() {
    console.log('考生登录页面加载')
  },

  // 输入身份证号
  onIdNumberInput(e) {
    this.setData({
      idNumber: e.detail.value.trim()
    })
  },

  // 登录
  async handleLogin() {
    const { idNumber } = this.data
    
    // 验证身份证号格式
    if (!idNumber) {
      utils.showError('请输入身份证号')
      return
    }
    
    if (!utils.validateIdNumber(idNumber)) {
      utils.showError('请输入正确的身份证号格式')
      return
    }

    // 检查网络状态
    const hasNetwork = await utils.checkNetworkStatus()
    if (!hasNetwork) {
      utils.showError('网络连接失败，请检查网络设置')
      return
    }

    this.setData({ isLoading: true })

    try {
      // 调用身份证登录API
      const loginResult = await authAPI.candidateLogin(idNumber)
      
      if (loginResult && loginResult.access_token && loginResult.candidate_info) {
        // 存储token和用户信息
        TokenManager.setToken(loginResult.access_token)
        
        const candidateInfo = loginResult.candidate_info
        
        // 保存用户信息到全局状态和本地存储
        wx.setStorageSync('userType', 'candidate')
        wx.setStorageSync('candidateInfo', candidateInfo)
        wx.setStorageSync('candidateId', candidateInfo.id)
        
        // 设置全局用户信息
        if (app.setUserInfo) {
          app.setUserInfo('candidate', candidateInfo)
        }
        
        utils.showSuccess('登录成功')
        
        // 跳转到考生个人信息页面
        setTimeout(() => {
          wx.switchTab({
            url: '/pages/candidate/profile/profile'
          })
        }, 1000)
        
      } else {
        utils.showError('登录响应数据异常，请重试')
      }
      
    } catch (error) {
      console.error('考生登录失败:', error)
      
      // 根据错误类型显示不同提示
      if (error.message.includes('网络')) {
        utils.showError('网络连接失败，请检查网络设置')
      } else if (error.message.includes('401') || error.message.includes('认证')) {
        utils.showError('身份证号不存在或未注册')
      } else if (error.message.includes('400')) {
        utils.showError('身份证号格式错误')
      } else {
        utils.showError(error.message || '登录失败，请重试')
      }
    } finally {
      this.setData({ isLoading: false })
    }
  },

  // 返回首页
  goBack() {
    wx.navigateBack()
  }
})