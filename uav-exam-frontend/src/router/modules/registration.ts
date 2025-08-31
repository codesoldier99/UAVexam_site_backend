export default [
  {
    path: '/registration/upload',
    name: 'RegistrationUpload',
    component: () => import('@/views/registration/upload/index.vue'),
    meta: {
      title: '报名文件上传',
      resource: 'REGISTRATION',
      action: 'CREATE',
      roles: ['super_admin', 'admin', 'operator']
    }
  },
  {
    path: '/registration/list',
    name: 'RegistrationList',
    component: () => import('@/views/registration/list/index.vue'),
    meta: {
      title: '报名列表',
      resource: 'REGISTRATION',
      action: 'READ',
      roles: ['super_admin', 'admin', 'operator', 'examiner']
    }
  },
  {
    path: '/registration/my-registrations',
    name: 'MyRegistrations',
    component: () => import('@/views/registration/my-registrations/index.vue'),
    meta: {
      title: '我的报名',
      resource: 'REGISTRATION',
      action: 'MY_REGISTRATION',
      roles: ['operator']
    }
  }
]