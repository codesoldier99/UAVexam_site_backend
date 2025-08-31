<template>
  <div class="candidates-import-page">
    <div class="page-header">
      <h2>考生导入</h2>
      <p>批量导入考生信息</p>
    </div>
    
    <div class="content-card">
      <el-card>
        <template #header>
          <span>批量导入考生</span>
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
              将考生信息文件拖到此处，或<em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                只能上传 xlsx/xls/csv 文件，且不超过 10MB
              </div>
            </template>
          </el-upload>
        </div>
        
        <div class="template-section">
          <h3>导入模板</h3>
          <p>请下载标准模板，按照格式填写考生信息后上传</p>
          <el-button type="primary" @click="downloadTemplate">
            下载考生信息模板
          </el-button>
        </div>
        
        <div class="import-rules">
          <h3>导入规则</h3>
          <ul>
            <li>姓名、身份证号、联系电话为必填项</li>
            <li>身份证号必须为18位有效身份证号</li>
            <li>联系电话必须为11位手机号码</li>
            <li>邮箱格式必须正确</li>
            <li>重复的身份证号将被跳过</li>
          </ul>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'

const uploadUrl = ref('/api/candidates/import')

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
  ElMessage.success('考生信息导入成功!')
  console.log('导入成功:', response)
}

const handleError = (error: any) => {
  ElMessage.error('考生信息导入失败!')
  console.error('导入失败:', error)
}

const downloadTemplate = () => {
  // 这里应该调用下载模板的API
  ElMessage.info('下载考生信息模板')
}
</script>

<style lang="scss" scoped>
.candidates-import-page {
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
    margin-bottom: 30px;
    
    h3 {
      margin: 0 0 10px 0;
      color: #303133;
    }
    
    p {
      margin: 0 0 15px 0;
      color: #606266;
    }
  }
  
  .import-rules {
    border-top: 1px solid #ebeef5;
    padding-top: 20px;
    
    h3 {
      margin: 0 0 15px 0;
      color: #303133;
    }
    
    ul {
      margin: 0;
      padding-left: 20px;
      color: #606266;
      
      li {
        margin-bottom: 8px;
      }
    }
  }
}
</style>