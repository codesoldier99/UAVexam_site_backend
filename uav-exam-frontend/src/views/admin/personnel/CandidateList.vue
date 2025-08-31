<template>
  <div class="candidate-list page-container">
    <div class="page-header">
      <h2 class="page-title">考生管理</h2>
      <p class="page-description">管理系统中的所有考生信息</p>
    </div>
    
    <!-- 搜索和操作栏 -->
    <el-card class="search-card">
      <div class="search-container">
        <el-form :inline="true" :model="searchForm" class="search-form">
          <el-form-item label="姓名">
            <el-input v-model="searchForm.name" placeholder="请输入考生姓名" clearable />
          </el-form-item>
          <el-form-item label="身份证号">
            <el-input v-model="searchForm.id_card" placeholder="请输入身份证号" clearable />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
              <el-option label="正常" value="active" />
              <el-option label="禁用" value="inactive" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">
              <el-icon><Search /></el-icon>
              搜索
            </el-button>
            <el-button @click="resetSearch">
              <el-icon><Refresh /></el-icon>
              重置
            </el-button>
          </el-form-item>
        </el-form>
        
        <div class="action-buttons">
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增考生
          </el-button>
          <el-button type="success" @click="handleImport">
            <el-icon><Upload /></el-icon>
            批量导入
          </el-button>
          <el-button @click="handleExport">
            <el-icon><Download /></el-icon>
            导出数据
          </el-button>
        </div>
      </div>
    </el-card>
    
    <!-- 考生列表 -->
    <el-card class="list-card">
      <el-table
        v-loading="loading"
        :data="candidateList"
        border
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column prop="gender" label="性别" width="80">
          <template #default="scope">
            {{ scope.row.gender === 'male' ? '男' : '女' }}
          </template>
        </el-table-column>
        <el-table-column prop="id_card" label="身份证号" width="180" />
        <el-table-column prop="phone" label="联系电话" width="150" />
        <el-table-column prop="email" label="电子邮箱" min-width="180" />
        <el-table-column prop="organization" label="所属单位" min-width="150" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'active' ? 'success' : 'danger'">
              {{ scope.row.status === 'active' ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button link type="primary" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button link type="primary" @click="handleView(scope.row)">查看</el-button>
            <el-popconfirm
              title="确定要删除此考生吗？"
              @confirm="handleDelete(scope.row)"
            >
              <template #reference>
                <el-button link type="danger">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
    <!-- 考生表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新增考生' : '编辑考生'"
      width="600px"
      destroy-on-close
    >
      <el-form
        ref="formRef"
        :model="candidateForm"
        :rules="formRules"
        label-width="100px"
      >
        <el-form-item label="姓名" prop="name">
          <el-input v-model="candidateForm.name" placeholder="请输入考生姓名" />
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-radio-group v-model="candidateForm.gender">
            <el-radio label="male">男</el-radio>
            <el-radio label="female">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="身份证号" prop="id_card">
          <el-input v-model="candidateForm.id_card" placeholder="请输入身份证号" />
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="candidateForm.phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="电子邮箱" prop="email">
          <el-input v-model="candidateForm.email" placeholder="请输入电子邮箱" />
        </el-form-item>
        <el-form-item label="所属单位" prop="organization">
          <el-input v-model="candidateForm.organization" placeholder="请输入所属单位" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="candidateForm.status">
            <el-radio label="active">正常</el-radio>
            <el-radio label="inactive">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input
            v-model="candidateForm.remark"
            type="textarea"
            placeholder="请输入备注信息"
            :rows="3"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm" :loading="submitLoading">
            确认
          </el-button>
        </div>
      </template>
    </el-dialog>
    
    <!-- 考生详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="考生详情"
      width="600px"
    >
      <el-descriptions
        v-if="currentCandidate"
        :column="1"
        border
      >
        <el-descriptions-item label="姓名">{{ currentCandidate.name }}</el-descriptions-item>
        <el-descriptions-item label="性别">{{ currentCandidate.gender === 'male' ? '男' : '女' }}</el-descriptions-item>
        <el-descriptions-item label="身份证号">{{ currentCandidate.id_card }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentCandidate.phone }}</el-descriptions-item>
        <el-descriptions-item label="电子邮箱">{{ currentCandidate.email }}</el-descriptions-item>
        <el-descriptions-item label="所属单位">{{ currentCandidate.organization }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="currentCandidate.status === 'active' ? 'success' : 'danger'">
            {{ currentCandidate.status === 'active' ? '正常' : '禁用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="备注">{{ currentCandidate.remark || '无' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ formatDate(currentCandidate.created_at) }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ formatDate(currentCandidate.updated_at) }}</el-descriptions-item>
      </el-descriptions>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="detailVisible = false">关闭</el-button>
          <el-button type="primary" @click="handleEdit(currentCandidate)">编辑</el-button>
        </div>
      </template>
    </el-dialog>
    
    <!-- 批量导入对话框 -->
    <el-dialog
      v-model="importVisible"
      title="批量导入考生"
      width="500px"
    >
      <div class="import-container">
        <el-upload
          class="upload-demo"
          drag
          action="#"
          :auto-upload="false"
          :on-change="handleFileChange"
          :limit="1"
          :file-list="fileList"
        >
          <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
          <div class="el-upload__text">
            将文件拖到此处，或<em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              请上传 Excel 文件 (xlsx, xls)，<el-link type="primary" @click="downloadTemplate">下载模板</el-link>
            </div>
          </template>
        </el-upload>
        
        <div class="import-actions">
          <el-button @click="importVisible = false">取消</el-button>
          <el-button type="primary" @click="submitImport" :loading="importLoading">
            开始导入
          </el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Refresh, Plus, Upload, Download, UploadFilled } from '@element-plus/icons-vue'

// 响应式数据
const loading = ref(false)
const candidateList = ref([])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 搜索表单
const searchForm = reactive({
  name: '',
  id_card: '',
  status: ''
})

// 对话框状态
const dialogVisible = ref(false)
const detailVisible = ref(false)
const importVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const submitLoading = ref(false)
const importLoading = ref(false)

// 当前选中的考生
const currentCandidate = ref(null)

// 表单引用
const formRef = ref()

// 考生表单数据
const candidateForm = reactive({
  id: null,
  name: '',
  gender: 'male',
  id_card: '',
  phone: '',
  email: '',
  organization: '',
  status: 'active',
  remark: ''
})

// 表单验证规则
const formRules = {
  name: [
    { required: true, message: '请输入考生姓名', trigger: 'blur' }
  ],
  gender: [
    { required: true, message: '请选择性别', trigger: 'change' }
  ],
  id_card: [
    { required: true, message: '请输入身份证号', trigger: 'blur' },
    { pattern: /^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$/, message: '身份证号格式不正确', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入电子邮箱', trigger: 'blur' },
    { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
  ],
  organization: [
    { required: true, message: '请输入所属单位', trigger: 'blur' }
  ]
}

// 文件列表
const fileList = ref([])

// 方法
const fetchCandidateList = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    candidateList.value = [
      {
        id: 1,
        name: '张三',
        gender: 'male',
        id_card: '110101199001011234',
        phone: '13800138000',
        email: 'zhangsan@example.com',
        organization: '北京航空公司',
        status: 'active',
        remark: '优秀考生',
        created_at: '2024-01-01 10:00:00',
        updated_at: '2024-01-01 10:00:00'
      }
    ]
    total.value = 1
  } catch (error) {
    console.error('获取考生列表失败:', error)
    ElMessage.error('获取考生列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchCandidateList()
}

const resetSearch = () => {
  Object.assign(searchForm, {
    name: '',
    id_card: '',
    status: ''
  })
  handleSearch()
}

const handleAdd = () => {
  dialogType.value = 'add'
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  dialogType.value = 'edit'
  Object.assign(candidateForm, row)
  dialogVisible.value = true
  detailVisible.value = false
}

const handleView = (row: any) => {
  currentCandidate.value = row
  detailVisible.value = true
}

const handleDelete = async (row: any) => {
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    ElMessage.success('删除成功')
    fetchCandidateList()
  } catch (error) {
    console.error('删除失败:', error)
    ElMessage.error('删除失败')
  }
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  fetchCandidateList()
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
  fetchCandidateList()
}

const submitForm = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    submitLoading.value = true
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success(dialogType.value === 'add' ? '新增成功' : '编辑成功')
    dialogVisible.value = false
    fetchCandidateList()
  } catch (error) {
    console.error('提交失败:', error)
  } finally {
    submitLoading.value = false
  }
}

const resetForm = () => {
  Object.assign(candidateForm, {
    id: null,
    name: '',
    gender: 'male',
    id_card: '',
    phone: '',
    email: '',
    organization: '',
    status: 'active',
    remark: ''
  })
}

const handleImport = () => {
  importVisible.value = true
  fileList.value = []
}

const handleExport = async () => {
  try {
    // 模拟导出
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败')
  }
}

const handleFileChange = (file: any) => {
  fileList.value = [file]
}

const submitImport = async () => {
  if (fileList.value.length === 0) {
    ElMessage.warning('请选择要导入的文件')
    return
  }
  
  try {
    importLoading.value = true
    // 模拟导入
    await new Promise(resolve => setTimeout(resolve, 2000))
    ElMessage.success('导入成功')
    importVisible.value = false
    fetchCandidateList()
  } catch (error) {
    console.error('导入失败:', error)
    ElMessage.error('导入失败')
  } finally {
    importLoading.value = false
  }
}

const downloadTemplate = () => {
  // 模拟下载模板
  ElMessage.success('模板下载成功')
}

const formatDate = (dateString: string) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('zh-CN')
}

// 生命周期
onMounted(() => {
  fetchCandidateList()
})
</script>

<style scoped>
.candidate-list {
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

.search-card {
  margin-bottom: 20px;
}

.search-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 16px;
}

.search-form {
  flex: 1;
  min-width: 600px;
}

.action-buttons {
  display: flex;
  gap: 12px;
  flex-shrink: 0;
}

.list-card {
  margin-bottom: 20px;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.dialog-footer {
  text-align: right;
}

.import-container {
  text-align: center;
}

.import-actions {
  margin-top: 20px;
  text-align: right;
}

@media (max-width: 768px) {
  .search-container {
    flex-direction: column;
  }
  
  .search-form {
    min-width: auto;
    width: 100%;
  }
  
  .action-buttons {
    width: 100%;
    justify-content: flex-start;
  }
}
</style>