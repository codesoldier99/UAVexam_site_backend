const { realtimeAPI } = require('../../../utils/api')
const { loading } = require('../../../utils/loading')
const { perf } = require('../../../utils/performance')

Page({
  data: {
    loading: false,
    updateTime: '',
    
    // Enhanced statistics
    stats: {
      totalVenues: 0,
      activeExams: 0,
      todaySchedules: 0,
      checkedInCandidates: 0,
      totalCandidates: 0,
      completedExams: 0,
      onlineStaff: 0,
      pendingIssues: 0
    },
    
    // Venue management
    venues: [],
    selectedVenue: null,
    showVenueDetail: false,
    
    // Real-time activities
    recentActivities: [],
    alerts: [],
    
    // Staff monitoring
    staffStatus: [],
    staffList: [],
    onlineStaffCount: 0,
    
    // Exam monitoring
    examProgress: [],
    
    // Filter and view options
    viewMode: 'overview', // overview, venues, staff, exams
    alertFilter: 'all', // all, high, medium, low
    
    // Auto refresh settings
    autoRefresh: true,
    refreshInterval: 30000
  },

  onLoad() {
    console.log('Dashboard page loaded')
    this.loadDashboardData()
    this.startAutoRefresh()
    
    // 设置自定义tabBar的选中状态
    if (typeof this.getTabBar === 'function' && this.getTabBar()) {
      this.getTabBar().setData({
        selected: 2 // 实时看板是第3个tab，索引为2
      })
    }
  },

  onShow() {
    this.refreshData()
  },

  onUnload() {
    this.stopAutoRefresh()
  },

  onHide() {
    // Stop auto refresh when page is hidden
    this.stopAutoRefresh()
  },

  // Load comprehensive dashboard data
  async loadDashboardData() {
    const loadingTasks = []
    
    try {
      // 使用批量加载管理器
      const tasks = [
        () => this.loadVenuesData(),
        () => this.loadSchedulesData(),
        () => this.loadStaffData(),
        () => this.loadExamData(),
        () => this.loadAlertsData()
      ]

      const results = await loading.batch(tasks, {
        concurrent: 3,
        showProgress: false
      })

      // 提取成功的结果
      const [venuesRes, schedulesRes, staffRes, examRes, alertsRes] = results.map(result => 
        result.success ? result.data : []
      )

      // Process and combine all data
      const venues = this.processVenuesData(venuesRes)
      const stats = this.calculateEnhancedStats(venues, schedulesRes, staffRes, examRes)
      const recentActivities = await this.getRecentActivities()
      const staffStatus = this.processStaffData(staffRes)
      const examProgress = this.processExamData(examRes)
      const alerts = this.processAlertsData(alertsRes)
      
      // Calculate online staff count
      const onlineStaffCount = staffStatus.filter(staff => staff.status === 'online' || staff.status === 'active').length

      this.setData({
        venues,
        stats,
        recentActivities,
        staffStatus,
        staffList: staffStatus,
        onlineStaffCount,
        examProgress,
        alerts,
        updateTime: this.formatDateTime(new Date()),
        loading: false
      })

      // 隐藏页面加载状态
      loading.hidePage('dashboard')
      
      // 记录页面加载性能
      if (this.perfId) {
        const loadTime = Date.now() - this.pageLoadStart
        perf.end(this.perfId, { 
          dataLoaded: true, 
          venuesCount: venues.length,
          activitiesCount: recentActivities.length 
        })
        perf.recordPage('/pages/public/dashboard/dashboard', loadTime, 0, JSON.stringify(this.data).length)
      }

    } catch (error) {
      console.error('Dashboard数据加载失败:', error)
      
      // 隐藏加载状态
      loading.hidePage('dashboard')
      
      // 记录错误
      perf.recordError(error, { page: 'dashboard', action: 'loadData' })
      
      this.setData({ loading: false })
      
      // 使用Mock数据作为后备方案
      console.log('尝试使用Mock数据作为后备方案...')
      this.loadMockDashboardData()
    }
  },

  // Load Mock dashboard data as fallback
  async loadMockDashboardData() {
    try {
      console.log('正在加载Mock数据...')
      
      // 直接使用Mock数据管理器
      const mockManager = require('../../../mock-data/index.js')
      
      // 获取Mock数据
      const venueResponse = await mockManager.getMockResponse('/realtime/venue-status', 'GET')
      const statusResponse = await mockManager.getMockResponse('/realtime/status', 'GET')
      const notificationResponse = await mockManager.getMockResponse('/realtime/notifications', 'GET')
      
      // 处理Mock数据
      const venues = this.processMockVenuesData(venueResponse?.data?.rooms || [])
      const stats = this.calculateMockStats(venues, statusResponse?.data || {})
      const recentActivities = this.processMockActivities(notificationResponse?.data?.notifications || [])
      const staffStatus = this.processMockStaffData(statusResponse?.data?.staff || [])
      const examProgress = this.processMockExamData(statusResponse?.data?.exams || [])
      const alerts = this.processMockAlertsData(statusResponse?.data?.alerts || [])
      
      // 计算在线工作人员数量
      const onlineStaffCount = staffStatus.filter(staff => staff.status === 'online' || staff.status === 'active').length

      this.setData({
        venues,
        stats,
        recentActivities,
        staffStatus,
        staffList: staffStatus,
        onlineStaffCount,
        examProgress,
        alerts,
        updateTime: this.formatDateTime(new Date()),
        loading: false
      })

      console.log('✅ Mock数据加载成功')
      wx.showToast({
        title: '使用演示数据',
        icon: 'success',
        duration: 2000
      })

    } catch (error) {
      console.error('Mock数据加载失败:', error)
      this.setData({ loading: false })
      wx.showToast({
        title: '数据加载失败',
        icon: 'error',
        duration: 2000
      })
    }
  },

  // Process mock venues data
  processMockVenuesData(venuesData) {
    return venuesData.map(venue => {
      const status = this.getVenueStatus(venue)
      const checkedIn = venue.checked_in_count || 0
      const capacity = venue.capacity || 30
      const progressPercent = capacity > 0 ? Math.round((checkedIn / capacity) * 100) : 0
      
      return {
        id: venue.id,
        name: venue.name || `考场${venue.id}`,
        capacity: capacity,
        status: status.status,
        statusText: status.text,
        currentExam: venue.current_exam || null,
        examTime: venue.exam_time ? this.formatTime(new Date(venue.exam_time)) : null,
        checkedIn: checkedIn,
        totalCandidates: venue.total_candidates || 0,
        progressPercent: progressPercent
      }
    })
  },

  // Calculate mock statistics
  calculateMockStats(venues, statusData) {
    const activeVenues = venues.filter(v => v.status === 'busy' || v.status === 'active').length
    const totalCandidates = venues.reduce((sum, v) => sum + (v.totalCandidates || 0), 0)
    const checkedInCandidates = venues.reduce((sum, v) => sum + (v.checkedIn || 0), 0)
    
    return {
      totalVenues: venues.length,
      activeExams: activeVenues,
      todaySchedules: statusData.schedules?.length || 0,
      checkedInCandidates: checkedInCandidates,
      totalCandidates: totalCandidates,
      completedExams: statusData.exams?.filter(e => e.status === 'completed').length || 0,
      onlineStaff: statusData.staff?.filter(s => s.status === 'online' || s.status === 'active').length || 0,
      pendingIssues: statusData.alerts?.filter(a => a.priority === 'high').length || 0
    }
  },

  // Process mock activities
  processMockActivities(activities) {
    return activities.map(activity => ({
      id: activity.id,
      type: this.getActivityType(activity.type),
      icon: this.getActivityIcon(activity.type),
      text: activity.message,
      time: this.formatTime(new Date(activity.created_at))
    }))
  },

  // Process mock staff data
  processMockStaffData(staffData) {
    return staffData.map(staff => ({
      id: staff.id,
      name: staff.name,
      role: staff.role || '监考员',
      status: staff.status || 'offline',
      statusText: this.getStaffStatusText(staff.status || 'offline'),
      location: staff.current_venue || '未分配',
      venue: staff.current_venue || '未分配',
      lastActivity: staff.last_activity ? this.formatTime(new Date(staff.last_activity)) : '无记录',
      tasksCompleted: staff.tasks_completed || 0,
      avatar: staff.avatar || staff.name.charAt(0)
    }))
  },

  // Process mock exam data
  processMockExamData(examData) {
    return examData.map(exam => ({
      id: exam.id,
      name: exam.name,
      venue: exam.venue,
      startTime: exam.start_time ? this.formatTime(new Date(exam.start_time)) : '待定',
      endTime: exam.end_time ? this.formatTime(new Date(exam.end_time)) : '待定',
      status: exam.status || 'scheduled',
      statusText: this.getExamStatusText(exam.status || 'scheduled'),
      progress: exam.progress || 0,
      totalCandidates: exam.total_candidates || 0,
      checkedIn: exam.checked_in || 0,
      completed: exam.completed || 0
    }))
  },

  // Process mock alerts data
  processMockAlertsData(alertsData) {
    return alertsData.map(alert => ({
      id: alert.id,
      type: alert.type,
      typeText: this.getAlertTypeText(alert.type),
      priority: alert.priority || 'medium',
      priorityText: this.getAlertPriorityText(alert.priority || 'medium'),
      title: alert.title,
      message: alert.message,
      venue: alert.venue,
      timestamp: alert.created_at ? this.formatTime(new Date(alert.created_at)) : '刚刚',
      resolved: alert.resolved || false
    }))
  },

  // Load venues data - 直接调用API，不使用模拟数据
  async loadVenuesData() {
    const response = await realtimeAPI.getVenueStatus()
    // 处理返回的数据结构，现在直接返回数组
    if (response.data && Array.isArray(response.data)) {
      return response.data.map(venue => ({
        id: venue.id,
        name: venue.name,
        capacity: venue.capacity,
        current_candidates: venue.checked_in_count,
        checked_in_count: venue.checked_in_count,
        total_candidates: venue.total_candidates,
        current_exam: venue.current_exam,
        exam_time: venue.exam_time,
        status: venue.status,
        temperature: venue.temperature,
        humidity: venue.humidity,
        next_exam_time: venue.next_exam_time
      }))
    }
    return []
  },

  // Load schedules data - 直接调用API，不使用模拟数据
  async loadSchedulesData() {
    const response = await realtimeAPI.getRealtimeStatus()
    return response.data?.schedules || []
  },

  // Load staff data - 直接调用API，不使用模拟数据
  async loadStaffData() {
    const response = await realtimeAPI.getRealtimeStatus()
    return response.data?.staff || []
  },

  // Load exam data - 直接调用API，不使用模拟数据
  async loadExamData() {
    const response = await realtimeAPI.getRealtimeStatus()
    return response.data?.exams || []
  },

  // Load alerts data - 直接调用API，不使用模拟数据
  async loadAlertsData() {
    const response = await realtimeAPI.getRealtimeStatus()
    return response.data?.alerts || []
  },

  // Process venues data
  processVenuesData(venuesData) {
    return venuesData.map(venue => {
      const status = this.getVenueStatus(venue)
      const checkedIn = venue.checked_in_count || 0
      const capacity = venue.capacity || 30
      const progressPercent = capacity > 0 ? Math.round((checkedIn / capacity) * 100) : 0
      
      return {
        id: venue.id,
        name: venue.name || `考场${venue.id}`,
        capacity: capacity,
        status: status.status,
        statusText: status.text,
        currentExam: venue.current_exam || null,
        examTime: venue.exam_time ? this.formatTime(new Date(venue.exam_time)) : null,
        checkedIn: checkedIn,
        totalCandidates: venue.total_candidates || 0,
        progressPercent: progressPercent
      }
    })
  },

  // Get venue status
  getVenueStatus(venue) {
    if (venue.current_exam) {
      return { status: 'busy', text: '进行中' }
    } else if (venue.next_exam_time) {
      const nextExamTime = new Date(venue.next_exam_time)
      const now = new Date()
      const timeDiff = nextExamTime - now
      
      if (timeDiff > 0 && timeDiff < 30 * 60 * 1000) { // Within 30 minutes
        return { status: 'active', text: '准备就绪' }
      }
    }
    return { status: 'inactive', text: '空闲' }
  },

  // Calculate enhanced statistics
  calculateEnhancedStats(venues, schedules, staff, exams) {
    const now = new Date()
    const today = now.toDateString()
    
    const todaySchedules = schedules.filter(schedule => {
      const scheduleDate = new Date(schedule.exam_date || schedule.date).toDateString()
      return scheduleDate === today
    })

    const activeStaff = staff.filter(s => s.status === 'online' || s.status === 'active')
    const completedExams = exams.filter(e => e.status === 'completed')
    const totalCandidates = schedules.reduce((sum, s) => sum + (s.candidates_count || 0), 0)
    const checkedInCandidates = venues.reduce((sum, v) => sum + (v.checkedIn || 0), 0)

    return {
      totalVenues: venues.length,
      activeExams: venues.filter(v => v.status === 'busy' || v.status === 'active').length,
      todaySchedules: todaySchedules.length,
      checkedInCandidates: checkedInCandidates,
      totalCandidates: totalCandidates,
      completedExams: completedExams.length,
      onlineStaff: activeStaff.length,
      pendingIssues: this.data.alerts.filter(a => a.priority === 'high').length
    }
  },

  // Process staff data
  processStaffData(staffData) {
    return staffData.map(staff => ({
      id: staff.id,
      name: staff.name,
      role: staff.role || '监考员',
      status: staff.status || 'offline',
      statusText: this.getStaffStatusText(staff.status || 'offline'),
      location: staff.current_venue || '未分配',
      venue: staff.current_venue || '未分配',
      lastActivity: staff.last_activity ? this.formatTime(new Date(staff.last_activity)) : '无记录',
      tasksCompleted: staff.tasks_completed || 0,
      avatar: staff.avatar || staff.name.charAt(0)
    }))
  },

  // Get staff status text
  getStaffStatusText(status) {
    const statusMap = {
      'online': '在线',
      'active': '活跃',
      'offline': '离线',
      'busy': '忙碌',
      'available': '可用',
      'on_duty': '值班中'
    }
    return statusMap[status] || '未知'
  },

  // Process exam data
  processExamData(examData) {
    return examData.map(exam => ({
      id: exam.id,
      name: exam.name,
      venue: exam.venue,
      startTime: exam.start_time ? this.formatTime(new Date(exam.start_time)) : '待定',
      endTime: exam.end_time ? this.formatTime(new Date(exam.end_time)) : '待定',
      status: exam.status || 'scheduled',
      statusText: this.getExamStatusText(exam.status || 'scheduled'),
      progress: exam.progress || 0,
      totalCandidates: exam.total_candidates || 0,
      checkedIn: exam.checked_in || 0,
      completed: exam.completed || 0
    }))
  },

  // Get exam status text
  getExamStatusText(status) {
    const statusMap = {
      'scheduled': '已安排',
      'in_progress': '进行中',
      'ongoing': '进行中',
      'completed': '已完成',
      'cancelled': '已取消',
      'postponed': '已延期'
    }
    return statusMap[status] || '未知'
  },

  // Process alerts data
  processAlertsData(alertsData) {
    return alertsData.map(alert => ({
      id: alert.id,
      type: alert.type,
      typeText: this.getAlertTypeText(alert.type),
      priority: alert.priority || 'medium',
      priorityText: this.getAlertPriorityText(alert.priority || 'medium'),
      title: alert.title,
      message: alert.message,
      venue: alert.venue,
      timestamp: alert.created_at ? this.formatTime(new Date(alert.created_at)) : '刚刚',
      resolved: alert.resolved || false
    }))
  },

  // Get alert type text
  getAlertTypeText(type) {
    const typeMap = {
      'system': '系统',
      'network': '网络',
      'hardware': '硬件',
      'candidate': '考生',
      'staff': '工作人员',
      'exam': '考试',
      'security': '安全'
    }
    return typeMap[type] || '其他'
  },

  // Get alert priority text
  getAlertPriorityText(priority) {
    const priorityMap = {
      'high': '高',
      'medium': '中',
      'low': '低',
      'critical': '紧急'
    }
    return priorityMap[priority] || '中'
  },

  // Get recent activities - 直接调用API，不使用模拟数据
  async getRecentActivities() {
    const response = await realtimeAPI.getNotifications()
    
    return (response.data?.notifications || []).map(activity => ({
      id: activity.id,
      type: this.getActivityType(activity.type),
      icon: this.getActivityIcon(activity.type),
      text: activity.message,
      time: this.formatTime(new Date(activity.created_at))
    }))
  },

  // Get activity type
  getActivityType(type) {
    const typeMap = {
      'checkin': '签到',
      'exam_start': '考试开始',
      'exam_end': '考试结束',
      'schedule_update': '日程更新',
      'staff_login': '工作人员登录',
      'venue_change': '考场变更',
      'alert': '系统警报'
    }
    return typeMap[type] || '其他活动'
  },

  // Get activity icon
  getActivityIcon(type) {
    const iconMap = {
      'checkin': '✓',
      'exam_start': '▶',
      'exam_end': '⏹',
      'schedule_update': '📅',
      'staff_login': '👤',
      'venue_change': '🏢',
      'alert': '⚠️'
    }
    return iconMap[type] || '📋'
  },

  // Refresh data
  async refreshData() {
    if (this.data.loading) return
    
    await this.loadDashboardData()
    
    wx.showToast({
      title: '数据已刷新',
      icon: 'success',
      duration: 1500
    })
  },

  // Start auto refresh
  startAutoRefresh() {
    this.autoRefreshTimer = setInterval(() => {
      this.loadDashboardData()
    }, 30000) // Refresh every 30 seconds
  },

  // Stop auto refresh
  stopAutoRefresh() {
    if (this.autoRefreshTimer) {
      clearInterval(this.autoRefreshTimer)
      this.autoRefreshTimer = null
    }
  },

  // Format time
  formatTime(date) {
    const hours = date.getHours().toString().padStart(2, '0')
    const minutes = date.getMinutes().toString().padStart(2, '0')
    return `${hours}:${minutes}`
  },

  // Format date time
  formatDateTime(date) {
    const year = date.getFullYear()
    const month = (date.getMonth() + 1).toString().padStart(2, '0')
    const day = date.getDate().toString().padStart(2, '0')
    const hours = date.getHours().toString().padStart(2, '0')
    const minutes = date.getMinutes().toString().padStart(2, '0')
    return `${year}-${month}-${day} ${hours}:${minutes}`
  },

  // Handle pull down refresh
  onPullDownRefresh() {
    this.refreshData().then(() => {
      wx.stopPullDownRefresh()
    })
  }
})