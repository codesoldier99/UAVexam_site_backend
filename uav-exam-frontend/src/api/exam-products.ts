import request from '@/utils/request'

// 考试产品接口类型定义
export interface ExamProduct {
  id: number
  name: string
  code: string
  description: string
  duration_minutes: number
  exam_type: 'PRACTICAL' | 'THEORY' | 'MIXED'
  is_active: boolean
  requirements?: string[]
  max_score?: number
  pass_score?: number
  price?: number
  registration_count?: number
  pass_rate?: number
  created_at: string
  updated_at: string
}

export interface ExamProductCreateRequest {
  name: string
  code: string
  description: string
  duration_minutes: number
  exam_type: 'PRACTICAL' | 'THEORY' | 'MIXED'
  is_active: boolean
  requirements?: string[]
  max_score?: number
  pass_score?: number
  price?: number
}

export interface ExamProductUpdateRequest {
  name?: string
  description?: string
  duration_minutes?: number
  price?: number
  pass_score?: number
  is_active?: boolean
  requirements?: string[]
}

export interface ExamProductListParams {
  skip?: number
  limit?: number
  search?: string
  is_active?: boolean | string
  page?: number
  size?: number
}

export interface ExamProductStatistics {
  total_products: number
  active_products: number
  inactive_products: number
  exam_type_breakdown: {
    PRACTICAL: number
    THEORY: number
    MIXED: number
  }
  registration_stats: {
    total_registrations: number
    average_per_product: number
    most_popular: {
      id: number
      name: string
      registrations: number
    }
  }
  pass_rate_stats: {
    overall_pass_rate: number
    highest_pass_rate: number
    lowest_pass_rate: number
  }
}

// 后端返回的分页数据格式
export interface ExamProductListResponse {
  items: ExamProduct[]
  total: number
  page: number
  size: number
  pages: number
}

// API 接口函数
export const getExamProducts = (params?: ExamProductListParams) => {
  // 过滤掉 undefined 的参数
  const cleanParams = params ? Object.fromEntries(
    Object.entries(params).filter(([_, value]) => value !== undefined)
  ) : {}
  
  return request.get<ExamProductListResponse>('/api/v1/pc/exam-products', { 
    params: cleanParams 
  })
}

export const createExamProduct = (data: ExamProductCreateRequest) => {
  return request.post('/api/v1/pc/exam-products', data)
}

export const getExamProductDetail = (productId: number) => {
  return request.get<ExamProduct>(`/api/v1/pc/exam-products/${productId}/`)
}

export const updateExamProduct = (productId: number, data: ExamProductUpdateRequest) => {
  return request.put(`/api/v1/pc/exam-products/${productId}/`, data)
}

export const deleteExamProduct = (productId: number) => {
  return request.delete(`/api/v1/pc/exam-products/${productId}/`)
}

export const searchExamProducts = (search: string) => {
  return request.get<ExamProductListResponse>('/api/v1/pc/exam-products', { 
    params: { search } 
  })
}

export const getExamProductStatistics = () => {
  return request.get<ExamProductStatistics>('/api/v1/pc/exam-products/statistics/')
}