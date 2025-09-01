<template>
  <div class="candidates-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">考生管理</h1>
      <p class="page-description">管理考试考生信息，包括考生注册、信息维护、考试安排等</p>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon total">
          <Users />
        </div>
        <div class="stat-content">
          <div class="stat-number">{{ statistics.totalCandidates }}</div>
          <div class="stat-label">总考生数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon active">
          <UserCheck />
        </div>
        <div class="stat-content">
          <div class="stat-number">{{ statistics.activeCandidates }}</div>
          <div class="stat-label">活跃考生</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon pending">
          <Clock />
        </div>
        <div class="stat-content">
          <div class="stat-number">{{ statistics.pendingCandidates }}</div>
          <div class="stat-label">待审核</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon exam">
          <BookOpen />
        </div>
        <div class="stat-content">
          <div class="stat-number">{{ statistics.examCandidates }}</div>
          <div class="stat-label">考试中</div>
        </div>
      </div>
    </div>

    <!-- 操作栏 -->
    <div class="action-bar">
      <div class="search-section">
        <el-input
          v-model="searchQuery"
          placeholder="搜索考生姓名、身份证号、手机号..."
          class="search-input"
          clearable
          @input="handleSearch"
        >
          <template #prefix>
            <Search />
          </template>
        </el-input>
        <el-select
          v-model="statusFilter"
          placeholder="状态筛选"
          clearable
          @change="handleFilter"
        >
          <el-option label="全部" value="" />
          <el-option label="待审核" value="pending" />
          <el-option label="已通过" value="approved" />
          <el-option label="已拒绝" value="rejected" />
          <el-option label="考试中" value="examining" />
          <el-option label="已完成" value="completed" />
        </el-select>
      </div>
      <div class="button-section">
        <el-button type="primary" @click="handleAdd">
          <Plus class="mr-1" />
          新增考生
        </el-button>
        <el-button @click="handleImport">
          <Upload class="mr-1" />
          批量导入
        </el-button>
        <el-button @click="handleExport">
          <Download class="mr-1" />
          导出数据
        </el-button>
      </div>
    </div>

    <!-- 考生列表 -->
    <div class="table-container">
      <el-table
        v-loading="loading"
        :data="candidates"
        stripe
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column prop="id_card" label="身份证号" width="180" />
        <el-table-column prop="phone" label="手机号" width="130" />
        <el-table-column prop="email" label="邮箱" width="200" />
        <el-table-column prop="gender" label="性别" width="80">
          <template #default="{ row }">
            <span>{{ row.gender === 'male' ? '男' : '女' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="注册时间" width="160">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="handleView(row)">
              <Eye class="mr-1" />
              查看
            </el-button>
            <el-button size="small" type="primary" @click="handleEdit(row)">
              <Edit class="mr-1" />
              编辑
            </el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">
              <Trash class="mr-1" />
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <!-- 批量操作栏 -->
    <div v-if="selectedCandidates.length > 0" class="batch-actions">
      <span class="batch-info">已选择 {{ selectedCandidates.length }} 项</span>
      <el-button type="danger" @click="handleBatchDelete">
        批量删除
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Users, UserCheck, Clock, BookOpen, Search, Plus, 
  Upload, Download, Eye, Edit, Trash 
} from 'lucide-vue-next'
import { useCandidatesStore } from '@/stores/candidates'
import { storeToRefs } from 'pinia'
import { formatDateTime } from '@/utils/date'

// Store
const candidatesStore = useCandidatesStore()
const { candidates, statistics, loading, total } = storeToRefs(candidatesStore)

// 响应式数据
const searchQuery = ref('')
const statusFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const selectedCandidates = ref<any[]>([])

// 计算属性
const skip = computed(() => (currentPage.value - 1) * pageSize.value)

// 生命周期
onMounted(() => {
  loadCandidates()
  loadStatistics()
})

// 方法
const loadCandidates = async () => {
  await candidatesStore.fetchCandidates({
    skip: skip.value,
    limit: pageSize.value,
    search: searchQuery.value,
    status: statusFilter.value
  })
}

const loadStatistics = async () => {
  await candidatesStore.fetchStatistics()
}

const handleSearch = () => {
  currentPage.value = 1
  loadCandidates()
}

const handleFilter = () => {
  currentPage.value = 1
  loadCandidates()
}

const handleAdd = () => {
  // TODO: 打开新增考生对话框
  ElMessage.info('新增考生功能开发中...')
}

const handleImport = () => {
  // TODO: 打开批量导入对话框
  ElMessage.info('批量导入功能开发中...')
}

const handleExport = async () => {
  try {
    await candidatesStore.exportCandidates({
      search: searchQuery.value,
      status: statusFilter.value
    })
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

const handleView = (candidate: any) => {
  // TODO: 打开考生详情对话框
  ElMessage.info(`查看考生: ${candidate.name}`)
}

const handleEdit = (candidate: any) => {
  // TODO: 打开编辑考生对话框
  ElMessage.info(`编辑考生: ${candidate.name}`)
}

const handleDelete = async (candidate: any) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除考生 "${candidate.name}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await candidatesStore.deleteCandidate(candidate.id)
    ElMessage.success('删除成功')
    loadCandidates()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleSelectionChange = (selection: any[]) => {
  selectedCandidates.value = selection
}

const handleBatchDelete = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedCandidates.value.length} 个考生吗？`,
      '确认批量删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const ids = selectedCandidates.value.map(item => item.id)
    await candidatesStore.batchDeleteCandidates(ids)
    ElMessage.success('批量删除成功')
    selectedCandidates.value = []
    loadCandidates()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('批量删除失败')
    }
  }
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  loadCandidates()
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
  loadCandidates()
}

const getStatusType = (status: string) => {
  const statusMap: Record<string, string> = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger',
    examining: 'primary',
    completed: 'info'
  }
  return statusMap[status] || 'info'
}

const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    pending: '待审核',
    approved: '已通过',
    rejected: '已拒绝',
    examining: '考试中',
    completed: '已完成'
  }
  return statusMap[status] || '未知'
}
</script>

<style scoped>
.candidates-container {
  padding: 24px;
  background: #f5f5f5;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 24px;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 8px 0;
}

.page-description {
  color: #6b7280;
  margin: 0;
  font-size: 14px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
}

.stat-icon.total {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.stat-icon.active {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.stat-icon.pending {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.stat-icon.exam {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  color: white;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  line-height: 1;
}

.stat-label {
  font-size: 14px;
  color: #6b7280;
  margin-top: 4px;
}

.action-bar {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.search-section {
  display: flex;
  gap: 12px;
  align-items: center;
}

.search-input {
  width: 300px;
}

.button-section {
  display: flex;
  gap: 12px;
}

.table-container {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.batch-actions {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: white;
  border-radius: 8px;
  padding: 12px 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  gap: 16px;
  z-index: 1000;
}

.batch-info {
  color: #6b7280;
  font-size: 14px;
}

@media (max-width: 768px) {
  .candidates-container {
    padding: 16px;
  }
  
  .action-bar {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .search-section {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-input {
    width: 100%;
  }
  
  .button-section {
    justify-content: center;
  }
}
</style>