// 分页请求参数
export interface PaginationParams {
  page: number
  limit: number
}

// 分页响应数据
export interface PaginationData<T> {
  items: T[]
  total: number
  page: number
  limit: number
  pages: number
}

// 通用响应格式
export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

// 通用ID参数
export interface IdParam {
  id: number | string
}

// 通用状态类型
export type Status = 'active' | 'inactive' | 'deleted'

// 通用搜索参数
export interface SearchParams extends PaginationParams {
  keyword?: string
  status?: Status
  start_date?: string
  end_date?: string
  [key: string]: any
}