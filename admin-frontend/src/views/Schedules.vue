<template>
  <div class="schedules-page">
    <div class="page-header">
      <h2>排期管理</h2>
      <el-button type="primary" @click="showBatchDialog = true">
        <el-icon><Plus /></el-icon>
        批量排期
      </el-button>
    </div>
    
    <el-card>
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="考试日期">
          <el-date-picker
            v-model="searchForm.date"
            type="date"
            placeholder="选择日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="考场">
          <el-select v-model="searchForm.venue_id" placeholder="请选择考场">
            <el-option label="全部" value="" />
            <el-option label="理论考场1" :value="1" />
            <el-option label="理论考场2" :value="2" />
            <el-option label="实操场A" :value="3" />
            <el-option label="实操场B" :value="4" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择">
            <el-option label="全部" value="" />
            <el-option label="待签到" value="pending" />
            <el-option label="已签到" value="checked_in" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已完成" value="completed" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
      
      <el-table :data="schedules" v-loading="loading" style="width: 100%">
        <el-table-column prop="exam_date" label="考试日期" width="110" />
        <el-table-column prop="time_range" label="时间段" width="120">
          <template #default="{ row }">
            {{ row.start_time }} - {{ row.end_time }}
          </template>
        </el-table-column>
        <el-table-column prop="candidate_name" label="考生姓名" />
        <el-table-column prop="institution_name" label="所属机构" />
        <el-table-column prop="activity_name" label="考试科目" />
        <el-table-column prop="venue_name" label="考场" />
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="check_in_time" label="签到时间" width="160" />
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button type="danger" size="small" text @click="handleCancel(row)">
              取消
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 批量排期对话框 -->
    <el-dialog 
      v-model="showBatchDialog" 
      title="批量排期"
      width="700px"
    >
      <el-form :model="batchForm" label-width="120px">
        <el-form-item label="选择日期" required>
          <el-date-picker
            v-model="batchForm.exam_date"
            type="date"
            placeholder="选择考试日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="考试类型" required>
          <el-radio-group v-model="batchForm.activity_type">
            <el-radio label="theory_exam">理论考试</el-radio>
            <el-radio label="practice_exam">实操考试</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="选择考场" required>
          <el-select v-model="batchForm.venue_id" placeholder="请选择考场">
            <el-option label="理论考场1" :value="1" v-if="batchForm.activity_type === 'theory_exam'" />
            <el-option label="理论考场2" :value="2" v-if="batchForm.activity_type === 'theory_exam'" />
            <el-option label="实操场A" :value="3" v-if="batchForm.activity_type === 'practice_exam'" />
            <el-option label="实操场B" :value="4" v-if="batchForm.activity_type === 'practice_exam'" />
          </el-select>
        </el-form-item>
        <el-form-item label="开始时间" required>
          <el-time-picker
            v-model="batchForm.start_time"
            placeholder="选择开始时间"
            format="HH:mm"
            value-format="HH:mm"
          />
        </el-form-item>
        <el-form-item label="每人时长(分钟)" required>
          <el-input-number v-model="batchForm.duration_minutes" :min="5" :max="120" />
        </el-form-item>
        <el-form-item label="选择考生" required>
          <el-button @click="selectCandidates">选择待排期考生 ({{ selectedCandidates.length }}人)</el-button>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showBatchDialog = false">取消</el-button>
        <el-button type="primary" @click="handleBatchSchedule">确定排期</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const schedules = ref([])
const showBatchDialog = ref(false)
const selectedCandidates = ref([])

const searchForm = reactive({
  date: '',
  venue_id: '',
  status: ''
})

const batchForm = reactive({
  exam_date: '',
  activity_type: 'theory_exam',
  venue_id: null,
  start_time: '',
  duration_minutes: 15,
  candidate_ids: []
})

const getStatusType = (status) => {
  const map = {
    'pending': 'warning',
    'checked_in': 'primary',
    'in_progress': 'primary',
    'completed': 'success',
    'cancelled': 'info'
  }
  return map[status] || 'info'
}

const getStatusText = (status) => {
  const map = {
    'pending': '待签到',
    'checked_in': '已签到',
    'in_progress': '进行中',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return map[status] || status
}

const fetchSchedules = async () => {
  loading.value = true
  // 模拟数据
  setTimeout(() => {
    schedules.value = [
      {
        id: 1,
        exam_date: '2025-08-16',
        start_time: '09:00',
        end_time: '11:00',
        candidate_name: '张三',
        institution_name: '福建飞行培训中心',
        activity_name: '理论考试',
        venue_name: '理论考场1',
        status: 'pending',
        check_in_time: null
      },
      {
        id: 2,
        exam_date: '2025-08-16',
        start_time: '14:00',
        end_time: '14:15',
        candidate_name: '李四',
        institution_name: '福建飞行培训中心',
        activity_name: '实操考试',
        venue_name: '实操场A',
        status: 'checked_in',
        check_in_time: '2025-08-16 13:55:00'
      }
    ]
    loading.value = false
  }, 500)
}

const handleSearch = () => {
  fetchSchedules()
}

const handleReset = () => {
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = ''
  })
  handleSearch()
}

const handleCancel = async (row) => {
  try {
    await ElMessageBox.confirm('确定要取消该排期吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    ElMessage.success('取消成功')
    fetchSchedules()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('取消失败')
    }
  }
}

const selectCandidates = () => {
  // 打开考生选择对话框
  ElMessage.info('选择考生功能开发中...')
  // 模拟选择了一些考生
  selectedCandidates.value = [1, 2, 3, 4, 5]
}

const handleBatchSchedule = () => {
  if (!batchForm.exam_date || !batchForm.venue_id || !batchForm.start_time) {
    ElMessage.warning('请填写完整信息')
    return
  }
  
  if (selectedCandidates.value.length === 0) {
    ElMessage.warning('请选择考生')
    return
  }
  
  ElMessage.success(`成功为 ${selectedCandidates.value.length} 名考生安排考试`)
  showBatchDialog.value = false
  fetchSchedules()
}

onMounted(() => {
  fetchSchedules()
})
</script>

<style scoped>
.schedules-page {
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

.search-form {
  margin-bottom: 20px;
}
</style>