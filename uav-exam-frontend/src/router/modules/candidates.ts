import type { RouteRecordRaw } from 'vue-router'

const candidatesRoutes: RouteRecordRaw[] = [
  {
    path: 'candidates',
    name: 'Candidates',
    component: () => import('@/views/candidates/index.vue'),
    meta: {
      title: '考生管理',
      requiresAuth: true,
      roles: ['SUPER_ADMIN', 'ADMIN', 'OPERATOR', 'EXAMINER']
    }
  },
  {
    path: 'candidates/list',
    name: 'CandidatesList',
    component: () => import('@/views/candidates/list/index.vue'),
    meta: {
      title: '考生列表',
      requiresAuth: true,
      resource: 'CANDIDATE',
      action: 'READ',
      roles: ['SUPER_ADMIN', 'ADMIN', 'EXAMINER']
    }
  },
  {
    path: 'candidates/institution',
    name: 'CandidatesInstitution',
    component: () => import('@/views/candidates/institution/index.vue'),
    meta: {
      title: '机构考生',
      requiresAuth: true,
      resource: 'CANDIDATE',
      action: 'INSTITUTION_READ',
      roles: ['OPERATOR']
    }
  },
  {
    path: 'candidates/import',
    name: 'CandidatesImport',
    component: () => import('@/views/candidates/import/index.vue'),
    meta: {
      title: '考生导入',
      requiresAuth: true,
      resource: 'CANDIDATE',
      action: 'CREATE',
      roles: ['SUPER_ADMIN', 'ADMIN']
    }
  }
]

export default candidatesRoutes