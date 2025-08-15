<template>
  <el-container class="main-layout">
    <el-aside width="200px" class="sidebar">
      <div class="logo">
        <h3>考点管理系统</h3>
      </div>
      
      <el-menu
        :default-active="activeMenu"
        router
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
      >
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          <span>首页</span>
        </el-menu-item>
        
        <el-sub-menu index="user-management" v-if="authStore.isSuperAdmin">
          <template #title>
            <el-icon><UserFilled /></el-icon>
            <span>用户管理</span>
          </template>
          <el-menu-item index="/users">用户列表</el-menu-item>
          <el-menu-item index="/institutions">培训机构</el-menu-item>
        </el-sub-menu>
        
        <el-sub-menu index="candidate-management">
          <template #title>
            <el-icon><User /></el-icon>
            <span>考生管理</span>
          </template>
          <el-menu-item index="/candidates">考生列表</el-menu-item>
          <el-menu-item index="/candidates/import">批量导入</el-menu-item>
        </el-sub-menu>
        
        <el-sub-menu index="exam-management" v-if="authStore.isExamAdmin">
          <template #title>
            <el-icon><Calendar /></el-icon>
            <span>考务管理</span>
          </template>
          <el-menu-item index="/schedules">排期管理</el-menu-item>
          <el-menu-item index="/venues">考场管理</el-menu-item>
          <el-menu-item index="/exam-products">考试产品</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header class="header">
        <div class="header-left">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item v-if="currentRoute">{{ currentRoute }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        
        <div class="header-right">
          <el-dropdown>
            <span class="user-info">
              <el-icon><UserFilled /></el-icon>
              {{ authStore.user?.full_name || authStore.user?.username }}
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleLogout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const activeMenu = computed(() => route.path)
const currentRoute = computed(() => route.meta?.title || route.name)

const handleLogout = () => {
  authStore.logout()
  ElMessage.success('已退出登录')
  router.push('/login')
}
</script>

<style scoped>
.main-layout {
  height: 100vh;
}

.sidebar {
  background-color: #304156;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #2b3648;
  color: white;
}

.logo h3 {
  margin: 0;
}

.header {
  background-color: white;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  gap: 5px;
}

.main-content {
  background-color: #f5f7fa;
}
</style>