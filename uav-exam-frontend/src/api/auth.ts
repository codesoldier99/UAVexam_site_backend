import request from '@/utils/request'

interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user_info: {
    id: number;
    username: string;
    real_name: string;
    role: string;
    institution_id: number;
  }
}

interface UserProfileResponse {
  id: number;
  username: string;
  email: string;
  real_name: string;
  role: string;
  institution_id: number;
  is_active: boolean;
  created_at: string;
}

interface UpdateProfileRequest {
  real_name?: string;
  email?: string;
  phone?: string;
}

interface UpdateProfileResponse {
  success: boolean;
  message: string;
  data: {
    id: number;
    real_name: string;
    email: string;
    updated_at: string;
  }
}

// PC端管理员登录
export function login(data: { username: string; password: string }): Promise<LoginResponse> {
  return request({
    url: '/api/v1/pc/auth/login',
    method: 'post',
    data
  })
}

// PC端管理员登出
export function logout() {
  return request({
    url: '/api/v1/pc/auth/logout',
    method: 'post'
  })
}

// 获取当前用户信息
export function getUserProfile(): Promise<UserProfileResponse> {
  return request({
    url: '/api/v1/pc/auth/profile',
    method: 'get'
  })
}

// 更新用户资料
export function updateUserProfile(data: UpdateProfileRequest): Promise<UpdateProfileResponse> {
  return request({
    url: '/api/v1/pc/auth/profile',
    method: 'put',
    data
  })
}

// 兼容旧版本的getUserInfo方法
export function getUserInfo(): Promise<UserProfileResponse> {
  return getUserProfile()
}

// 修改密码（保留原有接口，如果后端有实现的话）
export function changePassword(data: { old_password: string; new_password: string; confirm_password: string }) {
  return request({
    url: '/api/v1/pc/auth/change-password',
    method: 'post',
    data
  })
}