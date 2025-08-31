import { RouteRecordRaw } from 'vue-router'

const examRoutes: RouteRecordRaw = {
  path: 'exam/list',
  name: 'ExamList',
  component: () => import('@/views/admin/exam/ExamList.vue'),
  meta: {
    title: '考试管理',
    icon: 'calendar',
    roles: ['ADMIN', 'SUPER_ADMIN']
  }
}

export default examRoutes
