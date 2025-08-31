<template>
  <div class="settings page-container">
    <div class="page-header">
      <h2 class="page-title">系统设置</h2>
      <p class="page-description">管理系统的基本配置和参数</p>
    </div>
    
    <el-row :gutter="20">
      <!-- 基本设置 -->
      <el-col :span="12">
        <el-card class="settings-card">
          <template #header>
            <div class="card-header">
              <el-icon><Setting /></el-icon>
              <span>基本设置</span>
            </div>
          </template>
          
          <el-form :model="basicSettings" label-width="120px">
            <el-form-item label="系统名称">
              <el-input v-model="basicSettings.systemName" placeholder="请输入系统名称" />
            </el-form-item>
            <el-form-item label="系统版本">
              <el-input v-model="basicSettings.version" placeholder="请输入系统版本" />
            </el-form-item>
            <el-form-item label="系统描述">
              <el-input
                v-model="basicSettings.description"
                type="textarea"
                :rows="3"
                placeholder="请输入系统描述"
              />
            </el-form-item>
            <el-form-item label="维护模式">
              <el-switch
                v-model="basicSettings.maintenanceMode"
                active-text="开启"
                inactive-text="关闭"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveBasicSettings" :loading="basicLoading">
                保存设置
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      
      <!-- 邮件设置 -->
      <el-col :span="12">
        <el-card class="settings-card">
          <template #header>
            <div class="card-header">
              <el-icon><Message /></el-icon>
              <span>邮件设置</span>
            </div>
          </template>
          
          <el-form :model="emailSettings" label-width="120px">
            <el-form-item label="SMTP服务器">
              <el-input v-model="emailSettings.smtpHost" placeholder="请输入SMTP服务器地址" />
            </el-form-item>
            <el-form-item label="SMTP端口">
              <el-input-number v-model="emailSettings.smtpPort" :min="1" :max="65535" />
            </el-form-item>
            <el-form-item label="发件人邮箱">
              <el-input v-model="emailSettings.fromEmail" placeholder="请输入发件人邮箱" />
            </el-form-item>
            <el-form-item label="邮箱密码">
              <el-input
                v-model="emailSettings.password"
                type="password"
                placeholder="请输入邮箱密码"
                show-password
              />
            </el-form-item>
            <el-form-item label="启用SSL">
              <el-switch
                v-model="emailSettings.enableSSL"
                active-text="开启"
                inactive-text="关闭"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveEmailSettings" :loading="emailLoading">
                保存设置
              </el-button>
              <el-button @click="testEmail" :loading="testLoading">
                测试邮件
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;">
      <!-- 安全设置 -->
      <el-col :span="12">
        <el-card class="settings-card">
          <template #header>
            <div class="card-header">
              <el-icon><Lock /></el-icon>
              <span>安全设置</span>
            </div>
          </template>
          
          <el-form :model="securitySettings" label-width="120px">
            <el-form-item label="密码最小长度">
              <el-input-number v-model="securitySettings.minPasswordLength" :min="6" :max="20" />
            </el-form-item>
            <el-form-item label="登录失败次数">
              <el-input-number v-model="securitySettings.maxLoginAttempts" :min="3" :max="10" />
            </el-form-item>
            <el-form-item label="账户锁定时间">
              <el-input-number v-model="securitySettings.lockoutDuration" :min="5" :max="60" />
              <span style="margin-left: 8px; color: #909399;">分钟</span>
            </el-form-item>
            <el-form-item label="会话超时时间">
              <el-input-number v-model="securitySettings.sessionTimeout" :min="30" :max="480" />
              <span style="margin-left: 8px; color: #909399;">分钟</span>
            </el-form-item>
            <el-form-item label="强制HTTPS">
              <el-switch
                v-model="securitySettings.forceHttps"
                active-text="开启"
                inactive-text="关闭"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveSecuritySettings" :loading="securityLoading">
                保存设置
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      
      <!-- 系统信息 -->
      <el-col :span="12">
        <el-card class="settings-card">
          <template #header>
            <div class="card-header">
              <el-icon><Monitor /></el-icon>
              <span>系统信息</span>
            </div>
          </template>
          
          <el-descriptions :column="1" border>
            <el-descriptions-item label="系统版本">{{ systemInfo.version }}</el-descriptions-item>
            <el-descriptions-item label="运行时间">{{ systemInfo.uptime }}</el-descriptions-item>
            <el-descriptions-item label="CPU使用率">
              <el-progress :percentage="systemInfo.cpuUsage" :color="getProgressColor(systemInfo.cpuUsage)" />
            </el-descriptions-item>
            <el-descriptions-item label="内存使用率">
              <el-progress :percentage="systemInfo.memoryUsage" :color="getProgressColor(systemInfo.memoryUsage)" />
            </el-descriptions-item>
            <el-descriptions-item label="磁盘使用率">
              <el-progress :percentage="systemInfo.diskUsage" :color="getProgressColor(systemInfo.diskUsage)" />
            </el-descriptions-item>
            <el-descriptions-item label="数据库状态">
              <el-tag :type="systemInfo.dbStatus === 'connected' ? 'success' : 'danger'">
                {{ systemInfo.dbStatus === 'connected' ? '已连接' : '未连接' }}
              </el-tag>
            </el-descriptions-item>
          </el-descriptions>
          
          <div style="margin-top: 20px; text-align: center;">
            <el-button @click="refreshSystemInfo" :loading="refreshLoading">
              <el-icon><Refresh /></el-icon>
              刷新信息
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Setting, Message, Lock, Monitor, Refresh } from '@element-plus/icons-vue'

