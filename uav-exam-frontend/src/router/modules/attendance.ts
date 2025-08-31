import { RouteRecordRaw } from 'vue-router'

const attendanceRoutes: RouteRecordRaw[] = [
  {
    path: 'attendance/manager',
    name: 'AttendanceManager',
    component: () => import('@/views/admin/attendance/AttendanceManager.vue'),
    meta: {
      title: '考勤记录',
      icon: 'calendar-check',
      requiresAuth: true,
      roles: ['super_admin', 'admin', 'examiner'],
      resource: 'ATTENDANCE',
      action: 'READ'
    }
  },
  {
    path: 'attendance/statistics',
    name: 'AttendanceStatistics',
    component: () => import('@/views/admin/attendance/AttendanceStatistics.vue'),
    meta: {
      title: '考勤统计',
      icon: 'chart-bar',
      requiresAuth: true,
      roles: ['super_admin', 'admin'],
      resource: 'ATTENDANCE',
      action: 'READ'
    }
  }
]

export default attendanceRoutes
