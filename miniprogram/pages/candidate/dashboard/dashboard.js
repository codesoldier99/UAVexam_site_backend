// miniprogram/pages/candidate/dashboard/dashboard.js
const app = getApp()

Page({
  data: {
    userInfo: null,
    examSchedule: [],
    recentResults: [],
    loading: true,
    stats: {
      totalExams: 0,
      completedExams: 0,
      passedExams: 0,
      upcomingExams: 0
    }
  },

  onLoad() {
    this.loadDashboardData()
  },

  onShow() {
    // 每次显示页面时刷新数据
    this.loadDashboardData()
  },

  async loadDashboardData() {
    try {
      wx.showLoading({ title: '加载中...' })
      
      // 并行加载数据
      const [userInfo, examSchedule, examResults] = await Promise.all([
        this.loadUserInfo(),
        this.loadExamSchedule(),
        this.loadExamResults()
      ])

      // 计算统计数据
      const stats = this.calculateStats(examSchedule, examResults)

      this.setData({
        userInfo,
        examSchedule: examSchedule.slice(0, 3), // 只显示最近3个考试
        recentResults: examResults.slice(0, 2), // 只显示最近2个成绩
        stats,
        loading: false
      })

    } catch (error) {
      console.error('加载仪表板数据失败:', error)
      wx.showToast({
        title: '加载失败',
        icon: 'error'
      })
    } finally {
      wx.hideLoading()
    }
  },

  async loadUserInfo() {
    // 模拟API调用
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          name: '张三',
          id_number: '110101199001011234',
          status: '已审核',
          exam_product: '无人机驾驶员考试'
        })
      }, 500)
    })
  },

  async loadExamSchedule() {
    // 模拟API调用
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve([
          {
            id: 'EXAM001',
            exam_name: '无人机驾驶理论考试',
            exam_type: '理论',
            exam_time: '2025-08-10T09:00:00',
            venue: '北京航空培训中心A101教室',
            status: '待签到'
          },
          {
            id: 'EXAM002',
            exam_name: '无人机操作实践考试',
            exam_type: '实操',
            exam_time: '2025-08-15T14:00:00',
            venue: '北京航空培训中心室外场地B区',
            status: '待签到'
          }
        ])
      }, 600)
    })
  },

  async loadExamResults() {
    // 模拟API调用
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve([
          {
            id: 'RESULT001',
            exam_name: '航空法规考试',
            exam_date: '2025-07-20',
            score: 85,
            grade: '良好',
            pass_status: '通过'
          }
        ])
      }, 700)
    })
  },

  calculateStats(examSchedule, examResults) {
    const totalExams = examSchedule.length + examResults.length
    const completedExams = examResults.length
    const passedExams = examResults.filter(result => result.pass_status === '通过').length
    const upcomingExams = examSchedule.filter(exam => exam.status === '待签到').length

    return {
      totalExams,
      completedExams,
      passedExams,
      upcomingExams
    }
  },

  // 导航到考试安排页面
  goToExamSchedule() {
    wx.navigateTo({
      url: '/pages/candidate/exam-schedule/exam-schedule'
    })
  },

  // 导航到考试成绩页面
  goToExamResults() {
    wx.navigateTo({
      url: '/pages/candidate/exam-results/exam-results'
    })
  },

  // 导航到个人信息页面
  goToProfile() {
    wx.navigateTo({
      url: '/pages/candidate/profile/profile'
    })
  },

  // 查看考试详情
  viewExamDetail(e) {
    const examId = e.currentTarget.dataset.examId
    wx.navigateTo({
      url: `/pages/candidate/exam-detail/exam-detail?id=${examId}`
    })
  },

  // 查看成绩详情
  viewResultDetail(e) {
    const resultId = e.currentTarget.dataset.resultId
    wx.navigateTo({
      url: `/pages/candidate/result-detail/result-detail?id=${resultId}`
    })
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.loadDashboardData().finally(() => {
      wx.stopPullDownRefresh()
    })
  },

  // 格式化日期时间
  formatDateTime(dateTimeStr) {
    const date = new Date(dateTimeStr)
    const month = (date.getMonth() + 1).toString().padStart(2, '0')
    const day = date.getDate().toString().padStart(2, '0')
    const hour = date.getHours().toString().padStart(2, '0')
    const minute = date.getMinutes().toString().padStart(2, '0')
    return `${month}-${day} ${hour}:${minute}`
  },

  // 获取考试状态样式
  getExamStatusClass(status) {
    const statusMap = {
      '待签到': 'status-pending',
      '进行中': 'status-ongoing',
      '已完成': 'status-completed',
      '已取消': 'status-cancelled'
    }
    return statusMap[status] || 'status-default'
  },

  // 获取成绩等级样式
  getGradeClass(grade) {
    const gradeMap = {
      '优秀': 'grade-excellent',
      '良好': 'grade-good',
      '及格': 'grade-pass',
      '不及格': 'grade-fail'
    }
    return gradeMap[grade] || 'grade-default'
  }
})