// 权限配置常量 - 根据权限管理设计方案配置
export const PERMISSIONS = {
  // 考试产品管理
  EXAM_PRODUCT: {
    CREATE: ['SUPER_ADMIN', 'ADMIN'],
    READ: ['SUPER_ADMIN', 'ADMIN'],
    UPDATE: ['SUPER_ADMIN', 'ADMIN'],
    DELETE: ['SUPER_ADMIN', 'ADMIN']
  },
  
  // 考场管理
  VENUE: {
    CREATE: ['SUPER_ADMIN', 'ADMIN'],
    READ: ['SUPER_ADMIN', 'ADMIN'],
    UPDATE: ['SUPER_ADMIN', 'ADMIN'],
    DELETE: ['SUPER_ADMIN', 'ADMIN']
  },
  
  // 考试排期
  SCHEDULING: {
    CREATE: ['SUPER_ADMIN', 'ADMIN'],
    READ: ['SUPER_ADMIN', 'ADMIN'],
    UPDATE: ['SUPER_ADMIN', 'ADMIN'],
    DELETE: ['SUPER_ADMIN', 'ADMIN']
  },
  
  // 报名管理
  REGISTRATION: {
    // 报名上传 - 仅操作员
    UPLOAD: ['OPERATOR'],
    // 报名列表 - 管理员查看
    READ: ['SUPER_ADMIN', 'ADMIN'],
    // 我的报名 - 操作员查看自己机构的
    MY_REGISTRATION: ['OPERATOR'],
    CREATE: ['OPERATOR'],
    UPDATE: ['SUPER_ADMIN', 'ADMIN', 'OPERATOR'],
    DELETE: ['SUPER_ADMIN', 'ADMIN']
  },
  
  // 考生管理
  CANDIDATE: {
    // 考生列表 - 管理员和考官
    READ: ['SUPER_ADMIN', 'ADMIN', 'EXAMINER'],
    // 机构考生 - 操作员查看自己机构的
    INSTITUTION_READ: ['OPERATOR'],
    // 考生导入 - 管理员和操作员
    IMPORT: ['SUPER_ADMIN', 'ADMIN', 'OPERATOR'],
    CREATE: ['SUPER_ADMIN', 'ADMIN', 'OPERATOR'],
    UPDATE: ['SUPER_ADMIN', 'ADMIN', 'OPERATOR'],
    DELETE: ['SUPER_ADMIN', 'ADMIN']
  },
  
  // 考勤管理
  ATTENDANCE: {
    // 考勤记录 - 管理员和考官
    RECORD: ['SUPER_ADMIN', 'ADMIN', 'EXAMINER'],
    // 考勤统计 - 管理员
    STATISTICS: ['SUPER_ADMIN', 'ADMIN'],
    // 机构考勤 - 操作员查看自己机构的
    INSTITUTION_READ: ['OPERATOR'],
    READ: ['SUPER_ADMIN', 'ADMIN', 'EXAMINER'],
    CREATE: ['SUPER_ADMIN', 'ADMIN', 'EXAMINER'],
    UPDATE: ['SUPER_ADMIN', 'ADMIN', 'EXAMINER'],
    DELETE: ['SUPER_ADMIN', 'ADMIN']
  },
  
  // 考试信息 - 管理员和考生
  EXAM_INFO: {
    READ: ['SUPER_ADMIN', 'ADMIN', 'CANDIDATE']
  },
  
  // 我的考勤 - 管理员和考生
  MY_ATTENDANCE: {
    READ: ['SUPER_ADMIN', 'ADMIN', 'CANDIDATE']
  },
  
  // 系统设置
  SETTINGS: {
    BASIC: ['SUPER_ADMIN', 'ADMIN'],
    UPDATE: ['SUPER_ADMIN', 'ADMIN'],
    ADVANCED: ['SUPER_ADMIN'],
    SECURITY: ['SUPER_ADMIN'],
    MONITORING: ['SUPER_ADMIN']
  },
  
  // 仪表板 - 所有角色
  DASHBOARD: {
    READ: ['SUPER_ADMIN', 'ADMIN', 'OPERATOR', 'EXAMINER', 'CANDIDATE']
  }
} as const

// 权限检查工具函数
export const checkPermission = (
  userRole: string,
  resource: keyof typeof PERMISSIONS,
  action: string
): boolean => {
  // SUPER_ADMIN 拥有所有权限 - 角色匹配时忽略大小写
  const normalizedUserRole = userRole.toUpperCase();
  if (normalizedUserRole === 'SUPER_ADMIN') return true
  
  const permissionConfig = PERMISSIONS[resource]
  if (!permissionConfig) return false
  
  const allowedRoles = permissionConfig[action as keyof typeof permissionConfig]
  if (!allowedRoles || !Array.isArray(allowedRoles)) return false
  
  // 角色匹配时忽略大小写
  return allowedRoles.some(role => role.toUpperCase() === normalizedUserRole)
}

// 资源访问权限检查类型
export interface ResourceAccess {
  resource: keyof typeof PERMISSIONS
  action: string
  resourceId?: number
}