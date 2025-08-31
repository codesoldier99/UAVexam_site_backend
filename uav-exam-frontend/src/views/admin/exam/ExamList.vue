<template>
  <div class="exam-list page-container">
    <div class="page-header">
      <h2 class="page-title">考试管理</h2>
      <p class="page-description">管理所有考试，包括创建、编辑、发布和取消考试</p>
    </div>
    
    <!-- 搜索表单 -->
    <div class="search-form">
      <el-form :model="searchForm" label-width="80px" @keyup.enter="handleSearch">
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12" :md="8" :lg="6">
            <el-form-item label="考试名称">
              <el-input v-model="searchForm.keyword" placeholder="请输入考试名称" clearable />
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="8" :lg="6">
            <el-form-item label="考试类型">
              <el-select v-model="searchForm.type" placeholder="请选择考试类型" clearable style="width: 100%">
                <el-option label="理论考试" value="theory" />
                <el-option label="实操考试" value="practice" />
                <el-option label="综合考试" value="comprehensive" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="8" :lg="6">
            <el-form-item label="考试状态">
              <el-select v-model="searchForm.status" placeholder="请选择考试状态" clearable style="width: 100%">
                <el-option label="草稿" value="draft" />
                <el-option label="已发布" value="published" />
                <el-option label="即将开始" value="upcoming" />
                <el-option label="进行中" value="ongoing" />
                <el-option label="已完成" value="completed" />
                <el-option label="已取消" value="cancelled" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="8" :lg="6">
            <el-form-item label="日期范围">
              <el-date-picker
                v-model="dateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <div class="form-buttons">
          <el-button @click="resetSearch">重置</el-button>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button type="success" @click="handleCreate" v-permission="['SUPER_ADMIN', 'ADMIN', 'OPERATOR']">
            <el-icon><Plus /></el-icon>创建考试
          </el-button>
        </div>
      </el-form>
    </div>
    
    <!-- 考试列表 -->
    <el-card>
      <el-table
        v-loading="loading"
        :data="examList"
        border
        style="width: 100%"
        @sort-change="handleSortChange"
      >
        <el-table-column prop="id" label="ID" width="80" sortable="custom" />
        <el-table-column prop="title" label="考试名称" min-width="200" show-overflow-tooltip />
        <el-table-column prop="type" label="考试类型" width="120">
          <template #default="scope">
            {{ getExamTypeText(scope.row.type) }}
          </template>
        </el-table-column>
        <el-table-column prop="duration" label="考试时长" width="120">
          <template #default="scope">
            {{ scope.row.duration }} 分钟
          </template>
        </el-table-column>
        <el-table-column prop="start_date" label="开始日期" width="120" sortable="custom" />
        <el-table-column prop="end_date" label="结束日期" width="120" sortable="custom" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="scope">
            <el-tag :type="getExamStatusType(scope.row.status)">
              {{ getExamStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" sortable="custom" />
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="scope">
            <div class="table-operations">
              <el-button link type="primary" @click="handleView(scope.row)">查看</el-button>
              <el-button link type="primary" @click="handleEdit(scope.row)" v-if="canEdit(scope.row)">编辑</el-button>
              <el-button link type="success" @click="handlePublish(scope.row)" v-if="scope.row.status === 'draft'">发布</el-button>
              <el-button link type="danger" @click="handleCancel(scope.row)" v-if="['published', 'upcoming'].includes(scope.row.status)">取消</el-button>
              <el-button link type="danger" @click="handleDelete(scope.row)" v-if="scope.row.status === 'draft'">删除</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.limit"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { getExamList, deleteExam, publishExam, cancelExam } from '@/api/exam'
import { useUserStore } from '@/stores/user'
import type { Exam, ExamStatus, ExamType } from '@/types/exam'

const router = useRouter()
const userStore = useUserStore()

// 搜索表单
const searchForm = reactive({
  keyword: '',
  type: '',
  status: '',
  start_date: '',
  end_date: '',
  sort_by: '',
  sort_order: ''
})

// 日期范围
const dateRange = ref<[string, string] | null>(null)

// 分页
const pagination = reactive({
  page: 1,
  limit: 10,
  total: 0
})

// 考试列表
const examList = ref<Exam[]>([])
const loading = ref(false)

// 获取考试列表
const fetchExamList = async () => {
  try {
    loading.value = true
    
    // 处理日期范围
    if (dateRange.value) {
      searchForm.start_date = dateRange.value[0]
      searchForm.end_date = dateRange.value[1]
    } else {
      searchForm.start_date = ''
      searchForm.end_date = ''
    }
    
    const params = {
      ...searchForm,
      page: pagination.page,
      limit: pagination.limit
    }
    
    const res = await getExamList(params)
    examList.value = res.items
    pagination.total = res.total
  } catch (error) {
    console.error('Failed to fetch exam list:', error)
    ElMessage.error('获取考试列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  fetchExamList()
}

// 重置搜索
const resetSearch = () => {
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = ''
  })
  dateRange.value = null
  pagination.page = 1
  fetchExamList()
}

// 分页大小变化
const handleSizeChange = (val: number) => {
  pagination.limit = val
  fetchExamList()
}

// 页码变化
const handleCurrentChange = (val: number) => {
  pagination.page = val
  fetchExamList()
}

// 排序变化
const handleSortChange = (column: { prop: string, order: string }) => {
  if (column.prop && column.order) {
    searchForm.sort_by = column.prop
    searchForm.sort_order = column.order === 'ascending' ? 'asc' : 'desc'
  } else {
    searchForm.sort_by = ''
    searchForm.sort_order = ''
  }
  fetchExamList()
}

// 创建考试
const handleCreate = () => {
  router.push('/admin/exams/create')
}

// 查看考试
const handleView = (row: Exam) => {
  router.push(`/admin/exams/${row.id}`)
}

// 编辑考试
const handleEdit = (row: Exam) => {
  router.push(`/admin/exams/${row.id}/edit`)
}

// 发布考试
const handlePublish = (row: Exam) => {
  ElMessageBox.confirm('确定要发布该考试吗？发布后将无法修改基本信息', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await publishExam(row.id)
      ElMessage.success('考试发布成功')
      fetchExamList()
    } catch (error) {
      console.error('Failed to publish exam:', error)
      ElMessage.error('考试发布失败')
    }
  }).catch(() => {})
}

