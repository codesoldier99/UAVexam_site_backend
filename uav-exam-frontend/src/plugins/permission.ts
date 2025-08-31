import { App } from 'vue'
import permissionDirective from '@/directives/permission'
import PermissionGuard from '@/components/PermissionGuard.vue'

export default {
  install(app: App) {
    // 注册权限指令
    app.directive('permission', permissionDirective)
    
    // 注册权限守卫组件
    app.component('PermissionGuard', PermissionGuard)
  }
}