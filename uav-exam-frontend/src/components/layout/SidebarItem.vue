<template>
  <div v-if="shouldShow" class="sidebar-item">
    <!-- 如果有子菜单 -->
    <el-sub-menu
      v-if="item.children && item.children.length > 0"
      :index="item.id"
      :popper-append-to-body="false"
    >
      <template #title>
        <el-icon v-if="item.icon">
          <component :is="getIconComponent(item.icon)" />
        </el-icon>
        <span class="menu-title">{{ item.title }}</span>
      </template>
      
      <sidebar-item
        v-for="child in item.children"
        :key="child.id"
        :item="child"
        :base-path="resolvePath(child.path)"
      />
    </el-sub-menu>
    
    <!-- 如果是单个菜单项 -->
    <el-menu-item
      v-else
      :index="item.path || item.id"
      @click="handleClick"
    >
      <el-icon v-if="item.icon">
        <component :is="getIconComponent(item.icon)" />
      </el-icon>
      <span class="menu-title">{{ item.title }}</span>
      <el-badge
        v-if="item.badge"
        :value="item.badge"
        class="menu-badge"
      />
    </el-menu-item>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import type { MenuItem } from '@/config/menu'
import * as ElementPlusIcons from '@element-plus/icons-vue'

interface Props {
  item: MenuItem
  basePath?: string
}

const props = withDefaults(defineProps<Props>(), {
  basePath: ''
})

const router = useRouter()
const userStore = useUserStore()

// 检查权限
const hasPermission = (item: MenuItem): boolean => {
  if (!item.roles || item.roles.length === 0) return true
  
  const userRole = userStore.userInfo?.role
  if (!userRole) return false
  
  // 角色匹配时忽略大小写
  const normalizedUserRole = userRole.toUpperCase()
  const normalizedRoles = item.roles.map(role => role.toUpperCase())
  
  // SUPER_ADMIN 拥有所有权限
  if (normalizedUserRole === 'SUPER_ADMIN') return true
  
  // 检查用户角色是否在允许的角色列表中
  return normalizedRoles.includes(normalizedUserRole)
}

// 检查当前菜单项是否应该显示
const shouldShow = computed(() => {
  return hasPermission(props.item)
})

// 解析路径
const resolvePath = (routePath?: string) => {
  if (!routePath) return props.basePath
  
  if (routePath.startsWith('/')) {
    return routePath
  }
  
  return props.basePath ? `${props.basePath}/${routePath}` : `/${routePath}`
}

// 获取图标组件
const getIconComponent = (iconName: string) => {
  // 处理Element Plus图标
  const iconComponent = (ElementPlusIcons as any)[iconName]
  if (iconComponent) {
    return iconComponent
  }
  
  // 如果找不到图标，返回默认图标
  return ElementPlusIcons.Document
}

// 处理点击事件
const handleClick = () => {
  if (props.item.path) {
    const fullPath = resolvePath(props.item.path)
    if (fullPath !== router.currentRoute.value.path) {
      router.push(fullPath)
    }
  }
}
</script>

<style lang="scss" scoped>
.sidebar-item {
  .menu-badge {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
  }
  
  .menu-title {
    margin-left: 8px;
  }
}

// 深度选择器修复菜单样式
:deep(.el-sub-menu__title) {
  height: 50px;
  line-height: 50px;
  
  .el-icon {
    margin-right: 8px;
    width: 16px;
    text-align: center;
  }
}

:deep(.el-menu-item) {
  height: 50px;
  line-height: 50px;
  
  .el-icon {
    margin-right: 8px;
    width: 16px;
    text-align: center;
  }
  
  &.is-active {
    background-color: #263445 !important;
    color: #409EFF !important;
  }
}
</style>