<template>
  <el-breadcrumb separator="/" class="breadcrumb">
    <el-breadcrumb-item :to="{ path: '/' }">
      <el-icon><HomeFilled /></el-icon>
      <span>首页</span>
    </el-breadcrumb-item>
    
    <el-breadcrumb-item
      v-for="(item, index) in breadcrumbList"
      :key="item.path"
      :to="index === breadcrumbList.length - 1 ? undefined : { path: item.path }"
    >
      <el-icon v-if="item.icon">
        <component :is="item.icon" />
      </el-icon>
      <span>{{ item.title }}</span>
    </el-breadcrumb-item>
  </el-breadcrumb>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getUserMenus, getMenuBreadcrumb } from '@/config/menu'
import { HomeFilled } from '@element-plus/icons-vue'

const route = useRoute()
const userStore = useUserStore()

// 获取面包屑导航
const breadcrumbList = computed(() => {
  if (!userStore.userInfo?.role) return []
  
  const userMenus = getUserMenus(userStore.userInfo.role)
  const breadcrumb = getMenuBreadcrumb(userMenus, route.path)
  
  // 过滤掉首页，因为已经在模板中硬编码了
  return breadcrumb.filter(item => item.path !== '/' && item.path !== '/dashboard')
})
</script>

<style lang="scss" scoped>
.breadcrumb {
  :deep(.el-breadcrumb__item) {
    .el-breadcrumb__inner {
      display: flex;
      align-items: center;
      gap: 4px;
      
      &.is-link {
        color: #409EFF;
        
        &:hover {
          color: #66b1ff;
        }
      }
    }
    
    &:last-child {
      .el-breadcrumb__inner {
        color: #606266;
        font-weight: 500;
      }
    }
  }
}
</style>