<template>
  <div class="sidebar">
    <div class="sidebar-header">
      <div class="logo">
        <el-icon class="logo-icon"><Operation /></el-icon>
        <span class="logo-text">无人机考试系统</span>
      </div>
    </div>
    
    <el-scrollbar class="sidebar-scrollbar">
      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapse"
        :unique-opened="true"
        class="sidebar-menu"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
        @select="handleMenuSelect"
      >
        <sidebar-item
          v-for="menu in userMenus"
          :key="menu.id"
          :item="menu"
          :base-path="menu.path || ''"
        />
      </el-menu>
    </el-scrollbar>
    
    <div class="sidebar-footer">
      <el-button
        :icon="isCollapse ? Expand : Fold"
        circle
        size="small"
        @click="toggleCollapse"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getUserMenus, type MenuItem } from '@/config/menu'
import SidebarItem from './SidebarItem.vue'
import { Operation, Expand, Fold } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

// 侧边栏折叠状态
const isCollapse = ref(false)

// 获取用户菜单
const userMenus = computed(() => {
  if (!userStore.userInfo?.role) {
    console.log('用户角色为空，返回空菜单')
    return []
  }
  console.log('当前用户角色:', userStore.userInfo.role)
  const menus = getUserMenus(userStore.userInfo.role)
  console.log('获取到的菜单:', menus)
  return menus
})

// 当前激活的菜单
const activeMenu = computed(() => {
  const { path } = route
  return path
})

// 切换侧边栏折叠状态
const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
}

// 处理菜单选择
const handleMenuSelect = (path: string) => {
  if (path && path !== route.path) {
    router.push(path)
  }
}
</script>

<style lang="scss" scoped>
.sidebar {
  height: 100vh;
  width: 210px;
  background-color: #304156;
  display: flex;
  flex-direction: column;
  transition: width 0.3s;
  
  &.collapse {
    width: 64px;
  }
}

.sidebar-header {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #434a50;
  
  .logo {
    display: flex;
    align-items: center;
    color: #fff;
    font-size: 16px;
    font-weight: 600;
    
    .logo-icon {
      font-size: 24px;
      margin-right: 8px;
      color: #409EFF;
    }
    
    .logo-text {
      white-space: nowrap;
      transition: opacity 0.3s;
    }
  }
}

.sidebar-scrollbar {
  flex: 1;
  
  :deep(.el-scrollbar__view) {
    height: 100%;
  }
}

.sidebar-menu {
  border: none;
  height: 100%;
  width: 100% !important;
  
  :deep(.el-menu-item) {
    &.is-active {
      background-color: #263445 !important;
      
      &::before {
        content: '';
        position: absolute;
        right: 0;
        top: 0;
        bottom: 0;
        width: 3px;
        background-color: #409EFF;
      }
    }
    
    &:hover {
      background-color: #263445 !important;
    }
  }
  
  :deep(.el-sub-menu__title) {
    &:hover {
      background-color: #263445 !important;
    }
  }
  
  :deep(.el-sub-menu.is-active) {
    .el-sub-menu__title {
      color: #409EFF !important;
    }
  }
}

.sidebar-footer {
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-top: 1px solid #434a50;
  
  .el-button {
    background-color: transparent;
    border-color: #434a50;
    color: #bfcbd9;
    
    &:hover {
      background-color: #263445;
      border-color: #409EFF;
      color: #409EFF;
    }
  }
}

// 折叠状态样式
.sidebar.collapse {
  .logo-text {
    opacity: 0;
  }
  
  .sidebar-menu {
    :deep(.el-menu-item) {
      padding: 0 20px !important;
      text-align: center;
      
      .menu-title {
        display: none;
      }
    }
    
    :deep(.el-sub-menu) {
      .el-sub-menu__title {
        padding: 0 20px !important;
        text-align: center;
        
        .menu-title {
          display: none;
        }
        
        .el-sub-menu__icon-arrow {
          display: none;
        }
      }
    }
  }
}
</style>