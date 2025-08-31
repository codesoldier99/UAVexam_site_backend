import { createRouter, createWebHistory } from "vue-router";
import { useUserStore } from "@/stores/user";
import { checkPermission } from "@/config/permissions";
import NProgress from "nprogress";
import "nprogress/nprogress.css";
import dashboardRoutes from "./modules/dashboard";
import examRoutes from "./modules/exam-new";
import personnelRoutes from "./modules/personnel";
import attendanceRoutes from "./modules/attendance";
import attendanceNewRoutes from "./modules/attendance-new";
import settingsRoutes from "./modules/settings";
import registrationRoutes from "./modules/registration";
import candidatesRoutes from "./modules/candidates";

const routes = [
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/login/index.vue"),
    meta: {
      title: "登录",
      hidden: true
    }
  },
  {
    path: "/",
    name: "Layout",
    component: () => import("@/layouts/AdminLayout.vue"),
    redirect: "/dashboard/index",
    children: [
      dashboardRoutes,
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/profile/index.vue'),
        meta: {
          title: '个人信息',
          requiresAuth: true
        }
      },
      {
        path: 'change-password',
        name: 'ChangePassword',
        component: () => import('@/views/change-password/index.vue'),
        meta: {
          title: '修改密码',
          requiresAuth: true
        }
      },
      ...examRoutes,
      ...personnelRoutes,
      ...attendanceRoutes,
      ...settingsRoutes,
      ...registrationRoutes,
      ...candidatesRoutes,
      ...attendanceNewRoutes
    ],
    meta: {
      requiresAuth: true
    }
  },
  {
    path: "/403",
    name: "Forbidden",
    component: () => import("@/views/error/403.vue"),
    meta: {
      title: "403",
      hidden: true
    }
  },
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: () => import("@/views/error/404.vue"),
    meta: {
      title: "404",
      hidden: true
    }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// 路由权限检查函数
interface RoutePermissionResult {
  allowed: boolean;
  reason?: string;
}

const checkRoutePermission = (to: any, userStore: any): RoutePermissionResult => {
  const userRole = userStore.userInfo?.role;
  
  if (!userRole) {
    return { allowed: false, reason: '用户角色未定义' };
  }
  
  // SUPER_ADMIN 拥有所有权限 - 角色匹配时忽略大小写
  const normalizedUserRole = userRole.toUpperCase();
  if (normalizedUserRole === 'SUPER_ADMIN') {
    return { allowed: true };
  }
  
  // 优先检查资源权限（新版本）
  if (to.meta.resource && to.meta.action) {
    const hasResourcePermission = checkPermission(normalizedUserRole, to.meta.resource, to.meta.action);
    if (!hasResourcePermission) {
      return { 
        allowed: false, 
        reason: `需要资源权限: ${to.meta.resource}.${to.meta.action}，当前角色: ${userRole}` 
      };
    }
    // 如果资源权限检查通过，直接返回允许
    return { allowed: true };
  }
  
  // 检查角色权限（兼容旧版本，仅在没有资源权限配置时使用）
  if (to.meta.roles && to.meta.roles.length > 0) {
    const hasRolePermission = userStore.hasRole(to.meta.roles);
    if (!hasRolePermission) {
      return { 
        allowed: false, 
        reason: `需要角色权限: ${to.meta.roles.join(', ')}，当前角色: ${userRole}` 
      };
    }
  }
  
  return { allowed: true };
};

// 路由守卫
router.beforeEach(async (to, from, next) => {
  NProgress.start();
  
  // 添加调试信息
  console.log('路由跳转:', {
    from: from.path,
    to: to.path,
    matched: to.matched.length,
    routes: to.matched.map(r => r.path),
    meta: to.meta
  });
  
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 无人机考试管理系统` : "无人机考试管理系统";
  
  // 如果是登录页面，直接放行
  if (to.path === '/login') {
    next();
    return;
  }
  
  const userStore = useUserStore();
  
  // 检查是否已登录
  if (!userStore.token) {
    console.log('未登录，跳转到登录页');
    next({
      path: "/login",
      query: { redirect: to.fullPath }
    });
    return;
  }
  
  // 确保用户信息已加载
  if (!userStore.userInfo) {
    try {
      await userStore.getUserInfo();
    } catch (error) {
      console.error('获取用户信息失败:', error);
      userStore.logout();
      next('/login');
      return;
    }
  }
  
  // 检查是否需要权限验证
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 增强的权限检查逻辑
    const hasRoutePermission = checkRoutePermission(to, userStore);
    
    if (!hasRoutePermission.allowed) {
      console.log('路由权限检查失败:', {
        路由: to.path,
        用户角色: userStore.userInfo?.role,
        权限要求: to.meta,
        失败原因: hasRoutePermission.reason
      });
      
      // 重定向到403页面，并传递相关信息
      next({ 
        path: "/403", 
        query: { 
          from: to.path,
          reason: hasRoutePermission.reason 
        }
      });
      return;
    }
  }
  
  next();
});

router.afterEach(() => {
  NProgress.done();
});

export default router;