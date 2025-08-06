// miniprogram/pages/candidate/schedule/schedule.js
const { candidateAPI } = require('../../../utils/api.js')
const app = getApp()

Page({
  data: {
    examList: [],
    currentTab: 'all', // all, upcoming, completed
    isLoading: false,
    isEmpty: false,
    selectedExam: null,
    showExamDetail: false,
    filterOptions: [
      { value: 'all', label: 'All Exams', count: 0 },
      { value: 'upcoming', label: 'Upcoming', count: 0 },
      { value: 'ongoing', label: 'Ongoing', count: 0 },
      { value: 'completed', label: 'Completed', count: 0 }
    ]
  },

  onLoad: function(options) {
    this.loadExamSchedule()
    
    // 设置自定义tabBar的选中状态
    if (typeof this.getTabBar === 'function' && this.getTabBar()) {
      this.getTabBar().setData({
        selected: 1 // 考试安排是第2个tab，索引为1
      })
    }
  },

  onShow: function() {
    // Refresh data when page shows
    this.loadExamSchedule()
  },

  onPullDownRefresh: function() {
    this.loadExamSchedule().then(() => {
      wx.stopPullDownRefresh()
    })
  },

  // Load exam schedule
  loadExamSchedule: function() {
    this.setData({ isLoading: true })

    // Check network status first
    return new Promise((resolve) => {
      wx.getNetworkType({
        success: (res) => resolve(res.networkType !== 'none'),
        fail: () => resolve(false)
      });
    }).then(networkAvailable => {
      if (!networkAvailable) {
        throw new Error('网络连接不可用，请检查网络设置');
      }

      // Get candidate info from storage
      const candidateInfo = wx.getStorageSync('candidateInfo');
      if (!candidateInfo || !candidateInfo.id) {
        throw new Error('用户信息不存在，请重新登录');
      }

      return candidateAPI.getExamSchedule(candidateInfo.id);
    }).then(response => {
      if (response.success && response.data) {
        const examList = response.data.map(exam => ({
          id: exam.id,
          examName: exam.exam_name || exam.examName,
          examType: exam.exam_type || exam.examType || 'Written',
          startTime: new Date(exam.exam_time || exam.startTime),
          endTime: new Date(exam.end_time || exam.endTime || (new Date(exam.exam_time || exam.startTime).getTime() + 2 * 60 * 60 * 1000)),
          location: exam.venue || exam.location || '待定',
          status: this.mapExamStatus(exam.status),
          requirements: exam.requirements || ['身份证', '准考证'],
          description: exam.description || exam.exam_name || exam.examName,
          duration: exam.duration || 120,
          totalMarks: exam.total_marks || exam.totalMarks || 100,
          score: exam.score,
          grade: exam.grade
        }))
        
        this.setData({
          examList: examList,
          isEmpty: examList.length === 0
        })

        this.updateFilterCounts(examList)
      } else {
        throw new Error(response.message || '获取考试安排失败')
      }
    }).catch(error => {
      console.error('Failed to load exam schedule:', error)
      
      let errorMessage = '加载考试安排失败，请重试';
      if (error.message.includes('网络')) {
        errorMessage = error.message;
      } else if (error.message.includes('token') || error.message.includes('登录')) {
        errorMessage = '登录已过期，请重新登录';
        setTimeout(() => {
          wx.reLaunch({
            url: '/pages/candidate/login/login'
          });
        }, 2000);
      }
      
      wx.showToast({
        title: errorMessage,
        icon: 'none',
        duration: 2000
      });
      
      this.setData({
        examList: [],
        isEmpty: true
      });
    }).finally(() => {
      this.setData({ isLoading: false })
    })
  },

  // Map exam status from backend to frontend
  mapExamStatus: function(backendStatus) {
    const statusMap = {
      '待签到': 'upcoming',
      '已签到': 'ongoing', 
      '已完成': 'completed',
      '缺考': 'completed',
      'waiting': 'upcoming',
      'checked_in': 'ongoing',
      'completed': 'completed',
      'absent': 'completed'
    };
    return statusMap[backendStatus] || 'upcoming';
  },

  // Load mock data for demo
  loadMockData: function() {
    const now = new Date()
    const mockExams = [
      {
        id: 'EXAM001',
        examName: 'Computer Science Fundamentals',
        examType: 'Written',
        startTime: new Date(now.getTime() + 2 * 24 * 60 * 60 * 1000), // 2 days later
        endTime: new Date(now.getTime() + 2 * 24 * 60 * 60 * 1000 + 2 * 60 * 60 * 1000), // +2 hours
        location: 'Room A101',
        status: 'upcoming',
        requirements: ['ID Card', 'Student Card', 'Pencil'],
        description: 'Comprehensive exam covering basic computer science concepts',
        duration: 120,
        totalMarks: 100
      },
      {
        id: 'EXAM002',
        examName: 'Data Structures and Algorithms',
        examType: 'Practical',
        startTime: new Date(now.getTime() + 5 * 24 * 60 * 60 * 1000), // 5 days later
        endTime: new Date(now.getTime() + 5 * 24 * 60 * 60 * 1000 + 3 * 60 * 60 * 1000), // +3 hours
        location: 'Lab B205',
        status: 'upcoming',
        requirements: ['ID Card', 'Student Card', 'Laptop'],
        description: 'Hands-on programming exam for data structures and algorithms',
        duration: 180,
        totalMarks: 150
      },
      {
        id: 'EXAM003',
        examName: 'Database Management Systems',
        examType: 'Written',
        startTime: new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000), // 7 days ago
        endTime: new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000 + 2 * 60 * 60 * 1000), // +2 hours
        location: 'Room C301',
        status: 'completed',
        requirements: ['ID Card', 'Student Card'],
        description: 'Theory and practical aspects of database management',
        duration: 120,
        totalMarks: 100,
        score: 85,
        grade: 'A'
      },
      {
        id: 'EXAM004',
        examName: 'Software Engineering',
        examType: 'Project',
        startTime: new Date(now.getTime() - 1 * 60 * 60 * 1000), // 1 hour ago
        endTime: new Date(now.getTime() + 2 * 60 * 60 * 1000), // +2 hours from now
        location: 'Online',
        status: 'ongoing',
        requirements: ['Stable Internet', 'Webcam'],
        description: 'Project presentation and viva',
        duration: 180,
        totalMarks: 200
      }
    ]

    this.setData({
      examList: mockExams,
      isEmpty: false
    })

    this.updateFilterCounts(mockExams)
  },

  // Update filter counts
  updateFilterCounts: function(examList) {
    const counts = {
      all: examList.length,
      upcoming: examList.filter(exam => exam.status === 'upcoming').length,
      ongoing: examList.filter(exam => exam.status === 'ongoing').length,
      completed: examList.filter(exam => exam.status === 'completed').length
    }

    const filterOptions = this.data.filterOptions.map(option => ({
      ...option,
      count: counts[option.value] || 0
    }))

    this.setData({ filterOptions })
  },

  // Switch tab
  switchTab: function(e) {
    const tab = e.currentTarget.dataset.tab
    this.setData({
      currentTab: tab
    })
  },

  // Get filtered exam list
  getFilteredExams: function() {
    const { examList, currentTab } = this.data
    
    if (currentTab === 'all') {
      return examList
    }
    
    return examList.filter(exam => exam.status === currentTab)
  },

  // Show exam detail
  showExamDetail: function(e) {
    const examId = e.currentTarget.dataset.examId
    const exam = this.data.examList.find(exam => exam.id === examId)
    
    if (exam) {
      this.setData({
        selectedExam: exam,
        showExamDetail: true
      })
    }
  },

  // Hide exam detail
  hideExamDetail: function() {
    this.setData({
      showExamDetail: false,
      selectedExam: null
    })
  },

  // Get exam status info
  getStatusInfo: function(status) {
    const statusMap = {
      upcoming: { label: 'Upcoming', color: '#1890ff', bgColor: '#e6f7ff' },
      ongoing: { label: 'Ongoing', color: '#faad14', bgColor: '#fff7e6' },
      completed: { label: 'Completed', color: '#52c41a', bgColor: '#f6ffed' }
    }
    return statusMap[status] || statusMap.upcoming
  },

  // Format date
  formatDate: function(date) {
    const year = date.getFullYear()
    const month = (date.getMonth() + 1).toString().padStart(2, '0')
    const day = date.getDate().toString().padStart(2, '0')
    return `${year}-${month}-${day}`
  },

  // Format time
  formatTime: function(date) {
    const hours = date.getHours().toString().padStart(2, '0')
    const minutes = date.getMinutes().toString().padStart(2, '0')
    return `${hours}:${minutes}`
  },

  // Get time remaining
  getTimeRemaining: function(startTime) {
    const now = new Date()
    const diff = startTime.getTime() - now.getTime()
    
    if (diff <= 0) {
      return 'Started'
    }
    
    const days = Math.floor(diff / (1000 * 60 * 60 * 24))
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
    
    if (days > 0) {
      return `${days} days ${hours} hours`
    } else if (hours > 0) {
      return `${hours} hours`
    } else {
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
      return `${minutes} minutes`
    }
  },

  // Navigate to QR code
  goToQRCode: function() {
    wx.switchTab({
      url: '/pages/candidate/qrcode/qrcode'
    })
  },

  // Set exam reminder
  setReminder: function(e) {
    const examId = e.currentTarget.dataset.examId
    const exam = this.data.examList.find(exam => exam.id === examId)
    
    if (!exam) return
    
    wx.showModal({
      title: 'Set Reminder',
      content: `Set reminder for ${exam.examName}?`,
      success: (res) => {
        if (res.confirm) {
          // Here you would typically call an API to set the reminder
          wx.showToast({
            title: 'Reminder set',
            icon: 'success'
          })
        }
      }
    })
  },

  // Refresh data
  onRefresh: function() {
    this.loadExamSchedule()
    wx.showToast({
      title: 'Refreshed',
      icon: 'success'
    })
  }
})
