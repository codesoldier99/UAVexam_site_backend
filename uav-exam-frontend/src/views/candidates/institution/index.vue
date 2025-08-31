<template>
  <div class="institution-candidates-page">
    <div class="page-header">
      <h2>机构考生</h2>
      <p>管理本机构的考生信息</p>
    </div>
    
    <div class="content-card">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>机构考生列表</span>
            <el-button 
              type="primary" 
              v-permission="'CANDIDATE:CREATE'"
              @click="handleAdd"
            >
              添加考生
            </el-button>
          </div>
        </template>
        
        <el-table :data="institutionCandidates" style="width: 100%">
          <el-table-column prop="name" label="姓名" />
          <el-table-column prop="idCard" label="身份证号" />
          <el-table-column prop="phone" label="联系电话" />
          <el-table-column prop="examType" label="考试类型" />
          <el-table-column prop="registrationDate" label="报名日期" />
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
                v-permission="'CANDIDATE:UPDATE'"
                @click="handleEdit(row)"
              >
                编辑
              </el-button>
              <el-button 
                size="small" 
                type="danger" 
                v-permission="'CANDIDATE:DELETE'"
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

const institutionCandidates = ref([
  {
    id: 1,
    name: '王五',
    idCard: '110101199003031234',
    phone: '13800138002',
    examType: '无人机驾驶员',
    registrationDate: '2024-01-12',
    status: 'registered'
  },
  {
    id: 2,
    name: '赵六',
    idCard: '110101199004041234',
    phone: '13800138003',
    examType: '无人机教员',
    registrationDate: '2024-01-13',
    status: 'confirmed'
  }
])

const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    registered: 'warning',
    confirmed: 'success',
    cancelled: 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    registered: '已报名',
    confirmed: '已确认',
    cancelled: '已取消'
  }
  return texts[status] || '未知'
}

const handleAdd = () => {
  ElMessage.info('添加考生功能')
}

const handleEdit = (row: any) => {
  ElMessage.info(`编辑考生: ${row.name}`)
}

const handleDelete = (row: any) => {
  ElMessage.info(`删除考生: ${row.name}`)
}

onMounted(() => {
  // 加载机构考生数据
})
</script>

<style lang="scss" scoped>
.institution-candidates-page {
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