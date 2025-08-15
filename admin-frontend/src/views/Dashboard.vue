<template>
  <div class="dashboard">
    <h2>欢迎使用无人机考点管理系统</h2>
    
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <el-statistic title="今日考生" :value="stats.todayCandidates">
            <template #prefix>
              <el-icon><User /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <el-statistic title="待考人数" :value="stats.waitingCount">
            <template #prefix>
              <el-icon><Clock /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <el-statistic title="已完成" :value="stats.completedCount">
            <template #prefix>
              <el-icon><CircleCheck /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <el-statistic title="活跃考场" :value="stats.activeVenues">
            <template #prefix>
              <el-icon><Location /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" class="content-row">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>今日考试安排</span>
          </template>
          <el-table :data="todaySchedules" style="width: 100%">
            <el-table-column prop="time" label="时间" width="100" />
            <el-table-column prop="candidate" label="考生" />
            <el-table-column prop="exam" label="考试科目" />
            <el-table-column prop="venue" label="考场" />
            <el-table-column prop="status" label="状态">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>考场实时状态</span>
          </template>
          <div v-for="venue in venueStatus" :key="venue.id" class="venue-item">
            <div class="venue-header">
              <span class="venue-name">{{ venue.name }}</span>
              <el-tag :type="venue.active ? 'success' : 'info'">
                {{ venue.active ? '使用中' : '空闲' }}
              </el-tag>
            </div>
            <div class="venue-info">
              <span>当前考生: {{ venue.currentCandidate || '无' }}</span>
              <span>等待人数: {{ venue.waitingCount }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const stats = ref({
  todayCandidates: 125,
  waitingCount: 23,
  completedCount: 86,
  activeVenues: 5
})

const todaySchedules = ref([
  { time: '09:00', candidate: '张三', exam: '理论考试', venue: '理论考场1', status: '已完成' },
  { time: '10:00', candidate: '李四', exam: '实操考试', venue: '实操场A', status: '进行中' },
  { time: '11:00', candidate: '王五', exam: '理论考试', venue: '理论考场2', status: '待考' }
])

const venueStatus = ref([
  { id: 1, name: '理论考场1', active: true, currentCandidate: '张三', waitingCount: 5 },
  { id: 2, name: '实操场A', active: true, currentCandidate: '李四', waitingCount: 8 },
  { id: 3, name: '实操场B', active: false, currentCandidate: null, waitingCount: 0 }
])

const getStatusType = (status) => {
  const map = {
    '已完成': 'success',
    '进行中': 'primary',
    '待考': 'warning'
  }
  return map[status] || 'info'
}

onMounted(() => {
  // 加载真实数据
})
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
}

.content-row {
  margin-top: 20px;
}

.venue-item {
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.venue-item:last-child {
  border-bottom: none;
}

.venue-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.venue-name {
  font-weight: bold;
}

.venue-info {
  display: flex;
  justify-content: space-between;
  color: #666;
  font-size: 14px;
}
</style>