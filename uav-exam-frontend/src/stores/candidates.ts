import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  getCandidates,
  createCandidate,
  getCandidateById,
  updateCandidate,
  deleteCandidate,
  batchDeleteCandidates,
  importCandidates,
  exportCandidates,
  getCandidateStatistics,
  type Candidate,
  type CandidateQuery,
  type CandidateStatistics
} from '@/api/candidates'
import { useUserStore } from './user'

export const useCandidatesStore = defineStore('candidates', () => {
  // 状态
  const candidates = ref<Candidate[]>([])
  const currentCandidate = ref<Candidate | null>(null)
  const statistics = ref<CandidateStatistics>({
    totalCandidates: 0,
    activeCandidates: 0,
    pendingCandidates: 0,
    examCandidates: 0
  })
  const loading = ref(false)
  const total = ref(0)

  // 获取用户信息
  const userStore = useUserStore()

  // 获取考生列表
  const fetchCandidates = async (params: CandidateQuery = {}) => {
    try {
      loading.value = true
      console.log('获取考生列表，参数:', params)
      
      // 根据用户权限过滤数据
      const filteredParams = filterByUserRole(params)
      
      const response = await getCandidates(filteredParams)
      console.log('考生列表响应:', response)
      
      candidates.value = response.items || []
      total.value = response.total || 0
      
      console.log('考生列表更新完成，数量:', candidates.value.length)
    } catch (error) {
      console.error('获取考生列表失败:', error)
      candidates.value = []
      total.value = 0
    } finally {
      loading.value = false
    }
  }

  // 创建考生
  const addCandidate = async (candidateData: Partial<Candidate>) => {
    try {
      loading.value = true
      const newCandidate = await createCandidate(candidateData)
      candidates.value.unshift(newCandidate)
      total.value += 1
      return newCandidate
    } catch (error) {
      console.error('创建考生失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取考生详情
  const fetchCandidateById = async (id: number) => {
    try {
      loading.value = true
      const candidate = await getCandidateById(id)
      currentCandidate.value = candidate
      return candidate
    } catch (error) {
      console.error('获取考生详情失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 更新考生
  const editCandidate = async (id: number, candidateData: Partial<Candidate>) => {
    try {
      loading.value = true
      const updatedCandidate = await updateCandidate(id, candidateData)
      
      // 更新列表中的考生信息
      const index = candidates.value.findIndex(p => p.id === id)
      if (index !== -1) {
        candidates.value[index] = updatedCandidate
      }
      
      // 更新当前考生信息
      if (currentCandidate.value?.id === id) {
        currentCandidate.value = updatedCandidate
      }
      
      return updatedCandidate
    } catch (error) {
      console.error('更新考生失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 删除考生
  const removeCandidate = async (id: number) => {
    try {
      loading.value = true
      await deleteCandidate(id)
      
      // 从列表中移除
      candidates.value = candidates.value.filter(p => p.id !== id)
      total.value -= 1
      
      // 清空当前考生信息
      if (currentCandidate.value?.id === id) {
        currentCandidate.value = null
      }
    } catch (error) {
      console.error('删除考生失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 批量删除考生
  const removeCandidatesBatch = async (ids: number[]) => {
    try {
      loading.value = true
      await batchDeleteCandidates(ids)
      
      // 从列表中移除
      candidates.value = candidates.value.filter(p => !ids.includes(p.id))
      total.value -= ids.length
    } catch (error) {
      console.error('批量删除考生失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 导入考生
  const importCandidatesData = async (file: File) => {
    try {
      loading.value = true
      const result = await importCandidates(file)
      // 重新获取列表
      await fetchCandidates()
      return result
    } catch (error) {
      console.error('导入考生失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 导出考生
  const exportCandidatesData = async (params: CandidateQuery = {}) => {
    try {
      loading.value = true
      const filteredParams = filterByUserRole(params)
      const blob = await exportCandidates(filteredParams)
      
      // 创建下载链接
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `candidates_${new Date().toISOString().split('T')[0]}.xlsx`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('导出考生失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取统计信息
  const fetchStatistics = async () => {
    try {
      const stats = await getCandidateStatistics()
      statistics.value = stats
    } catch (error) {
      console.error('获取考生统计失败:', error)
      // 设置默认值
      statistics.value = {
        totalCandidates: 0,
        activeCandidates: 0,
        pendingCandidates: 0,
        examCandidates: 0
      }
    }
  }

  // 根据用户角色过滤参数
  const filterByUserRole = (params: CandidateQuery) => {
    const userRole = userStore.user?.role
    const filteredParams = { ...params }

    // 根据不同角色添加不同的过滤条件
    switch (userRole) {
      case 'EXAMINER':
        // 考官只能看到自己负责的考生
        // 这里可以根据实际业务逻辑添加过滤条件
        break
      case 'OPERATOR':
        // 操作员可能有特定的权限范围
        break
      case 'ADMIN':
      case 'SUPER_ADMIN':
        // 管理员可以看到所有考生
        break
      default:
        // 其他角色可能有限制
        break
    }

    return filteredParams
  }

  // 清空状态
  const clearState = () => {
    candidates.value = []
    currentCandidate.value = null
    statistics.value = {
      totalCandidates: 0,
      activeCandidates: 0,
      pendingCandidates: 0,
      examCandidates: 0
    }
    total.value = 0
    loading.value = false
  }

  return {
    // 状态
    candidates,
    currentCandidate,
    statistics,
    loading,
    total,
    
    // 方法
    fetchCandidates,
    addCandidate,
    fetchCandidateById,
    editCandidate,
    removeCandidate,
    removeCandidatesBatch,
    importCandidatesData,
    exportCandidatesData,
    fetchStatistics,
    clearState,
    
    // 别名方法（为了保持一致性）
    createCandidate: addCandidate,
    updateCandidate: editCandidate,
    deleteCandidate: removeCandidate,
    batchDeleteCandidates: removeCandidatesBatch,
    importCandidates: importCandidatesData,
    exportCandidates: exportCandidatesData
  }
})