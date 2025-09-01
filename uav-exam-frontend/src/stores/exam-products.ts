import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { 
  getExamProducts, 
  createExamProduct, 
  getExamProductDetail, 
  updateExamProduct, 
  deleteExamProduct,
  searchExamProducts,
  getExamProductStatistics
} from '@/api/exam-products'
import type { 
  ExamProduct, 
  ExamProductCreateRequest, 
  ExamProductUpdateRequest,
  ExamProductListParams,
  ExamProductStatistics,
  ExamProductListResponse
} from '@/api/exam-products'
import { ElMessage } from 'element-plus'

export const useExamProductsStore = defineStore('examProducts', () => {
  // 状态
  const examProducts = ref<ExamProduct[]>([])
  const currentProduct = ref<ExamProduct | null>(null)
  const statistics = ref<ExamProductStatistics | null>(null)
  const loading = ref(false)
  const searchLoading = ref(false)
  
  // 分页状态
  const pagination = ref({
    current: 1,
    pageSize: 20,
    total: 0
  })

  // 计算属性
  const activeProducts = computed(() => 
    examProducts.value.filter(product => product.is_active)
  )

  const inactiveProducts = computed(() => 
    examProducts.value.filter(product => !product.is_active)
  )

  const productsByType = computed(() => {
    const types = { PRACTICAL: 0, THEORY: 0, MIXED: 0 }
    examProducts.value.forEach(product => {
      types[product.exam_type]++
    })
    return types
  })

  // 获取考试产品列表
  const fetchExamProducts = async (params?: ExamProductListParams) => {
    try {
      loading.value = true
      console.log('请求考试产品列表，参数:', params)
      
      const response = await getExamProducts(params)
      console.log('获取考试产品列表成功:', response)
      
      // 响应拦截器返回response.data，所以response就是数据本身
      examProducts.value = response.items || []
      pagination.value = {
        current: response.page || 1,
        pageSize: response.size || 20,
        total: response.total || 0
      }
      
      return response
    } catch (error) {
      console.error('获取考试产品列表失败:', error)
      ElMessage.error('获取考试产品列表失败')
      throw error
    } finally {
      loading.value = false
    }
  }

  // 创建考试产品
  const createProduct = async (productData: ExamProductCreateRequest) => {
    try {
      loading.value = true
      const response = await createExamProduct(productData)
      ElMessage.success('考试产品创建成功')
      
      // 重新获取列表
      await fetchExamProducts()
      return response
    } catch (error) {
      console.error('创建考试产品失败:', error)
      ElMessage.error('创建考试产品失败')
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取考试产品详情
  const fetchProductDetail = async (productId: number) => {
    try {
      loading.value = true
      const response = await getExamProductDetail(productId)
      currentProduct.value = response
      return response
    } catch (error) {
      console.error('获取考试产品详情失败:', error)
      ElMessage.error('获取考试产品详情失败')
      throw error
    } finally {
      loading.value = false
    }
  }

  // 更新考试产品
  const updateProduct = async (productId: number, updateData: ExamProductUpdateRequest) => {
    try {
      loading.value = true
      const response = await updateExamProduct(productId, updateData)
      ElMessage.success('考试产品更新成功')
      
      // 更新本地数据
      const index = examProducts.value.findIndex(p => p.id === productId)
      if (index !== -1) {
        await fetchProductDetail(productId)
        examProducts.value[index] = currentProduct.value!
      }
      
      return response
    } catch (error) {
      console.error('更新考试产品失败:', error)
      ElMessage.error('更新考试产品失败')
      throw error
    } finally {
      loading.value = false
    }
  }

  // 删除考试产品
  const deleteProduct = async (productId: number) => {
    try {
      loading.value = true
      await deleteExamProduct(productId)
      ElMessage.success('考试产品删除成功')
      
      // 从本地列表中移除
      examProducts.value = examProducts.value.filter(p => p.id !== productId)
      return true
    } catch (error) {
      console.error('删除考试产品失败:', error)
      ElMessage.error('删除考试产品失败')
      throw error
    } finally {
      loading.value = false
    }
  }

  // 搜索考试产品
  const searchProducts = async (keyword: string) => {
    try {
      searchLoading.value = true
      const response = await searchExamProducts(keyword)
      // 搜索也返回分页格式
      examProducts.value = response.data.items
      pagination.value = {
        current: response.data.page,
        pageSize: response.data.size,
        total: response.data.total
      }
      return response.data
    } catch (error) {
      console.error('搜索考试产品失败:', error)
      ElMessage.error('搜索失败')
      throw error
    } finally {
      searchLoading.value = false
    }
  }

  // 获取统计数据
  const fetchStatistics = async () => {
    try {
      const response = await getExamProductStatistics()
      statistics.value = response
      return response
    } catch (error) {
      console.error('获取统计数据失败:', error)
      ElMessage.error('获取统计数据失败')
      throw error
    }
  }

  // 重置状态
  const resetState = () => {
    examProducts.value = []
    currentProduct.value = null
    statistics.value = null
    loading.value = false
    searchLoading.value = false
    pagination.value = {
      current: 1,
      pageSize: 20,
      total: 0
    }
  }

  return {
    // 状态
    examProducts,
    currentProduct,
    statistics,
    loading,
    searchLoading,
    pagination,
    
    // 计算属性
    activeProducts,
    inactiveProducts,
    productsByType,
    
    // 方法
    fetchExamProducts,
    createProduct,
    fetchProductDetail,
    updateProduct,
    deleteProduct,
    searchProducts,
    fetchStatistics,
    resetState
  }
})