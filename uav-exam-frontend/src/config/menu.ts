// 菜单配置系统
import { UserRole } from '@/stores/user'

export interface MenuItem {
  id: string
  title: string
  icon?: string
  path?: string
  children?: MenuItem[]
  roles: UserRole[]
  resource?: string
  action?: string
  hidden?: boolean
  badge?: string | number
}

// 菜单配置 - 严格按照权限设计方案
export const MENU_CONFIG: MenuItem[] = [
  {
    id: 'dashboard',
    title: '仪表板',
    icon: 'DataBoard',
    path: '/dashboard/index',
    roles: ['SUPER_ADMIN', 'ADMIN', 'OPERATOR', 'EXAMINER', 'CANDIDATE'],
    resource: 'DASHBOARD',
    action: 'READ'
  },
  {
    id: 'exam-management',
    title: '考试管理',
    icon: 'Document',
    roles: ['SUPER_ADMIN', 'ADMIN'],
    children: [
      {
        id: 'exam-products',
        title: '考试产品',
        path: '/exam/products',
        roles: ['SUPER_ADMIN', 'ADMIN'],
        resource: 'EXAM_PRODUCT',
        action: 'READ'
      },
      {
        id: 'venues',
        title: '考场管理',
        path: '/exam/venues',
        roles: ['SUPER_ADMIN', 'ADMIN'],
        resource: 'VENUE',
        action: 'READ'
      },
      {
        id: 'scheduling',
        title: '考试排期',
        path: '/exam/scheduling',
        roles: ['SUPER_ADMIN', 'ADMIN'],
        resource: 'SCHEDULING',
        action: 'READ'
      }
    ]
  },
  {
    id: 'registration-management',
    title: '报名管理',
    icon: 'UserFilled',
    roles: ['SUPER_ADMIN', 'ADMIN', 'OPERATOR'],
    children: [
      {
        id: 'registration-upload',
        title: '报名上传',
        path: '/registration/upload',
        roles: ['OPERATOR'],
        resource: 'REGISTRATION',
        action: 'CREATE'
      },
      {
        id: 'registration-list',
        title: '报名列表',
        path: '/registration/list',
        roles: ['SUPER_ADMIN', 'ADMIN'],
        resource: 'REGISTRATION',
        action: 'READ'
      },
      {
        id: 'my-registrations',
        title: '我的报名',
        path: '/registration/my-registrations',
        roles: ['OPERATOR'],
        resource: 'REGISTRATION',
        action: 'INSTITUTION_READ'
      }
    ]
  },
  {
    id: 'candidate-management',
    title: '考生管理',
    icon: 'User',
    roles: ['SUPER_ADMIN', 'ADMIN', 'OPERATOR', 'EXAMINER'],
    children: [
      {
        id: 'candidate-list',
        title: '考生列表',
        path: '/candidates/list',
        roles: ['SUPER_ADMIN', 'ADMIN', 'EXAMINER'],
        resource: 'CANDIDATE',
        action: 'READ'
      },
      {
        id: 'institution-candidates',
        title: '机构考生',
        path: '/candidates/institution',
        roles: ['OPERATOR'],
        resource: 'CANDIDATE',
        action: 'INSTITUTION_READ'
      },
      {
        id: 'candidate-import',
        title: '考生导入',
        path: '/candidates/import',
        roles: ['SUPER_ADMIN', 'ADMIN'],
        resource: 'CANDIDATE',
        action: 'CREATE'
      }
    ]
  },
  {
    id: 'attendance-management',
    title: '考勤管理',
    icon: 'Clock',
    roles: ['SUPER_ADMIN', 'ADMIN', 'OPERATOR', 'EXAMINER'],
    children: [
      {
        id: 'attendance-record',
        title: '考勤记录',
        path: '/attendance/record',
        roles: ['SUPER_ADMIN', 'ADMIN', 'EXAMINER'],
        resource: 'ATTENDANCE',
        action: 'RECORD'
      },
      {
        id: 'attendance-statistics',
        title: '考勤统计',
        path: '/attendance/statistics',
        roles: ['SUPER_ADMIN', 'ADMIN'],
        resource: 'ATTENDANCE',
        action: 'READ_ALL'
      },
      {
        id: 'institution-attendance',
        title: '机构考勤',
        path: '/attendance/institution',
        roles: ['OPERATOR'],
        resource: 'ATTENDANCE',
        action: 'INSTITUTION_READ'
      }
    ]
  },
  {
    id: 'exam-info',
    title: '考试信息',
    icon: 'InfoFilled',
    path: '/exam-info',
    roles: ['SUPER_ADMIN', 'ADMIN', 'CANDIDATE'],
    resource: 'SCHEDULING',
    action: 'READ'
  },
  {
    id: 'my-attendance',
    title: '我的考勤',
    icon: 'Clock',
    path: '/my-attendance',
    roles: ['SUPER_ADMIN', 'ADMIN', 'CANDIDATE'],
    resource: 'ATTENDANCE',
    action: 'READ_OWN'
  },
  {
    id: 'system-settings',
    title: '系统设置',
    icon: 'Setting',
    roles: ['SUPER_ADMIN', 'ADMIN'],
    children: [
      {
        id: 'basic-settings',
        title: '基础设置',
        path: '/settings/basic',
        roles: ['SUPER_ADMIN', 'ADMIN'],
        resource: 'SETTINGS',
        action: 'BASIC'
      },
      {
        id: 'advanced-settings',
        title: '高级设置',
        path: '/settings/advanced',
        roles: ['SUPER_ADMIN'],
        resource: 'SETTINGS',
        action: 'ADVANCED'
      },
      {
        id: 'security-settings',
        title: '安全设置',
        path: '/settings/security',
        roles: ['SUPER_ADMIN'],
        resource: 'SETTINGS',
        action: 'SECURITY'
      },
      {
        id: 'system-monitoring',
        title: '系统监控',
        path: '/settings/monitoring',
        roles: ['SUPER_ADMIN'],
        resource: 'SETTINGS',
        action: 'MONITORING'
      }
    ]
  }
]

