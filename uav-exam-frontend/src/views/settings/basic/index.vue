<template>
  <div class="basic-settings-page">
    <div class="page-header">
      <h2>基础设置</h2>
      <p>系统基础配置管理</p>
    </div>
    
    <div class="content-card">
      <el-card>
        <template #header>
          <span>系统配置</span>
        </template>
        
        <el-form :model="settings" label-width="120px">
          <el-form-item label="系统名称">
            <el-input v-model="settings.systemName" placeholder="请输入系统名称" />
          </el-form-item>
          
          <el-form-item label="系统版本">
            <el-input v-model="settings.systemVersion" placeholder="请输入系统版本" />
          </el-form-item>
          
          <el-form-item label="系统描述">
            <el-input 
              v-model="settings.systemDescription" 
              type="textarea" 
              :rows="3"
              placeholder="请输入系统描述"
            />
          </el-form-item>
          
          <el-form-item label="联系电话">
            <el-input v-model="settings.contactPhone" placeholder="请输入联系电话" />
          </el-form-item>
          
          <el-form-item label="联系邮箱">
            <el-input v-model="settings.contactEmail" placeholder="请输入联系邮箱" />
          </el-form-item>
          
          <el-form-item label="系统地址">
            <el-input v-model="settings.systemAddress" placeholder="请输入系统地址" />
          </el-form-item>
          
          <el-form-item label="备案信息">
            <el-input v-model="settings.recordInfo" placeholder="请输入备案信息" />
          </el-form-item>
          
          <el-form-item label="维护模式">
            <el-switch 
              v-model="settings.maintenanceMode"
              active-text="开启"
              inactive-text="关闭"
            />
          </el-form-item>
          
          <el-form-item label="用户注册">
            <el-switch 
              v-model="settings.allowRegistration"
              active-text="允许"
              inactive-text="禁止"
            />
          </el-form-item>
          
          <el-form-item label="数据备份">
            <el-switch 
              v-model="settings.autoBackup"
              active-text="自动"
              inactive-text="手动"
            />
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="handleSave">保存设置</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
    
    <div class="content-card">
      <el-card>
        <template #header>
          <span>系统信息</span>
        </template>
        
        <el-descriptions :column="2" border>
          <el-descriptions-item label="服务器时间">
            {{ systemInfo.serverTime }}
          </el-descriptions-item>
          <el-descriptions-item label="系统运行时间">
            {{ systemInfo.uptime }}
          </el-descriptions-item>
          <el-descriptions-item label="数据库版本">
            {{ systemInfo.databaseVersion }}
          </el-descriptions-item>
          <el-descriptions-item label="PHP版本">
            {{ systemInfo.phpVersion }}
          </el-descriptions-item>
          <el-descriptions-item label="磁盘使用">
            {{ systemInfo.diskUsage }}
          </el-descriptions-item>
          <el-descriptions-item label="内存使用">
            {{ systemInfo.memoryUsage }}
          </el-descriptions-item>
        </el-descriptions>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const settings = ref({
  systemName: '无人机考试管理系统',
  systemVersion: 'v1.0.0',
  systemDescription: '专业的无人机考试管理平台，提供完整的考试流程管理功能',
  contactPhone: '400-123-4567',
  contactEmail: 'admin@uav-exam.com',
  systemAddress: '北京市朝阳区建国路88号',
  recordInfo: '京ICP备12345678号',
  maintenanceMode: false,
  allowRegistration: true,
  autoBackup: true
})

const systemInfo = ref({
  serverTime: '2024-01-15 16:30:00',
  uptime: '15天 8小时 30分钟',
  databaseVersion: 'MySQL 8.0.25',
  phpVersion: 'PHP 8.1.0',
  diskUsage: '45.2GB / 100GB (45%)',
  memoryUsage: '2.1GB / 8GB (26%)'
})

const handleSave = () => {
  // 这里应该调用保存设置的API
  ElMessage.success('设置保存成功!')
}

const handleReset = () => {
  // 重置为默认值
  ElMessage.info('设置已重置')
}

onMounted(() => {
  // 加载系统设置和信息
})
</script>

<style lang="scss" scoped>
.basic-settings-page {
  .page-header {
    margin-bottom: 20px;
    
    h2 {
      margin: 0 0 8px 0;
      color: #303133;
    }
    
    p {
      margin: 0;
      color: #909399;
    }
  }
  
  .content-card {
    margin-bottom: 20px;
    
    &:last-child {
      margin-bottom: 0;
    }
  }
}
</style>