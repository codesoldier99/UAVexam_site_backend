<template>
  <div class="security-settings-page">
    <div class="page-header">
      <h2>安全设置</h2>
      <p>系统安全策略配置</p>
    </div>
    
    <div class="content-card">
      <el-card>
        <template #header>
          <span>密码策略</span>
        </template>
        
        <el-form :model="passwordPolicy" label-width="120px">
          <el-form-item label="最小长度">
            <el-input-number 
              v-model="passwordPolicy.minLength"
              :min="6"
              :max="20"
              controls-position="right"
            />
          </el-form-item>
          
          <el-form-item label="必须包含数字">
            <el-switch 
              v-model="passwordPolicy.requireNumbers"
              active-text="是"
              inactive-text="否"
            />
          </el-form-item>
          
          <el-form-item label="必须包含字母">
            <el-switch 
              v-model="passwordPolicy.requireLetters"
              active-text="是"
              inactive-text="否"
            />
          </el-form-item>
          
          <el-form-item label="必须包含特殊字符">
            <el-switch 
              v-model="passwordPolicy.requireSpecialChars"
              active-text="是"
              inactive-text="否"
            />
          </el-form-item>
          
          <el-form-item label="密码有效期">
            <el-input-number 
              v-model="passwordPolicy.expireDays"
              :min="30"
              :max="365"
              controls-position="right"
            />
            <span style="margin-left: 10px;">天</span>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
    
    <div class="content-card">
      <el-card>
        <template #header>
          <span>登录安全</span>
        </template>
        
        <el-form :model="loginSecurity" label-width="120px">
          <el-form-item label="最大失败次数">
            <el-input-number 
              v-model="loginSecurity.maxFailAttempts"
              :min="3"
              :max="10"
              controls-position="right"
            />
          </el-form-item>
          
          <el-form-item label="锁定时间">
            <el-input-number 
              v-model="loginSecurity.lockoutDuration"
              :min="5"
              :max="60"
              controls-position="right"
            />
            <span style="margin-left: 10px;">分钟</span>
          </el-form-item>
          
          <el-form-item label="会话超时">
            <el-input-number 
              v-model="loginSecurity.sessionTimeout"
              :min="30"
              :max="480"
              controls-position="right"
            />
            <span style="margin-left: 10px;">分钟</span>
          </el-form-item>
          
          <el-form-item label="强制HTTPS">
            <el-switch 
              v-model="loginSecurity.forceHttps"
              active-text="启用"
              inactive-text="禁用"
            />
          </el-form-item>
          
          <el-form-item label="双因子认证">
            <el-switch 
              v-model="loginSecurity.twoFactorAuth"
              active-text="启用"
              inactive-text="禁用"
            />
          </el-form-item>
        </el-form>
      </el-card>
    </div>
    
    <div class="content-card">
      <el-card>
        <template #header>
          <span>访问控制</span>
        </template>
        
        <el-form :model="accessControl" label-width="120px">
          <el-form-item label="IP白名单">
            <el-input 
              v-model="accessControl.ipWhitelist"
              type="textarea"
              :rows="3"
              placeholder="请输入允许访问的IP地址，多个IP用逗号分隔"
            />
          </el-form-item>
          
          <el-form-item label="IP黑名单">
            <el-input 
              v-model="accessControl.ipBlacklist"
              type="textarea"
              :rows="3"
              placeholder="请输入禁止访问的IP地址，多个IP用逗号分隔"
            />
          </el-form-item>
          
          <el-form-item label="地理位置限制">
            <el-switch 
              v-model="accessControl.geoRestriction"
              active-text="启用"
              inactive-text="禁用"
            />
          </el-form-item>
          
          <el-form-item label="允许的国家/地区">
            <el-select 
              v-model="accessControl.allowedCountries" 
              multiple 
              placeholder="请选择允许的国家/地区"
              style="width: 100%"
            >
              <el-option label="中国" value="CN" />
              <el-option label="美国" value="US" />
              <el-option label="日本" value="JP" />
              <el-option label="韩国" value="KR" />
            </el-select>
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

const passwordPolicy = ref({
  minLength: 8,
  requireNumbers: true,
  requireLetters: true,
  requireSpecialChars: false,
  expireDays: 90
})

const loginSecurity = ref({
  maxFailAttempts: 5,
  lockoutDuration: 15,
  sessionTimeout: 120,
  forceHttps: true,
  twoFactorAuth: false
})

const accessControl = ref({
  ipWhitelist: '',
  ipBlacklist: '',
  geoRestriction: false,
  allowedCountries: ['CN']
})

const handleSaveSettings = () => {
  ElMessage.success('安全设置保存成功')
}

const handleResetSettings = () => {
  ElMessage.info('设置已重置为默认值')
}

onMounted(() => {
  // 加载安全设置数据
})
</script>

<style lang="scss" scoped>
.security-settings-page {
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