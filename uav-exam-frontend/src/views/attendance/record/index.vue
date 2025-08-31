<template>
  <div class="attendance-record-page">
    <div class="page-header">
      <h2>考勤记录</h2>
      <p>查看和管理考勤记录</p>
    </div>
    
    <div class="content-card">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>考勤记录</span>
            <el-button 
              type="primary" 
              v-permission="'ATTENDANCE:CREATE'"
              @click="handleAdd"
            >
              手动记录
            </el-button>
          </div>
        </template>
        
        <div class="filter-section">
          <el-form :model="filters" inline>
            <el-form-item label="姓名">
              <el-input v-model="filters.name" placeholder="请输入姓名" />
            </el-form-item>
            <el-form-item label="日期">
              <el-date-picker
                v-model="filters.date"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
              />
            </el-form-item>
            <el-form-item label="状态">
              <el-select v-model="filters.status" placeholder="请选择状态">
                <el-option label="全部" value="" />
                <el-option label="正常" value="present" />
                <el-option label="迟到" value="late" />
                <el-option label="缺席" value="absent" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSearch">搜索</el-button>
              <el-button @click="handleReset">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
        
        <el-table :data="attendanceRecords" style="width: 100%">
          <el-table-column prop="name" label="姓名" />
          <el-table-column prop="idCard" label="身份证号" />
          <el-table-column prop="date" label="日期" />
          <el-table-column prop="checkInTime" label="签到时间" />
          <el-table-column prop="checkOutTime" label="签退时间" />
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
                v-permission="'ATTENDANCE:UPDATE'"
                @click="handleEdit(row)"
              >
                编辑
              </el-button>
              <el-button 
                size="small" 
                type="danger" 
                v-permission="'ATTENDANCE:DELETE'"
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

const filters = ref({
  name: '',
  date: [],
  status: ''
})

const attendanceRecords = ref([
  {
    id: 1,
    name: '张三',
    idCard: '110101199001011234',
    date: '2024-01-15',
    checkInTime: '08:30:00',
    checkOutTime: '17:30:00',
    status: 'present'
  },
  {
    id: 2,
    name: '李四',
    idCard: '110101199002021234',
    date: '2024-01-15',
    checkInTime: '09:15:00',
    checkOutTime: '17:30:00',
    status: 'late'
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

const handleSearch = () => {
  ElMessage.info('搜索功能')
}

const handleReset = () => {
  filters.value = { name: '', date: [], status: '' }
}

const handleAdd = () => {
  ElMessage.info('手动记录考勤')
}

const handleEdit = (row: any) => {
  ElMessage.info(`编辑考勤记录: ${row.name}`)
}

const handleDelete = (row: any) => {
  ElMessage.info(`删除考勤记录: ${row.name}`)
}

onMounted(() => {
  // 加载考勤记录数据
})
</script>

<style lang="scss" scoped>
.attendance-record-page {
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
    
    .filter-section {
      margin-bottom: 20px;
      padding: 20px;
      background-color: #f5f7fa;
      border-radius: 4px;
    }
  }
}
</style>