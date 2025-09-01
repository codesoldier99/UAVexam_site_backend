<template>
  <div class="exam-products-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <h2 class="page-title">考试产品管理</h2>
        <p class="page-description">管理所有考试产品信息</p>
      </div>
      <div class="header-right">
        <el-button 
          type="primary" 
          :icon="Plus" 
          @click="handleCreate"
          v-if="canCreate"
        >
          新增产品
        </el-button>
      </div>
    </div>

    <!-- 搜索和筛选 -->
    <div class="search-section">
      <el-row :gutter="16">
        <el-col :span="8">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索产品名称或编码"
            :prefix-icon="Search"
            @input="handleSearch"
            clearable
          />
        </el-col>
        <el-col :span="6">
          <el-select
            v-model="statusFilter"
            placeholder="状态筛选"
            @change="handleFilter"
            clearable
          >
            <el-option label="全部" value="" />
            <el-option label="启用" :value="true" />
            <el-option label="禁用" :value="false" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-select
            v-model="typeFilter"
            placeholder="类型筛选"
            @change="handleFilter"
            clearable
          >
            <el-option label="全部" value="" />
            <el-option label="实操考试" value="PRACTICAL" />
            <el-option label="理论考试" value="THEORY" />
            <el-option label="综合考试" value="MIXED" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="handleRefresh">刷新</el-button>
        </el-col>
      </el-row>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-section" v-if="statistics">
      <el-row :gutter="16">
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ statistics.total_products }}</div>
              <div class="stat-label">总产品数</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ statistics.active_products }}</div>
              <div class="stat-label">启用产品</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ statistics.registration_stats.total_registrations }}</div>
              <div class="stat-label">总报名数</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ statistics.pass_rate_stats.overall_pass_rate }}%</div>
              <div class="stat-label">整体通过率</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 产品列表 -->
    <el-card class="table-card">
      <el-table
        :data="examProducts"
        :loading="loading"
        stripe
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="name" label="产品名称" min-width="200">
          <template #default="{ row }">
            <div class="product-name">
              <span class="name">{{ row.name }}</span>
              <el-tag 
                :type="getTypeTagType(row.exam_type)" 
                size="small"
                class="type-tag"
              >
                {{ getTypeLabel(row.exam_type) }}
              </el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="code" label="产品编码" width="150" />
        <el-table-column prop="duration_minutes" label="考试时长" width="100">
          <template #default="{ row }">
            {{ row.duration_minutes }}分钟
          </template>
        </el-table-column>
        <el-table-column prop="price" label="价格" width="100">
          <template #default="{ row }">
            <span v-if="row.price">¥{{ row.price }}</span>
            <span v-else class="text-gray-400">-</span>
          </template>
        </el-table-column>
        <el-table-column prop="registration_count" label="报名数" width="100">
          <template #default="{ row }">
            {{ row.registration_count || 0 }}
          </template>
        </el-table-column>
        <el-table-column prop="pass_rate" label="通过率" width="100">
          <template #default="{ row }">
            <span v-if="row.pass_rate">{{ row.pass_rate }}%</span>
            <span v-else class="text-gray-400">-</span>
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="{ row }">
            <el-switch
              v-model="row.is_active"
              @change="handleStatusChange(row)"
              :disabled="!canEdit"
            />
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button 
              type="primary" 
              size="small" 
              @click="handleView(row)"
              link
            >
              查看
            </el-button>
            <el-button 
              type="primary" 
              size="small" 
              @click="handleEdit(row)"
              link
              v-if="canEdit"
            >
              编辑
            </el-button>
            <el-button 
              type="danger" 
              size="small" 
              @click="handleDelete(row)"
              link
              v-if="canDelete"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="pagination.current"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 产品详情/编辑对话框 -->
    <ProductDialog
      v-model="dialogVisible"
      :product="currentProduct"
      :mode="dialogMode"
      @success="handleDialogSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { Plus, Search } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useExamProductsStore } from '@/stores/exam-products'
import { useUserStore } from '@/stores/user'
import ProductDialog from './components/ProductDialog.vue'
import type { ExamProduct } from '@/api/exam-products'
import { formatDateTime } from '@/utils/date'

// Store
const examProductsStore = useExamProductsStore()
const userStore = useUserStore()

