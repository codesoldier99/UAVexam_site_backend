<template>
  <div class="users-page">
    <div class="page-header">
      <h2>用户管理</h2>
      <el-button type="primary" @click="showAddDialog = true">
        <el-icon><Plus /></el-icon>
        新增用户
      </el-button>
    </div>
    
    <el-card>
      <el-table :data="users" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="full_name" label="姓名" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="phone" label="电话" />
        <el-table-column prop="role" label="角色">
          <template #default="{ row }">
            <el-tag>{{ getRoleName(row.role_id) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="institution" label="所属机构">
          <template #default="{ row }">
            {{ row.institution?.name || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态">
          <template #default="{ row }">
            <el-switch v-model="row.is_active" @change="toggleUserStatus(row)" />
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
      :title="editMode ? '编辑用户' : '新增用户'"
      width="500px"
    >
      <el-form :model="userForm" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" :disabled="editMode" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!editMode">
          <el-input v-model="userForm.password" type="password" show-password />
        </el-form-item>
        <el-form-item label="姓名" prop="full_name">
          <el-input v-model="userForm.full_name" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" />
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="userForm.phone" />
        </el-form-item>
        <el-form-item label="角色" prop="role_id">
          <el-select v-model="userForm.role_id" placeholder="请选择角色">
            <el-option label="超级管理员" :value="1" />
            <el-option label="考务管理员" :value="2" />
            <el-option label="培训机构" :value="3" />
            <el-option label="考务人员" :value="4" />
          </el-select>
        </el-form-item>
        <el-form-item label="所属机构" prop="institution_id" v-if="userForm.role_id === 3">
          <el-select v-model="userForm.institution_id" placeholder="请选择机构">
            <el-option 
              v-for="inst in institutions" 
              :key="inst.id"
              :label="inst.name"
              :value="inst.id"
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

const loading = ref(false)
const users = ref([])
const showAddDialog = ref(false)
const editMode = ref(false)
const formRef = ref()
const institutions = ref([])

const userForm = reactive({
  username: '',
  password: '',
  full_name: '',
  email: '',
  phone: '',
  role_id: null,
  institution_id: null
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  role_id: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ]
}

const getRoleName = (roleId) => {
  const roleMap = {
    1: '超级管理员',
    2: '考务管理员',
    3: '培训机构',
    4: '考务人员'
  }
  return roleMap[roleId] || '未知'
}

const fetchUsers = async () => {
  loading.value = true
  // 模拟数据
  setTimeout(() => {
    users.value = [
      { id: 1, username: 'admin', full_name: '系统管理员', email: 'admin@example.com', phone: '13800000001', role_id: 1, is_active: true },
      { id: 2, username: 'examadmin', full_name: '考务管理员', email: 'exam@example.com', phone: '13800000002', role_id: 2, is_active: true },
      { id: 3, username: 'institution', full_name: '机构用户', email: 'inst@example.com', phone: '13800000003', role_id: 3, is_active: true }
    ]
    loading.value = false
  }, 500)
}

const handleEdit = (row) => {
  editMode.value = true
  Object.assign(userForm, row)
  showAddDialog.value = true
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该用户吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    ElMessage.success('删除成功')
    fetchUsers()
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
  fetchUsers()
}

const toggleUserStatus = (row) => {
  ElMessage.success(`用户状态已${row.is_active ? '启用' : '禁用'}`)
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.users-page {
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