<template>
  <div class="candidates-list-page">
    <div class="page-header">
      <h2>考生列表</h2>
      <p>管理考生信息</p>
    </div>
    
    <div class="content-card">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>考生信息</span>
            <el-button 
              type="primary" 
              v-permission="'CANDIDATE:CREATE'"
              @click="handleAdd"
            >
              新增考生
            </el-button>
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
                <el-option label="正常" value="active" />
                <el-option label="禁用" value="inactive" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSearch">搜索</el-button>
              <el-button @click="handleReset">重置</el-button>
            </el-form-item>
          </el-form>
        </div>
        
        <el-table :data="candidates" style="width: 100%">
          <el-table-column prop="name" label="姓名" />
          <el-table-column prop="idCard" label="身份证号" />
          <el-table-column prop="phone" label="联系电话" />
          <el-table-column prop="email" label="邮箱" />
          <el-table-column prop="institution" label="所属机构" />
          <el-table-column prop="status" label="状态">
            <template #default="{ row }">
              <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
                {{ row.status === 'active' ? '正常' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200">
            <template #default="{ row }">
              <el-button 
                size="small" 
                v-permission="'CANDIDATE:READ'"
                @click="handleView(row)"
              >
                查看
              </el-button>
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

const filters = ref({
  name: '',
  idCard: '',
  status: ''
})

const candidates = ref([
  {
    id: 1,
    name: '张三',
    idCard: '110101199001011234',
    phone: '13800138000',
    email: 'zhangsan@example.com',
    institution: '北京航空学院',
    status: 'active'
  },
  {
    id: 2,
    name: '李四',
    idCard: '110101199002021234',
    phone: '13800138001',
    email: 'lisi@example.com',
    institution: '上海飞行学校',
    status: 'active'
  }
])

const handleSearch = () => {
  ElMessage.info('搜索功能')
}

const handleReset = () => {
  filters.value = { name: '', idCard: '', status: '' }
}

const handleAdd = () => {
  ElMessage.info('新增考生功能')
}

const handleView = (row: any) => {
  ElMessage.info(`查看考生: ${row.name}`)
}

const handleEdit = (row: any) => {
  ElMessage.info(`编辑考生: ${row.name}`)
}

const handleDelete = (row: any) => {
  ElMessage.info(`删除考生: ${row.name}`)
}

onMounted(() => {
  // 加载考生数据
})
</script>

<style lang="scss" scoped>
.candidates-list-page {
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