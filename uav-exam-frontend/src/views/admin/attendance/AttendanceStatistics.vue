<template>
  <div class="attendance-statistics">
    <div class="page-header">
      <h2 class="page-title">考勤统计</h2>
      <p class="page-description">查看考勤数据统计和分析</p>
    </div>
    
    <!-- 过滤条件 -->
    <el-card class="filter-card">
      <el-form :model="filterForm" inline>
        <el-form-item label="考试名称">
          <el-select
            v-model="filterForm.exam_id"
            placeholder="选择考试"
            clearable
            filterable
            style="width: 220px"
          >
            <el-option
              v-for="exam in examOptions"
              :key="exam.id"
              :label="exam.name"
              :value="exam.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="filterForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            style="width: 300px"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="resetFilter">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-cards">
      <el-col :span="6">
        <el-card class="stats-card">
          <div class="stats-card-content">
            <div class="stats-icon">
              <el-icon><User /></el-icon>
            </div>
            <div class="stats-info">
              <div class="stats-title">总人数</div>
              <div class="stats-value">{{ stats.totalCount }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stats-card">
          <div class="stats-card-content">
            <div class="stats-icon checked-icon">
              <el-icon><Check /></el-icon>
            </div>
            <div class="stats-info">
              <div class="stats-title">已签到</div>
              <div class="stats-value">{{ stats.checkedInCount }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stats-card">
          <div class="stats-card-content">
            <div class="stats-icon absent-icon">
              <el-icon><Close /></el-icon>
            </div>
            <div class="stats-info">
              <div class="stats-title">未签到</div>
              <div class="stats-value">{{ stats.absentCount }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stats-card">
          <div class="stats-card-content">
            <div class="stats-icon rate-icon">
              <el-icon><DataAnalysis /></el-icon>
            </div>
            <div class="stats-info">
              <div class="stats-title">签到率</div>
              <div class="stats-value">{{ stats.attendanceRate }}%</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 图表区域 -->
    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>考勤趋势</span>
            </div>
          </template>
          <div class="chart-container">
            <v-chart class="chart" :option="attendanceTrendOption" autoresize />
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>考勤分布</span>
            </div>
          </template>
          <div class="chart-container">
            <v-chart class="chart" :option="attendanceDistributionOption" autoresize />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Search, Refresh, User, Check, Close, DataAnalysis, Download } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, BarChart, PieChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import VChart from 'vue-echarts'

// 注册 ECharts 组件
use([
  CanvasRenderer,
  LineChart,
  BarChart,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
])

// 过滤表单
const filterForm = reactive({
  exam_id: '',
  dateRange: []
})

// 表格加载状态
const loading = ref(false)

// 分页
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 考试选项
const examOptions = ref([
  { id: 1, name: '无人机驾驶员理论考试' },
  { id: 2, name: '无人机实操技能考核' },
  { id: 3, name: '无人机驾驶员综合考试' }
])

// 统计数据
const stats = reactive({
  totalCount: 150,
  checkedInCount: 135,
  absentCount: 15,
  attendanceRate: 90
})

// 考勤趋势图表配置
const attendanceTrendOption = ref({
  title: {
    text: '近7天考勤趋势',
    left: 'center'
  },
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['总人数', '已签到', '未签到'],
    bottom: 0
  },
  xAxis: {
    type: 'category',
    data: ['8/22', '8/23', '8/24', '8/25', '8/26', '8/27', '8/28']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: '总人数',
      type: 'line',
      data: [20, 25, 30, 22, 18, 15, 20],
      smooth: true,
      lineStyle: {
        width: 3,
        color: '#409EFF'
      },
      itemStyle: {
        color: '#409EFF'
      }
    },
    {
      name: '已签到',
      type: 'line',
      data: [18, 22, 28, 20, 16, 14, 17],
      smooth: true,
      lineStyle: {
        width: 3,
        color: '#67C23A'
      },
      itemStyle: {
        color: '#67C23A'
      }
    },
    {
      name: '未签到',
      type: 'line',
      data: [2, 3, 2, 2, 2, 1, 3],
      smooth: true,
      lineStyle: {
        width: 3,
        color: '#F56C6C'
      },
      itemStyle: {
        color: '#F56C6C'
      }
    }
  ]
})

