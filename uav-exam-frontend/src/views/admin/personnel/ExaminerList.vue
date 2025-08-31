<template>
  <div class="examiner-list page-container">
    <div class="page-header">
      <h2 class="page-title">考官管理</h2>
      <p class="page-description">管理系统中的所有考官信息</p>
    </div>
    
    <!-- 搜索和操作栏 -->
    <el-card class="search-card">
      <div class="search-container">
        <el-form :inline="true" :model="searchForm" class="search-form">
          <el-form-item label="姓名">
            <el-input v-model="searchForm.name" placeholder="请输入考官姓名" clearable />
          </el-form-item>
          <el-form-item label="证书编号">
            <el-input v-model="searchForm.certificate_no" placeholder="请输入证书编号" clearable />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
              <el-option label="在职" value="active" />
              <el-option label="休假" value="leave" />
              <el-option label="离职" value="inactive" />
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
            新增考官
          </el-button>
        </div>
      </div>
    </el-card>
    
    <!-- 考官列表 -->
    <el-card class="list-card">
      <el-table
        v-loading="loading"
        :data="examinerList"
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
        <el-table-column prop="phone" label="联系电话" width="150" />
        <el-table-column prop="email" label="电子邮箱" min-width="180" />
        <el-table-column prop="certificate_no" label="证书编号" width="150" />
        <el-table-column prop="qualification" label="资质等级" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button link type="primary" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button link type="primary" @click="handleView(scope.row)">查看</el-button>
            <el-popconfirm
              title="确定要删除此考官吗？"
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
    
    <!-- 考官表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新增考官' : '编辑考官'"
      width="600px"
      destroy-on-close
    >
      <el-form
        ref="formRef"
        :model="examinerForm"
        :rules="formRules"
        label-width="100px"
      >
        <el-form-item label="姓名" prop="name">
          <el-input v-model="examinerForm.name" placeholder="请输入考官姓名" />
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-radio-group v-model="examinerForm.gender">
            <el-radio label="male">男</el-radio>
            <el-radio label="female">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="examinerForm.phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="电子邮箱" prop="email">
          <el-input v-model="examinerForm.email" placeholder="请输入电子邮箱" />
        </el-form-item>
        <el-form-item label="证书编号" prop="certificate_no">
          <el-input v-model="examinerForm.certificate_no" placeholder="请输入证书编号" />
        </el-form-item>
        <el-form-item label="资质等级" prop="qualification">
          <el-select v-model="examinerForm.qualification" placeholder="请选择资质等级">
            <el-option label="初级" value="junior" />
            <el-option label="中级" value="intermediate" />
            <el-option label="高级" value="senior" />
            <el-option label="专家" value="expert" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="examinerForm.status" placeholder="请选择状态">
            <el-option label="在职" value="active" />
            <el-option label="休假" value="leave" />
            <el-option label="离职" value="inactive" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input
            v-model="examinerForm.remark"
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
    
    <!-- 考官详情对话框 -->
    <el-dialog
      v-model="detailVisible"
      title="考官详情"
      width="600px"
    >
      <el-descriptions
        v-if="currentExaminer"
        :column="1"
        border
      >
        <el-descriptions-item label="姓名">{{ currentExaminer.name }}</el-descriptions-item>
        <el-descriptions-item label="性别">{{ currentExaminer.gender === 'male' ? '男' : '女' }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentExaminer.phone }}</el-descriptions-item>
        <el-descriptions-item label="电子邮箱">{{ currentExaminer.email }}</el-descriptions-item>
        <el-descriptions-item label="证书编号">{{ currentExaminer.certificate_no }}</el-descriptions-item>
        <el-descriptions-item label="资质等级">{{ getQualificationText(currentExaminer.qualification) }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(currentExaminer.status)">
            {{ getStatusText(currentExaminer.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="备注">{{ currentExaminer.remark || '无' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ formatDate(currentExaminer.created_at) }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ formatDate(currentExaminer.updated_at) }}</el-descriptions-item>
      </el-descriptions>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="detailVisible = false">关闭</el-button>
          <el-button type="primary" @click="handleEdit(currentExaminer)">编辑</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, FormInstance } from 'element-plus'
import { Search, Refresh, Plus } from '@element-plus/icons-vue'
import { getExaminers, createExaminer, updateExaminer, deleteExaminer, getExaminerDetail } from '@/api/personnel'
import dayjs from 'dayjs'

// 搜索表单
const searchForm = reactive({
  name: '',
  certificate_no: '',
  status: ''
})

// 考官列表数据
const examinerList = ref<any[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 对话框控制
const dialogVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const detailVisible = ref(false)
const currentExaminer = ref<any>(null)
const submitLoading = ref(false)

// 表单相关
const formRef = ref<FormInstance>()
const examinerForm = reactive({
  id: undefined,
  name: '',
  gender: 'male',
  phone: '',
  email: '',
  certificate_no: '',
  qualification: '',
  status: 'active',
  remark: ''
})

// 表单验证规则
const formRules = {
  name: [
    { required: true, message: '请输入考官姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  gender: [
    { required: true, message: '请选择性别', trigger: 'change' }
  ],
  phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入电子邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  certificate_no: [
    { required: true, message: '请输入证书编号', trigger: 'blur' }
  ],
  qualification: [
    { required: true, message: '请选择资质等级', trigger: 'change' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ]
}

// 获取考官列表
const fetchExaminers = async () => {
  try {
    loading.value = true
    const params = {
      page: currentPage.value,
      limit: pageSize.value,
      ...searchForm
    }
    
    const res = await getExaminers(params)
    examinerList.value = res.items
    total.value = res.total
  } catch (error) {
    console.error('Failed to fetch examiners:', error)
    ElMessage.error('获取考官列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  fetchExaminers()
}

// 重置搜索
const resetSearch = () => {
  Object.keys(searchForm).forEach(key => {
    searchForm[key as keyof typeof searchForm] = ''
  })
  currentPage.value = 1
  fetchExaminers()
}

// 分页相关
const handleSizeChange = (val: number) => {
  pageSize.value = val
  fetchExaminers()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchExaminers()
}

// 新增考官
const handleAdd = () => {
  dialogType.value = 'add'
  resetForm()
  dialogVisible.value = true
}

// 编辑考官
const handleEdit = (row: any) => {
  dialogType.value = 'edit'
  resetForm()
  
  Object.keys(examinerForm).forEach(key => {
    if (key in row) {
      examinerForm[key as keyof typeof examinerForm] = row[key]
    }
  })
  
  examinerForm.id = row.id
  dialogVisible.value = true
}

// 查看考官详情
const handleView = async (row: any) => {
  try {
    loading.value = true
    const res = await getExaminerDetail(row.id)
    currentExaminer.value = res
    detailVisible.value = true
  } catch (error) {
    console.error('Failed to get examiner detail:', error)
    ElMessage.error('获取考官详情失败')
  } finally {
    loading.value = false
  }
}

// 删除考官
const handleDelete = async (row: any) => {
  try {
    await deleteExaminer(row.id)
    ElMessage.success('删除成功')
    fetchExaminers()
  } catch (error) {
    console.error('Failed to delete examiner:', error)
    ElMessage.error('删除考官失败')
  }
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        submitLoading.value = true
        
        if (dialogType.value === 'add') {
          await createExaminer(examinerForm)
          ElMessage.success('新增考官成功')
        } else {
          await updateExaminer(examinerForm.id as number, examinerForm)
          ElMessage.success('更新考官成功')
        }
        
        dialogVisible.value = false
        fetchExaminers()
      } catch (error) {
        console.error('Failed to submit form:', error)
        ElMessage.error(dialogType.value === 'add' ? '新增考官失败' : '更新考官失败')
      } finally {
        submitLoading.value = false
      }
    }
  })
}

// 重置表单
const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  
  examinerForm.id = undefined
  examinerForm.name = ''
  examinerForm.gender = 'male'
  examinerForm.phone = ''
  examinerForm.email = ''
  examinerForm.certificate_no = ''
  examinerForm.qualification = ''
  examinerForm.status = 'active'
  examinerForm.remark = ''
}

// 获取状态类型
const getStatusType = (status: string) => {
  const statusMap: Record<string, string> = {
    'active': 'success',
    'leave': 'warning',
    'inactive': 'danger'
  }
  
  return statusMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    'active': '在职',
    'leave': '休假',
    'inactive': '离职'
  }
  
  return statusMap[status] || status
}

// 获取资质等级文本
const getQualificationText = (qualification: string) => {
  const qualificationMap: Record<string, string> = {
    'junior': '初级',
    'intermediate': '中级',
    'senior': '高级',
    'expert': '专家'
  }
  
  return qualificationMap[qualification] || qualification
}

// 格式化日期
const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

// 页面加载时获取数据
onMounted(() => {
  fetchExaminers()
})
</script>

<style lang="scss" scoped>
.examiner-list {
  .search-card {
    margin-bottom: 20px;
  }
  
  .search-container {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    
    .search-form {
      flex: 1;
      display: flex;
      flex-wrap: wrap;
    }
    
    .action-buttons {
      display: flex;
      align-items: flex-start;
    }
  }
  
  .list-card {
    margin-bottom: 20px;
  }
  
  .pagination-container {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>