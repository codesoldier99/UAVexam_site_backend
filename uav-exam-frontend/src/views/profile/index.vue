<template>
  <div class="profile-container">
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <span>个人信息</span>
        </div>
      </template>
      
      <el-form
        ref="profileFormRef"
        :model="profileForm"
        :rules="profileRules"
        label-width="100px"
        class="profile-form"
      >
        <el-form-item label="用户名">
          <el-input v-model="profileForm.username" disabled />
        </el-form-item>
        
        <el-form-item label="真实姓名" prop="real_name">
          <el-input v-model="profileForm.real_name" />
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="profileForm.email" />
        </el-form-item>
        
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="profileForm.phone" />
        </el-form-item>
        
        <el-form-item label="角色">
          <el-input v-model="roleDisplay" disabled />
        </el-form-item>
        
        <el-form-item label="机构ID" v-if="profileForm.institution_id">
          <el-input v-model="profileForm.institution_id" disabled />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="loading">
            保存修改
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, FormInstance, FormRules } from 'element-plus'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const profileFormRef = ref<FormInstance>()
const loading = ref(false)

// 表单数据
const profileForm = ref({
  username: '',
  real_name: '',
  email: '',
  phone: '',
  role: '',
  institution_id: ''
})

// 角色显示名称
const roleDisplay = computed(() => {
  const roleMap = {
    'SUPER_ADMIN': '超级管理员',
    'ADMIN': '管理员',
    'OPERATOR': '操作员',
    'EXAMINER': '考官',
    'CANDIDATE': '考生'
  }
  return roleMap[profileForm.value.role as keyof typeof roleMap] || profileForm.value.role
})

// 表单验证规则
const profileRules: FormRules = {
  real_name: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ]
}

// 初始化表单数据
const initForm = () => {
  if (userStore.userInfo) {
    profileForm.value = {
      username: userStore.userInfo.username || '',
      real_name: userStore.userInfo.real_name || '',
      email: userStore.userInfo.email || '',
      phone: userStore.userInfo.phone || '',
      role: userStore.userInfo.role || '',
      institution_id: userStore.userInfo.institution_id?.toString() || ''
    }
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!profileFormRef.value) return
  
  try {
    await profileFormRef.value.validate()
    loading.value = true
    
    const updateData = {
      real_name: profileForm.value.real_name,
      email: profileForm.value.email,
      phone: profileForm.value.phone
    }
    
    await userStore.updateProfile(updateData)
    ElMessage.success('个人信息更新成功')
  } catch (error) {
    console.error('更新个人信息失败:', error)
    ElMessage.error('更新失败，请重试')
  } finally {
    loading.value = false
  }
}

// 重置表单
const handleReset = () => {
  initForm()
}

onMounted(() => {
  initForm()
})
</script>

<style lang="scss" scoped>
.profile-container {
  max-width: 600px;
  margin: 0 auto;
}

.profile-card {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 600;
  }
}

.profile-form {
  .el-form-item {
    margin-bottom: 20px;
  }
}
</style>