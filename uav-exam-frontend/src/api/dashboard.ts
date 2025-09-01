import request from '@/utils/request'

// 系统概览数据接口
interface OverviewData {
  total_candidates: number
  total_venues: number
  total_exams: number
  active_schedules: number
  today_checkins: number
  pending_registrations: number
  system_status: string
  last_updated: string
}

// 统计数据接口
interface StatisticsData {
  exam_statistics: {
    total_exams: number
    passed_exams: number
    failed_exams: number
    pass_rate: number
  }
  checkin_statistics: {
    total_checkins: number
    on_time: number
    late: number
    absent: number
  }
  venue_utilization: Array<{
    venue_name: string
    utilization_rate: number
    total_sessions: number
    completed_sessions: number
  }>
}

// 活动日志接口
interface ActivityLog {
  id: number
  type: string
  description: string
  user: string
  venue?: string
  exam_product?: string
  timestamp: string
  status: string
}

interface RecentActivitiesData {
  activities: ActivityLog[]
}

// 统计查询参数
interface StatisticsParams {
  period?: 'day' | 'week' | 'month'
  start_date?: string
  end_date?: string
}

// 获取仪表板统计数据（合并了概览和统计）
export function getDashboardStats(params?: StatisticsParams): Promise<OverviewData & StatisticsData> {
  return request({
    url: '/api/v1/pc/dashboard/stats',
    method: 'get',
    params
  })
}

// 获取最近考试信息
export function getRecentExams(): Promise<any> {
  return request({
    url: '/api/v1/pc/dashboard/recent-exams',
    method: 'get'
  })
}

// 获取活动日志
export function getDashboardActivities(limit: number = 20): Promise<RecentActivitiesData> {
  return request({
    url: '/api/v1/pc/dashboard/activities',
    method: 'get',
    params: { limit }
  })
}

// 兼容旧版本的方法名
export function getDashboardOverview(): Promise<OverviewData> {
  return getDashboardStats()
}

export function getDashboardStatistics(params?: StatisticsParams): Promise<StatisticsData> {
  return getDashboardStats(params)
}

export function getRecentActivities(limit: number = 20): Promise<RecentActivitiesData> {
  return getDashboardActivities(limit)
}