// 响应式数据
const searchKeyword = ref('')
const statusFilter = ref<boolean | ''>('')
const typeFilter = ref('')
const selectedProducts = ref<ExamProduct[]>([])
const dialogVisible = ref(false)
const dialogMode = ref<'view' | 'create' | 'edit'>('view')
const currentProduct = ref<ExamProduct | null>(null)

// 计算属性 - 使用 storeToRefs 保持响应式
const { examProducts, loading, statistics, pagination } = storeToRefs(examProductsStore)
const userRole = computed(() => userStore.userInfo?.role?.toUpperCase())

// 权限控制
const canCreate = computed(() => ['SUPER_ADMIN', 'ADMIN'].includes(userRole.value || ''))
const canEdit = computed(() => ['SUPER_ADMIN', 'ADMIN'].includes(userRole.value || ''))
const canDelete = computed(() => ['SUPER_ADMIN'].includes(userRole.value || ''))

// 方法
const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    examProductsStore.searchProducts(searchKeyword.value.trim())
  } else {
    loadData()
  }
}

const handleFilter = () => {
  const params: any = {}
  if (statusFilter.value !== '') {
    params.is_active = statusFilter.value
  }
  loadData(params)
}

const handleRefresh = () => {
  searchKeyword.value = ''
  statusFilter.value = ''
  typeFilter.value = ''
  loadData()
}

const handleCreate = () => {
  currentProduct.value = null
  dialogMode.value = 'create'
  dialogVisible.value = true
}

const handleView = (product: ExamProduct) => {
  currentProduct.value = product
  dialogMode.value = 'view'
  dialogVisible.value = true
}

const handleEdit = (product: ExamProduct) => {
  currentProduct.value = product
  dialogMode.value = 'edit'
  dialogVisible.value = true
}

const handleDelete = async (product: ExamProduct) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除考试产品"${product.name}"吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await examProductsStore.deleteProduct(product.id)
  } catch (error) {
    // 用户取消删除
  }
}

const handleStatusChange = async (product: ExamProduct) => {
  try {
    await examProductsStore.updateProduct(product.id, {
      is_active: product.is_active
    })
  } catch (error) {
    // 恢复原状态
    product.is_active = !product.is_active
  }
}

const handleSelectionChange = (selection: ExamProduct[]) => {
  selectedProducts.value = selection
}

const handleSizeChange = (size: number) => {
  pagination.value.pageSize = size
  pagination.value.current = 1  // 重置到第一页
  loadData()
}

const handleCurrentChange = (page: number) => {
  pagination.value.current = page
  loadData()
}

const handleDialogSuccess = () => {
  dialogVisible.value = false
  loadData()
}

const getTypeTagType = (type: string) => {
  const typeMap: Record<string, string> = {
    'PRACTICAL': 'success',
    'THEORY': 'info',
    'MIXED': 'warning'
  }
  return typeMap[type] || 'info'
}

const getTypeLabel = (type: string) => {
  const labelMap: Record<string, string> = {
    'PRACTICAL': '实操',
    'THEORY': '理论',
    'MIXED': '综合'
  }
  return labelMap[type] || type
}

const loadData = async (params?: any) => {
  try {
    console.log('开始加载考试产品数据...')
    
    // 根据当前分页计算 skip 参数
    const currentPage = pagination.value.current
    const pageSize = pagination.value.pageSize
    const skip = (currentPage - 1) * pageSize
    
    const requestParams = {
      skip,
      limit: pageSize,
      ...params
    }
    
    console.log('请求参数:', requestParams)
    await examProductsStore.fetchExamProducts(requestParams)
    
    // 加载统计数据
    await examProductsStore.fetchStatistics()
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

// 生命周期
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.exam-products-page {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.page-description {
  margin: 4px 0 0 0;
  color: #909399;
  font-size: 14px;
}

.search-section {
  margin-bottom: 20px;
}

.stats-section {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
}

.stat-content {
  padding: 10px;
}

.stat-number {
  font-size: 28px;
  font-weight: 600;
  color: #409EFF;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.table-card {
  margin-bottom: 20px;
}

.product-name {
  display: flex;
  align-items: center;
  gap: 8px;
}

.name {
  font-weight: 500;
}

.type-tag {
  margin-left: 8px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.text-gray-400 {
  color: #c0c4cc;
}
</style>