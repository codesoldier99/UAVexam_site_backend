<template>
  <div class="attendance-manager">
    <div class="page-header">
      <h2 class="page-title">考勤管理</h2>
      <p class="page-description">管理考试人员的签到记录</p>
    </div>
    
    <!-- 搜索和过滤 -->
    <el-card class="filter-card">
      <el-form :model="filterForm" inline>
        <el-form-item label="考试名称">
          <el-select
            v-model="filterForm.exam_id"
            placeholder="选择考试"
            clearable
            filterable
            style="width: 220px"
          >
            <el-option
              v-for="exam in examOptions"
              :key="exam.id"
              :label="exam.name"
              :value="exam.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="考场">
          <el-select
            v-model="filterForm.venue_id"
            placeholder="选择考场"
            clearable
            filterable
            style="width: 180px"
          >
            <el-option
              v-for="venue in venueOptions"
              :key="venue.id"
              :label="venue.name"
              :value="venue.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="日期">
          <el-date-picker
            v-model="filterForm.date"
            type="date"
            placeholder="选择日期"
            style="width: 180px"
          />
        </el-form-item>
        
        <el-form-item label="角色">
          <el-select
            v-model="filterForm.role"
            placeholder="选择角色"
            clearable
            style="width: 120px"
          >
            <el-option label="考官" value="examiner" />
            <el-option label="考生" value="candidate" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="状态">
          <el-select
            v-model="filterForm.status"
            placeholder="选择状态"
            clearable
            style="width: 120px"
          >
            <el-option label="已签到" value="checked_in" />
            <el-option label="未签到" value="absent" />
          </el-select>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="resetFilter">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 操作按钮 -->
    <div class="action-bar">
      <el-button type="primary" @click="openQrCodeScanner">
        <el-icon><Aim /></el-icon>
        扫码签到
      </el-button>
      <el-button type="success" @click="openManualCheckInDialog">
        <el-icon><Check /></el-icon>
        手动签到
      </el-button>
      <el-button @click="exportAttendanceData">
        <el-icon><Download /></el-icon>
        导出数据
      </el-button>
    </div>
    
    <!-- 考勤记录表格 -->
    <el-card class="attendance-table-card">
      <el-table
        v-loading="loading"
        :data="attendanceList"
        border
        style="width: 100%"
      >
        <el-table-column prop="user_name" label="姓名" min-width="120" />
        <el-table-column prop="user_id" label="ID" width="100" />
        <el-table-column prop="role" label="角色" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.role === 'examiner' ? 'success' : 'primary'">
              {{ scope.row.role === 'examiner' ? '考官' : '考生' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="exam_name" label="考试名称" min-width="200" />
        <el-table-column prop="venue_name" label="考场" width="150" />
        <el-table-column prop="check_in_time" label="签到时间" width="180" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'checked_in' ? 'success' : 'danger'">
              {{ scope.row.status === 'checked_in' ? '已签到' : '未签到' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="check_in_method" label="签到方式" width="120" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button
              v-if="scope.row.status !== 'checked_in'"
              link
              type="primary"
              @click="handleManualCheckIn(scope.row)"
            >
              签到
            </el-button>
            <el-button
              v-else
              link
              type="danger"
              @click="handleCancelCheckIn(scope.row)"
            >
              取消签到
            </el-button>
            <el-button
              link
              type="primary"
              @click="viewAttendanceDetail(scope.row)"
            >
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
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
import { ref, reactive, onMounted } from 'vue'
import { Search, Refresh, Aim, Check, Download } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 过滤表单
const filterForm = reactive({
  exam_id: '',
  venue_id: '',
  date: '',
  role: '',
  status: ''
})

// 表格加载状态
const loading = ref(false)

// 分页
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 考试选项
const examOptions = ref([
  { id: 1, name: '无人机驾驶员理论考试' },
  { id: 2, name: '无人机实操技能考核' },
  { id: 3, name: '无人机驾驶员综合考试' }
])

// 考场选项
const venueOptions = ref([
  { id: 1, name: '考场A' },
  { id: 2, name: '考场B' },
  { id: 3, name: '考场C' }
])

// 用户选项
const userOptions = ref([])

// 考勤记录列表
const attendanceList = ref([
  {
    id: 1,
    user_id: 101,
    user_name: '张三',
    role: 'examiner',
    exam_id: 1,
    exam_name: '无人机驾驶员理论考试',
    venue_id: 1,
    venue_name: '考场A',
    check_in_time: '2025-08-28 09:30:45',
    status: 'checked_in',
    check_in_method: '扫码签到'
  },
  {
    id: 2,
    user_id: 102,
    user_name: '李四',
    role: 'examiner',
    exam_id: 2,
    exam_name: '无人机实操技能考核',
    venue_id: 2,
    venue_name: '考场B',
    check_in_time: '2025-08-28 10:15:22',
    status: 'checked_in',
    check_in_method: '手动签到'
  },
  {
    id: 3,
    user_id: 201,
    user_name: '王五',
    role: 'candidate',
    exam_id: 1,
    exam_name: '无人机驾驶员理论考试',
    venue_id: 1,
    venue_name: '考场A',
    check_in_time: '',
    status: 'absent',
    check_in_method: ''
  },
  {
    id: 4,
    user_id: 202,
    user_name: '赵六',
    role: 'candidate',
    exam_id: 2,
    exam_name: '无人机实操技能考核',
    venue_id: 2,
    venue_name: '考场B',
    check_in_time: '2025-08-28 09:55:18',
    status: 'checked_in',
    check_in_method: '扫码签到'
  },
  {
    id: 5,
    user_id: 203,
    user_name: '钱七',
    role: 'candidate',
    exam_id: 3,
    exam_name: '无人机驾驶员综合考试',
    venue_id: 3,
    venue_name: '考场C',
    check_in_time: '',
    status: 'absent',
    check_in_method: ''
  }
])

// 搜索
const handleSearch = () => {
  loading.value = true
  
  // 模拟API请求
  setTimeout(() => {
    // 这里应该是实际的API请求
    loading.value = false
    ElMessage.success('搜索完成')
  }, 500)
}

// 重置过滤条件
const resetFilter = () => {
  Object.keys(filterForm).forEach(key => {
    filterForm[key] = ''
  })
  handleSearch()
}

// 分页大小变化
const handleSizeChange = (size: number) => {
  pagination.pageSize = size
  handleSearch()
}

// 页码变化
const handleCurrentChange = (page: number) => {
  pagination.currentPage = page
  handleSearch()
}

// 打开扫码签到
const openQrCodeScanner = () => {
  ElMessage.info('扫码签到功能开发中...')
}

// 打开手动签到对话框
const openManualCheckInDialog = () => {
  ElMessage.info('手动签到功能开发中...')
}

// 导出考勤数据
const exportAttendanceData = () => {
  ElMessage.info('导出数据功能开发中...')
}

// 手动签到
const handleManualCheckIn = (row: any) => {
  ElMessageBox.confirm(`确定为 ${row.user_name} 签到吗?`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 模拟API请求
    setTimeout(() => {
      row.status = 'checked_in'
      row.check_in_time = new Date().toLocaleString()
      row.check_in_method = '手动签到'
      ElMessage.success('签到成功')
    }, 500)
  }).catch(() => {})
}

// 取消签到
const handleCancelCheckIn = (row: any) => {
  ElMessageBox.confirm(`确定取消 ${row.user_name} 的签到记录吗?`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 模拟API请求
    setTimeout(() => {
      row.status = 'absent'
      row.check_in_time = ''
      row.check_in_method = ''
      ElMessage.success('已取消签到')
    }, 500)
  }).catch(() => {})
}

// 查看考勤详情
const viewAttendanceDetail = (row: any) => {
  ElMessage.info(`查看 ${row.user_name} 的考勤详情，功能开发中...`)
}

// 页面加载时获取数据
onMounted(() => {
  handleSearch()
})
</script>

<style lang="scss" scoped>
.attendance-manager {
  .filter-card {
    margin-bottom: 20px;
  }
  
  .action-bar {
    margin-bottom: 20px;
    display: flex;
    gap: 10px;
  }
  
  .attendance-table-card {
    .pagination-container {
      margin-top: 20px;
      display: flex;
      justify-content: flex-end;
    }
  }
}
</style>