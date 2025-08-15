<template>
  <div class="import-page">
    <div class="page-header">
      <h2>批量导入考生</h2>
    </div>
    
    <el-card>
      <el-steps :active="activeStep" align-center>
        <el-step title="下载模板" description="下载Excel模板文件" />
        <el-step title="填写数据" description="按模板格式填写考生信息" />
        <el-step title="上传文件" description="上传填写好的Excel文件" />
        <el-step title="导入完成" description="查看导入结果" />
      </el-steps>
      
      <div class="import-content">
        <!-- Step 1: 下载模板 -->
        <div v-if="activeStep === 0" class="step-content">
          <el-alert type="info" :closable="false">
            <template #title>
              <div>
                <p>请先下载Excel模板，按照模板格式填写考生信息</p>
                <p>模板包含以下列：姓名、身份证号、电话（可选）、邮箱（可选）、考试产品</p>
              </div>
            </template>
          </el-alert>
          <div class="download-section">
            <el-button type="primary" size="large" @click="downloadTemplate">
              <el-icon><Download /></el-icon>
              下载Excel模板
            </el-button>
          </div>
          <el-button @click="activeStep = 1" style="margin-top: 20px">下一步</el-button>
        </div>
        
        <!-- Step 2: 填写数据说明 -->
        <div v-if="activeStep === 1" class="step-content">
          <el-alert type="warning" :closable="false">
            <template #title>
              <div>
                <h4>填写注意事项：</h4>
                <ul>
                  <li>姓名：必填，不超过50个字符</li>
                  <li>身份证号：必填，18位身份证号码</li>
                  <li>电话：选填，11位手机号码</li>
                  <li>邮箱：选填，有效的邮箱地址</li>
                  <li>考试产品：必填，必须与系统中的考试产品名称完全一致</li>
                </ul>
              </div>
            </template>
          </el-alert>
          <div class="button-group">
            <el-button @click="activeStep = 0">上一步</el-button>
            <el-button type="primary" @click="activeStep = 2">下一步</el-button>
          </div>
        </div>
        
        <!-- Step 3: 上传文件 -->
        <div v-if="activeStep === 2" class="step-content">
          <el-upload
            class="upload-demo"
            drag
            :auto-upload="false"
            :on-change="handleFileChange"
            :file-list="fileList"
            accept=".xlsx,.xls"
            :limit="1"
          >
            <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
            <div class="el-upload__text">
              将文件拖到此处，或<em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">只能上传 Excel 文件</div>
            </template>
          </el-upload>
          <div class="button-group">
            <el-button @click="activeStep = 1">上一步</el-button>
            <el-button type="primary" @click="handleUpload" :disabled="!fileList.length">
              开始导入
            </el-button>
          </div>
        </div>
        
        <!-- Step 4: 导入结果 -->
        <div v-if="activeStep === 3" class="step-content">
          <el-result
            :icon="importResult.success ? 'success' : 'warning'"
            :title="importResult.success ? '导入成功' : '部分导入成功'"
          >
            <template #sub-title>
              <div>
                <p>成功导入: {{ importResult.successCount }} 条</p>
                <p v-if="importResult.failCount > 0">失败: {{ importResult.failCount }} 条</p>
              </div>
            </template>
            <template #extra>
              <div v-if="importResult.errors.length > 0" class="error-list">
                <el-alert type="error" :closable="false">
                  <template #title>
                    <div>
                      <h4>错误详情：</h4>
                      <ul>
                        <li v-for="(error, index) in importResult.errors" :key="index">
                          {{ error }}
                        </li>
                      </ul>
                    </div>
                  </template>
                </el-alert>
              </div>
              <div class="button-group">
                <el-button @click="resetImport">重新导入</el-button>
                <el-button type="primary" @click="$router.push('/candidates')">
                  查看考生列表
                </el-button>
              </div>
            </template>
          </el-result>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { importCandidates } from '../api/candidates'

const activeStep = ref(0)
const fileList = ref([])
const importResult = ref({
  success: false,
  successCount: 0,
  failCount: 0,
  errors: []
})

const downloadTemplate = () => {
  // 创建模板数据
  const templateData = '姓名,身份证号,电话,邮箱,考试产品\n张三,350102199001011234,13800138000,zhangsan@example.com,多旋翼视距内驾驶员\n'
  
  // 创建Blob对象
  const blob = new Blob(['\uFEFF' + templateData], { type: 'text/csv;charset=utf-8' })
  
  // 创建下载链接
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = '考生导入模板.csv'
  link.click()
  
  ElMessage.success('模板下载成功')
}

const handleFileChange = (file) => {
  fileList.value = [file]
}

const handleUpload = async () => {
  if (!fileList.value.length) {
    ElMessage.warning('请选择要上传的文件')
    return
  }
  
  try {
    ElMessage.info('正在导入，请稍候...')
    
    // 模拟导入结果
    setTimeout(() => {
      importResult.value = {
        success: true,
        successCount: 45,
        failCount: 2,
        errors: [
          '第3行: 身份证号格式不正确',
          '第15行: 考试产品"固定翼驾驶员"不存在'
        ]
      }
      activeStep.value = 3
      ElMessage.success('导入完成')
    }, 2000)
    
    // 实际调用API
    // const result = await importCandidates(fileList.value[0].raw)
    // importResult.value = result
    // activeStep.value = 3
  } catch (error) {
    ElMessage.error('导入失败，请重试')
  }
}

const resetImport = () => {
  activeStep.value = 0
  fileList.value = []
  importResult.value = {
    success: false,
    successCount: 0,
    failCount: 0,
    errors: []
  }
}
</script>

<style scoped>
.import-page {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
}

.import-content {
  margin-top: 40px;
  min-height: 400px;
}

.step-content {
  padding: 40px;
  text-align: center;
}

.download-section {
  margin: 40px 0;
}

.button-group {
  margin-top: 30px;
}

.button-group .el-button {
  margin: 0 10px;
}

.upload-demo {
  margin: 20px auto;
  max-width: 500px;
}

.error-list {
  margin: 20px 0;
  text-align: left;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.error-list ul {
  margin: 10px 0;
  padding-left: 20px;
}

.error-list li {
  margin: 5px 0;
  color: #f56c6c;
}
</style>