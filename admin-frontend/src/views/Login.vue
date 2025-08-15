<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <h2 class="login-title">无人机考点管理系统</h2>
      </template>
      
      <el-form 
        ref="loginForm" 
        :model="loginData" 
        :rules="loginRules"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginData.username"
            placeholder="请输入用户名"
            prefix-icon="User"
            size="large"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="loginData.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            size="large"
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            @click="handleLogin"
            style="width: 100%"
          >
            登 录
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="login-tips">
        <p>测试账号：</p>
        <p>超级管理员: admin / admin123</p>
        <p>考务管理员: examadmin / exam123</p>
        <p>培训机构: institution / inst123</p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const loginForm = ref()
const loading = ref(false)

const loginData = reactive({
  username: '',
  password: ''
})

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  const valid = await loginForm.value.validate()
  if (!valid) return
  
  loading.value = true
  try {
    const result = await authStore.login(loginData.username, loginData.password)
    if (result.success) {
      ElMessage.success('登录成功')
      router.push('/')
    } else {
      ElMessage.error(result.error)
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  width: 400px;
  border-radius: 10px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.login-title {
  text-align: center;
  margin: 0;
  color: #333;
  font-size: 24px;
}

.login-tips {
  margin-top: 20px;
  padding: 10px;
  background: #f5f5f5;
  border-radius: 5px;
  font-size: 12px;
  color: #666;
}

.login-tips p {
  margin: 5px 0;
}
</style>