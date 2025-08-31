<template>
  <div class="exam-form page-container">
    <div class="page-header">
      <h2 class="page-title">{{ isEdit ? '编辑考试' : '创建考试' }}</h2>
      <p class="page-description">{{ isEdit ? '修改考试信息' : '创建新的考试' }}</p>
    </div>
    
    <el-card>
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="120px"
        label-position="right"
        @submit.prevent
      >
        <!-- 基本信息 -->
        <h3 class="form-section-title">基本信息</h3>
        
        <el-form-item label="考试名称" prop="title">
          <el-input v-model="formData.title" placeholder="请输入考试名称" />
        </el-form-item>
        
        <el-form-item label="考试类型" prop="type">
          <el-select v-model="formData.type" placeholder="请选择考试类型" style="width: 100%">
            <el-option label="理论考试" value="theory" />
            <el-option label="实操考试" value="practice" />
            <el-option label="综合考试" value="comprehensive" />
          </el-select>
        </el-form-item>
        
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12">
            <el-form-item label="考试时长(分钟)" prop="duration">
              <el-input-number v-model="formData.duration" :min="1" :max="1440" style="width: 100%" />
            </el-form-item>
          </el-col>
          
          <el-col :xs="24" :sm="12">
            <el-form-item label="总分" prop="total_score">
              <el-input-number v-model="formData.total_score" :min="1" :max="1000" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12">
            <el-form-item label="及格分数" prop="pass_score">
              <el-input-number
                v-model="formData.pass_score"
                :min="1"
                :max="formData.total_score"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="考试日期范围" prop="date_range">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
            @change="handleDateRangeChange"
          />
        </el-form-item>
        
        <el-form-item label="考试描述" prop="description">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="4"
            placeholder="请输入考试描述"
          />
        </el-form-item>
        
        <!-- 表单操作 -->
        <div class="form-footer">
          <el-button @click="goBack">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">保存</el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, FormInstance, FormRules } from 'element-plus'
import { createExam, updateExam, getExamDetail } from '@/api/exam'
import type { Exam } from '@/types/exam'

const route = useRoute()
const router = useRouter()
const formRef = ref<FormInstance>()

// 判断是否为编辑模式
const isEdit = computed(() => route.path.includes('/edit'))
const examId = computed(() => route.params.id as string)

// 表单数据
const formData = reactive<Partial<Exam>>({
  title: '',
  description: '',
  type: 'theory',
  duration: 120,
  total_score: 100,
  pass_score: 60,
  start_date: '',
  end_date: ''
})

// 日期范围
const dateRange = ref<[string, string] | null>(null)

// 表单验证规则
const formRules = reactive<FormRules>({
  title: [
    { required: true, message: '请输入考试名称', trigger: 'blur' },
    { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择考试类型', trigger: 'change' }
  ],
  duration: [
    { required: true, message: '请输入考试时长', trigger: 'blur' },
    { type: 'number', min: 1, message: '考试时长必须大于0', trigger: 'blur' }
  ],
  total_score: [
    { required: true, message: '请输入总分', trigger: 'blur' },
    { type: 'number', min: 1, message: '总分必须大于0', trigger: 'blur' }
  ],
  pass_score: [
    { required: true, message: '请输入及格分数', trigger: 'blur' },
    { type: 'number', min: 1, message: '及格分数必须大于0', trigger: 'blur' }
  ],
  date_range: [
    { required: true, message: '请选择考试日期范围', trigger: 'change' }
  ],
  description: [
    { required: true, message: '请输入考试描述', trigger: 'blur' }
  ]
})

// 提交状态
const submitting = ref(false)

// 处理日期范围变化
const handleDateRangeChange = (val: [string, string] | null) => {
  if (val) {
    formData.start_date = val[0]
    formData.end_date = val[1]
  } else {
    formData.start_date = ''
    formData.end_date = ''
  }
}

// 获取考试详情
const fetchExamDetail = async () => {
  try {
    const res = await getExamDetail(examId.value)
    
    // 填充表单数据
    Object.keys(formData).forEach(key => {
      if (key in res) {
        formData[key] = res[key]
      }
    })
    
    // 设置日期范围
    if (res.start_date && res.end_date) {
      dateRange.value = [res.start_date, res.end_date]
    }
  } catch (error) {
    console.error('Failed to fetch exam detail:', error)
    ElMessage.error('获取考试详情失败')
    goBack()
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        submitting.value = true
        
        if (isEdit.value) {
          await updateExam(examId.value, formData)
          ElMessage.success('考试更新成功')
        } else {
          await createExam(formData)
          ElMessage.success('考试创建成功')
        }
        
        goBack()
      } catch (error) {
        console.error('Failed to save exam:', error)
        ElMessage.error(isEdit.value ? '更新考试失败' : '创建考试失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

// 返回上一页
const goBack = () => {
  router.push('/admin/exams')
}

// 页面加载时获取数据
onMounted(() => {
  if (isEdit.value) {
    fetchExamDetail()
  }
})
</script>

<style lang="scss" scoped>
.exam-form {
  .form-section-title {
    font-size: 16px;
    font-weight: 600;
    margin: 0 0 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #ebeef5;
  }
}
</style>