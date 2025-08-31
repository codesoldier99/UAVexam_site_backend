export default [
  {
    path: '/candidates/list',
    name: 'CandidatesList',
    component: () => import('@/views/candidates/list/index.vue'),
    meta: {
      title: '考生列表',
      resource: 'CANDIDATE',
      action: 'READ',
      roles: ['super_admin', 'admin', 'operator', 'examiner']
    }
  },
  {
    path: '/candidates/institution',
    name: 'CandidatesInstitution',
    component: () => import('@/views/candidates/institution/index.vue'),
    meta: {
      title: '机构考生',
      resource: 'CANDIDATE',
      action: 'INSTITUTION_READ',
      roles: ['operator']
    }
  },
  {
    path: '/candidates/import',
    name: 'CandidatesImport',
    component: () => import('@/views/candidates/import/index.vue'),
    meta: {
      title: '考生导入',
      resource: 'CANDIDATE',
      action: 'CREATE',
      roles: ['super_admin', 'admin', 'operator']
    }
  }
]