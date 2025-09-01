import type { RouteRecordRaw } from 'vue-router'

const examProductsRoutes: RouteRecordRaw[] = [
  {
    path: '/exam/products',
    name: 'ExamProducts',
    component: () => import('@/views/exam-products/index.vue'),
    meta: {
      title: '考试产品管理',
      requiresAuth: true,
      resource: 'EXAM_PRODUCT',
      action: 'READ'
    }
  }
]

export default examProductsRoutes