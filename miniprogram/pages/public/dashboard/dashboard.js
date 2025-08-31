Page({
  data: {
    // 统计数据
    totalExams: 0,
    totalCandidates: 0,
    completedExams: 0,
    ongoingExams: 0,
    
    // 实时状态
    realtimeStatus: 'online', // online, offline
    
    // 进行中的考试列表
    ongoingExamsList: [],
    
    // 今日考试
    todayDate: '',
    todayExams: [],
    
    // 加载状态
    isLoading: false
  },

  onLoad() {
    console.log('Dashboard页面加载 - 使用新的简化版本')
    this.initData()
    this.loadDashboardData()
    
    // 设置自定义tabBar的选中状态
    if (typeof this.getTabBar === 'function' && this.getTabBar()) {
      this.getTabBar().setData({
        selected: 2 // 实时看板是第3个tab，索引为2
      })
    }
  },

  onShow() {
    console.log('Dashboard页面显示')
    this.refreshData()
  },

  // 初始化数据
  initData() {
    const today = new Date()
    const todayStr = `${today.getFullYear()}年${today.getMonth() + 1}月${today.getDate()}日`
    this.setData({
      todayDate: todayStr
    })
    console.log('初始化数据完成，今日日期:', todayStr)
  },

  // 加载看板数据
  async loadDashboardData() {
    console.log('开始加载简化版看板数据...')
    this.setData({ isLoading: true })
    
    try {
      // 模拟API调用延迟
      await this.delay(800)
      
      // 加载统计数据
      await this.loadStatistics()
      
      // 加载进行中的考试
      await this.loadOngoingExams()
      
      // 加载今日考试
      await this.loadTodayExams()
      
      console.log('✅ 简化版看板数据加载完成')
      
    } catch (error) {
      console.error('加载数据失败:', error)
      wx.showToast({
        title: '数据加载失败',
        icon: 'error'
      })
    } finally {
      this.setData({ isLoading: false })
    }
  },

  // 加载统计数据
  async loadStatistics() {
    console.log('加载统计数据...')
    // 模拟从API获取统计数据
    const stats = {
      totalExams: 156,
      totalCandidates: 2847,
      completedExams: 89,
      ongoingExams: 12
    }
    
    this.setData(stats)
    console.log('统计数据加载完成:', stats)
  },

  // 加载进行中的考试
  async loadOngoingExams() {
    console.log('加载进行中的考试...')
    const ongoingExams = [
      {
        id: 1,
        name: '2024年春季英语四级考试',
        startTime: '09:00',
        endTime: '11:20',
        location: '教学楼A座101-105',
        progress: 65,
        currentParticipants: 156,
        totalParticipants: 240
      },
      {
        id: 2,
        name: '计算机二级等级考试',
        startTime: '14:00',
        endTime: '16:00',
        location: '机房B座201-203',
        progress: 32,
        currentParticipants: 89,
        totalParticipants: 180
      },
      {
        id: 3,
        name: '会计从业资格考试',
        startTime: '10:30',
        endTime: '12:00',
        location: '综合楼C座301',
        progress: 78,
        currentParticipants: 67,
        totalParticipants: 85
      }
    ]
    
    this.setData({
      ongoingExamsList: ongoingExams
    })
    console.log('进行中的考试加载完成，数量:', ongoingExams.length)
  },

  // 加载今日考试
  async loadTodayExams() {
    console.log('加载今日考试...')
    const todayExams = [
      {
        id: 1,
        time: '08:30',
        name: '英语四级考试',
        location: '教学楼A座',
        participants: 240,
        status: 'ongoing',
        statusText: '进行中'
      },
      {
        id: 2,
        time: '10:00',
        name: '数学竞赛初赛',
        location: '教学楼B座',
        participants: 156,
        status: 'completed',
        statusText: '已完成'
      },
      {
        id: 3,
        time: '14:00',
        name: '计算机二级考试',
        location: '机房B座',
        participants: 180,
        status: 'ongoing',
        statusText: '进行中'
      },
      {
        id: 4,
        time: '16:30',
        name: '物理实验考核',
        location: '实验楼D座',
        participants: 95,
        status: 'pending',
        statusText: '待开始'
      },
      {
        id: 5,
        time: '19:00',
        name: '英语口语测试',
        location: '语音室E座',
        participants: 68,
        status: 'pending',
        statusText: '待开始'
      }
    ]
    
    this.setData({
      todayExams: todayExams
    })
    console.log('今日考试加载完成，数量:', todayExams.length)
  },

  // 刷新数据
  async refreshData() {
    console.log('刷新数据...')
    if (this.data.isLoading) {
      console.log('正在加载中，跳过刷新')
      return
    }
    
    wx.showLoading({
      title: '刷新中...'
    })
    
    try {
      await this.loadDashboardData()
      wx.showToast({
        title: '刷新成功',
        icon: 'success'
      })
      console.log('数据刷新成功')
    } catch (error) {
      console.error('刷新失败:', error)
      wx.showToast({
        title: '刷新失败',
        icon: 'error'
      })
    } finally {
      wx.hideLoading()
    }
  },

  // 导出报告
  exportReport() {
    console.log('导出报告')
    wx.showModal({
      title: '导出报告',
      content: '是否导出今日考试数据报告？',
      success: (res) => {
        if (res.confirm) {
          wx.showLoading({
            title: '导出中...'
          })
          
          // 模拟导出过程
          setTimeout(() => {
            wx.hideLoading()
            wx.showToast({
              title: '导出成功',
              icon: 'success'
            })
            console.log('报告导出完成')
          }, 2000)
        }
      }
    })
  },

  // 查看系统设置
  viewSettings() {
    console.log('查看系统设置')
    wx.showToast({
      title: '功能开发中',
      icon: 'none'
    })
  },

  // 查看帮助
  viewHelp() {
    console.log('查看帮助')
    wx.showModal({
      title: '帮助中心',
      content: '如需帮助，请联系系统管理员\n电话：400-123-4567\n邮箱：support@exam.com',
      showCancel: false,
      confirmText: '知道了'
    })
  },

  // 工具函数：延迟
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
  },

  // 页面分享
  onShareAppMessage() {
    return {
      title: '考试管理系统 - 实时看板',
      path: '/pages/public/dashboard/dashboard'
    }
  },

  // 下拉刷新
  async onPullDownRefresh() {
    console.log('下拉刷新')
    await this.refreshData()
    wx.stopPullDownRefresh()
  },

  // 页面滚动
  onPageScroll(e) {
    // 可以在这里添加滚动相关的逻辑
  },

  // 页面卸载
  onUnload() {
    console.log('Dashboard页面卸载')
    // 清理定时器等资源
  }
})