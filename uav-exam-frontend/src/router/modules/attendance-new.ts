export default [
  {
    path: '/attendance/record',
    name: 'AttendanceRecord',
    component: () => import('@/views/attendance/record/index.vue'),
    meta: {
      title: '考勤记录',
      resource: 'ATTENDANCE',
      action: 'READ',
      roles: ['super_admin', 'admin', 'examiner']
    }
  },
  {
    path: '/attendance/institution',
    name: 'AttendanceInstitution',
    component: () => import('@/views/attendance/institution/index.vue'),
    meta: {
      title: '机构考勤',
      resource: 'ATTENDANCE',
      action: 'INSTITUTION_READ',
      roles: ['operator']
    }
  },
  {
    path: '/exam-info',
    name: 'ExamInfo',
    component: () => import('@/views/exam-info/index.vue'),
    meta: {
      title: '考试信息',
      resource: 'EXAM_INFO',
      action: 'READ',
      roles: ['super_admin', 'admin', 'candidate']
    }
  },
  {
    path: '/my-attendance',
    name: 'MyAttendance',
    component: () => import('@/views/my-attendance/index.vue'),
    meta: {
      title: '我的考勤',
      resource: 'MY_ATTENDANCE',
      action: 'READ',
      roles: ['candidate']
    }
  },
  {
    path: '/settings/basic',
    name: 'BasicSettings',
    component: () => import('@/views/settings/basic/index.vue'),
    meta: {
      title: '基础设置',
      resource: 'SETTINGS',
      action: 'BASIC',
      roles: ['super_admin', 'admin']
    }
  }
]