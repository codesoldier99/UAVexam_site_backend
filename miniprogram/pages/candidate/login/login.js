// 考生登录页面 - 更新为两步验证流程
const { authAPI, candidateAPI, utils, TokenManager } = require('../../../utils/api')
const app = getApp()

Page({
  data: {
    idNumber: '',
    isLoading: false,
    candidateInfo: null,
    showConfirm: false
  },

  onLoad() {
    console.log('考生登录页面加载')
  },

  // 输入身份证号
  onIdNumberInput(e) {
    this.setData({
      idNumber: e.detail.value.trim(),
      candidateInfo: null,
      showConfirm: false
    })
  },

  // 验证身份证号
  async handleVerifyId() {
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
      // 第一步：验证身份证号是否存在
      const verifyResult = await candidateAPI.getCandidateInfoByIdCard(idNumber)
      
      if (verifyResult && verifyResult.success && verifyResult.data) {
        // 显示考生信息确认
        this.setData({
          candidateInfo: verifyResult.data,
          showConfirm: true
        })
        
        utils.showSuccess('身份验证成功')
      } else {
        utils.showError('未找到该身份证号对应的考生信息')
      }
      
    } catch (error) {
      console.error('身份证验证失败:', error)
      this.handleVerificationError(error)
    } finally {
      this.setData({ isLoading: false })
    }
  },

  // 确认登录
  async handleConfirmLogin() {
    const { idNumber, candidateInfo } = this.data

    this.setData({ isLoading: true })

    try {
      // 第二步：执行实际登录
      const loginResult = await authAPI.candidateLogin(idNumber)
      
      console.log('登录结果:', loginResult)
      
      // 兼容不同的响应结构，并提取考试安排信息
      let accessToken, userInfo, currentExam
      
      if (loginResult && loginResult.success && loginResult.data) {
        // Mock数据结构：{ success: true, data: { access_token, user } }
        accessToken = loginResult.data.access_token
        userInfo = loginResult.data.user
        currentExam = loginResult.data.current_exam
      } else if (loginResult && loginResult.access_token) {
        // 真实API结构：{ access_token, user, current_exam }
        accessToken = loginResult.access_token
        userInfo = loginResult.user
        currentExam = loginResult.current_exam
      }
      
      console.log('提取的考试安排信息:', currentExam)
      
      if (accessToken && userInfo) {
        console.log('开始存储登录信息')
        console.log('accessToken:', accessToken)
        console.log('userInfo:', userInfo)
        console.log('验证阶段的candidateInfo:', candidateInfo)
        
        // 合并验证阶段的完整信息和登录返回的用户信息
        const completeUserInfo = {
          ...userInfo,
          // 保留验证阶段获取的完整信息，特别是身份证号
          id_card: candidateInfo.id_card,
          phone: candidateInfo.phone,
          full_name: candidateInfo.name || candidateInfo.full_name || userInfo.real_name,
          // 确保其他重要字段也被保留
          institution: candidateInfo.institution,
          status: candidateInfo.status
        }
        
        console.log('合并后的完整用户信息:', completeUserInfo)
        
        // 存储token和用户信息
        TokenManager.setToken(accessToken)
        console.log('Token已存储，验证:', TokenManager.getToken())
        
        // 保存完整的用户信息到全局状态和本地存储
        wx.setStorageSync('userType', 'candidate')
        wx.setStorageSync('candidateInfo', completeUserInfo)
        wx.setStorageSync('candidateId', completeUserInfo.id)
        
        // 🆕 保存考试安排信息（用于二维码生成）
        if (currentExam) {
          wx.setStorageSync('currentExam', currentExam)
          console.log('考试安排信息已保存:', currentExam)
        } else {
          console.warn('登录响应中未包含考试安排信息')
        }
        
        console.log('本地存储已保存:')
        console.log('- userType:', wx.getStorageSync('userType'))
        console.log('- candidateInfo:', wx.getStorageSync('candidateInfo'))
        console.log('- candidateId:', wx.getStorageSync('candidateId'))
        
        // 设置全局用户信息
        if (app.setUserInfo) {
          app.setUserInfo('candidate', completeUserInfo)
        }
        
        utils.showSuccess('登录成功')
        
        // 跳转到考生二维码页面（主页）
        setTimeout(() => {
          wx.switchTab({
            url: '/pages/candidate/qrcode/qrcode-enhanced',
            success: () => {
              console.log('成功跳转到二维码页面')
            },
            fail: (error) => {
              console.error('跳转失败:', error)
              // 如果跳转失败，尝试跳转到个人信息页面
              wx.switchTab({
                url: '/pages/candidate/profile/profile'
              })
            }
          })
        }, 1500)
        
      } else {
        console.error('登录响应数据结构异常:', loginResult)
        utils.showError('登录响应数据异常，请重试')
      }
      
    } catch (error) {
      console.error('考生登录失败:', error)
      this.handleLoginError(error)
    } finally {
      this.setData({ isLoading: false })
    }
  },

  // 取消确认，重新输入
  handleCancelConfirm() {
    this.setData({
      candidateInfo: null,
      showConfirm: false,
      idNumber: ''
    })
  },

  // 处理身份证验证错误
  handleVerificationError(error) {
    if (error.message && error.message.includes('CANDIDATE_NOT_FOUND')) {
      utils.showError('未找到该身份证号对应的考生信息，请确认身份证号是否正确')
    } else if (error.message && error.message.includes('网络')) {
      utils.showError('网络连接失败，请检查网络设置')
    } else {
      utils.showError('身份验证失败，请重试')
    }
  },

  // 处理登录错误
  handleLoginError(error) {
    if (error.message && error.message.includes('网络')) {
      utils.showError('网络连接失败，请检查网络设置')
    } else if (error.message && error.message.includes('401')) {
      utils.showError('登录认证失败，请重新验证身份')
      this.setData({
        candidateInfo: null,
        showConfirm: false
      })
    } else {
      utils.showError(error.message || '登录失败，请重试')
    }
  },

  // 返回首页
  goBack() {
    wx.navigateBack()
  }
})