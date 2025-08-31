<template>
  <div class="venues-page">
    <div class="page-header">
      <h2>考场管理</h2>
      <p>管理考试场地信息</p>
    </div>
    
    <div class="content-card">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>考场列表</span>
            <el-button 
              type="primary" 
              v-permission="'VENUE:CREATE'"
              @click="handleAdd"
            >
              新增考场
            </el-button>
          </div>
        </template>
        
        <el-table :data="venues" style="width: 100%">
          <el-table-column prop="name" label="考场名称" />
          <el-table-column prop="address" label="地址" />
          <el-table-column prop="capacity" label="容量" />
          <el-table-column prop="status" label="状态">
            <template #default="{ row }">
              <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
                {{ row.status === 'active' ? '启用' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200">
            <template #default="{ row }">
              <el-button 
                size="small" 
                v-permission="'VENUE:UPDATE'"
                @click="handleEdit(row)"
              >
                编辑
              </el-button>
              <el-button 
                size="small" 
                type="danger" 
                v-permission="'VENUE:DELETE'"
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

const venues = ref([
  { id: 1, name: '考场A', address: '北京市朝阳区', capacity: 50, status: 'active' },
  { id: 2, name: '考场B', address: '北京市海淀区', capacity: 30, status: 'active' }
])

const handleAdd = () => {
  ElMessage.info('新增考场功能')
}

const handleEdit = (row: any) => {
  ElMessage.info(`编辑考场: ${row.name}`)
}

const handleDelete = (row: any) => {
  ElMessage.info(`删除考场: ${row.name}`)
}

onMounted(() => {
  // 加载考场数据
})
</script>

<style lang="scss" scoped>
.venues-page {
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