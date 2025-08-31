<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="max-w-md w-full bg-white shadow-lg rounded-lg p-8 text-center">
      <div class="mb-6">
        <div class="text-6xl font-bold text-red-500 mb-4">403</div>
        <h1 class="text-2xl font-semibold text-gray-800 mb-2">访问被拒绝</h1>
        <p class="text-gray-600 mb-4">
          抱歉，您没有权限访问此页面
        </p>
        <div v-if="reason" class="bg-red-50 border border-red-200 rounded-md p-3 mb-4">
          <p class="text-sm text-red-700">{{ reason }}</p>
        </div>
        <div v-if="fromPath" class="bg-gray-50 border border-gray-200 rounded-md p-3 mb-4">
          <p class="text-sm text-gray-600">尝试访问的页面: {{ fromPath }}</p>
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
        <p>如果您认为这是一个错误，请联系系统管理员</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const reason = ref<string>('')
const fromPath = ref<string>('')

onMounted(() => {
  reason.value = route.query.reason as string || ''
  fromPath.value = route.query.from as string || ''
})

const goBack = () => {
  router.go(-1)
}

const goHome = () => {
  router.push('/dashboard/index')
}
</script>