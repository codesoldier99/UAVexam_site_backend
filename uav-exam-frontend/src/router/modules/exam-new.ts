import { RouteRecordRaw } from 'vue-router'

const examRoutes: RouteRecordRaw[] = [
  {
    path: 'exam/products',
    name: 'ExamProducts',
    component: () => import('@/views/exam/products/index.vue'),
    meta: {
      title: '考试产品',
      requiresAuth: true,
      roles: ['super_admin', 'admin'],
      resource: 'EXAM_PRODUCT',
      action: 'READ'
    }
  },
  {
    path: 'exam/venues',
    name: 'ExamVenues', 
    component: () => import('@/views/exam/venues/index.vue'),
    meta: {
      title: '考场管理',
      requiresAuth: true,
      roles: ['super_admin', 'admin'],
      resource: 'VENUE',
      action: 'READ'
    }
  },
  {
    path: 'exam/scheduling',
    name: 'ExamScheduling',
    component: () => import('@/views/exam/scheduling/index.vue'),
    meta: {
      title: '考试排期',
      requiresAuth: true,
      roles: ['super_admin', 'admin'],
      resource: 'SCHEDULING',
      action: 'READ'
    }
  },
]

export default examRoutes
