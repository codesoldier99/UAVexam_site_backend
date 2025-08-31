import type { RouteRecordRaw } from 'vue-router'

const settingsRoutes: RouteRecordRaw[] = [
  {
    path: 'settings/basic',
    name: 'BasicSettings',
    component: () => import('@/views/settings/basic/index.vue'),
    meta: {
      title: '基础设置',
      requiresAuth: true,
      roles: ['SUPER_ADMIN'],
      resource: 'SETTINGS',
      action: 'BASIC'
    }
  },
  {
    path: 'settings/advanced',
    name: 'AdvancedSettings',
    component: () => import('@/views/settings/advanced/index.vue'),
    meta: {
      title: '高级设置',
      requiresAuth: true,
      roles: ['SUPER_ADMIN'],
      resource: 'SETTINGS',
      action: 'ADVANCED'
    }
  },
  {
    path: 'settings/security',
    name: 'SecuritySettings',
    component: () => import('@/views/settings/security/index.vue'),
    meta: {
      title: '安全设置',
      requiresAuth: true,
      roles: ['SUPER_ADMIN'],
      resource: 'SETTINGS',
      action: 'SECURITY'
    }
  },
  {
    path: 'settings/monitoring',
    name: 'SystemMonitoring',
    component: () => import('@/views/settings/monitoring/index.vue'),
    meta: {
      title: '系统监控',
      requiresAuth: true,
      roles: ['SUPER_ADMIN'],
      resource: 'SETTINGS',
      action: 'MONITORING'
    }
  }
]

export default settingsRoutes
