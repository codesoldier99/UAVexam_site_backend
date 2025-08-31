// miniprogram/pages/candidate/schedule/schedule.js
const { candidateAPI } = require('../../../utils/api.js')
const app = getApp()

Page({
  data: {
    examList: [],
    filteredExamList: [],
    currentTab: 'all',
    isLoading: false,
    isEmpty: false,
    selectedExam: null,
    showExamDetail: false,
    filterOptions: [
      { value: 'all', label: '全部考试', count: 0 },
      { value: 'upcoming', label: '即将开始', count: 0 },
      { value: 'completed', label: '已完成', count: 0 }
    ]
  },

  onLoad: function(options) {
    this.loadExamSchedule()
    
    if (typeof this.getTabBar === 'function' && this.getTabBar()) {
      this.getTabBar().setData({
        selected: 1
      })
    }
  },

  onShow: function() {
    this.loadExamSchedule()
  },

  onPullDownRefresh: function() {
    this.loadExamSchedule().then(() => {
      wx.stopPullDownRefresh()
    })
  },

  loadExamSchedule: function() {
    this.setData({ isLoading: true })

    return new Promise((resolve) => {
      wx.getNetworkType({
        success: (res) => resolve(res.networkType !== 'none'),
        fail: () => resolve(false)
      })
    }).then(hasNetwork => {
      if (!hasNetwork) {
        wx.showToast({
          title: '网络连接失败',
          icon: 'none'
        })
        this.setData({ isLoading: false })
        return Promise.reject('No network')
      }

      return candidateAPI.getExamSchedule()
    }).then(response => {
      console.log('=== 原始API响应数据 ===')
      console.log('完整响应对象:', JSON.stringify(response, null, 2))
      console.log('响应数据类型:', typeof response)
      console.log('是否为数组:', Array.isArray(response))
      
      if (response && typeof response === 'object') {
        console.log('响应对象的所有属性:', Object.keys(response))
        
        if (response.upcoming_exams) {
          console.log('即将开始的考试数量:', response.upcoming_exams.length)
          console.log('即将开始的考试详情:', JSON.stringify(response.upcoming_exams, null, 2))
        }
        
        if (response.completed_exams) {
          console.log('已完成的考试数量:', response.completed_exams.length)
          console.log('已完成的考试详情:', JSON.stringify(response.completed_exams, null, 2))
        }
        
        if (response.summary) {
          console.log('考试统计信息:', JSON.stringify(response.summary, null, 2))
        }
      }
      console.log('=== 原始API响应数据结束 ===')

      let examData = []
      
      if (response && typeof response === 'object') {
        if (response.upcoming_exams && Array.isArray(response.upcoming_exams)) {
          examData = examData.concat(response.upcoming_exams)
        }
        if (response.completed_exams && Array.isArray(response.completed_exams)) {
          examData = examData.concat(response.completed_exams)
        }
      } else if (Array.isArray(response)) {
        examData = response
      }

      if (examData.length === 0) {
        this.setData({
          examList: [],
          filteredExamList: [],
          isEmpty: true,
          isLoading: false
        })
        this.updateFilterCounts([])
        return
      }

      console.log('Raw exam data:', examData)

      const mappedExams = examData.map(exam => {
        console.log('Processing exam:', exam)
        
        const startTimeObj = new Date(exam.exam_time || exam.startTime)
        const endTimeObj = new Date(exam.exam_end_time || exam.end_time || exam.endTime || (startTimeObj.getTime() + 2 * 60 * 60 * 1000))
        
        const mappedExam = {
          id: exam.schedule_id || exam.id || exam.exam_id,
          examName: exam.exam_name || exam.examName,
          examType: exam.exam_type || exam.examType || '实操',
          startTime: startTimeObj,
          endTime: endTimeObj,
          // 预格式化的时间字符串，供模板直接使用
          formattedDate: this.formatDate(startTimeObj),
          formattedStartTime: this.formatTime(startTimeObj),
          formattedEndTime: this.formatTime(endTimeObj),
          formattedTimeRange: `${this.formatTime(startTimeObj)} - ${this.formatTime(endTimeObj)}`,
          location: exam.venue ? (exam.venue.name || exam.venue.address || exam.venue) : (exam.location || '待定'),
          locationDetail: exam.venue ? `${exam.venue.name || ''} ${exam.venue.address || ''}`.trim() : (exam.location || '待定'),
          status: this.mapExamStatus(exam.status),
          requirements: exam.requirements || ['身份证', '准考证'],
          description: exam.description || exam.exam_name || exam.examName,
          duration: exam.duration || 120,
          totalMarks: exam.total_marks || exam.totalMarks || 100,
          score: exam.score,
          grade: exam.grade,
          canCheckin: exam.can_checkin || false,
          checkinStartTime: exam.checkin_start_time ? new Date(exam.checkin_start_time) : null,
          examResult: exam.exam_result,
          originalStatus: exam.status
        }
        
        // 添加时间调试信息
        console.log('时间调试 - 原始时间:', exam.exam_time, exam.exam_end_time)
        console.log('时间调试 - 转换后:', mappedExam.startTime, mappedExam.endTime)
        console.log('时间调试 - 是否为Date对象:', mappedExam.startTime instanceof Date, mappedExam.endTime instanceof Date)
        console.log('时间调试 - 格式化测试:', this.formatTime(mappedExam.startTime), this.formatDate(mappedExam.startTime))
        
        console.log('Mapped exam:', mappedExam)
        return mappedExam
      })
      
      // 数据去重处理
      console.log('=== 数据去重分析 ===')
      console.log('原始数据数量:', mappedExams.length)
      
      const uniqueExamsMap = new Map()
      mappedExams.forEach(exam => {
        const existingExam = uniqueExamsMap.get(exam.id)
        if (!existingExam) {
          uniqueExamsMap.set(exam.id, exam)
          console.log(`新增考试 ID ${exam.id}:`, exam.examName, '状态:', exam.status, '(原始:', exam.originalStatus, ')')
        } else {
          const statusPriority = { 'completed': 3, 'ongoing': 2, 'upcoming': 1 }
          const currentPriority = statusPriority[exam.status] || 0
          const existingPriority = statusPriority[existingExam.status] || 0
          
          if (currentPriority > existingPriority) {
            uniqueExamsMap.set(exam.id, exam)
            console.log(`替换重复考试 ID ${exam.id}:`, existingExam.originalStatus, '->', exam.originalStatus)
          } else {
            console.log(`保留原有考试 ID ${exam.id}:`, existingExam.originalStatus, '(忽略', exam.originalStatus, ')')
          }
        }
      })
      
      const uniqueExams = Array.from(uniqueExamsMap.values())
      console.log('去重后数量:', uniqueExams.length)
      console.log('去重详情:')
      uniqueExams.forEach(exam => {
        console.log(`- ID: ${exam.id}, 考试: ${exam.examName}, 状态: ${exam.status} (原始: ${exam.originalStatus})`)
      })
      console.log('=== 数据去重分析结束 ===')

      console.log('Final exam list:', uniqueExams)

      this.setData({
        examList: uniqueExams,
        isLoading: false,
        isEmpty: uniqueExams.length === 0
      })

      this.updateFilterCounts(uniqueExams)
      this.filterExams()

      console.log('Setting filteredExamList:', uniqueExams)

    }).catch(error => {
      console.error('Load exam schedule error:', error)
      wx.showToast({
        title: '加载失败，请重试',
        icon: 'none'
      })
      this.setData({ isLoading: false })
    })
  },

  mapExamStatus: function(backendStatus) {
    const statusMap = {
      '待签到': 'upcoming',
      '已签到': 'ongoing', 
      '已完成': 'completed',
      '缺考': 'completed',
      'confirmed': 'upcoming',
      'waiting': 'upcoming',
      'scheduled': 'upcoming',
      'checked_in': 'ongoing',
      'completed': 'completed',
      'absent': 'completed',
      'in_progress': 'ongoing',
      'finished': 'completed'
    }
    
    console.log('映射状态:', backendStatus, '->', statusMap[backendStatus] || 'upcoming')
    
    if (!backendStatus) {
      return 'upcoming'
    }
    
    return statusMap[backendStatus] || 'upcoming'
  },

  updateFilterCounts: function(examList) {
    const counts = {
      all: examList.length,
      upcoming: examList.filter(exam => exam.status === 'upcoming').length,
      completed: examList.filter(exam => exam.status === 'completed').length
    }

    const filterOptions = this.data.filterOptions.map(option => ({
      ...option,
      count: counts[option.value] || 0
    }))

    this.setData({ filterOptions })
  },

  switchTab: function(e) {
    const tab = e.currentTarget.dataset.tab
    this.setData({ currentTab: tab })
    this.filterExams()
  },

  filterExams: function() {
    const { examList, currentTab } = this.data
    let filteredList = examList

    if (currentTab === 'upcoming') {
      filteredList = examList.filter(exam => exam.status === 'upcoming')
    } else if (currentTab === 'completed') {
      filteredList = examList.filter(exam => exam.status === 'completed')
    }

    this.setData({ 
      filteredExamList: filteredList,
      isEmpty: filteredList.length === 0
    })
  },

  onRefresh: function() {
    this.loadExamSchedule()
  },

  showExamDetail: function(e) {
    const examId = e.currentTarget.dataset.examId
    const exam = this.data.examList.find(item => item.id == examId)
    if (exam) {
      this.setData({
        selectedExam: exam,
        showExamDetail: true
      })
    }
  },

  hideExamDetail: function() {
    this.setData({
      showExamDetail: false,
      selectedExam: null
    })
  },

  setReminder: function(e) {
    const examId = e.currentTarget.dataset.examId
    wx.showToast({
      title: '提醒设置成功',
      icon: 'success'
    })
  },

  getStatusInfo: function(status) {
    const statusMap = {
      upcoming: { label: '即将开始', color: '#1890ff', bgColor: '#e6f7ff' },
      ongoing: { label: '进行中', color: '#52c41a', bgColor: '#f6ffed' },
      completed: { label: '已完成', color: '#8c8c8c', bgColor: '#f5f5f5' }
    }
    return statusMap[status] || statusMap.upcoming
  },

  formatDate: function(date) {
    if (!date || !(date instanceof Date) || isNaN(date.getTime())) {
      console.log('Invalid date for formatDate:', date)
      return '-'
    }
    const year = date.getFullYear()
    const month = (date.getMonth() + 1).toString().padStart(2, '0')
    const day = date.getDate().toString().padStart(2, '0')
    return `${year}-${month}-${day}`
  },

  formatTime: function(date) {
    if (!date || !(date instanceof Date) || isNaN(date.getTime())) {
      console.log('Invalid date for formatTime:', date)
      return '-'
    }
    const hours = date.getHours().toString().padStart(2, '0')
    const minutes = date.getMinutes().toString().padStart(2, '0')
    return `${hours}:${minutes}`
  },

  getTimeRemaining: function(startTime) {
    if (!startTime || !(startTime instanceof Date)) {
      return '-'
    }
    
    const now = new Date()
    const diff = startTime.getTime() - now.getTime()
    
    if (diff <= 0) {
      return '已开始'
    }
    
    const days = Math.floor(diff / (1000 * 60 * 60 * 24))
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
    
    if (days > 0) {
      return `${days}天${hours}小时`
    } else if (hours > 0) {
      return `${hours}小时${minutes}分钟`
    } else {
      return `${minutes}分钟`
    }
  }
})