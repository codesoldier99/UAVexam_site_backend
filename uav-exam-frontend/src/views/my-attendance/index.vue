<template>
  <div class="my-attendance-page">
    <div class="page-header">
      <h2>我的考勤</h2>
      <p>查看我的考勤记录和统计</p>
    </div>
    
    <div class="stats-section">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.thisMonth }}</div>
              <div class="stat-label">本月出勤</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.lateCount }}</div>
              <div class="stat-label">迟到次数</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.attendanceRate }}</div>
              <div class="stat-label">出勤率</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.totalHours }}</div>
              <div class="stat-label">总学时</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <div class="content-card">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>考勤记录</span>
            <div class="date-filter">
              <el-date-picker
                v-model="selectedMonth"
                type="month"
                placeholder="选择月份"
                @change="handleMonthChange"
              />
            </div>
          </div>
        </template>
        
        <el-table :data="attendanceRecords" style="width: 100%">
          <el-table-column prop="date" label="日期" />
          <el-table-column prop="checkInTime" label="签到时间" />
          <el-table-column prop="checkOutTime" label="签退时间" />
          <el-table-column prop="duration" label="学习时长" />
          <el-table-column prop="status" label="状态">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)">
                {{ getStatusText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="remark" label="备注" />
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const selectedMonth = ref(new Date())

const stats = ref({
  thisMonth: 22,
  lateCount: 1,
  attendanceRate: '95.5%',
  totalHours: '176h'
})

const attendanceRecords = ref([
  {
    id: 1,
    date: '2024-01-15',
    checkInTime: '08:30:00',
    checkOutTime: '17:30:00',
    duration: '8h',
    status: 'present',
    remark: ''
  },
  {
    id: 2,
    date: '2024-01-16',
    checkInTime: '09:15:00',
    checkOutTime: '17:30:00',
    duration: '7.5h',
    status: 'late',
    remark: '交通堵塞'
  },
  {
    id: 3,
    date: '2024-01-17',
    checkInTime: '-',
    checkOutTime: '-',
    duration: '0h',
    status: 'absent',
    remark: '请假'
  }
])

const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    present: 'success',
    late: 'warning',
    absent: 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    present: '正常',
    late: '迟到',
    absent: '缺席'
  }
  return texts[status] || '未知'
}

const handleMonthChange = (value: Date) => {
  console.log('选择月份:', value)
  // 根据选择的月份加载对应的考勤记录
}

onMounted(() => {
  // 加载我的考勤数据
})
</script>

<style lang="scss" scoped>
.my-attendance-page {
  .page-header {
    margin-bottom: 20px;
    
    h2 {
      margin: 0 0 8px 0;
      color: #303133;
    }
    
    p {
      margin: 0;
      color: #909399;
    }
  }
  
  .stats-section {
    margin-bottom: 20px;
    
    .stat-card {
      .stat-content {
        text-align: center;
        padding: 10px 0;
        
        .stat-number {
          font-size: 28px;
          font-weight: bold;
          color: #409eff;
          margin-bottom: 8px;
        }
        
        .stat-label {
          color: #606266;
          font-size: 14px;
        }
      }
    }
  }
  
  .content-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  }
}
</style>