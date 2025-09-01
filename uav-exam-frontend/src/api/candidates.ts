import request from '@/utils/request'

// 考生相关接口
export interface Candidate {
  id: number
  name: string
  id_card: string
  phone: string
  email: string
  gender: 'male' | 'female'
  birth_date: string
  address: string
  status: 'pending' | 'approved' | 'rejected' | 'examining' | 'completed'
  avatar?: string
  created_at: string
  updated_at: string
}

export interface CandidateQuery {
  skip?: number
  limit?: number
  search?: string
  status?: string
  gender?: string
}

export interface CandidateStatistics {
  totalCandidates: number
  activeCandidates: number
  pendingCandidates: number
  examCandidates: number
}

export interface CandidateResponse {
  items: Candidate[]
  total: number
  page: number
  size: number
  pages: number
}

// 获取考生列表
export const getCandidates = (params: CandidateQuery = {}) => {
  return request<CandidateResponse>({
    url: '/api/v1/pc/candidates',
    method: 'get',
    params
  })
}

// 创建考生
export const createCandidate = (data: Partial<Candidate>) => {
  return request<Candidate>({
    url: '/api/v1/pc/candidates/',
    method: 'post',
    data
  })
}

// 获取考生详情
export const getCandidateById = (id: number) => {
  return request<Candidate>({
    url: `/api/v1/pc/candidates/${id}/`,
    method: 'get'
  })
}

// 更新考生信息
export const updateCandidate = (id: number, data: Partial<Candidate>) => {
  return request<Candidate>({
    url: `/api/v1/pc/candidates/${id}/`,
    method: 'put',
    data
  })
}

// 删除考生
export const deleteCandidate = (id: number) => {
  return request({
    url: `/api/v1/pc/candidates/${id}/`,
    method: 'delete'
  })
}

// 批量删除考生
export const batchDeleteCandidates = (ids: number[]) => {
  return request({
    url: '/api/v1/pc/candidates/batch-delete/',
    method: 'post',
    data: { ids }
  })
}

// 批量导入考生
export const importCandidates = (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  
  return request({
    url: '/api/v1/pc/candidates/import/',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 导出考生数据
export const exportCandidates = (params: CandidateQuery = {}) => {
  return request({
    url: '/api/v1/pc/candidates/export/',
    method: 'get',
    params,
    responseType: 'blob'
  })
}

// 获取考生统计信息
export const getCandidateStatistics = () => {
  return request<CandidateStatistics>({
    url: '/api/v1/pc/candidates/statistics/',
    method: 'get'
  })
}