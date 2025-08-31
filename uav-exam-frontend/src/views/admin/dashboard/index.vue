<template>
  <div class="dashboard-container">
    <div class="page-header">
      <h2 class="page-title">仪表盘</h2>
      <p class="page-description">无人机考试管理系统概览</p>
    </div>
    
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-cards">
      <el-col :span="6">
        <el-card class="stats-card">
          <div class="stats-card-content">
            <div class="stats-icon">
              <el-icon><Calendar /></el-icon>
            </div>
            <div class="stats-info">
              <div class="stats-title">考试总数</div>
              <div class="stats-value">{{ stats.examCount }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stats-card">
          <div class="stats-card-content">
            <div class="stats-icon examiner-icon">
              <el-icon><User /></el-icon>
            </div>
            <div class="stats-info">
              <div class="stats-title">考官总数</div>
              <div class="stats-value">{{ stats.examinerCount }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stats-card">
          <div class="stats-card-content">
            <div class="stats-icon candidate-icon">
              <el-icon><User /></el-icon>
            </div>
            <div class="stats-info">
              <div class="stats-title">考生总数</div>
              <div class="stats-value">{{ stats.candidateCount }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stats-card">
          <div class="stats-card-content">
            <div class="stats-icon venue-icon">
              <el-icon><Location /></el-icon>
            </div>
            <div class="stats-info">
              <div class="stats-title">考场总数</div>
              <div class="stats-value">{{ stats.venueCount }}</div>
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
              <span>考试数量趋势</span>
            </div>
          </template>
          <div class="chart-container">
            <v-chart class="chart" :option="examTrendOption" autoresize />
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>考试类型分布</span>
            </div>
          </template>
          <div class="chart-container">
            <v-chart class="chart" :option="examTypeOption" autoresize />
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 最近考试 -->
    <el-card class="recent-exams-card">
      <template #header>
        <div class="card-header">
          <span>最近考试</span>
          <el-button type="primary" size="small" @click="viewAllExams">
            查看全部
          </el-button>
        </div>
      </template>
      <el-table :data="recentExams" style="width: 100%">
        <el-table-column prop="name" label="考试名称" min-width="200" />
        <el-table-column prop="exam_type" label="考试类型" width="120" />
        <el-table-column prop="start_date" label="开始日期" width="120" />
        <el-table-column prop="end_date" label="结束日期" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="scope">
            <el-button link type="primary" @click="viewExamDetail(scope.row)">
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Calendar, User, Location } from '@element-plus/icons-vue'
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

const router = useRouter()

// 统计数据
const stats = reactive({
  examCount: 24,
  examinerCount: 36,
  candidateCount: 128,
  venueCount: 8
})

// 考试趋势图表配置
const examTrendOption = ref({
  title: {
    text: '近6个月考试数量',
    left: 'center'
  },
  tooltip: {
    trigger: 'axis'
  },
  xAxis: {
    type: 'category',
    data: ['1月', '2月', '3月', '4月', '5月', '6月']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      data: [3, 5, 4, 6, 2, 4],
      type: 'line',
      smooth: true,
      lineStyle: {
        width: 3,
        color: '#409EFF'
      },
      itemStyle: {
        color: '#409EFF'
      }
    }
  ]
})

// 考试类型图表配置
const examTypeOption = ref({
  title: {
    text: '考试类型分布',
    left: 'center'
  },
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b}: {c} ({d}%)'
  },
  legend: {
    orient: 'vertical',
    left: 'left',
    data: ['理论考试', '实操考试', '综合考试']
  },
  series: [
    {
      name: '考试类型',
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
        { value: 10, name: '理论考试', itemStyle: { color: '#409EFF' } },
        { value: 8, name: '实操考试', itemStyle: { color: '#67C23A' } },
        { value: 6, name: '综合考试', itemStyle: { color: '#E6A23C' } }
      ]
    }
  ]
})

// 最近考试数据
const recentExams = ref([
  {
    id: 1,
    name: '无人机驾驶员理论考试',
    exam_type: '理论考试',
    start_date: '2025-08-30',
    end_date: '2025-08-30',
    status: 'pending'
  },
  {
    id: 2,
    name: '无人机实操技能考核',
    exam_type: '实操考试',
    start_date: '2025-09-05',
    end_date: '2025-09-05',
    status: 'pending'
  },
  {
    id: 3,
    name: '无人机驾驶员综合考试',
    exam_type: '综合考试',
    start_date: '2025-09-15',
    end_date: '2025-09-15',
    status: 'pending'
  },
  {
    id: 4,
    name: '无人机应用技术考试',
    exam_type: '理论考试',
    start_date: '2025-08-20',
    end_date: '2025-08-20',
    status: 'completed'
  },
  {
    id: 5,
    name: '无人机飞行技能考核',
    exam_type: '实操考试',
    start_date: '2025-08-15',
    end_date: '2025-08-15',
    status: 'completed'
  }
])

// 获取状态类型
const getStatusType = (status: string) => {
  const statusMap: Record<string, string> = {
    'pending': 'primary',
    'ongoing': 'warning',
    'completed': 'success',
    'cancelled': 'danger'
  }
  
  return statusMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    'pending': '未开始',
    'ongoing': '进行中',
    'completed': '已结束',
    'cancelled': '已取消'
  }
  
  return statusMap[status] || status
}

// 查看全部考试
const viewAllExams = () => {
  router.push('/exam/list')
}

// 查看考试详情
const viewExamDetail = (exam: any) => {
  router.push(`/exam/detail/${exam.id}`)
}

// 页面加载时获取数据
onMounted(() => {
  // 这里可以添加获取数据的逻辑
})
</script>

<style lang="scss" scoped>
.dashboard-container {
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
          
          &.examiner-icon {
            background-color: #67C23A;
          }
          
          &.candidate-icon {
            background-color: #E6A23C;
          }
          
          &.venue-icon {
            background-color: #F56C6C;
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
  
  .recent-exams-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  }
}
</style>