// 取消考试
const handleCancel = (row: Exam) => {
  ElMessageBox.confirm('确定要取消该考试吗？取消后将无法恢复', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await cancelExam(row.id)
      ElMessage.success('考试取消成功')
      fetchExamList()
    } catch (error) {
      console.error('Failed to cancel exam:', error)
      ElMessage.error('考试取消失败')
    }
  }).catch(() => {})
}

// 删除考试
const handleDelete = (row: Exam) => {
  ElMessageBox.confirm('确定要删除该考试吗？删除后将无法恢复', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'danger'
  }).then(async () => {
    try {
      await deleteExam(row.id)
      ElMessage.success('考试删除成功')
      fetchExamList()
    } catch (error) {
      console.error('Failed to delete exam:', error)
      ElMessage.error('考试删除失败')
    }
  }).catch(() => {})
}

// 判断是否可以编辑
const canEdit = (row: Exam): boolean => {
  return row.status === 'draft'
}

// 获取考试类型文本
const getExamTypeText = (type: ExamType): string => {
  const typeMap: Record<string, string> = {
    'theory': '理论考试',
    'practice': '实操考试',
    'comprehensive': '综合考试'
  }
  return typeMap[type] || type
}

// 获取考试状态类型
const getExamStatusType = (status: ExamStatus): string => {
  const statusMap: Record<string, string> = {
    'draft': 'info',
    'published': 'success',
    'upcoming': 'primary',
    'ongoing': 'warning',
    'completed': '',
    'cancelled': 'danger'
  }
  return statusMap[status] || ''
}

// 获取考试状态文本
const getExamStatusText = (status: ExamStatus): string => {
  const statusMap: Record<string, string> = {
    'draft': '草稿',
    'published': '已发布',
    'upcoming': '即将开始',
    'ongoing': '进行中',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return statusMap[status] || status
}

// 页面加载时获取数据
onMounted(() => {
  fetchExamList()
})
</script>

<style lang="scss" scoped>
.exam-list {
  .pagination-container {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
}
</style>