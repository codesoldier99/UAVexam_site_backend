// 工作人员登录页面
const { authAPI, utils, TokenManager } = require('../../../utils/api')
const app = getApp()

Page({
  data: {
    username: '',
    password: '',
    isLoading: false,
    showPassword: false
  },

  onLoad() {
    console.log('工作人员登录页面加载')
  },

  // 输入用户名
  onUsernameInput(e) {
    this.setData({
      username: e.detail.value.trim()
    })
  },

  // 输入密码
  onPasswordInput(e) {
    this.setData({
      password: e.detail.value
    })
  },

  // 切换密码显示/隐藏
  togglePasswordVisibility() {
    this.setData({
      showPassword: !this.data.showPassword
    })
  },

  // 登录
  async handleLogin() {
    const { username, password } = this.data
    
    // 验证输入
    if (!username) {
      utils.showError('请输入用户名')
      return
    }
    
    if (!password) {
      utils.showError('请输入密码')
      return
    }

    if (username.length < 3) {
      utils.showError('用户名至少3个字符')
      return
    }

    if (password.length < 6) {
      utils.showError('密码至少6个字符')
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
      // 调用工作人员登录API
      const loginResult = await authAPI.staffLogin(username, password)
      
      if (loginResult && loginResult.access_token) {
        // 存储token
        TokenManager.setToken(loginResult.access_token)
        
        // 获取用户详细信息
        const userInfo = await authAPI.getCurrentUser()
        
        if (userInfo && userInfo.data) {
          const staffInfo = userInfo.data
          
          // 验证用户角色
          if (staffInfo.role !== 'staff' && staffInfo.role !== 'exam_admin') {
            utils.showError('您没有工作人员权限')
            TokenManager.clearToken()
            return
          }
          
          // 保存用户信息
          wx.setStorageSync('userType', 'staff')
          wx.setStorageSync('staffInfo', staffInfo)
          wx.setStorageSync('staffId', staffInfo.id)
          
          // 设置全局用户信息
          if (app.setUserInfo) {
            app.setUserInfo('staff', staffInfo)
          }
          
          utils.showSuccess('登录成功')
          
          // 跳转到扫码页面
          setTimeout(() => {
            wx.switchTab({
              url: '/pages/staff/scan/scan'
            })
          }, 1000)
        } else {
          utils.showError('获取用户信息失败')
          TokenManager.clearToken()
        }
        
      } else {
        utils.showError('登录响应数据异常')
      }
      
    } catch (error) {
      console.error('工作人员登录失败:', error)
      
      // 根据错误类型显示不同提示
      if (error.message.includes('网络')) {
        utils.showError('网络连接失败，请检查网络设置')
      } else if (error.message.includes('401') || error.message.includes('认证')) {
        utils.showError('用户名或密码错误')
      } else if (error.message.includes('403')) {
        utils.showError('账号被禁用，请联系管理员')
      } else if (error.message.includes('400')) {
        utils.showError('请求参数错误')
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