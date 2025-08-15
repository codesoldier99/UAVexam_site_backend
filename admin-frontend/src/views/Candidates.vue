<template>
  <div class="candidates-page">
    <div class="page-header">
      <h2>考生管理</h2>
      <div class="actions">
        <el-button type="primary" @click="showAddDialog = true">
          <el-icon><Plus /></el-icon>
          添加考生
        </el-button>
        <el-button @click="$router.push('/candidates/import')">
          <el-icon><Upload /></el-icon>
          批量导入
        </el-button>
      </div>
    </div>
    
    <el-card>
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="姓名">
          <el-input v-model="searchForm.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="身份证">
          <el-input v-model="searchForm.idCard" placeholder="请输入身份证号" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择">
            <el-option label="全部" value="" />
            <el-option label="待排期" value="pending_schedule" />
            <el-option label="已排期" value="scheduled" />
            <el-option label="已完成" value="completed" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
      
      <el-table 
        :data="candidates" 
        v-loading="loading"
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="id_card" label="身份证号" width="180" />
        <el-table-column prop="phone" label="电话" />
        <el-table-column prop="institution_name" label="培训机构" />
        <el-table-column prop="exam_product_name" label="考试产品" />
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" size="small" text @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button type="danger" size="small" text @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </el-card>
    
    <!-- 添加/编辑对话框 -->
    <el-dialog 
      v-model="showAddDialog" 
      :title="editMode ? '编辑考生' : '添加考生'"
      width="500px"
    >
      <el-form :model="candidateForm" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="candidateForm.name" />
        </el-form-item>
        <el-form-item label="身份证号" prop="id_card">
          <el-input v-model="candidateForm.id_card" :disabled="editMode" />
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="candidateForm.phone" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="candidateForm.email" />
        </el-form-item>
        <el-form-item label="培训机构" prop="institution_id">
          <el-select v-model="candidateForm.institution_id" placeholder="请选择">
            <el-option 
              v-for="inst in institutions" 
              :key="inst.id"
              :label="inst.name"
              :value="inst.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="考试产品" prop="exam_product_id">
          <el-select v-model="candidateForm.exam_product_id" placeholder="请选择">
            <el-option 
              v-for="product in examProducts" 
              :key="product.id"
              :label="product.name"
              :value="product.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getCandidates, createCandidate, updateCandidate, deleteCandidate } from '../api/candidates'

const loading = ref(false)
const candidates = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const showAddDialog = ref(false)
const editMode = ref(false)
const formRef = ref()
const institutions = ref([])
const examProducts = ref([])

const searchForm = reactive({
  name: '',
  idCard: '',
  status: ''
})

const candidateForm = reactive({
  name: '',
  id_card: '',
  phone: '',
  email: '',
  institution_id: null,
  exam_product_id: null
})

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  id_card: [
    { required: true, message: '请输入身份证号', trigger: 'blur' },
    { pattern: /^\d{17}[\dXx]$/, message: '身份证号格式不正确', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }
  ],
  institution_id: [{ required: true, message: '请选择培训机构', trigger: 'change' }],
  exam_product_id: [{ required: true, message: '请选择考试产品', trigger: 'change' }]
}

const getStatusType = (status) => {
  const map = {
    'pending_schedule': 'warning',
    'scheduled': 'primary',
    'completed': 'success',
    'cancelled': 'danger'
  }
  return map[status] || 'info'
}

const getStatusText = (status) => {
  const map = {
    'pending_schedule': '待排期',
    'scheduled': '已排期',
    'theory_waiting': '待理论考试',
    'theory_completed': '理论已完成',
    'practice_waiting': '待实操考试',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return map[status] || status
}

const fetchCandidates = async () => {
  loading.value = true
  try {
    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
      ...searchForm
    }
    const data = await getCandidates(params)
    candidates.value = data
    // 实际应该从后端返回total
    total.value = data.length * 10 
  } catch (error) {
    ElMessage.error('获取考生列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchCandidates()
}

const handleReset = () => {
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = ''
  })
  handleSearch()
}

const handleEdit = (row) => {
  editMode.value = true
  Object.assign(candidateForm, row)
  showAddDialog.value = true
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该考生吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await deleteCandidate(row.id)
    ElMessage.success('删除成功')
    fetchCandidates()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleSubmit = async () => {
  const valid = await formRef.value.validate()
  if (!valid) return
  
  try {
    if (editMode.value) {
      await updateCandidate(candidateForm.id, candidateForm)
      ElMessage.success('更新成功')
    } else {
      await createCandidate(candidateForm)
      ElMessage.success('添加成功')
    }
    showAddDialog.value = false
    fetchCandidates()
  } catch (error) {
    ElMessage.error(editMode.value ? '更新失败' : '添加失败')
  }
}

const handleSizeChange = (val) => {
  pageSize.value = val
  fetchCandidates()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchCandidates()
}

onMounted(() => {
  fetchCandidates()
  // 加载机构和考试产品列表
  // fetchInstitutions()
  // fetchExamProducts()
})
</script>

<style scoped>
.candidates-page {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
}

.actions {
  display: flex;
  gap: 10px;
}

.search-form {
  margin-bottom: 20px;
}
</style>