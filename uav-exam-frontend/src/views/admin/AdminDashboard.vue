<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { User, Calendar, Collection, OfficeBuilding } from '@element-plus/icons-vue'
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

// 仪表板数据
const dashboardData = reactive({
  total_candidates: 1250,
  new_candidates: 78,
  total_exams: 156,
  upcoming_exams: 12,
  total_questions: 2450,
  question_categories: 18,
  total_venues: 25,
  active_venues: 15
})

// 考试图表时间范围
const examChartTimeRange = ref('month')

// 考试数据图表配置
const examChartOption = reactive({
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['考试数量', '参考人数', '通过人数']
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: '考试数量',
      type: 'line',
      data: [10, 12, 15, 14, 16, 18, 20, 22, 18, 16, 14, 12],
      smooth: true,
      lineStyle: {
        width: 3,
        color: '#409EFF'
      }
    },
    {
      name: '参考人数',
      type: 'line',
      data: [120, 132, 145, 160, 168, 180, 190, 210, 185, 170, 155, 140],
      smooth: true,
      lineStyle: {
        width: 3,
        color: '#67C23A'
      }
    },
    {
      name: '通过人数',
      type: 'line',
      data: [95, 105, 120, 130, 140, 150, 160, 175, 155, 140, 130, 115],
      smooth: true,
      lineStyle: {
        width: 3,
        color: '#E6A23C'
      }
    }
  ]
})

// 通过率图表配置
const passRateChartOption = reactive({
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b}: {c} ({d}%)'
  },
  legend: {
    orient: 'vertical',
    left: 10,
    data: ['优秀', '良好', '及格', '不及格']
  },
  series: [
    {
      name: '考试成绩',
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
        { value: 35, name: '优秀', itemStyle: { color: '#67C23A' } },
        { value: 40, name: '良好', itemStyle: { color: '#409EFF' } },
        { value: 15, name: '及格', itemStyle: { color: '#E6A23C' } },
        { value: 10, name: '不及格', itemStyle: { color: '#F56C6C' } }
      ]
    }
  ]
})

// 最近考试数据
const recentExams = ref([
  {
    id: 1,
    title: '无人机基础理论考试',
    start_time: '2025-08-30 09:00',
    status: 'upcoming'
  },
  {
    id: 2,
    title: '无人机飞行操作技能考试',
    start_time: '2025-08-29 14:00',
    status: 'upcoming'
  },
  {
    id: 3,
    title: '无人机安全规范考试',
    start_time: '2025-08-25 10:00',
    status: 'completed'
  },
  {
    id: 4,
    title: '无人机航拍技术考试',
    start_time: '2025-08-20 13:30',
    status: 'completed'
  },
  {
    id: 5,
    title: '无人机维护保养考试',
    start_time: '2025-08-15 09:30',
    status: 'completed'
  }
])

// 最近活动数据
const recentActivities = ref([
  {
    content: '管理员 张三 创建了新考试 "无人机基础理论考试"',
    time: '2025-08-27 15:32',
    type: 'primary'
  },
  {
    content: '系统自动备份数据完成',
    time: '2025-08-27 03:00',
    type: 'info'
  },
  {
    content: '管理员 李四 添加了15名新考生',
    time: '2025-08-26 14:20',
    type: 'success'
  },
  {
    content: '操作员 王五 修改了考试 "无人机飞行操作技能考试" 的时间',
    time: '2025-08-26 11:05',
    type: 'warning'
  },
  {
    content: '系统检测到异常登录尝试',
    time: '2025-08-25 22:43',
    type: 'danger'
  }
])

// 获取考试状态类型
const getExamStatusType = (status: string): string => {
  const statusMap: Record<string, string> = {
    'upcoming': 'primary',
    'ongoing': 'success',
    'completed': 'info',
    'cancelled': 'danger'
  }
  return statusMap[status] || 'info'
}

// 获取考试状态文本
const getExamStatusText = (status: string): string => {
  const statusMap: Record<string, string> = {
    'upcoming': '即将开始',
    'ongoing': '进行中',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return statusMap[status] || status
}

// 页面跳转
const navigateTo = (path: string) => {
  router.push(path)
}

// 查看考试详情
const viewExamDetail = (examId: number) => {
  router.push(`/admin/exams/${examId}`)
}

// 监听图表时间范围变化
watch(examChartTimeRange, (newValue) => {
  // 根据选择的时间范围更新图表数据
  if (newValue === 'week') {
    examChartOption.xAxis.data = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    examChartOption.series[0].data = [2, 3, 4, 3, 5, 2, 1]
    examChartOption.series[1].data = [25, 30, 35, 28, 32, 20, 15]
    examChartOption.series[2].data = [20, 25, 30, 22, 28, 18, 12]
  } else if (newValue === 'month') {
    examChartOption.xAxis.data = Array.from({ length: 30 }, (_, i) => `${i + 1}日`)
    examChartOption.series[0].data = Array.from({ length: 30 }, () => Math.floor(Math.random() * 5) + 1)
    examChartOption.series[1].data = Array.from({ length: 30 }, () => Math.floor(Math.random() * 50) + 10)
    examChartOption.series[2].data = Array.from({ length: 30 }, () => Math.floor(Math.random() * 40) + 8)
  } else if (newValue === 'year') {
    examChartOption.xAxis.data = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
    examChartOption.series[0].data = [10, 12, 15, 14, 16, 18, 20, 22, 18, 16, 14, 12]
    examChartOption.series[1].data = [120, 132, 145, 160, 168, 180, 190, 210, 185, 170, 155, 140]
    examChartOption.series[2].data = [95, 105, 120, 130, 140, 150, 160, 175, 155, 140, 130, 115]
  }
})

// 页面加载时获取数据
onMounted(() => {
  // 这里应该调用API获取仪表板数据
  // 暂时使用模拟数据
})
</script>

<style lang="scss" scoped>
.admin-dashboard {
  padding: 20px;
  
  .stat-card {
    margin-bottom: 20px;
    display: flex;
    position: relative;
    overflow: hidden;
    
    .stat-icon {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 64px;
      height: 64px;
      border-radius: 8px;
      margin-right: 16px;
      
      .el-icon {
        font-size: 32px;
        color: #fff;
      }
      
      &.blue {
        background-color: #409EFF;
      }
      
      &.green {
        background-color: #67C23A;
      }
      
      &.orange {
        background-color: #E6A23C;
      }
      
      &.purple {
        background-color: #909399;
      }
    }
    
    .stat-info {
      flex: 1;
      
      .stat-value {
        font-size: 24px;
        font-weight: bold;
        color: #303133;
        margin-bottom: 4px;
      }
      
      .stat-label {
        font-size: 14px;
        color: #909399;
      }
    }
    
    .stat-chart {
      position: absolute;
      right: 16px;
      bottom: 16px;
      
      .trend-info {
        text-align: right;
        
        .trend-value {
          font-size: 14px;
          font-weight: bold;
          color: #67C23A;
        }
        
        .trend-label {
          font-size: 12px;
          color: #909399;
          margin-left: 4px;
        }
      }
    }
  }
  
  .chart-row {
    margin-bottom: 20px;
    
    .chart-card {
      margin-bottom: 20px;
      
      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        
        h3 {
          margin: 0;
          font-size: 16px;
          font-weight: 600;
        }
      }
      
      .chart-container {
        height: 350px;
        
        .chart {
          height: 100%;
        }
      }
    }
  }
  
  .table-row {
    .table-card {
      margin-bottom: 20px;
      
      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        
        h3 {
          margin: 0;
          font-size: 16px;
          font-weight: 600;
        }
      }
    }
  }
}
</style>