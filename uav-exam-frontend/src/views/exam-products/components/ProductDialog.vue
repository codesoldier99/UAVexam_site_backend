<template>
  <el-dialog
    v-model="visible"
    :title="dialogTitle"
    width="800px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="formRules"
      label-width="120px"
      :disabled="mode === 'view'"
    >
      <el-row :gutter="16">
        <el-col :span="12">
          <el-form-item label="产品名称" prop="name">
            <el-input v-model="formData.name" placeholder="请输入产品名称" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="产品编码" prop="code">
            <el-input v-model="formData.code" placeholder="请输入产品编码" />
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item label="产品描述" prop="description">
        <el-input
          v-model="formData.description"
          type="textarea"
          :rows="3"
          placeholder="请输入产品描述"
        />
      </el-form-item>

      <el-row :gutter="16">
        <el-col :span="8">
          <el-form-item label="考试类型" prop="exam_type">
            <el-select v-model="formData.exam_type" placeholder="请选择考试类型">
              <el-option label="实操考试" value="PRACTICAL" />
              <el-option label="理论考试" value="THEORY" />
              <el-option label="综合考试" value="MIXED" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="考试时长" prop="duration_minutes">
            <el-input-number
              v-model="formData.duration_minutes"
              :min="1"
              :max="480"
              placeholder="分钟"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="考试价格" prop="price">
            <el-input-number
              v-model="formData.price"
              :min="0"
              :precision="2"
              placeholder="元"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="16">
        <el-col :span="8">
          <el-form-item label="满分" prop="max_score">
            <el-input-number
              v-model="formData.max_score"
              :min="1"
              placeholder="分"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="及格分" prop="pass_score">
            <el-input-number
              v-model="formData.pass_score"
              :min="1"
              :max="formData.max_score || 100"
              placeholder="分"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="状态" prop="is_active">
            <el-switch
              v-model="formData.is_active"
              active-text="启用"
              inactive-text="禁用"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item label="考试要求">
        <div class="requirements-section">
          <el-tag
            v-for="(requirement, index) in formData.requirements"
            :key="index"
            closable
            @close="removeRequirement(index)"
            style="margin-right: 8px; margin-bottom: 8px;"
          >
            {{ requirement }}
          </el-tag>
          <el-input
            v-if="inputVisible"
            ref="inputRef"
            v-model="inputValue"
            size="small"
            style="width: 120px; margin-right: 8px;"
            @keyup.enter="handleInputConfirm"
            @blur="handleInputConfirm"
          />
          <el-button
            v-else
            size="small"
            @click="showInput"
            :disabled="mode === 'view'"
          >
            + 添加要求
          </el-button>
        </div>
      </el-form-item>

      <!-- 查看模式下显示统计信息 -->
      <template v-if="mode === 'view' && product">
        <el-divider content-position="left">统计信息</el-divider>
        <el-row :gutter="16">
          <el-col :span="8">
            <el-form-item label="报名人数">
              <span class="stat-value">{{ product.registration_count || 0 }}</span>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="通过率">
              <span class="stat-value">{{ product.pass_rate || 0 }}%</span>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="创建时间">
              <span class="stat-value">{{ formatDateTime(product.created_at) }}</span>
            </el-form-item>
          </el-col>
        </el-row>
      </template>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button
          v-if="mode !== 'view'"
          type="primary"
          :loading="loading"
          @click="handleSubmit"
        >
          {{ mode === 'create' ? '创建' : '保存' }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { useExamProductsStore } from '@/stores/exam-products'
import type { ExamProduct, ExamProductCreateRequest, ExamProductUpdateRequest } from '@/api/exam-products'
import { formatDateTime } from '@/utils/date'

interface Props {
  modelValue: boolean
  product?: ExamProduct | null
  mode: 'view' | 'create' | 'edit'
}

interface Emits {
  (e: 'update:modelValue', value: boolean): void
  (e: 'success'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// Store
const examProductsStore = useExamProductsStore()

// 响应式数据
const formRef = ref<FormInstance>()
const inputRef = ref()
const loading = ref(false)
const inputVisible = ref(false)
const inputValue = ref('')

// 表单数据
const formData = ref<ExamProductCreateRequest>({
  name: '',
  code: '',
  description: '',
  duration_minutes: 120,
  exam_type: 'PRACTICAL',
  is_active: true,
  requirements: [],
  max_score: 100,
  pass_score: 80,
  price: 0
})

// 计算属性
const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const dialogTitle = computed(() => {
  const titleMap = {
    view: '查看考试产品',
    create: '新增考试产品',
    edit: '编辑考试产品'
  }
  return titleMap[props.mode]
})

// 表单验证规则
const formRules: FormRules = {
  name: [
    { required: true, message: '请输入产品名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入产品编码', trigger: 'blur' },
    { pattern: /^[A-Z0-9_]+$/, message: '编码只能包含大写字母、数字和下划线', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入产品描述', trigger: 'blur' },
    { max: 500, message: '描述不能超过500个字符', trigger: 'blur' }
  ],
  exam_type: [
    { required: true, message: '请选择考试类型', trigger: 'change' }
  ],
  duration_minutes: [
    { required: true, message: '请输入考试时长', trigger: 'blur' },
    { type: 'number', min: 1, max: 480, message: '考试时长应在1-480分钟之间', trigger: 'blur' }
  ]
}

// 监听产品数据变化
watch(() => props.product, (newProduct) => {
  if (newProduct && props.mode !== 'create') {
    formData.value = {
      name: newProduct.name,
      code: newProduct.code,
      description: newProduct.description,
      duration_minutes: newProduct.duration_minutes,
      exam_type: newProduct.exam_type,
      is_active: newProduct.is_active,
      requirements: newProduct.requirements || [],
      max_score: newProduct.max_score || 100,
      pass_score: newProduct.pass_score || 80,
      price: newProduct.price || 0
    }
  }
}, { immediate: true })

// 重置表单
const resetForm = () => {
  formData.value = {
    name: '',
    code: '',
    description: '',
    duration_minutes: 120,
    exam_type: 'PRACTICAL',
    is_active: true,
    requirements: [],
    max_score: 100,
    pass_score: 80,
    price: 0
  }
  formRef.value?.clearValidate()
}

// 添加要求
const showInput = () => {
  inputVisible.value = true
  nextTick(() => {
    inputRef.value?.focus()
  })
}

const handleInputConfirm = () => {
  if (inputValue.value && !formData.value.requirements?.includes(inputValue.value)) {
    formData.value.requirements = formData.value.requirements || []
    formData.value.requirements.push(inputValue.value)
  }
  inputVisible.value = false
  inputValue.value = ''
}

const removeRequirement = (index: number) => {
  formData.value.requirements?.splice(index, 1)
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    loading.value = true

    if (props.mode === 'create') {
      await examProductsStore.createProduct(formData.value)
      ElMessage.success('考试产品创建成功')
    } else if (props.mode === 'edit' && props.product) {
      const updateData: ExamProductUpdateRequest = {
        name: formData.value.name,
        description: formData.value.description,
        duration_minutes: formData.value.duration_minutes,
        price: formData.value.price,
        pass_score: formData.value.pass_score,
        is_active: formData.value.is_active,
        requirements: formData.value.requirements
      }
      await examProductsStore.updateProduct(props.product.id, updateData)
      ElMessage.success('考试产品更新成功')
    }

    emit('success')
  } catch (error) {
    console.error('提交失败:', error)
  } finally {
    loading.value = false
  }
}

// 关闭对话框
const handleClose = () => {
  if (props.mode === 'create') {
    resetForm()
  }
  emit('update:modelValue', false)
}
</script>

<style scoped>
.requirements-section {
  min-height: 32px;
}

.stat-value {
  font-weight: 500;
  color: #303133;
}

.dialog-footer {
  text-align: right;
}
</style>