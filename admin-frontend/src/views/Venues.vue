<template>
  <div class="venues-page">
    <div class="page-header">
      <h2>考场管理</h2>
      <el-button type="primary" @click="showAddDialog = true">
        <el-icon><Plus /></el-icon>
        新增考场
      </el-button>
    </div>
    
    <el-card>
      <el-table :data="venues" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="code" label="考场代码" />
        <el-table-column prop="name" label="考场名称" />
        <el-table-column prop="type" label="考场类型">
          <template #default="{ row }">
            <el-tag :type="getTypeColor(row.type)">
              {{ getTypeText(row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="capacity" label="容量" />
        <el-table-column prop="location" label="位置" />
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
      :title="editMode ? '编辑考场' : '新增考场'"
      width="600px"
    >
      <el-form :model="venueForm" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="考场代码" prop="code">
          <el-input v-model="venueForm.code" placeholder="如：THEORY_1" />
        </el-form-item>
        <el-form-item label="考场名称" prop="name">
          <el-input v-model="venueForm.name" />
        </el-form-item>
        <el-form-item label="考场类型" prop="type">
          <el-select v-model="venueForm.type" placeholder="请选择考场类型">
            <el-option label="理论考场" value="theory" />
            <el-option label="实操考场" value="practice" />
            <el-option label="候考室" value="waiting" />
          </el-select>
        </el-form-item>
        <el-form-item label="容量" prop="capacity">
          <el-input-number v-model="venueForm.capacity" :min="1" :max="100" />
        </el-form-item>
        <el-form-item label="位置" prop="location">
          <el-input v-model="venueForm.location" placeholder="如：教学楼3楼301室" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="venueForm.description" type="textarea" :rows="3" />
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
const venues = ref([])
const showAddDialog = ref(false)
const editMode = ref(false)
const formRef = ref()

const venueForm = reactive({
  code: '',
  name: '',
  type: '',
  capacity: 1,
  location: '',
  description: ''
})

const rules = {
  code: [
    { required: true, message: '请输入考场代码', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入考场名称', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择考场类型', trigger: 'change' }
  ],
  capacity: [
    { required: true, message: '请输入容量', trigger: 'blur' }
  ]
}

const getTypeColor = (type) => {
  const map = {
    'theory': 'primary',
    'practice': 'success',
    'waiting': 'warning'
  }
  return map[type] || 'info'
}

const getTypeText = (type) => {
  const map = {
    'theory': '理论考场',
    'practice': '实操考场',
    'waiting': '候考室'
  }
  return map[type] || type
}

const fetchVenues = async () => {
  loading.value = true
  // 模拟数据
  setTimeout(() => {
    venues.value = [
      {
        id: 1,
        code: 'THEORY_1',
        name: '理论考场1',
        type: 'theory',
        capacity: 30,
        location: '教学楼3楼301室',
        description: '配备投影仪和空调',
        is_active: true
      },
      {
        id: 2,
        code: 'THEORY_2',
        name: '理论考场2',
        type: 'theory',
        capacity: 30,
        location: '教学楼3楼302室',
        description: '配备投影仪和空调',
        is_active: true
      },
      {
        id: 3,
        code: 'PRACTICE_A',
        name: '实操场A',
        type: 'practice',
        capacity: 1,
        location: '室外飞行场A区',
        description: '标准飞行场地',
        is_active: true
      },
      {
        id: 4,
        code: 'PRACTICE_B',
        name: '实操场B',
        type: 'practice',
        capacity: 1,
        location: '室外飞行场B区',
        description: '标准飞行场地',
        is_active: true
      },
      {
        id: 5,
        code: 'WAITING_1',
        name: '候考室',
        type: 'waiting',
        capacity: 50,
        location: '教学楼2楼大厅',
        description: '配备座椅和饮水机',
        is_active: true
      }
    ]
    loading.value = false
  }, 500)
}

const handleEdit = (row) => {
  editMode.value = true
  Object.assign(venueForm, row)
  showAddDialog.value = true
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该考场吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    ElMessage.success('删除成功')
    fetchVenues()
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
  fetchVenues()
}

const toggleStatus = (row) => {
  ElMessage.success(`考场已${row.is_active ? '启用' : '停用'}`)
}

onMounted(() => {
  fetchVenues()
})
</script>

<style scoped>
.venues-page {
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