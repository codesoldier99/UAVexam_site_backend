<template>
  <div v-if="hasPermission" :class="wrapperClass">
    <slot />
  </div>
  <div v-else-if="showFallback" :class="fallbackClass">
    <slot name="fallback">
      <div class="permission-denied">
        <el-empty 
          :image-size="100" 
          description="您没有权限访问此内容"
        >
          <template #image>
            <el-icon size="100" color="#c0c4cc">
              <Lock />
            </el-icon>
          </template>
        </el-empty>
      </div>
    </slot>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Lock } from '@element-plus/icons-vue'
import { usePermission, type PermissionConfig } from '@/composables/usePermission'

interface Props {
  // 权限配置
  permission?: PermissionConfig | string | string[]
  // 角色权限（向后兼容）
  roles?: string[]
  // 资源权限
  resource?: string
  action?: string
  resourceId?: number
  // 显示选项
  showFallback?: boolean
  wrapperClass?: string
  fallbackClass?: string
}

const props = withDefaults(defineProps<Props>(), {
  showFallback: false,
  wrapperClass: '',
  fallbackClass: 'permission-fallback'
})

const { hasPermission: checkPermission } = usePermission()

// 权限检查
const hasPermission = computed(() => {
  // 优先使用 permission 配置
  if (props.permission) {
    return checkPermission(props.permission)
  }
  
  // 使用角色权限（向后兼容）
  if (props.roles) {
    return checkPermission(props.roles)
  }
  
  // 使用资源权限
  if (props.resource && props.action) {
    return checkPermission({
      resource: props.resource,
      action: props.action,
      resourceId: props.resourceId
    })
  }
  
  // 默认允许访问
  return true
})
</script>

<style scoped>
.permission-denied {
  padding: 40px 20px;
  text-align: center;
  color: #909399;
}

.permission-fallback {
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>