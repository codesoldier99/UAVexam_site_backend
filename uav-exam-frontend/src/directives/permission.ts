import type { Directive, DirectiveBinding } from 'vue'
import { useUserStore } from '@/stores/user'

interface PermissionValue {
  // 角色权限
  roles?: string[]
  // 资源权限
  resource?: string
  action?: string
  resourceId?: number
  // 组合权限（AND逻辑）
  and?: PermissionValue[]
  // 组合权限（OR逻辑）
  or?: PermissionValue[]
  // 反向权限（NOT逻辑）
  not?: PermissionValue
}

// 权限检查核心函数
const checkPermission = (value: any, userStore: any): boolean => {
  if (!value) return true
  
  // 字符串格式：单个角色
  if (typeof value === 'string') {
    return userStore.hasRole([value])
  }
  
  // 数组格式：多个角色（OR逻辑）
  if (Array.isArray(value)) {
    return userStore.hasRole(value)
  }
  
  // 对象格式：复杂权限检查
  if (typeof value === 'object') {
    const permValue = value as PermissionValue
    
    // 角色权限检查
    if (permValue.roles) {
      const roleResult = userStore.hasRole(permValue.roles)
      if (!roleResult) return false
    }
    
    // 资源权限检查
    if (permValue.resource && permValue.action) {
      const resourceResult = userStore.hasPermission(
        permValue.resource, 
        permValue.action, 
        permValue.resourceId
      )
      if (!resourceResult) return false
    }
    
    // AND逻辑：所有条件都必须满足
    if (permValue.and) {
      return permValue.and.every(condition => checkPermission(condition, userStore))
    }
    
    // OR逻辑：任一条件满足即可
    if (permValue.or) {
      return permValue.or.some(condition => checkPermission(condition, userStore))
    }
    
    // NOT逻辑：条件不满足
    if (permValue.not) {
      return !checkPermission(permValue.not, userStore)
    }
    
    return true
  }
  
  return false
}

const permission: Directive = {
  mounted(el: HTMLElement, binding: DirectiveBinding) {
    const { value } = binding
    const userStore = useUserStore()
    
    const hasPermission = checkPermission(value, userStore)
    
    if (!hasPermission) {
      // 根据修饰符决定隐藏方式
      if (binding.modifiers.remove) {
        // v-permission.remove - 完全移除元素
        el.parentNode?.removeChild(el)
      } else if (binding.modifiers.disable) {
        // v-permission.disable - 禁用元素
        el.setAttribute('disabled', 'true')
        el.style.opacity = '0.5'
        el.style.cursor = 'not-allowed'
      } else {
        // 默认：隐藏元素
        el.style.display = 'none'
      }
    }
  },
  
  updated(el: HTMLElement, binding: DirectiveBinding) {
    const { value } = binding
    const userStore = useUserStore()
    
    const hasPermission = checkPermission(value, userStore)
    
    if (hasPermission) {
      el.style.display = ''
      el.removeAttribute('disabled')
      el.style.opacity = ''
      el.style.cursor = ''
    } else {
      if (binding.modifiers.disable) {
        el.setAttribute('disabled', 'true')
        el.style.opacity = '0.5'
        el.style.cursor = 'not-allowed'
      } else {
        el.style.display = 'none'
      }
    }
  }
}

export default permission