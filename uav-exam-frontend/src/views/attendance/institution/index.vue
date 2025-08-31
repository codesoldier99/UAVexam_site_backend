<template>
  <div class="institution-attendance-page">
    <div class="page-header">
      <h2>机构考勤</h2>
      <p>查看本机构的考勤统计</p>
    </div>
    
    <div class="content-card">
      <el-card>
        <template #header>
          <span>机构考勤统计</span>
        </template>
        
        <div class="stats-section">
          <el-row :gutter="20">
            <el-col :span="6">
              <div class="stat-card">
                <div class="stat-number">{{ stats.totalPersons }}</div>
                <div class="stat-label">总人数</div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-card">
                <div class="stat-number">{{ stats.presentToday }}</div>
                <div class="stat-label">今日出勤</div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-card">
                <div class="stat-number">{{ stats.lateToday }}</div>
                <div class="stat-label">今日迟到</div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-card">
                <div class="stat-number">{{ stats.absentToday }}</div>
                <div class="stat-label">今日缺席</div>
              </div>
            </el-col>
          </el-row>
        </div>
        
        <el-table :data="institutionAttendance" style="width: 100%">
          <el-table-column prop="name" label="姓名" />
          <el-table-column prop="department" label="部门" />
          <el-table-column prop="todayStatus" label="今日状态">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.todayStatus)">
                {{ getStatusText(row.todayStatus) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="checkInTime" label="签到时间" />
          <el-table-column prop="monthlyAttendance" label="本月出勤率" />
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const stats = ref({
  totalPersons: 45,
  presentToday: 42,
  lateToday: 2,
  absentToday: 1
})

const institutionAttendance = ref([
  {
    id: 1,
    name: '王五',
    department: '教学部',
    todayStatus: 'present',
    checkInTime: '08:30:00',
    monthlyAttendance: '95%'
  },
  {
    id: 2,
    name: '赵六',
    department: '管理部',
    todayStatus: 'late',
    checkInTime: '09:15:00',
    monthlyAttendance: '88%'
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

onMounted(() => {
  // 加载机构考勤数据
})
</script>

<style lang="scss" scoped>
.institution-attendance-page {
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
    margin-bottom: 30px;
    
    .stat-card {
      text-align: center;
      padding: 20px;
      background-color: #f5f7fa;
      border-radius: 8px;
      
      .stat-number {
        font-size: 32px;
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
</style>