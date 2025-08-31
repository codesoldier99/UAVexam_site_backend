<template>
  <div class="admin-layout">
    <!-- 动态侧边栏 -->
    <Sidebar />
    
    <!-- 主内容区 -->
    <div class="main-container" :class="{ 'main-expanded': isCollapsed }">
      <!-- 头部 -->
      <div class="header">
        <div class="header-left">
          <Breadcrumb />
        </div>
        
        <div class="header-right">
          <el-dropdown trigger="click" @command="handleCommand">
            <div class="user-info">
              <el-avatar :size="32" :src="userAvatar" />
              <span class="username">{{ displayName }}</span>
              <el-icon><CaretBottom /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                <el-dropdown-item command="changePassword">修改密码</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
      
      <!-- 内容区 -->
      <div class="content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { CaretBottom } from '@element-plus/icons-vue'
import Sidebar from '@/components/layout/Sidebar.vue'
import Breadcrumb from '@/components/layout/Breadcrumb.vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

// 侧边栏折叠状态
const isCollapsed = ref(false)

// 用户信息
const userInfo = computed(() => userStore.userInfo || {})
const userAvatar = computed(() => 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png')
const displayName = computed(() => {
  if (userInfo.value?.real_name) return userInfo.value.real_name
  if (userInfo.value?.username) return userInfo.value.username
  return '用户'
})

// 当前路由
const currentRoute = computed(() => route)

// 处理下拉菜单命令
const handleCommand = (command: string) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'changePassword':
      router.push('/change-password')
      break
    case 'logout':
      ElMessageBox.confirm('确定要退出登录吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        await userStore.logout()
        router.push('/login')
      }).catch(() => {})
      break
  }
}

// 页面加载时检查用户登录状态
onMounted(() => {
  // 这里可以添加检查登录状态的逻辑
})
</script>

<style lang="scss" scoped>
.admin-layout {
  display: flex;
  height: 100vh;
  
  .main-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    transition: margin-left 0.3s;
    
    .header {
      height: 60px;
      background-color: #fff;
      box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
      padding: 0 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      
      .header-left {
        display: flex;
        align-items: center;
      }
      
      .header-right {
        .user-info {
          display: flex;
          align-items: center;
          cursor: pointer;
          
          .username {
            margin: 0 8px;
          }
        }
      }
    }
    
    .content {
      flex: 1;
      padding: 20px;
      background-color: #f0f2f5;
      overflow-y: auto;
    }
  }
}

// 路由过渡动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>