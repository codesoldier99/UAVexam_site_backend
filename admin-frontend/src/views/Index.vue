<template>
  <div class="index-page">
    <el-result icon="info" title="欢迎使用无人机考点管理系统">
      <template #sub-title>
        <p>请先登录系统</p>
      </template>
      <template #extra>
        <el-button type="primary" @click="$router.push('/login')">前往登录</el-button>
      </template>
    </el-result>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

onMounted(() => {
  // 如果已登录，跳转到首页
  if (authStore.isAuthenticated) {
    router.push('/dashboard')
  } else {
    router.push('/login')
  }
})
</script>

<style scoped>
.index-page {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>