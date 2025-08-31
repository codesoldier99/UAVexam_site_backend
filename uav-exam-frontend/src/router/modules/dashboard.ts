import { RouteRecordRaw } from 'vue-router'

const dashboardRoutes: RouteRecordRaw = {
  path: 'dashboard/index',
  name: 'DashboardIndex',
  component: () => import('@/views/admin/dashboard/index.vue'),
  meta: {
    title: '首页',
    icon: 'home',
    requiresAuth: true,
    // 首页所有登录用户都可以访问
    roles: ['super_admin', 'admin', 'operator', 'examiner', 'candidate']
  }
}

export default dashboardRoutes
