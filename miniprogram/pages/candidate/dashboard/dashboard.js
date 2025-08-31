// 引入API和工具函数
const { realtimeAPI, candidateAPI, utils } = require('../../../utils/api')

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
    console.log('考生Dashboard页面加载 - 使用新的优化版本')
    this.initData()
    this.loadDashboardData()
    
    // 设置自定义tabBar的选中状态
    if (typeof this.getTabBar === 'function' && this.getTabBar()) {
      this.getTabBar().setData({
        selected: 2 // 实时看板是第3个tab，索引为2
      })
    }
    
    // 启动自动刷新定时器（每5分钟自动刷新一次）
    this.startAutoRefresh()
  },

  onShow() {
    console.log('考生Dashboard页面显示')
    
    // 检查数据是否需要更新（超过2分钟则刷新）
    const now = Date.now()
    const lastLoadTime = this.lastLoadTime || 0
    const dataExpireTime = 2 * 60 * 1000 // 2分钟
    
    if (now - lastLoadTime > dataExpireTime) {
      console.log('数据已过期，自动刷新')
      this.refreshData()
    } else {
      console.log('数据仍然有效，跳过刷新')
    }
    
    // 重新启动自动刷新
    this.startAutoRefresh()
  },

  onHide() {
    console.log('考生Dashboard页面隐藏')
    // 停止自动刷新
    this.stopAutoRefresh()
  },

  onUnload() {
    console.log('考生Dashboard页面卸载')
    // 清理定时器等资源
    this.stopAutoRefresh()
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
    console.log('开始加载考生看板数据...')
    this.setData({ isLoading: true })
    
    try {
      // 并行加载所有数据
      await Promise.all([
        this.loadPublicBoardData(),
        this.loadExamScheduleData(),
        this.loadExamResultsData()
      ])
      
      // 记录加载时间
      this.lastLoadTime = Date.now()
      console.log('✅ 考生看板数据加载完成')
      
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

  // 启动自动刷新
  startAutoRefresh() {
    // 清除之前的定时器
    this.stopAutoRefresh()
    
    // 设置新的定时器（5分钟）
    this.autoRefreshTimer = setInterval(() => {
      console.log('自动刷新数据...')
      this.silentRefresh()
    }, 5 * 60 * 1000) // 5分钟
    
    console.log('自动刷新定时器已启动')
  },

  // 停止自动刷新
  stopAutoRefresh() {
    if (this.autoRefreshTimer) {
      clearInterval(this.autoRefreshTimer)
      this.autoRefreshTimer = null
      console.log('自动刷新定时器已停止')
    }
  },

  // 静默刷新（不显示加载提示）
  async silentRefresh() {
    if (this.data.isLoading) {
      console.log('正在加载中，跳过静默刷新')
      return
    }
    
    try {
      console.log('执行静默刷新...')
      await this.loadDashboardData()
      console.log('静默刷新完成')
    } catch (error) {
      console.error('静默刷新失败:', error)
      // 静默刷新失败不显示错误提示
    }
  },

  // 加载公共看板数据
  async loadPublicBoardData() {
    try {
      console.log('🚀 开始调用公共看板API: /api/v1/wechat/dashboard')
      const response = await realtimeAPI.getPublicBoard()
      
      console.log('📊 公共看板API完整响应:')
      console.log('响应类型:', typeof response)
      console.log('响应内容:', JSON.stringify(response, null, 2))
      
      // 处理实际的API响应格式
      if (response && typeof response === 'object') {
        console.log('✅ 响应数据有效，开始解析...')
        
        // 从statistics字段获取统计数据
        if (response.statistics) {
          const stats = response.statistics
          console.log('📈 统计数据详情:', JSON.stringify(stats, null, 2))
          
          // 根据实际返回的字段名进行映射
          const mappedStats = {
            totalExams: stats.total_scheduled || stats.total_exams || stats.totalExams || 0,
            totalCandidates: stats.checked_in || stats.total_candidates || stats.totalCandidates || 0,
            completedExams: stats.completed || stats.completed_exams || stats.completedExams || 0,
            ongoingExams: stats.in_progress || stats.ongoing_exams || stats.ongoingExams || 0
          }
          
          console.log('🔄 映射后的统计数据:', mappedStats)
          this.setData(mappedStats)
          console.log('✅ 统计数据更新成功')
        } else {
          console.log('⚠️ 未找到statistics字段')
        }
        
        // 从system_status获取系统状态
        if (response.system_status) {
          const systemStatus = response.system_status
          console.log('🔧 系统状态详情:', JSON.stringify(systemStatus, null, 2))
          
          this.setData({
            realtimeStatus: (systemStatus.status === 'normal' || systemStatus.online) ? 'online' : 'offline'
          })
          console.log('✅ 系统状态更新成功')
        } else {
          console.log('⚠️ 未找到system_status字段，使用默认状态')
          this.setData({ realtimeStatus: 'online' })
        }
        
        // 从venues获取场地信息
        if (response.venues && Array.isArray(response.venues)) {
          console.log('🏢 场地信息详情:', JSON.stringify(response.venues, null, 2))
          console.log('场地数量:', response.venues.length)
        } else {
          console.log('⚠️ 未找到venues字段或不是数组')
        }
        
        // 从announcements获取公告信息
        if (response.announcements && Array.isArray(response.announcements)) {
          console.log('📢 公告信息详情:', JSON.stringify(response.announcements, null, 2))
          console.log('公告数量:', response.announcements.length)
        } else {
          console.log('⚠️ 未找到announcements字段或不是数组')
        }
        
        console.log('✅ 公共看板数据处理完成')
        return
      } else {
        console.log('❌ 响应数据无效或为空')
      }
      
      // 如果没有有效数据，使用默认数据
      console.warn('公共看板API返回数据无效，使用默认数据')
      this.setDefaultStatistics()
      
    } catch (error) {
      console.error('加载公共看板数据失败:', error)
      // 使用默认数据
      this.setDefaultStatistics()
    }
  },

  // 加载考试日程数据
  async loadExamScheduleData() {
    try {
      console.log('调用考试日程API...')
      const response = await candidateAPI.getExamSchedule()
      console.log('考试日程API响应:', response)
      
      // 处理实际的API响应格式
      if (response && typeof response === 'object') {
        let allExams = []
        
        // 合并即将开始的考试和已完成的考试
        if (response.upcoming_exams && Array.isArray(response.upcoming_exams)) {
          allExams = allExams.concat(response.upcoming_exams)
          console.log('即将开始的考试:', response.upcoming_exams.length, '个')
        }
        
        if (response.completed_exams && Array.isArray(response.completed_exams)) {
          allExams = allExams.concat(response.completed_exams)
          console.log('已完成的考试:', response.completed_exams.length, '个')
        }
        
        if (allExams.length > 0) {
          console.log('📋 开始处理考试数据，总数:', allExams.length)
          
          // 先显示所有考试（不限制今日），然后再优化
          const allExamsList = allExams
            .map(exam => {
              console.log('🔍 处理考试:', JSON.stringify(exam, null, 2))
              
              // 确保location是字符串而不是对象
              let location = '未知地点'
              if (exam.venue_name && typeof exam.venue_name === 'string') {
                location = exam.venue_name
              } else if (exam.venue && typeof exam.venue === 'string') {
                location = exam.venue
              } else if (exam.location && typeof exam.location === 'string') {
                location = exam.location
              }
              
              return {
                id: exam.id || Math.random(),
                time: this.formatTime(exam.start_time || exam.startTime || exam.exam_time),
                name: exam.exam_name || exam.name || exam.title || '未知考试',
                location: location,
                participants: exam.total_candidates || exam.totalCandidates || exam.participants || 0,
                status: this.getExamStatus(exam.start_time || exam.startTime, exam.end_time || exam.endTime),
                statusText: this.getStatusText(this.getExamStatus(exam.start_time || exam.startTime, exam.end_time || exam.endTime)),
                examDate: this.formatDate(new Date(exam.exam_date || exam.start_time || exam.date))
              }
            })
            .sort((a, b) => {
              // 按日期和时间排序
              if (a.examDate !== b.examDate) {
                return a.examDate.localeCompare(b.examDate)
              }
              return a.time.localeCompare(b.time)
            })
          
          console.log('📅 处理后的考试列表:', JSON.stringify(allExamsList, null, 2))
          
          // 筛选今日考试
          const today = new Date()
          const todayStr = this.formatDate(today)
          const todayExams = allExamsList.filter(exam => exam.examDate === todayStr)
          
          if (todayExams.length > 0) {
            console.log('✅ 找到今日考试:', todayExams.length, '个')
            this.setData({ todayExams })
            return
          } else {
            console.log('⚠️ 今日无考试，显示最近的考试')
            // 如果今日无考试，显示最近的几个考试
            const recentExams = allExamsList.slice(0, 3)
            this.setData({ todayExams: recentExams })
            console.log('📋 显示最近考试:', recentExams.length, '个')
            return
          }
        }
        
        // 从即将开始的考试中筛选出正在进行的考试
        if (response.upcoming_exams && Array.isArray(response.upcoming_exams)) {
          const ongoingExams = response.upcoming_exams
            .filter(exam => {
              const status = this.getExamStatus(exam.start_time || exam.startTime, exam.end_time || exam.endTime)
              return status === 'ongoing'
            })
            .map(exam => ({
              id: exam.id || Math.random(),
              name: exam.exam_name || exam.name || exam.title || '未知考试',
              startTime: this.formatTime(exam.start_time || exam.startTime),
              endTime: this.formatTime(exam.end_time || exam.endTime),
              location: exam.venue_name || exam.venue || exam.location || '未知地点',
              progress: this.calculateProgress(exam.start_time || exam.startTime, exam.end_time || exam.endTime),
              currentParticipants: exam.current_candidates || exam.currentParticipants || 0,
              totalParticipants: exam.total_candidates || exam.totalParticipants || 0
            }))
          
          if (ongoingExams.length > 0) {
            this.setData({ ongoingExamsList: ongoingExams })
            console.log('进行中的考试列表更新成功，数量:', ongoingExams.length)
          }
        }
        
        // 处理summary信息
        if (response.summary) {
          console.log('考试摘要信息:', response.summary)
        }
      }
      
      // 如果没有今日考试或数据为空，使用默认数据
      console.warn('今日无考试安排或数据为空，使用默认数据')
      this.setDefaultTodayExams()
      
    } catch (error) {
      console.error('加载考试日程失败:', error)
      this.setDefaultTodayExams()
    }
  },

  // 加载考试结果统计
  async loadExamResultsData() {
    try {
      console.log('调用考试结果统计API...')
      const response = await candidateAPI.getExamResults()
      
      if (response && response.success && response.data) {
        const results = response.data
        console.log('考试结果统计加载成功:', results)
        // 可以在这里添加个人统计数据的处理
      }
    } catch (error) {
      console.error('加载考试结果统计失败:', error)
      // 不影响主要功能，静默处理
    }
  },

  // 设置默认统计数据
  setDefaultStatistics() {
    console.log('使用默认统计数据')
    this.setData({
      totalExams: 0,
      totalCandidates: 0,
      completedExams: 0,
      ongoingExams: 0,
      ongoingExamsList: [],
      realtimeStatus: 'offline'
    })
  },

  // 设置默认今日考试
  setDefaultTodayExams() {
    console.log('使用默认今日考试数据')
    this.setData({
      todayExams: [{
        id: 0,
        time: '暂无',
        name: '今日暂无考试安排',
        location: '',
        participants: 0,
        status: 'pending',
        statusText: '待安排'
      }]
    })
  },

  // 获取考试状态
  getExamStatus(startTime, endTime) {
    const now = new Date()
    const start = new Date(startTime)
    const end = new Date(endTime)
    
    if (now < start) {
      return 'pending'
    } else if (now >= start && now <= end) {
      return 'ongoing'
    } else {
      return 'completed'
    }
  },

  // 获取状态文本
  getStatusText(status) {
    const statusMap = {
      'pending': '待开始',
      'ongoing': '进行中',
      'completed': '已完成'
    }
    return statusMap[status] || '未知'
  },

  // 计算考试进度
  calculateProgress(startTime, endTime) {
    if (!startTime || !endTime) return 0
    
    const now = new Date()
    const start = new Date(startTime)
    const end = new Date(endTime)
    
    if (now < start) {
      return 0
    } else if (now > end) {
      return 100
    } else {
      const total = end.getTime() - start.getTime()
      const elapsed = now.getTime() - start.getTime()
      return Math.round((elapsed / total) * 100)
    }
  },

  // 格式化时间 (HH:MM)
  formatTime(dateString) {
    if (!dateString) return '--:--'
    const date = new Date(dateString)
    const hour = String(date.getHours()).padStart(2, '0')
    const minute = String(date.getMinutes()).padStart(2, '0')
    return `${hour}:${minute}`
  },

  // 格式化日期 (YYYY-MM-DD)
  formatDate(date) {
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
  },

  // 刷新数据 - 添加节流控制
  async refreshData() {
    console.log('刷新数据...')
    
    // 检查是否正在加载
    if (this.data.isLoading) {
      console.log('正在加载中，跳过刷新')
      return
    }
    
    // 节流控制：限制刷新频率（30秒内只能刷新一次）
    const now = Date.now()
    const lastRefreshTime = this.lastRefreshTime || 0
    const refreshInterval = 30 * 1000 // 30秒
    
    if (now - lastRefreshTime < refreshInterval) {
      const remainingTime = Math.ceil((refreshInterval - (now - lastRefreshTime)) / 1000)
      console.log(`刷新过于频繁，请等待 ${remainingTime} 秒后再试`)
      wx.showToast({
        title: `请等待${remainingTime}秒后再刷新`,
        icon: 'none',
        duration: 2000
      })
      return
    }
    
    try {
      this.lastRefreshTime = now
      await this.loadDashboardData()
      
      wx.showToast({
        title: '数据已更新',
        icon: 'success',
        duration: 1500
      })
      
      console.log('数据刷新成功')
    } catch (error) {
      console.error('刷新失败:', error)
      wx.showToast({
        title: '刷新失败',
        icon: 'error'
      })
    }
  },


  // 工具函数：延迟
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
  },

  // 页面分享
  onShareAppMessage() {
    return {
      title: '考试管理系统 - 实时看板',
      path: '/pages/candidate/dashboard/dashboard'
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

})