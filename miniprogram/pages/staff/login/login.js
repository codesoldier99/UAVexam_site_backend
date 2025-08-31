// 工作人员登录页面
const { authAPI, utils, TokenManager } = require('../../../utils/api')
const app = getApp()

Page({
  data: {
    username: '',
    password: '',
    isLoading: false,
    showPassword: false,
    rememberMe: false,
    showSuccess: false,
    inputFocused: false,
    usernameFocused: false,
    passwordFocused: false
  },

  onLoad() {
    console.log('工作人员登录页面加载')
  },

  // 输入框获得焦点
  onInputFocus(e) {
    const field = e.currentTarget.dataset.field
    if (field) {
      this.setData({
        [field]: true
      })
    }
  },

  // 输入框失去焦点
  onInputBlur(e) {
    const field = e.currentTarget.dataset.field
    if (field) {
      this.setData({
        [field]: false
      })
    }
  },

  // 切换记住密码选项
  toggleRemember() {
    this.setData({
      rememberMe: !this.data.rememberMe
    })
  },

  // 输入用户名 (Staff ID)
  onStaffIdInput(e) {
    this.setData({
      username: e.detail.value.trim()
    })
  },

  // 输入用户名 (兼容性保留)
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

  // 切换密码显示/隐藏 (WXML中使用的函数名)
  togglePassword() {
    this.setData({
      showPassword: !this.data.showPassword
    })
  },

  // 记住我选项变化
  onRememberChange(e) {
    this.setData({
      rememberMe: e.detail.value.length > 0
    })
  },

  // 忘记密码
  forgotPassword() {
    wx.showToast({
      title: '请联系系统管理员重置密码',
      icon: 'none',
      duration: 2000
    })
  },

  // 联系支持
  contactSupport() {
    wx.showToast({
      title: '技术支持: 400-123-4567',
      icon: 'none',
      duration: 3000
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
      
      console.log('工作人员登录结果:', loginResult)
      
      // 兼容不同的响应结构
      let accessToken
      
      if (loginResult && loginResult.success && loginResult.data && loginResult.data.access_token) {
        // Mock数据结构：{ success: true, data: { access_token } }
        accessToken = loginResult.data.access_token
      } else if (loginResult && loginResult.access_token) {
        // 真实API结构：{ access_token }
        accessToken = loginResult.access_token
      }
      
      if (accessToken) {
        // 存储token
        TokenManager.setToken(accessToken)
        
        // 获取用户详细信息
        const userInfo = await authAPI.getCurrentUser()
        
        console.log('用户信息结果:', userInfo)
        
        // 兼容不同的用户信息响应结构
        let staffInfo
        
        if (userInfo && userInfo.success && userInfo.data) {
          // Mock数据结构：{ success: true, data: { ... } }
          staffInfo = userInfo.data
        } else if (userInfo && userInfo.id) {
          // 真实API结构：直接返回用户信息
          staffInfo = userInfo
        }
        
        console.log('解析后的用户信息:', staffInfo)
        
        if (staffInfo) {
          // 打印角色信息用于调试
          console.log('用户角色:', staffInfo.role)
          console.log('用户类型:', staffInfo.user_type)
          
          // 验证用户角色 - 支持operator和super_admin角色
          const validRoles = ['operator', 'super_admin']
          const userRole = staffInfo.role || staffInfo.user_type
          
          if (!validRoles.includes(userRole)) {
            console.log('角色验证失败，当前角色:', userRole, '有效角色:', validRoles)
            utils.showError('您没有工作人员权限，当前角色: ' + (userRole || '未知'))
            TokenManager.clearToken()
            return
          }
          
          console.log('角色验证通过，角色:', userRole)
          
          // 保存用户信息
          console.log('开始保存用户信息到本地存储')
          wx.setStorageSync('userType', 'staff')
          wx.setStorageSync('staffInfo', staffInfo)
          wx.setStorageSync('staffId', staffInfo.id)
          console.log('用户信息已保存到本地存储')
          
          // 设置全局用户信息
          if (app.setUserInfo) {
            console.log('设置全局用户信息')
            app.setUserInfo('staff', staffInfo)
          }
          
          console.log('显示登录成功提示')
          utils.showSuccess('登录成功')
          
          // 显示成功动画
          console.log('显示成功动画')
          this.setData({ showSuccess: true })
          
          // 延迟跳转，让用户看到成功动画
          console.log('准备跳转到工作人员扫码页面')
          setTimeout(() => {
            console.log('执行页面跳转')
            wx.redirectTo({
              url: '/pages/staff/scan/scan',
              success: () => {
                console.log('页面跳转成功')
              },
              fail: (error) => {
                console.error('页面跳转失败:', error)
                // 如果跳转失败，尝试跳转到其他页面
                wx.switchTab({
                  url: '/pages/index/index',
                  success: () => {
                    console.log('跳转到首页成功')
                  },
                  fail: (tabError) => {
                    console.error('跳转到首页也失败:', tabError)
                  }
                })
              }
            })
          }, 2000)
        } else {
          console.error('用户信息响应数据结构异常:', userInfo)
          utils.showError('获取用户信息失败')
          TokenManager.clearToken()
        }
        
      } else {
        console.error('登录响应数据结构异常:', loginResult)
        utils.showError('登录响应数据异常')
      }
      
    } catch (error) {
      console.error('工作人员登录失败:', error)
      
      // 根据错误类型显示不同提示
      if (error.message && error.message.includes('网络')) {
        utils.showError('网络连接失败，请检查网络设置')
      } else if (error.message && error.message.includes('401') || error.message && error.message.includes('认证')) {
        utils.showError('用户名或密码错误')
      } else if (error.message && error.message.includes('403')) {
        utils.showError('账号被禁用，请联系管理员')
      } else if (error.message && error.message.includes('400')) {
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
