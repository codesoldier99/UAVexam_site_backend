<template>
  <div v-if="hasPermission">
    <slot></slot>
  </div>
  <div v-else>
    <el-empty description="您没有权限访问此内容" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'
import type { UserRole } from '@/types/user'

const props = defineProps<{
  roles?: UserRole[]
  permission?: string
}>()

const userStore = useUserStore()

const hasPermission = computed(() => {
  if (!props.roles && !props.permission) return true
  
  if (props.roles && props.roles.length > 0) {
    return userStore.hasRole(props.roles)
  }
  
  if (props.permission) {
    return userStore.hasPermission(props.permission)
  }
  
  return false
})
</script>