import request from '@/utils/request'

// 获取仪表板统计数据
export function getDashboardStats() {
  return request({
    url: '/dashboard/stats',
    method: 'get'
  })
}

// 获取考试数据统计
export function getExamStats(params: { time_range: string }) {
  return request({
    url: '/dashboard/exam-stats',
    method: 'get',
    params
  })
}

// 获取考试通过率
export function getPassRateStats() {
  return request({
    url: '/dashboard/pass-rate',
    method: 'get'
  })
}

// 获取最近考试
export function getRecentExams(params: { limit: number }) {
  return request({
    url: '/dashboard/recent-exams',
    method: 'get',
    params
  })
}

// 获取系统活动日志
export function getSystemActivities(params: { limit: number }) {
  return request({
    url: '/dashboard/activities',
    method: 'get',
    params
  })
}