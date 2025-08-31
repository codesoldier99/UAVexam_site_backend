import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login as apiLogin, logout as apiLogout, getUserProfile as apiGetUserProfile, updateUserProfile as apiUpdateUserProfile } from '@/api/auth'

export type UserRole = 'SUPER_ADMIN' | 'ADMIN' | 'OPERATOR' | 'EXAMINER' | 'CANDIDATE'

export interface UserInfo {
  id: number
  username: string
  real_name: string
  role: UserRole
  email?: string
  phone?: string
  institution_id?: number  // 机构ID
  is_active?: boolean
  permissions?: string[]   // 用户具体权限列表
  created_at: string
  updated_at?: string
}

export const useUserStore = defineStore('user', () => {
  const token = ref<string>('')
  const userInfo = ref<UserInfo | null>(null)
  const roles = ref<string[]>([])
  
  // 从本地存储初始化状态
  const initFromStorage = () => {
    const storedToken = localStorage.getItem('token')
    const storedUserInfo = localStorage.getItem('userInfo')
    
    if (storedToken) {
      token.value = storedToken
    }
    
    if (storedUserInfo) {
      try {
        userInfo.value = JSON.parse(storedUserInfo)
        if (userInfo.value && userInfo.value.role) {
          roles.value = [userInfo.value.role]
        }
      } catch (error) {
        console.error('Failed to parse user info from storage', error)
      }
    }
  }
  
  // 登录
  const login = async (credentials: { username: string; password: string }) => {
    try {
      const response = await apiLogin(credentials)
      
      // 根据后端返回的格式处理token
      token.value = response.access_token
      localStorage.setItem('token', token.value)
      
      // 设置用户信息
      if (response.user_info) {
        userInfo.value = {
          id: response.user_info.id,
          username: response.user_info.username,
          real_name: response.user_info.real_name,
          role: response.user_info.role as UserRole,
          institution_id: response.user_info.institution_id,
          created_at: new Date().toISOString()
        }
        
        // 设置用户角色
        if (userInfo.value.role) {
          roles.value = [userInfo.value.role]
        }
        
        localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
      }
      
      return response
    } catch (error) {
      console.error('Login failed', error)
      throw error
    }
  }
  
  // 获取用户信息
  const getUserInfo = async () => {
    try {
      const response = await apiGetUserProfile()
      userInfo.value = {
        id: response.id,
        username: response.username,
        real_name: response.real_name,
        role: response.role as UserRole,
        email: response.email,
        institution_id: response.institution_id,
        is_active: response.is_active,
        created_at: response.created_at
      }
      
      // 设置用户角色
      if (userInfo.value.role) {
        roles.value = [userInfo.value.role]
      }
      
      localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
      return response
    } catch (error) {
      console.error('Get user info failed', error)
      throw error
    }
  }
  
  // 更新用户资料
  const updateProfile = async (data: { real_name?: string; email?: string; phone?: string }) => {
    try {
      const response = await apiUpdateUserProfile(data)
      
      // 更新本地用户信息
      if (userInfo.value && response.success) {
        userInfo.value = {
          ...userInfo.value,
          real_name: response.data.real_name,
          email: response.data.email,
          updated_at: response.data.updated_at
        }
        localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
      }
      
      return response
    } catch (error) {
      console.error('Update profile failed', error)
      throw error
    }
  }
  
  // 登出
  const logout = async () => {
    try {
      if (token.value) {
        await apiLogout()
      }
    } catch (error) {
      console.error('Logout failed', error)
    } finally {
      // 清除状态和本地存储
      token.value = ''
      userInfo.value = null
      roles.value = []
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
    }
  }
  
  // 检查角色权限（向后兼容）
  const hasRole = (roles: string[] | undefined): boolean => {
    if (!roles || roles.length === 0) return true
    if (!userInfo.value?.role) return false
    
    // SUPER_ADMIN 拥有所有权限
    if (userInfo.value.role === 'SUPER_ADMIN') return true
    
    return roles.includes(userInfo.value.role)
  }

  // 检查资源权限
  const hasPermission = (resource: string, action: string, resourceId?: number): boolean => {
    if (!userInfo.value?.role) return false
    
    // SUPER_ADMIN 拥有所有权限
    if (userInfo.value.role === 'SUPER_ADMIN') return true
    
    // 直接导入权限配置并检查基础权限
    try {
      // 使用静态导入避免 require 问题
      const { checkPermission } = require('@/config/permissions')
      const hasBasicPermission = checkPermission(userInfo.value.role, resource, action)
      
      if (!hasBasicPermission) return false
      
      // 资源级权限检查
      if (resourceId) {
        return checkResourceAccess(resource, resourceId, userInfo.value)
      }
      
      return true
    } catch (error) {
      console.error('权限检查失败:', error)
      // 如果权限检查失败，根据角色给予基本权限
      const basicRolePermissions = {
        'SUPER_ADMIN': true,
        'ADMIN': ['EXAM_PRODUCT', 'VENUE', 'SCHEDULING', 'REGISTRATION', 'CANDIDATE', 'ATTENDANCE', 'SETTINGS'].includes(resource),
        'OPERATOR': ['REGISTRATION', 'CANDIDATE', 'ATTENDANCE'].includes(resource),
        'EXAMINER': ['CANDIDATE', 'ATTENDANCE'].includes(resource),
        'CANDIDATE': ['EXAM_INFO', 'ATTENDANCE'].includes(resource)
      }
      
      return basicRolePermissions[userInfo.value.role as keyof typeof basicRolePermissions] || false
    }
  }

  // 资源访问权限检查辅助方法
  const checkResourceAccess = (resource: string, resourceId: number, user: UserInfo): boolean => {
    switch (user.role) {
      case 'OPERATOR':
        // 操作员用户只能操作自己机构的资源
        return checkInstitutionAccess(resource, resourceId, user.institution_id)
      case 'EXAMINER':
        // 考官只能操作分配给自己的考试相关资源
        return checkExaminerAccess(resource, resourceId, user.id)
      case 'CANDIDATE':
        // 考生只能操作自己的资源
        return checkCandidateAccess(resource, resourceId, user.id)
      default:
        return true
    }
  }

  // 机构访问权限检查
  const checkInstitutionAccess = (resource: string, resourceId: number, institutionId?: number): boolean => {
    // 这里需要根据具体业务逻辑实现
    // 例如：检查考生是否属于该机构
    // 临时返回true，实际需要调用API验证
    return institutionId !== undefined
  }

  // 考官访问权限检查
  const checkExaminerAccess = (resource: string, resourceId: number, examinerId: number): boolean => {
    // 检查考官是否被分配到该考试
    // 临时返回true，实际需要调用API验证
    return true
  }

  // 考生访问权限检查
  const checkCandidateAccess = (resource: string, resourceId: number, candidateId: number): boolean => {
    // 检查资源是否属于该考生
    return resourceId === candidateId
  }

  // 兼容旧版本的权限检查方法
  const hasLegacyPermission = (permissions: string[] | undefined): boolean => {
    return hasRole(permissions)
  }
  
  // 初始化
  initFromStorage()
  
  return {
    token,
    userInfo,
    roles,
    login,
    getUserInfo,
    updateProfile,
    logout,
    hasRole,
    hasPermission,
    hasLegacyPermission,
    checkResourceAccess,
    checkInstitutionAccess,
    checkExaminerAccess,
    checkCandidateAccess
  }
})