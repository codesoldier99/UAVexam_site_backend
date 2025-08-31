import { RouteRecordRaw } from 'vue-router'

const personnelRoutes: RouteRecordRaw[] = [
  {
    path: 'personnel/examiners',
    name: 'Examiners',
    component: () => import('@/views/admin/personnel/ExaminerList.vue'),
    meta: {
      title: '考官管理',
      icon: 'user-tie',
      requiresAuth: true,
      roles: ['super_admin', 'admin'],
      resource: 'EXAMINER',
      action: 'READ'
    }
  },
  {
    path: 'personnel/candidates',
    name: 'Candidates',
    component: () => import('@/views/admin/personnel/CandidateList.vue'),
    meta: {
      title: '考生管理',
      icon: 'users',
      requiresAuth: true,
      roles: ['super_admin', 'admin', 'operator'],
      resource: 'CANDIDATE',
      action: 'READ'
    }
  },
  {
    path: 'personnel/assignments',
    name: 'Assignment',
    component: () => import('@/views/admin/personnel/AssignmentManager.vue'),
    meta: {
      title: '人员分配',
      icon: 'user-plus',
      requiresAuth: true,
      roles: ['super_admin', 'admin'],
      resource: 'ASSIGNMENT',
      action: 'READ'
    }
  }
]

export default personnelRoutes
