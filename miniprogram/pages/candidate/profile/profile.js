// 考生个人信息页面
const { candidateAPI, utils, TokenManager } = require('../../../utils/api')
const app = getApp()

Page({
  data: {
    candidateInfo: {},
    isLoading: true,
    refreshing: false
  },

  onLoad() {
    console.log('考生个人信息页面加载')
    this.loadCandidateInfo()
    
    // 设置自定义tabBar的选中状态
    if (typeof this.getTabBar === 'function' && this.getTabBar()) {
      this.getTabBar().setData({
        selected: 3 // 个人信息是第4个tab，索引为3
      })
    }
  },

  onShow() {
    // 检查登录状态
    if (!TokenManager.hasToken()) {
      wx.showModal({
        title: '提示',
        content: '登录已过期，请重新登录',
        showCancel: false,
        success: () => {
          wx.reLaunch({
            url: '/pages/index/index'
          })
        }
      })
      return
    }
    
    // 页面显示时刷新数据
    this.loadCandidateInfo()
  },

  // 加载考生信息
  async loadCandidateInfo() {
    try {
      const candidateId = wx.getStorageSync('candidateId')
      if (!candidateId) {
        utils.showError('考生信息丢失，请重新登录')
        this.redirectToLogin()
        return
      }

      this.setData({ isLoading: true })

      // 获取考生详细信息
      const response = await candidateAPI.getCandidateDetail(candidateId)
      
      if (response && response.data) {
        const candidateInfo = response.data
        
        // 更新本地存储
        wx.setStorageSync('candidateInfo', candidateInfo)
        
        this.setData({
          candidateInfo: candidateInfo,
          isLoading: false
        })
      } else {
        utils.showError('获取考生信息失败')
        this.setData({ isLoading: false })
      }
      
    } catch (error) {
      console.error('加载考生信息失败:', error)
      this.setData({ isLoading: false })
      
      if (error.message.includes('401')) {
        this.redirectToLogin()
      } else {
        utils.showError(error.message || '获取考生信息失败')
      }
    }
  },

  // 下拉刷新
  async onPullDownRefresh() {
    this.setData({ refreshing: true })
    
    try {
      await this.loadCandidateInfo()
      utils.showSuccess('刷新成功')
    } catch (error) {
      utils.showError('刷新失败')
    } finally {
      this.setData({ refreshing: false })
      wx.stopPullDownRefresh()
    }
  },

  // 跳转到考试安排
  goToSchedule() {
    wx.switchTab({
      url: '/pages/candidate/schedule/schedule'
    })
  },

  // 跳转到二维码
  goToQRCode() {
    wx.switchTab({
      url: '/pages/candidate/qrcode/qrcode'
    })
  },

  // 查看签到历史
  async viewCheckinHistory() {
    try {
      const candidateId = wx.getStorageSync('candidateId')
      const response = await candidateAPI.getCheckinHistory(candidateId)
      
      if (response && response.data) {
        const history = response.data
        
        if (history.length === 0) {
          utils.showError('暂无签到记录')
          return
        }
        
        // 显示签到历史
        const historyText = history.map(item => 
          `${utils.formatTime(item.checkin_time)} - ${item.exam_name || '考试'} - ${item.status === 'success' ? '成功' : '失败'}`
        ).join('\n')
        
        wx.showModal({
          title: '签到历史',
          content: historyText,
          showCancel: false
        })
      }
    } catch (error) {
      console.error('获取签到历史失败:', error)
      utils.showError('获取签到历史失败')
    }
  },

  // 联系客服
  contactService() {
    wx.showModal({
      title: '联系客服',
      content: '如有问题请联系考务人员或拨打客服电话：400-123-4567',
      showCancel: false
    })
  },

  // 退出登录
  logout() {
    wx.showModal({
      title: '确认退出',
      content: '确定要退出登录吗？',
      success: (res) => {
        if (res.confirm) {
          // 清除本地数据
          TokenManager.clearToken()
          wx.removeStorageSync('userType')
          wx.removeStorageSync('candidateInfo')
          wx.removeStorageSync('candidateId')
          
          utils.showSuccess('已退出登录')
          
          // 跳转到首页
          setTimeout(() => {
            wx.reLaunch({
              url: '/pages/index/index'
            })
          }, 1000)
        }
      }
    })
  },

  // 重定向到登录页面
  redirectToLogin() {
    TokenManager.clearToken()
    wx.reLaunch({
      url: '/pages/index/index'
    })
  }
})