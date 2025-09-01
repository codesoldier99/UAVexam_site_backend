import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getDashboardStats, getRecentExams, getDashboardActivities } from '@/api/dashboard'
import { useUserStore } from '@/stores/user'
import type { StatisticsParams } from '@/api/dashboard'

export const useDashboardStore = defineStore('dashboard', () => {
  // 状态
  const overviewData = ref<any>(null)
  const statisticsData = ref<any>(null)
  const recentActivities = ref<any[]>([])
  const loading = ref(false)
  const lastUpdated = ref<string>('')

  // 获取仪表板统计数据（合并概览和统计）
  const fetchStats = async (params?: StatisticsParams) => {
    try {
      loading.value = true
      const userStore = useUserStore()
      const userRole = userStore.userInfo?.role
      
      // 根据用户角色添加权限参数
      const requestParams = {
        ...params,
        // 后端会根据用户token自动过滤数据范围
        role: userRole,
        institution_id: userStore.userInfo?.institution_id
      }
      
      const data = await getDashboardStats(requestParams)
      
      // 根据用户权限过滤和处理数据
      const filteredData = filterDataByRole(data, userRole)
      
      // 分离概览数据和统计数据
      overviewData.value = {
        total_candidates: filteredData.total_candidates,
        total_venues: filteredData.total_venues,
        total_exams: filteredData.total_exams,
        active_schedules: filteredData.active_schedules,
        today_checkins: filteredData.today_checkins,
        pending_registrations: filteredData.pending_registrations,
        system_status: filteredData.system_status,
        last_updated: filteredData.last_updated
      }
      
      statisticsData.value = {
        exam_statistics: filteredData.exam_statistics,
        checkin_statistics: filteredData.checkin_statistics,
        venue_utilization: filteredData.venue_utilization
      }
      
      lastUpdated.value = filteredData.last_updated
      return filteredData
    } catch (error) {
      console.error('获取仪表板数据失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 根据用户角色过滤数据
  const filterDataByRole = (data: any, role?: string) => {
    if (!role) return data
    
    switch (role.toUpperCase()) {
      case 'SUPER_ADMIN':
        // 超级管理员看到所有数据
        return data
        
      case 'ADMIN':
        // 管理员看到机构范围内的数据
        return {
          ...data,
          // 后端应该已经过滤了机构数据，这里做前端二次确认
          system_status: '正常', // 管理员不需要看系统状态
        }
        
      case 'OPERATOR':
        // 操作员看到有限的数据
        return {
          total_candidates: data.total_candidates || 0,
          total_venues: data.total_venues || 0,
          total_exams: data.total_exams || 0,
          active_schedules: data.active_schedules || 0,
          today_checkins: data.today_checkins || 0,
          pending_registrations: data.pending_registrations || 0,
          system_status: '正常',
          last_updated: data.last_updated,
          // 限制统计数据
          exam_statistics: data.exam_statistics,
          checkin_statistics: data.checkin_statistics,
          venue_utilization: [] // 操作员不看考场利用率
        }
        
      case 'EXAMINER':
        // 考官只看到分配给自己的数据
        return {
          total_candidates: data.my_candidates || 0,
          total_venues: data.my_venues || 0,
          total_exams: data.my_exams || 0,
          active_schedules: data.my_schedules || 0,
          today_checkins: data.my_checkins || 0,
          pending_registrations: 0,
          system_status: '正常',
          last_updated: data.last_updated,
          exam_statistics: data.my_exam_statistics || {},
          checkin_statistics: data.my_checkin_statistics || {},
          venue_utilization: []
        }
        
      case 'CANDIDATE':
        // 考生只看到个人相关数据
        return {
          total_candidates: 1, // 只有自己
          total_venues: data.my_venues || 0,
          total_exams: data.my_exams || 0,
          active_schedules: data.my_schedules || 0,
          today_checkins: data.my_checkin_status ? 1 : 0,
          pending_registrations: data.my_pending_registrations || 0,
          system_status: '正常',
          last_updated: data.last_updated,
          exam_statistics: data.my_exam_statistics || {},
          checkin_statistics: {},
          venue_utilization: []
        }
        
      default:
        return data
    }
  }

  // 获取最近考试信息
  const fetchRecentExams = async () => {
    try {
      const data = await getRecentExams()
      return data
    } catch (error) {
      console.error('获取最近考试失败:', error)
      throw error
    }
  }

  // 获取活动日志
  const fetchActivities = async (limit: number = 20) => {
    try {
      const data = await getDashboardActivities(limit)
      recentActivities.value = data.activities
      return data.activities
    } catch (error) {
      console.error('获取活动日志失败:', error)
      throw error
    }
  }

  // 兼容旧版本的方法名
  const fetchOverview = async () => {
    return fetchStats()
  }

  const fetchStatistics = async (params?: StatisticsParams) => {
    return fetchStats(params)
  }

  const fetchRecentActivities = async (limit: number = 20) => {
    return fetchActivities(limit)
  }

  // 刷新所有数据
  const refreshAll = async () => {
    await Promise.all([
      fetchStats(),
      fetchActivities()
    ])
  }

  return {
    // 状态
    overviewData,
    statisticsData,
    recentActivities,
    loading,
    lastUpdated,
    
    // 新方法
    fetchStats,
    fetchRecentExams,
    fetchActivities,
    refreshAll,
    
    // 兼容旧版本的方法
    fetchOverview,
    fetchStatistics,
    fetchRecentActivities
  }
})