import { computed } from 'vue'
import { useUserStore } from '@/stores/user'

export interface PermissionConfig {
  roles?: string[]
  resource?: string
  action?: string
  resourceId?: number
  and?: PermissionConfig[]
  or?: PermissionConfig[]
  not?: PermissionConfig
}

export const usePermission = () => {
  const userStore = useUserStore()
  
  // 权限检查核心函数
  const checkPermission = (config: any): boolean => {
    if (!config) return true
    
    // 字符串格式：单个角色
    if (typeof config === 'string') {
      return userStore.hasRole([config])
    }
    
    // 数组格式：多个角色（OR逻辑）
    if (Array.isArray(config)) {
      return userStore.hasRole(config)
    }
    
    // 对象格式：复杂权限检查
    if (typeof config === 'object') {
      const permConfig = config as PermissionConfig
      
      // 角色权限检查
      if (permConfig.roles) {
        const roleResult = userStore.hasRole(permConfig.roles)
        if (!roleResult) return false
      }
      
      // 资源权限检查
      if (permConfig.resource && permConfig.action) {
        const resourceResult = userStore.hasPermission(
          permConfig.resource, 
          permConfig.action, 
          permConfig.resourceId
        )
        if (!resourceResult) return false
      }
      
      // AND逻辑：所有条件都必须满足
      if (permConfig.and) {
        return permConfig.and.every(condition => checkPermission(condition))
      }
      
      // OR逻辑：任一条件满足即可
      if (permConfig.or) {
        return permConfig.or.some(condition => checkPermission(condition))
      }
      
      // NOT逻辑：条件不满足
      if (permConfig.not) {
        return !checkPermission(permConfig.not)
      }
      
      return true
    }
    
    return false
  }
  
  // 常用权限检查方法
  const hasRole = (roles: string | string[]) => {
    const roleArray = Array.isArray(roles) ? roles : [roles]
    return userStore.hasRole(roleArray)
  }
  
  const hasResource = (resource: string, action: string, resourceId?: number) => {
    return userStore.hasPermission(resource, action, resourceId)
  }
  
  // 当前用户信息
  const currentUser = computed(() => userStore.userInfo)
  const currentRole = computed(() => userStore.userInfo?.role)
  const isLoggedIn = computed(() => !!userStore.token)
  
  // 角色判断
  const isSuperAdmin = computed(() => currentRole.value === 'super_admin')
  const isAdmin = computed(() => currentRole.value === 'admin')
  const isInstitution = computed(() => currentRole.value === 'institution')
  const isExaminer = computed(() => currentRole.value === 'examiner')
  const isCandidate = computed(() => currentRole.value === 'candidate')
  
  // 权限组合检查
  const canManageUsers = computed(() => hasRole(['super_admin', 'admin']))
  const canManageExams = computed(() => hasRole(['super_admin', 'admin']))
  const canViewReports = computed(() => hasRole(['super_admin', 'admin', 'examiner']))
  const canManageInstitution = computed(() => hasRole(['super_admin', 'admin', 'institution']))
  
  return {
    // 核心权限检查
    hasPermission: checkPermission,
    hasRole,
    hasResource,
    
    // 用户信息
    currentUser,
    currentRole,
    isLoggedIn,
    
    // 角色判断
    isSuperAdmin,
    isAdmin,
    isInstitution,
    isExaminer,
    isCandidate,
    
    // 权限组合
    canManageUsers,
    canManageExams,
    canViewReports,
    canManageInstitution
  }
}

// 页面级权限检查工具
export const usePagePermission = () => {
  const { hasPermission, hasRole, hasResource } = usePermission()
  
  // 表格操作权限
  const getTableActions = (resource: string, item?: any) => {
    const actions = []
    
    if (hasResource(resource, 'READ', item?.id)) {
      actions.push('view')
    }
    
    if (hasResource(resource, 'UPDATE', item?.id)) {
      actions.push('edit')
    }
    
    if (hasResource(resource, 'DELETE', item?.id)) {
      actions.push('delete')
    }
    
    return actions
  }
  
  // 表单字段权限
  const getFieldPermission = (resource: string, field: string, item?: any) => {
    return {
      readable: hasResource(resource, 'READ', item?.id),
      writable: hasResource(resource, 'UPDATE', item?.id),
      required: hasResource(resource, 'CREATE') || hasResource(resource, 'UPDATE', item?.id)
    }
  }
  
  // 批量操作权限
  const getBatchActions = (resource: string) => {
    const actions = []
    
    if (hasResource(resource, 'CREATE')) {
      actions.push('import')
    }
    
    if (hasResource(resource, 'READ')) {
      actions.push('export')
    }
    
    if (hasResource(resource, 'DELETE')) {
      actions.push('batchDelete')
    }
    
    return actions
  }
  
  return {
    getTableActions,
    getFieldPermission,
    getBatchActions,
    hasPermission,
    hasRole,
    hasResource
  }
}