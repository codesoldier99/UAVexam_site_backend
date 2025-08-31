<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, FormInstance, FormRules } from 'element-plus'
import { Plus, Search, SetUp } from '@element-plus/icons-vue'
import {
  getExamDetail,
  publishExam,
  cancelExam,
  getExamSessions,
  createExamSession,
  updateExamSession,
  deleteExamSession,
  getExamCandidates,
  addExamCandidates,
  removeExamCandidate
} from '@/api/exam'
import { getVenueList } from '@/api/venue'
import { getCandidateList } from '@/api/candidate'
import type { ExamDetail, ExamSession, ExamCandidate, ExamStatus, ExamType, Venue } from '@/types/exam'
import type { UserInfo } from '@/types/user'

const route = useRoute()
const router = useRouter()
const examId = computed(() => route.params.id as string)

// 考试详情
const examDetail = ref<ExamDetail>()
const loading = ref(false)

// 是否可以编辑
const canEdit = computed(() => {
  return examDetail.value?.status === 'draft'
})

// 获取考试详情
const fetchExamDetail = async () => {
  try {
    loading.value = true
    const res = await getExamDetail(examId.value)
    examDetail.value = res
  } catch (error) {
    console.error('Failed to fetch exam detail:', error)
    ElMessage.error('获取考试详情失败')
    goBack()
  } finally {
    loading.value = false
  }
}

// 考生相关
const candidates = ref<ExamCandidate[]>([])
const loadingCandidates = ref(false)
const candidateSearchKeyword = ref('')

// 考生分页
const candidatePagination = reactive({
  page: 1,
  limit: 10,
  total: 0
})

// 获取考生列表
const fetchCandidates = async () => {
  try {
    loadingCandidates.value = true
    
    const params = {
      page: candidatePagination.page,
      limit: candidatePagination.limit,
      keyword: candidateSearchKeyword.value
    }
    
    const res = await getExamCandidates(examId.value, params)
    candidates.value = res.items
    candidatePagination.total = res.total
  } catch (error) {
    console.error('Failed to fetch candidates:', error)
    ElMessage.error('获取考生列表失败')
  } finally {
    loadingCandidates.value = false
  }
}

// 考生分页大小变化
const handleCandidateSizeChange = (val: number) => {
  candidatePagination.limit = val
  fetchCandidates()
}

// 考生页码变化
const handleCandidatePageChange = (val: number) => {
  candidatePagination.page = val
  fetchCandidates()
}

// 添加考生对话框
const candidateDialogVisible = ref(false)
const availableCandidates = ref<UserInfo[]>([])
const loadingAvailableCandidates = ref(false)
const availableCandidateKeyword = ref('')
const selectedCandidates = ref<UserInfo[]>([])
const submittingCandidates = ref(false)
const availableCandidateTableRef = ref()

// 可用考生分页
const availableCandidatePagination = reactive({
  page: 1,
  limit: 10,
  total: 0
})

// 搜索可用考生
const searchAvailableCandidates = async () => {
  try {
    loadingAvailableCandidates.value = true
    
    const params = {
      page: availableCandidatePagination.page,
      limit: availableCandidatePagination.limit,
      keyword: availableCandidateKeyword.value,
      exclude_exam_id: examId.value
    }
    
    const res = await getCandidateList(params)
    availableCandidates.value = res.items
    availableCandidatePagination.total = res.total
  } catch (error) {
    console.error('Failed to fetch available candidates:', error)
    ElMessage.error('获取可用考生列表失败')
  } finally {
    loadingAvailableCandidates.value = false
  }
}

// 可用考生分页大小变化
const handleAvailableCandidateSizeChange = (val: number) => {
  availableCandidatePagination.limit = val
  searchAvailableCandidates()
}

// 可用考生页码变化
const handleAvailableCandidatePageChange = (val: number) => {
  availableCandidatePagination.page = val
  searchAvailableCandidates()
}

// 可用考生选择变化
const handleAvailableCandidateSelectionChange = (selection: UserInfo[]) => {
  selectedCandidates.value = selection
}

// 添加考生
const handleAddCandidates = () => {
  candidateDialogVisible.value = true
  availableCandidateKeyword.value = ''
  selectedCandidates.value = []
  
  // 重置分页
  availableCandidatePagination.page = 1
  
  // 获取可用考生列表
  searchAvailableCandidates()
}

// 提交添加考生
const submitAddCandidates = async () => {
  if (selectedCandidates.value.length === 0) return
  
  try {
    submittingCandidates.value = true
    
    const candidateIds = selectedCandidates.value.map(c => c.id)
    await addExamCandidates(examId.value, { candidate_ids: candidateIds })
    
    ElMessage.success('添加考生成功')
    candidateDialogVisible.value = false
    
    // 刷新考生列表和考试详情
    fetchCandidates()
    fetchExamDetail()
  } catch (error) {
    console.error('Failed to add candidates:', error)
    ElMessage.error('添加考生失败')
  } finally {
    submittingCandidates.value = false
  }
}

