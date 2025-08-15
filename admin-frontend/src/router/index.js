import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('../layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue')
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('../views/Users.vue'),
        meta: { requiresRole: 'admin' }
      },
      {
        path: 'institutions',
        name: 'Institutions',
        component: () => import('../views/Institutions.vue'),
        meta: { requiresRole: 'admin' }
      },
      {
        path: 'candidates',
        name: 'Candidates',
        component: () => import('../views/Candidates.vue')
      },
      {
        path: 'candidates/import',
        name: 'CandidatesImport',
        component: () => import('../views/CandidatesImport.vue')
      },
      {
        path: 'schedules',
        name: 'Schedules',
        component: () => import('../views/Schedules.vue'),
        meta: { requiresRole: 'exam_admin' }
      },
      {
        path: 'venues',
        name: 'Venues',
        component: () => import('../views/Venues.vue'),
        meta: { requiresRole: 'exam_admin' }
      },
      {
        path: 'exam-products',
        name: 'ExamProducts',
        component: () => import('../views/ExamProducts.vue'),
        meta: { requiresRole: 'exam_admin' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresRole) {
    // 检查角色权限
    const userRole = authStore.user?.role?.name
    if (!userRole || (to.meta.requiresRole !== userRole && !authStore.user?.is_superuser)) {
      next('/')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router