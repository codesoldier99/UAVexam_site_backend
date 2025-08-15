<template>
  <div class="institutions-page">
    <div class="page-header">
      <h2>培训机构管理</h2>
      <el-button type="primary" @click="showAddDialog = true">
        <el-icon><Plus /></el-icon>
        新增机构
      </el-button>
    </div>
    
    <el-card>
      <el-table :data="institutions" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="code" label="机构代码" />
        <el-table-column prop="name" label="机构名称" />
        <el-table-column prop="contact_person" label="联系人" />
        <el-table-column prop="phone" label="联系电话" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="address" label="地址" show-overflow-tooltip />
        <el-table-column prop="is_active" label="状态">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'">
              {{ row.is_active ? '正常' : '停用' }}
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
    </el-card>
    
    <!-- 添加/编辑对话框 -->
    <el-dialog 
      v-model="showAddDialog" 
      :title="editMode ? '编辑机构' : '新增机构'"
      width="600px"
    >
      <el-form :model="institutionForm" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="机构代码" prop="code">
          <el-input v-model="institutionForm.code" placeholder="如：INST001" />
        </el-form-item>
        <el-form-item label="机构名称" prop="name">
          <el-input v-model="institutionForm.name" />
        </el-form-item>
        <el-form-item label="联系人" prop="contact_person">
          <el-input v-model="institutionForm.contact_person" />
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="institutionForm.phone" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="institutionForm.email" />
        </el-form-item>
        <el-form-item label="地址" prop="address">
          <el-input v-model="institutionForm.address" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="状态" prop="is_active">
          <el-switch v-model="institutionForm.is_active" />
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
const institutions = ref([])
const showAddDialog = ref(false)
const editMode = ref(false)
const formRef = ref()

const institutionForm = reactive({
  code: '',
  name: '',
  contact_person: '',
  phone: '',
  email: '',
  address: '',
  is_active: true
})

const rules = {
  code: [
    { required: true, message: '请输入机构代码', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入机构名称', trigger: 'blur' }
  ],
  contact_person: [
    { required: true, message: '请输入联系人', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }
  ]
}

const fetchInstitutions = async () => {
  loading.value = true
  // 模拟数据
  setTimeout(() => {
    institutions.value = [
      {
        id: 1,
        code: 'INST001',
        name: '福建飞行培训中心',
        contact_person: '张经理',
        phone: '13800138000',
        email: 'contact@fjftc.com',
        address: '福建省福州市仓山区XX路XX号',
        is_active: true
      },
      {
        id: 2,
        code: 'INST002',
        name: '厦门无人机培训学院',
        contact_person: '李主任',
        phone: '13900139000',
        email: 'info@xmuav.com',
        address: '福建省厦门市思明区XX路XX号',
        is_active: true
      }
    ]
    loading.value = false
  }, 500)
}

const handleEdit = (row) => {
  editMode.value = true
  Object.assign(institutionForm, row)
  showAddDialog.value = true
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该机构吗？删除后该机构下的所有考生信息将受影响', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    ElMessage.success('删除成功')
    fetchInstitutions()
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
  fetchInstitutions()
}

onMounted(() => {
  fetchInstitutions()
})
</script>

<style scoped>
.institutions-page {
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