// 菜单过滤工具函数
export const filterMenuByRole = (menus: MenuItem[], userRole: UserRole): MenuItem[] => {
  console.log('过滤菜单 - 用户角色:', userRole, '菜单数量:', menus.length)
  
  return menus.filter(menu => {
    console.log('检查菜单项:', menu.title, '允许角色:', menu.roles, '用户角色:', userRole)
    
    // 检查当前菜单项是否对用户角色可见 - 角色匹配时忽略大小写
    const normalizedUserRole = userRole.toUpperCase()
    const normalizedRoles = menu.roles.map(role => role.toUpperCase())
    
    if (!normalizedRoles.includes(normalizedUserRole) && normalizedUserRole !== 'SUPER_ADMIN') {
      console.log('菜单项被过滤:', menu.title)
      return false
    }

    // 如果有子菜单，递归过滤
    if (menu.children && menu.children.length > 0) {
      menu.children = filterMenuByRole(menu.children, userRole)
      // 如果过滤后没有可见的子菜单，隐藏父菜单
      if (menu.children.length === 0) {
        console.log('父菜单因无子菜单被过滤:', menu.title)
        return false
      }
    }

    console.log('菜单项通过过滤:', menu.title)
    return true
  })
}

// 获取用户可访问的菜单
export const getUserMenus = (userRole: UserRole): MenuItem[] => {
  return filterMenuByRole(JSON.parse(JSON.stringify(MENU_CONFIG)), userRole)
}

// 根据路径查找菜单项
export const findMenuByPath = (menus: MenuItem[], path: string): MenuItem | null => {
  for (const menu of menus) {
    if (menu.path === path) {
      return menu
    }
    if (menu.children) {
      const found = findMenuByPath(menu.children, path)
      if (found) return found
    }
  }
  return null
}

// 获取菜单面包屑
export const getMenuBreadcrumb = (menus: MenuItem[], path: string): MenuItem[] => {
  const breadcrumb: MenuItem[] = []
  
  const findPath = (items: MenuItem[], targetPath: string, parents: MenuItem[] = []): boolean => {
    for (const item of items) {
      const currentPath = [...parents, item]
      
      if (item.path === targetPath) {
        breadcrumb.push(...currentPath)
        return true
      }
      
      if (item.children && findPath(item.children, targetPath, currentPath)) {
        return true
      }
    }
    return false
  }
  
  findPath(menus, path)
  return breadcrumb
}