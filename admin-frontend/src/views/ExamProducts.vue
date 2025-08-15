<template>
  <div class="exam-products-page">
    <div class="page-header">
      <h2>考试产品管理</h2>
      <el-button type="primary" @click="showAddDialog = true">
        <el-icon><Plus /></el-icon>
        新增考试产品
      </el-button>
    </div>
    
    <el-card>
      <el-table :data="products" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="code" label="产品代码" />
        <el-table-column prop="name" label="产品名称" />
        <el-table-column prop="exam_duration_theory" label="理论时长(分钟)" />
        <el-table-column prop="exam_duration_practice" label="实操时长(分钟)" />
        <el-table-column prop="description" label="描述" show-overflow-tooltip />
        <el-table-column prop="is_active" label="状态">
          <template #default="{ row }">
            <el-switch v-model="row.is_active" @change="toggleStatus(row)" />
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
    </el-card>
    
    <!-- 添加/编辑对话框 -->
    <el-dialog 
      v-model="showAddDialog" 
      :title="editMode ? '编辑考试产品' : '新增考试产品'"
      width="600px"
    >
      <el-form :model="productForm" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="产品代码" prop="code">
          <el-input v-model="productForm.code" placeholder="如：MR_VLOS_PILOT" />
        </el-form-item>
        <el-form-item label="产品名称" prop="name">
          <el-input v-model="productForm.name" placeholder="如：多旋翼视距内驾驶员" />
        </el-form-item>
        <el-form-item label="理论时长(分钟)" prop="exam_duration_theory">
          <el-input-number v-model="productForm.exam_duration_theory" :min="30" :max="300" />
        </el-form-item>
        <el-form-item label="实操时长(分钟)" prop="exam_duration_practice">
          <el-input-number v-model="productForm.exam_duration_practice" :min="5" :max="60" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="productForm.description" type="textarea" :rows="3" />
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

const loading = ref(false)
const products = ref([])
const showAddDialog = ref(false)
const editMode = ref(false)
const formRef = ref()

const productForm = reactive({
  code: '',
  name: '',
  exam_duration_theory: 120,
  exam_duration_practice: 15,
  description: ''
})

const rules = {
  code: [
    { required: true, message: '请输入产品代码', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入产品名称', trigger: 'blur' }
  ],
  exam_duration_theory: [
    { required: true, message: '请输入理论考试时长', trigger: 'blur' }
  ],
  exam_duration_practice: [
    { required: true, message: '请输入实操考试时长', trigger: 'blur' }
  ]
}

const fetchProducts = async () => {
  loading.value = true
  // 模拟数据
  setTimeout(() => {
    products.value = [
      {
        id: 1,
        code: 'MR_VLOS_PILOT',
        name: '多旋翼视距内驾驶员',
        exam_duration_theory: 120,
        exam_duration_practice: 15,
        description: '多旋翼无人机视距内驾驶员执照考试',
        is_active: true
      },
      {
        id: 2,
        code: 'MR_BVLOS_PILOT',
        name: '多旋翼超视距驾驶员',
        exam_duration_theory: 120,
        exam_duration_practice: 20,
        description: '多旋翼无人机超视距驾驶员执照考试',
        is_active: true
      },
      {
        id: 3,
        code: 'FW_VLOS_PILOT',
        name: '固定翼视距内驾驶员',
        exam_duration_theory: 120,
        exam_duration_practice: 20,
        description: '固定翼无人机视距内驾驶员执照考试',
        is_active: true
      },
      {
        id: 4,
        code: 'VERTICAL_PILOT',
        name: '垂直起降固定翼驾驶员',
        exam_duration_theory: 120,
        exam_duration_practice: 25,
        description: '垂直起降固定翼无人机驾驶员执照考试',
        is_active: true
      }
    ]
    loading.value = false
  }, 500)
}

const handleEdit = (row) => {
  editMode.value = true
  Object.assign(productForm, row)
  showAddDialog.value = true
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该考试产品吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    ElMessage.success('删除成功')
    fetchProducts()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleSubmit = async () => {
  const valid = await formRef.value.validate()
  if (!valid) return
  
  ElMessage.success(editMode.value ? '更新成功' : '添加成功')
  showAddDialog.value = false
  fetchProducts()
}

const toggleStatus = (row) => {
  ElMessage.success(`考试产品已${row.is_active ? '启用' : '停用'}`)
}

onMounted(() => {
  fetchProducts()
})
</script>

<style scoped>
.exam-products-page {
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
</style>