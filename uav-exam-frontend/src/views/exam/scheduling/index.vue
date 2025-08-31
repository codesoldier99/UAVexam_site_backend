<template>
  <div class="scheduling-page">
    <div class="page-header">
      <h2>考试排期</h2>
      <p>管理考试时间安排</p>
    </div>
    
    <div class="content-card">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>排期列表</span>
            <el-button 
              type="primary" 
              v-permission="'EXAM_SCHEDULE:CREATE'"
              @click="handleAdd"
            >
              新增排期
            </el-button>
          </div>
        </template>
        
        <el-table :data="schedules" style="width: 100%">
          <el-table-column prop="examName" label="考试名称" />
          <el-table-column prop="venue" label="考场" />
          <el-table-column prop="date" label="考试日期" />
          <el-table-column prop="time" label="考试时间" />
          <el-table-column prop="status" label="状态">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)">
                {{ getStatusText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200">
            <template #default="{ row }">
              <el-button 
                size="small" 
                v-permission="'EXAM_SCHEDULE:UPDATE'"
                @click="handleEdit(row)"
              >
                编辑
              </el-button>
              <el-button 
                size="small" 
                type="danger" 
                v-permission="'EXAM_SCHEDULE:DELETE'"
                @click="handleDelete(row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const schedules = ref([
  { 
    id: 1, 
    examName: '无人机驾驶员考试', 
    venue: '考场A', 
    date: '2024-01-15', 
    time: '09:00-12:00', 
    status: 'scheduled' 
  },
  { 
    id: 2, 
    examName: '无人机教员考试', 
    venue: '考场B', 
    date: '2024-01-16', 
    time: '14:00-17:00', 
    status: 'completed' 
  }
])

const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    scheduled: 'warning',
    ongoing: 'primary',
    completed: 'success',
    cancelled: 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    scheduled: '已安排',
    ongoing: '进行中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return texts[status] || '未知'
}

const handleAdd = () => {
  ElMessage.info('新增排期功能')
}

const handleEdit = (row: any) => {
  ElMessage.info(`编辑排期: ${row.examName}`)
}

const handleDelete = (row: any) => {
  ElMessage.info(`删除排期: ${row.examName}`)
}

onMounted(() => {
  // 加载排期数据
})
</script>

<style lang="scss" scoped>
.scheduling-page {
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
  
  .content-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  }
}
</style>