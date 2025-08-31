<template>
  <div class="upload-page">
    <div class="page-header">
      <h2>报名文件上传</h2>
      <p>上传考生报名信息文件</p>
    </div>
    
    <div class="content-card">
      <el-card>
        <template #header>
          <span>文件上传</span>
        </template>
        
        <div class="upload-section">
          <el-upload
            class="upload-demo"
            drag
            :action="uploadUrl"
            :before-upload="beforeUpload"
            :on-success="handleSuccess"
            :on-error="handleError"
            accept=".xlsx,.xls,.csv"
          >
            <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
            <div class="el-upload__text">
              将文件拖到此处，或<em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                只能上传 xlsx/xls/csv 文件，且不超过 10MB
              </div>
            </template>
          </el-upload>
        </div>
        
        <div class="template-section">
          <h3>模板下载</h3>
          <p>请下载标准模板，按照格式填写报名信息</p>
          <el-button type="primary" @click="downloadTemplate">
            下载报名模板
          </el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'

const uploadUrl = ref('/api/registration/upload')

const beforeUpload = (file: File) => {
  const isValidType = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                      'application/vnd.ms-excel', 
                      'text/csv'].includes(file.type)
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isValidType) {
    ElMessage.error('只能上传 Excel 或 CSV 文件!')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('文件大小不能超过 10MB!')
    return false
  }
  return true
}

const handleSuccess = (response: any) => {
  ElMessage.success('文件上传成功!')
  console.log('上传成功:', response)
}

const handleError = (error: any) => {
  ElMessage.error('文件上传失败!')
  console.error('上传失败:', error)
}

const downloadTemplate = () => {
  // 这里应该调用下载模板的API
  ElMessage.info('下载模板功能')
}
</script>

<style lang="scss" scoped>
.upload-page {
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
  
  .upload-section {
    margin-bottom: 30px;
  }
  
  .template-section {
    border-top: 1px solid #ebeef5;
    padding-top: 20px;
    
    h3 {
      margin: 0 0 10px 0;
      color: #303133;
    }
    
    p {
      margin: 0 0 15px 0;
      color: #606266;
    }
  }
}
</style>