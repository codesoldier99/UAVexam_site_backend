// 用户角色类型
export type UserRole = 'SUPER_ADMIN' | 'ADMIN' | 'OPERATOR' | 'CANDIDATE'

// 登录表单类型
export interface LoginForm {
  username: string
  password: string
}

// 用户信息类型
export interface UserInfo {
  id: number
  username: string
  real_name: string
  role: UserRole
  email?: string
  phone?: string
  avatar?: string
  institution_id?: number
  institution_name?: string
  created_at: string
  updated_at: string
}

// 登录响应类型
export interface LoginResponse {
  access_token: string
  refresh_token: string
  expires_in: number
  user: UserInfo
}