// 考勤分布图表配置
const attendanceDistributionOption = ref({
  title: {
    text: '考勤状态分布',
    left: 'center'
  },
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b}: {c} ({d}%)'
  },
  legend: {
    orient: 'vertical',
    left: 'left',
    data: ['已签到', '未签到']
  },
  series: [
    {
      name: '考勤状态',
      type: 'pie',
      radius: ['50%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: '18',
          fontWeight: 'bold'
        }
      },
      labelLine: {
        show: false
      },
      data: [
        { value: 135, name: '已签到', itemStyle: { color: '#67C23A' } },
        { value: 15, name: '未签到', itemStyle: { color: '#F56C6C' } }
      ]
    }
  ]
})

// 考勤详情列表
const examAttendanceList = ref([
  {
    id: 1,
    exam_name: '无人机驾驶员理论考试',
    exam_date: '2025-08-20',
    total_count: 50,
    checked_in_count: 48,
    absent_count: 2,
    attendance_rate: 96
  },
  {
    id: 2,
    exam_name: '无人机实操技能考核',
    exam_date: '2025-08-22',
    total_count: 40,
    checked_in_count: 37,
    absent_count: 3,
    attendance_rate: 92.5
  },
  {
    id: 3,
    exam_name: '无人机驾驶员综合考试',
    exam_date: '2025-08-25',
    total_count: 30,
    checked_in_count: 28,
    absent_count: 2,
    attendance_rate: 93.3
  },
  {
    id: 4,
    exam_name: '无人机应用技术考试',
    exam_date: '2025-08-27',
    total_count: 30,
    checked_in_count: 22,
    absent_count: 8,
    attendance_rate: 73.3
  }
])

// 搜索
const handleSearch = () => {
  loading.value = true
  
  // 模拟API请求
  setTimeout(() => {
    // 这里应该是实际的API请求
    loading.value = false
    ElMessage.success('搜索完成')
  }, 500)
}

// 重置过滤条件
const resetFilter = () => {
  filterForm.exam_id = ''
  filterForm.dateRange = []
  handleSearch()
}

// 分页大小变化
const handleSizeChange = (size: number) => {
  pagination.pageSize = size
  handleSearch()
}

// 页码变化
const handleCurrentChange = (page: number) => {
  pagination.currentPage = page
  handleSearch()
}

// 导出数据
const exportData = () => {
  ElMessage.info('导出数据功能开发中...')
}

// 查看考试考勤详情
const viewExamAttendanceDetail = (row: any) => {
  ElMessage.info(`查看 ${row.exam_name} 的考勤详情，功能开发中...`)
}

// 页面加载时获取数据
onMounted(() => {
  handleSearch()
})
</script>

<style lang="scss" scoped>
.attendance-statistics {
  .filter-card {
    margin-bottom: 20px;
  }
  
  .stats-cards {
    margin-bottom: 20px;
    
    .stats-card {
      .stats-card-content {
        display: flex;
        align-items: center;
        
        .stats-icon {
          width: 60px;
          height: 60px;
          border-radius: 50%;
          background-color: #409EFF;
          display: flex;
          justify-content: center;
          align-items: center;
          margin-right: 15px;
          
          .el-icon {
            font-size: 30px;
            color: #fff;
          }
          
          &.checked-icon {
            background-color: #67C23A;
          }
          
          &.absent-icon {
            background-color: #F56C6C;
          }
          
          &.rate-icon {
            background-color: #E6A23C;
          }
        }
        
        .stats-info {
          .stats-title {
            font-size: 14px;
            color: #606266;
            margin-bottom: 5px;
          }
          
          .stats-value {
            font-size: 24px;
            font-weight: bold;
            color: #303133;
          }
        }
      }
    }
  }
  
  .chart-row {
    margin-bottom: 20px;
    
    .chart-card {
      .chart-container {
        height: 350px;
        
        .chart {
          height: 100%;
        }
      }
    }
  }
  
  .attendance-details-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .pagination-container {
      margin-top: 20px;
      display: flex;
      justify-content: flex-end;
    }
  }
}
</style>