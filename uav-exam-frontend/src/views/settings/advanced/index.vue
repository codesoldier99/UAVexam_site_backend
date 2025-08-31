<template>
  <div class="advanced-settings-page">
    <div class="page-header">
      <h2>高级设置</h2>
      <p>系统高级功能配置</p>
    </div>
    
    <div class="content-card">
      <el-card>
        <template #header>
          <span>缓存设置</span>
        </template>
        
        <el-form :model="cacheSettings" label-width="120px">
          <el-form-item label="Redis缓存">
            <el-switch 
              v-model="cacheSettings.redisEnabled"
              active-text="启用"
              inactive-text="禁用"
            />
          </el-form-item>
          
          <el-form-item label="缓存过期时间">
            <el-input-number 
              v-model="cacheSettings.expireTime"
              :min="1"
              :max="3600"
              controls-position="right"
            />
            <span style="margin-left: 10px;">秒</span>
          </el-form-item>
          
          <el-form-item label="文件缓存">
            <el-switch 
              v-model="cacheSettings.fileCache"
              active-text="启用"
              inactive-text="禁用"
            />
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="handleClearCache">清空缓存</el-button>
            <el-button type="warning" @click="handleRefreshCache">刷新缓存</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
    
    <div class="content-card">
      <el-card>
        <template #header>
          <span>API设置</span>
        </template>
        
        <el-form :model="apiSettings" label-width="120px">
          <el-form-item label="API限流">
            <el-switch 
              v-model="apiSettings.rateLimitEnabled"
              active-text="启用"
              inactive-text="禁用"
            />
          </el-form-item>
          
          <el-form-item label="每分钟请求数">
            <el-input-number 
              v-model="apiSettings.requestsPerMinute"
              :min="10"
              :max="1000"
              controls-position="right"
            />
          </el-form-item>
          
          <el-form-item label="API版本">
            <el-select v-model="apiSettings.version" placeholder="请选择API版本">
              <el-option label="v1.0" value="v1.0" />
              <el-option label="v1.1" value="v1.1" />
              <el-option label="v2.0" value="v2.0" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="跨域设置">
            <el-input 
              v-model="apiSettings.corsOrigins"
              type="textarea"
              :rows="3"
              placeholder="请输入允许的域名，多个域名用逗号分隔"
            />
          </el-form-item>
        </el-form>
      </el-card>
    </div>
    
    <div class="content-card">
      <el-card>
        <template #header>
          <span>性能优化</span>
        </template>
        
        <el-form :model="performanceSettings" label-width="120px">
          <el-form-item label="数据库连接池">
            <el-input-number 
              v-model="performanceSettings.dbPoolSize"
              :min="5"
              :max="100"
              controls-position="right"
            />
          </el-form-item>
          
          <el-form-item label="查询超时时间">
            <el-input-number 
              v-model="performanceSettings.queryTimeout"
              :min="5"
              :max="300"
              controls-position="right"
            />
            <span style="margin-left: 10px;">秒</span>
          </el-form-item>
          
          <el-form-item label="静态资源压缩">
            <el-switch 
              v-model="performanceSettings.gzipEnabled"
              active-text="启用"
              inactive-text="禁用"
            />
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="handleSaveSettings">保存设置</el-button>
            <el-button @click="handleResetSettings">重置设置</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const cacheSettings = ref({
  redisEnabled: true,
  expireTime: 3600,
  fileCache: true
})

const apiSettings = ref({
  rateLimitEnabled: true,
  requestsPerMinute: 100,
  version: 'v1.0',
  corsOrigins: 'http://localhost:3000,https://example.com'
})

const performanceSettings = ref({
  dbPoolSize: 20,
  queryTimeout: 30,
  gzipEnabled: true
})

const handleClearCache = () => {
  ElMessage.success('缓存已清空')
}

const handleRefreshCache = () => {
  ElMessage.success('缓存已刷新')
}

const handleSaveSettings = () => {
  ElMessage.success('高级设置保存成功')
}

const handleResetSettings = () => {
  ElMessage.info('设置已重置为默认值')
}

onMounted(() => {
  // 加载高级设置数据
})
</script>

<style lang="scss" scoped>
.advanced-settings-page {
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