// 移除考生
const handleRemoveCandidate = (candidate: ExamCandidate) => {
  ElMessageBox.confirm('确定要移除该考生吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await removeExamCandidate(examId.value, candidate.candidate_id)
      ElMessage.success('移除考生成功')
      
      // 刷新考生列表和考试详情
      fetchCandidates()
      fetchExamDetail()
    } catch (error) {
      console.error('Failed to remove candidate:', error)
      ElMessage.error('移除考生失败')
    }
  }).catch(() => {})
}

// 分配考场相关
const assignSessionDialogVisible = ref(false)
const assignSessionFormRef = ref<FormInstance>()
const submittingAssignSession = ref(false)
const assigningCandidate = ref<ExamCandidate | null>(null)
const availableSessions = computed(() => examDetail.value?.sessions || [])

// 分配考场表单
const assignSessionForm = reactive({
  session_id: undefined as number | undefined
})

// 分配考场表单验证规则
const assignSessionFormRules = reactive<FormRules>({
  session_id: [
    { required: true, message: '请选择考场场次', trigger: 'change' }
  ]
})

// 分配考场
const handleAssignCandidate = (candidate: ExamCandidate) => {
  assigningCandidate.value = candidate
  assignSessionForm.session_id = undefined
  assignSessionDialogVisible.value = true
}

// 批量分配考场
const handleAssignCandidates = () => {
  ElMessage.info('批量分配考场功能待实现')
}

// 提交分配考场
const submitAssignSession = async () => {
  if (!assignSessionFormRef.value || !assigningCandidate.value) return
  
  await assignSessionFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        submittingAssignSession.value = true
        
        // 这里应该调用API更新考生的考场分配
        // 暂时模拟API调用
        await new Promise(resolve => setTimeout(resolve, 500))
        
        ElMessage.success('分配考场成功')
        assignSessionDialogVisible.value = false
        
        // 刷新考生列表
        fetchCandidates()
      } catch (error) {
        console.error('Failed to assign session:', error)
        ElMessage.error('分配考场失败')
      } finally {
        submittingAssignSession.value = false
      }
    }
  })
}

// 分配考官
const handleAssignExaminers = (session: ExamSession) => {
  ElMessage.info('分配考官功能待实现')
}

// 编辑考试
const handleEdit = () => {
  router.push(`/admin/exams/${examId.value}/edit`)
}

// 发布考试
const handlePublish = () => {
  ElMessageBox.confirm('确定要发布该考试吗？发布后将无法修改基本信息', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await publishExam(examId.value)
      ElMessage.success('考试发布成功')
      fetchExamDetail()
    } catch (error) {
      console.error('Failed to publish exam:', error)
      ElMessage.error('考试发布失败')
    }
  }).catch(() => {})
}

// 取消考试
const handleCancel = () => {
  ElMessageBox.confirm('确定要取消该考试吗？取消后将无法恢复', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await cancelExam(examId.value)
      ElMessage.success('考试取消成功')
      fetchExamDetail()
    } catch (error) {
      console.error('Failed to cancel exam:', error)
      ElMessage.error('考试取消失败')
    }
  }).catch(() => {})
}

// 返回列表
const goBack = () => {
  router.push('/admin/exams')
}

// 获取考试类型文本
const getExamTypeText = (type?: ExamType): string => {
  if (!type) return ''
  
  const typeMap: Record<string, string> = {
    'theory': '理论考试',
    'practice': '实操考试',
    'comprehensive': '综合考试'
  }
  return typeMap[type] || type
}

// 获取考试状态类型
const getExamStatusType = (status?: ExamStatus): string => {
  if (!status) return ''
  
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
const getExamStatusText = (status?: ExamStatus): string => {
  if (!status) return ''
  
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

// 获取考生状态类型
const getCandidateStatusType = (status: string): string => {
  const statusMap: Record<string, string> = {
    'enrolled': 'info',
    'assigned': 'primary',
    'attended': 'success',
    'absent': 'danger',
    'completed': ''
  }
  return statusMap[status] || ''
}

// 获取考生状态文本
const getCandidateStatusText = (status: string): string => {
  const statusMap: Record<string, string> = {
    'enrolled': '已报名',
    'assigned': '已分配',
    'attended': '已参加',
    'absent': '缺席',
    'completed': '已完成'
  }
  return statusMap[status] || status
}

// 页面加载时获取数据
onMounted(() => {
  fetchExamDetail()
  fetchCandidates()
})
</script>

<style lang="scss" scoped>
.exam-detail {
  .stat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    
    .stat-item {
      text-align: center;
      
      .stat-value {
        font-size: 24px;
        font-weight: bold;
        color: var(--el-color-primary);
      }
      
      .stat-label {
        font-size: 14px;
        color: var(--el-text-color-secondary);
        margin-top: 5px;
      }
    }
  }
  
  .examiner-list {
    display: flex;
    align-items: center;
    
    .more-examiners {
      margin-left: 5px;
      font-size: 12px;
      color: var(--el-text-color-secondary);
    }
  }
  
  .empty-block {
    padding: 30px 0;
  }
  
  .search-form-mini {
    margin-bottom: 20px;
    max-width: 300px;
  }
  
  .pagination-container {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
}
</style>