// 加载状态
const basicLoading = ref(false)
const emailLoading = ref(false)
const securityLoading = ref(false)
const testLoading = ref(false)
const refreshLoading = ref(false)

// 基本设置
const basicSettings = reactive({
  systemName: '无人机考试管理系统',
  version: '1.0.0',
  description: '专业的无人机考试管理平台，提供完整的考试流程管理功能',
  maintenanceMode: false
})

// 邮件设置
const emailSettings = reactive({
  smtpHost: 'smtp.qq.com',
  smtpPort: 587,
  fromEmail: '',
  password: '',
  enableSSL: true
})

// 安全设置
const securitySettings = reactive({
  minPasswordLength: 8,
  maxLoginAttempts: 5,
  lockoutDuration: 15,
  sessionTimeout: 120,
  forceHttps: false
})

// 系统信息
const systemInfo = reactive({
  version: '1.0.0',
  uptime: '3天 12小时 45分钟',
  cpuUsage: 35,
  memoryUsage: 68,
  diskUsage: 42,
  dbStatus: 'connected'
})

// 保存基本设置
const saveBasicSettings = async () => {
  basicLoading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('基本设置保存成功')
  } catch (error) {
    console.error('保存基本设置失败:', error)
    ElMessage.error('保存基本设置失败')
  } finally {
    basicLoading.value = false
  }
}

// 保存邮件设置
const saveEmailSettings = async () => {
  emailLoading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('邮件设置保存成功')
  } catch (error) {
    console.error('保存邮件设置失败:', error)
    ElMessage.error('保存邮件设置失败')
  } finally {
    emailLoading.value = false
  }
}

// 保存安全设置
const saveSecuritySettings = async () => {
  securityLoading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('安全设置保存成功')
  } catch (error) {
    console.error('保存安全设置失败:', error)
    ElMessage.error('保存安全设置失败')
  } finally {
    securityLoading.value = false
  }
}

// 测试邮件
const testEmail = async () => {
  if (!emailSettings.fromEmail) {
    ElMessage.warning('请先填写发件人邮箱')
    return
  }
  
  testLoading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 2000))
    ElMessage.success('测试邮件发送成功')
  } catch (error) {
    console.error('测试邮件发送失败:', error)
    ElMessage.error('测试邮件发送失败')
  } finally {
    testLoading.value = false
  }
}

// 刷新系统信息
const refreshSystemInfo = async () => {
  refreshLoading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 模拟更新系统信息
    systemInfo.cpuUsage = Math.floor(Math.random() * 100)
    systemInfo.memoryUsage = Math.floor(Math.random() * 100)
    systemInfo.diskUsage = Math.floor(Math.random() * 100)
    
    ElMessage.success('系统信息刷新成功')
  } catch (error) {
    console.error('刷新系统信息失败:', error)
    ElMessage.error('刷新系统信息失败')
  } finally {
    refreshLoading.value = false
  }
}

// 获取进度条颜色
const getProgressColor = (percentage: number) => {
  if (percentage < 50) return '#67c23a'
  if (percentage < 80) return '#e6a23c'
  return '#f56c6c'
}

// 页面加载时获取设置数据
onMounted(async () => {
  try {
    // 模拟获取设置数据
    await new Promise(resolve => setTimeout(resolve, 500))
  } catch (error) {
    console.error('获取设置数据失败:', error)
  }
})
</script>

<style scoped>
.settings {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px 0;
}

.page-description {
  color: #909399;
  margin: 0;
}

.settings-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.el-form-item {
  margin-bottom: 20px;
}

.el-descriptions {
  margin-bottom: 20px;
}

.el-progress {
  width: 100%;
}

@media (max-width: 768px) {
  .el-col {
    margin-bottom: 20px;
  }
}
</style>