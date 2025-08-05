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
      console.error('API调用失败:', error)
      
      // 隐藏加载状态
      loading.hidePage('dashboard')
      
      // 记录错误
      perf.recordError(error, { page: 'dashboard', action: 'loadData' })
      
      this.setData({ loading: false })
      
      // 显示具体的错误信息给用户，不再使用模拟数据
      wx.showModal({
        title: 'API连接失败',
        content: `无法连接到服务器: ${error.message}\n\n请检查:\n1. API服务器是否启动 (端口8000)\n2. 网络连接是否正常\n3. 服务器地址: http://10.20.175.146:8000`,
        showCancel: true,
        cancelText: '重试',
        confirmText: '确定',
        success: (res) => {
          if (!res.confirm) {
            // 用户点击重试
            this.loadDashboardData()
          }
        }
      })
    }
  },

  // Load venues data - 直接调用API，不使用模拟数据
  async loadVenuesData() {
    const response = await realtimeAPI.getVenueStatus()
    return response.data || []
  },

  // Load schedules data - 直接调用API，不使用模拟数据
  async loadSchedulesData() {
    const response = await realtimeAPI.getDashboardData()
    return response.data?.schedules || []
  },

  // Load staff data - 直接调用API，不使用模拟数据
  async loadStaffData() {
    const response = await realtimeAPI.getDashboardData()
    return response.data?.staff || []
  },

  // Load exam data - 直接调用API，不使用模拟数据
  async loadExamData() {
    const response = await realtimeAPI.getDashboardData()
    return response.data?.exams || []
  },

  // Load alerts data - 直接调用API，不使用模拟数据
  async loadAlertsData() {
    const response = await realtimeAPI.getQueueStatus()
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
    const response = await realtimeAPI.getRealtimeNotifications({ limit: 10 })
    
    return (response.data || []).map(activity => ({
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
