<template>
  <div class="exam-products-container">
    <!-- 页面标题和操作栏 -->
    <div class="page-header">
      <div class="header-left">
        <h2>考试产品管理</h2>
        <p class="page-description">管理无人机考试的产品类型和配置</p>
      </div>
      <div class="header-right">
        <!-- 新增按钮 - 只有管理员可见 -->
        <el-button 
          v-permission="{ resource: 'EXAM_PRODUCT', action: 'CREATE' }"
          type="primary" 
          @click="handleAdd"
        >
          <el-icon><Plus /></el-icon>
          新增产品
        </el-button>
        
        <!-- 批量操作 - 根据权限显示 -->
        <el-dropdown v-permission="['super_admin', 'admin']" @command="handleBatchAction">
          <el-button>
            批量操作
            <el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item 
                v-permission="{ resource: 'EXAM_PRODUCT', action: 'CREATE' }"
                command="import"
              >
                批量导入
              </el-dropdown-item>
              <el-dropdown-item 
                v-permission="{ resource: 'EXAM_PRODUCT', action: 'READ' }"
                command="export"
              >
                导出数据
              </el-dropdown-item>
              <el-dropdown-item 
                v-permission="{ resource: 'EXAM_PRODUCT', action: 'DELETE' }"
                command="batchDelete"
                divided
              >
                批量删除
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="search-card">
      <el-form :model="searchForm" inline>
        <el-form-item label="产品名称">
          <el-input 
            v-model="searchForm.name" 
            placeholder="请输入产品名称"
            clearable
          />
        </el-form-item>
        <el-form-item label="产品类型">
          <el-select 
            v-model="searchForm.type" 
            placeholder="请选择产品类型"
            clearable
          >
            <el-option label="多旋翼" value="multirotor" />
            <el-option label="固定翼" value="fixed-wing" />
            <el-option label="直升机" value="helicopter" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select 
            v-model="searchForm.status" 
            placeholder="请选择状态"
            clearable
          >
            <el-option label="启用" value="active" />
            <el-option label="禁用" value="inactive" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 数据表格 -->
    <el-card class="table-card">
      <el-table 
        :data="tableData" 
        v-loading="loading"
        @selection-change="handleSelectionChange"
      >
        <!-- 选择列 - 只有有删除权限的用户才显示 -->
        <el-table-column 
          v-permission="{ resource: 'EXAM_PRODUCT', action: 'DELETE' }"
          type="selection" 
          width="55" 
        />
        
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="产品名称" min-width="150" />
        <el-table-column prop="type" label="产品类型" width="120">
          <template #default="scope">
            <el-tag :type="getTypeTagType(scope.row.type)">
              {{ getTypeLabel(scope.row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="产品描述" min-width="200" />
        
        <!-- 价格列 - 只有管理员可见 -->
        <el-table-column 
          v-permission="['super_admin', 'admin']"
          prop="price" 
          label="考试费用" 
          width="120"
        >
          <template #default="scope">
            ¥{{ scope.row.price }}
          </template>
        </el-table-column>
        
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-switch
              v-permission.disable="{ resource: 'EXAM_PRODUCT', action: 'UPDATE' }"
              v-model="scope.row.status"
              :active-value="'active'"
              :inactive-value="'inactive'"
              @change="handleStatusChange(scope.row)"
            />
          </template>
        </el-table-column>
        
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button 
              v-permission="{ resource: 'EXAM_PRODUCT', action: 'READ' }"
              type="primary" 
              link 
              @click="handleView(scope.row)"
            >
              查看
            </el-button>
            <el-button 
              v-permission="{ resource: 'EXAM_PRODUCT', action: 'UPDATE' }"
              type="primary" 
              link 
              @click="handleEdit(scope.row)"
            >
              编辑
            </el-button>
            <el-button 
              v-permission="{ resource: 'EXAM_PRODUCT', action: 'DELETE' }"
              type="danger" 
              link 
              @click="handleDelete(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @close="handleDialogClose"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="100px"
      >
        <el-form-item label="产品名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入产品名称" />
        </el-form-item>
        <el-form-item label="产品类型" prop="type">
          <el-select v-model="formData.type" placeholder="请选择产品类型">
            <el-option label="多旋翼" value="multirotor" />
            <el-option label="固定翼" value="fixed-wing" />
            <el-option label="直升机" value="helicopter" />
          </el-select>
        </el-form-item>
        <el-form-item label="产品描述" prop="description">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入产品描述"
          />
        </el-form-item>
        
        <!-- 价格字段 - 只有管理员可编辑 -->
        <el-form-item 
          v-permission="['super_admin', 'admin']"
          label="考试费用" 
          prop="price"
        >
          <el-input-number
            v-model="formData.price"
            :min="0"
            :precision="2"
            placeholder="请输入考试费用"
          />
        </el-form-item>
        
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="formData.status">
            <el-radio value="active">启用</el-radio>
            <el-radio value="inactive">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button 
          type="primary" 
          :loading="submitLoading"
          @click="handleSubmit"
        >
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, ArrowDown } from '@element-plus/icons-vue'
import { usePermission } from '@/composables/usePermission'

// 权限检查
const { hasResource, canManageExams } = usePermission()

// 响应式数据
const loading = ref(false)
const submitLoading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const selectedRows = ref([])

// 搜索表单
const searchForm = reactive({
  name: '',
  type: '',
  status: ''
})

// 表格数据
const tableData = ref([
  {
    id: 1,
    name: '多旋翼无人机驾驶员',
    type: 'multirotor',
    description: '多旋翼无人机驾驶员资格考试',
    price: 1200,
    status: 'active',
    created_at: '2024-01-15 10:30:00'
  },
  {
    id: 2,
    name: '固定翼无人机驾驶员',
    type: 'fixed-wing',
    description: '固定翼无人机驾驶员资格考试',
    price: 1500,
    status: 'active',
    created_at: '2024-01-16 14:20:00'
  }
])

// 分页
const pagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

// 表单数据
const formData = reactive({
  id: null,
  name: '',
  type: '',
  description: '',
  price: 0,
  status: 'active'
})

// 表单验证规则
const formRules = {
  name: [
    { required: true, message: '请输入产品名称', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择产品类型', trigger: 'change' }
  ],
  description: [
    { required: true, message: '请输入产品描述', trigger: 'blur' }
  ]
}

// 方法
const getTypeTagType = (type: string) => {
  const typeMap = {
    'multirotor': 'primary',
    'fixed-wing': 'success',
    'helicopter': 'warning'
  }
  return typeMap[type] || 'info'
}

const getTypeLabel = (type: string) => {
  const labelMap = {
    'multirotor': '多旋翼',
    'fixed-wing': '固定翼',
    'helicopter': '直升机'
  }
  return labelMap[type] || type
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('zh-CN')
}

const handleSearch = () => {
  pagination.page = 1
  loadData()
}

const handleReset = () => {
  Object.assign(searchForm, {
    name: '',
    type: '',
    status: ''
  })
  handleSearch()
}

const handleAdd = () => {
  if (!hasResource('EXAM_PRODUCT', 'CREATE')) {
    ElMessage.error('您没有权限执行此操作')
    return
  }
  
  dialogTitle.value = '新增考试产品'
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  if (!hasResource('EXAM_PRODUCT', 'UPDATE')) {
    ElMessage.error('您没有权限执行此操作')
    return
  }
  
  dialogTitle.value = '编辑考试产品'
  isEdit.value = true
  Object.assign(formData, row)
  dialogVisible.value = true
}

const handleView = (row: any) => {
  // 查看详情逻辑
  ElMessage.info('查看功能待实现')
}

const handleDelete = async (row: any) => {
  if (!hasResource('EXAM_PRODUCT', 'DELETE')) {
    ElMessage.error('您没有权限执行此操作')
    return
  }
  
  try {
    await ElMessageBox.confirm(
      `确定要删除产品"${row.name}"吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 执行删除逻辑
    ElMessage.success('删除成功')
    loadData()
  } catch {
    // 用户取消删除
  }
}

const handleStatusChange = (row: any) => {
  if (!hasResource('EXAM_PRODUCT', 'UPDATE')) {
    ElMessage.error('您没有权限执行此操作')
    // 恢复原状态
    row.status = row.status === 'active' ? 'inactive' : 'active'
    return
  }
  
  ElMessage.success(`已${row.status === 'active' ? '启用' : '禁用'}产品`)
}

const handleSelectionChange = (selection: any[]) => {
  selectedRows.value = selection
}

const handleBatchAction = (command: string) => {
  switch (command) {
    case 'import':
      if (!hasResource('EXAM_PRODUCT', 'CREATE')) {
        ElMessage.error('您没有权限执行此操作')
        return
      }
      ElMessage.info('批量导入功能待实现')
      break
    case 'export':
      if (!hasResource('EXAM_PRODUCT', 'READ')) {
        ElMessage.error('您没有权限执行此操作')
        return
      }
      ElMessage.info('导出功能待实现')
      break
    case 'batchDelete':
      if (!hasResource('EXAM_PRODUCT', 'DELETE')) {
        ElMessage.error('您没有权限执行此操作')
        return
      }
      if (selectedRows.value.length === 0) {
        ElMessage.warning('请选择要删除的数据')
        return
      }
      ElMessage.info('批量删除功能待实现')
      break
  }
}

const handleSubmit = async () => {
  // 表单提交逻辑
  submitLoading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
    dialogVisible.value = false
    loadData()
  } catch (error) {
    ElMessage.error('操作失败')
  } finally {
    submitLoading.value = false
  }
}

const handleDialogClose = () => {
  resetForm()
}

const resetForm = () => {
  Object.assign(formData, {
    id: null,
    name: '',
    type: '',
    description: '',
    price: 0,
    status: 'active'
  })
}

const handleSizeChange = (size: number) => {
  pagination.size = size
  loadData()
}

const handleCurrentChange = (page: number) => {
  pagination.page = page
  loadData()
}

const loadData = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    pagination.total = tableData.value.length
  } catch (error) {
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

// 生命周期
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.exam-products-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-left h2 {
  margin: 0 0 8px 0;
  color: #303133;
}

.page-description {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

.header-right {
  display: flex;
  gap: 12px;
}

.search-card {
  margin-bottom: 20px;
}

.table-card {
  margin-bottom: 20px;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>