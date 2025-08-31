<template>
  <div class="my-registrations-page">
    <div class="page-header">
      <h2>我的报名</h2>
      <p>查看我的考试报名信息</p>
    </div>
    
    <div class="content-card">
      <el-card>
        <template #header>
          <span>报名记录</span>
        </template>
        
        <el-table :data="myRegistrations" style="width: 100%">
          <el-table-column prop="examName" label="考试名称" />
          <el-table-column prop="examType" label="考试类型" />
          <el-table-column prop="examDate" label="考试日期" />
          <el-table-column prop="venue" label="考场" />
          <el-table-column prop="status" label="状态">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)">
                {{ getStatusText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150">
            <template #default="{ row }">
              <el-button 
                size="small" 
                @click="handleView(row)"
              >
                查看详情
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

const myRegistrations = ref([
  {
    id: 1,
    examName: '2024年第一期无人机驾驶员考试',
    examType: '无人机驾驶员',
    examDate: '2024-02-15',
    venue: '考场A',
    status: 'confirmed'
  },
  {
    id: 2,
    examName: '2024年第二期无人机教员考试',
    examType: '无人机教员',
    examDate: '2024-03-20',
    venue: '考场B',
    status: 'pending'
  }
])

const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    pending: 'warning',
    confirmed: 'success',
    cancelled: 'danger',
    completed: 'info'
  }
  return types[status] || 'info'
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    pending: '待确认',
    confirmed: '已确认',
    cancelled: '已取消',
    completed: '已完成'
  }
  return texts[status] || '未知'
}

const handleView = (row: any) => {
  ElMessage.info(`查看考试详情: ${row.examName}`)
}

onMounted(() => {
  // 加载我的报名数据
})
</script>

<style lang="scss" scoped>
.my-registrations-page {
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
}
</style>