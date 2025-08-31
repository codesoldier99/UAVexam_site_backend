<template>
  <div class="registration-list-page">
    <div class="page-header">
      <h2>报名列表</h2>
      <p>查看和管理考生报名信息</p>
    </div>
    
    <div class="content-card">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>报名信息</span>
            <div class="header-actions">
              <el-button 
                type="primary" 
                v-permission="'REGISTRATION:CREATE'"
                @click="handleAdd"
              >
                手动添加
              </el-button>
              <el-button 
                type="success" 
                v-permission="'REGISTRATION:EXPORT'"
                @click="handleExport"
              >
                导出数据
              </el-button>
            </div>
          </div>
        </template>
        
        <div class="filter-section">
          <el-form :model="filters" inline>
            <el-form-item label="姓名">
              <el-input v-model="filters.name" placeholder="请输入姓名" />
            </el-form-item>
            <el-form-item label="身份证号">
              <el-input v-model="filters.idCard" placeholder="请输入身份证号" />
            </el-form-item>
            <el-form-item label="状态">
              <el-select v-model="filters.status" placeholder="请选择状态">
                <el-option label="全部" value="" />
                <el-option label="待审核" value="pending" />
                <el-option label="已通过" value="approved" />
                <el-option label="已拒绝" value="rejected" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSearch">搜索</el-button>
              <el-button @click="handleReset">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
        
        <el-table :data="registrations" style="width: 100%">
          <el-table-column prop="name" label="姓名" />
          <el-table-column prop="idCard" label="身份证号" />
          <el-table-column prop="phone" label="联系电话" />
          <el-table-column prop="examType" label="考试类型" />
          <el-table-column prop="status" label="状态">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)">
                {{ getStatusText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="createTime" label="报名时间" />
          <el-table-column label="操作" width="200">
            <template #default="{ row }">
              <el-button 
                size="small" 
                v-permission="'REGISTRATION:READ'"
                @click="handleView(row)"
              >
                查看
              </el-button>
              <el-button 
                size="small" 
                v-permission="'REGISTRATION:UPDATE'"
                @click="handleEdit(row)"
              >
                编辑
              </el-button>
              <el-button 
                size="small" 
                type="danger" 
                v-permission="'REGISTRATION:DELETE'"
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
  idCard: '',
  status: ''
})

const registrations = ref([
  {
    id: 1,
    name: '张三',
    idCard: '110101199001011234',
    phone: '13800138000',
    examType: '无人机驾驶员',
    status: 'approved',
    createTime: '2024-01-10 10:30:00'
  },
  {
    id: 2,
    name: '李四',
    idCard: '110101199002021234',
    phone: '13800138001',
    examType: '无人机教员',
    status: 'pending',
    createTime: '2024-01-11 14:20:00'
  }
])

const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    pending: '待审核',
    approved: '已通过',
    rejected: '已拒绝'
  }
  return texts[status] || '未知'
}

const handleSearch = () => {
  ElMessage.info('搜索功能')
}

const handleReset = () => {
  filters.value = { name: '', idCard: '', status: '' }
}

const handleAdd = () => {
  ElMessage.info('手动添加报名信息')
}

const handleExport = () => {
  ElMessage.info('导出报名数据')
}

const handleView = (row: any) => {
  ElMessage.info(`查看报名信息: ${row.name}`)
}

const handleEdit = (row: any) => {
  ElMessage.info(`编辑报名信息: ${row.name}`)
}

const handleDelete = (row: any) => {
  ElMessage.info(`删除报名信息: ${row.name}`)
}

onMounted(() => {
  // 加载报名数据
})
</script>

<style lang="scss" scoped>
.registration-list-page {
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
      
      .header-actions {
        display: flex;
        gap: 10px;
      }
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