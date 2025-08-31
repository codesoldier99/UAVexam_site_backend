<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="max-w-md w-full bg-white shadow-lg rounded-lg p-8 text-center">
      <div class="mb-6">
        <div class="text-6xl font-bold text-blue-500 mb-4">404</div>
        <h1 class="text-2xl font-semibold text-gray-800 mb-2">页面未找到</h1>
        <p class="text-gray-600 mb-4">
          抱歉，您访问的页面不存在或已被移除
        </p>
        <div v-if="currentPath" class="bg-gray-50 border border-gray-200 rounded-md p-3 mb-4">
          <p class="text-sm text-gray-600">当前路径: {{ currentPath }}</p>
        </div>
      </div>
      
      <div class="space-y-3">
        <button 
          @click="goBack" 
          class="w-full bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded-md transition-colors"
        >
          返回上一页
        </button>
        <button 
          @click="goHome" 
          class="w-full bg-gray-500 hover:bg-gray-600 text-white font-medium py-2 px-4 rounded-md transition-colors"
        >
          返回首页
        </button>
      </div>
      
      <div class="mt-6 text-sm text-gray-500">
        <p>请检查URL是否正确，或从导航菜单重新选择页面</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const currentPath = ref<string>('')

onMounted(() => {
  currentPath.value = route.path
})

const goBack = () => {
  router.go(-1)
}

const goHome = () => {
  router.push('/dashboard/index')
}
</script>