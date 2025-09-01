<template>
  <div class="statistics-charts">
    <el-row :gutter="20">
      <!-- 考试通过率饼图 -->
      <el-col :xs="24" :md="12">
        <el-card class="chart-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>考试通过率</span>
              <el-tag :type="passRateType">{{ passRate }}%</el-tag>
            </div>
          </template>
          <div class="chart-container">
            <v-chart 
              class="chart" 
              :option="examPassRateOption" 
              v-if="data?.exam_statistics"
            />
            <div v-else class="no-data">暂无数据</div>
          </div>
        </el-card>
      </el-col>

      <!-- 签到统计柱状图 -->
      <el-col :xs="24" :md="12">
        <el-card class="chart-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>签到统计</span>
              <el-tag type="info">今日</el-tag>
            </div>
          </template>
          <div class="chart-container">
            <v-chart 
              class="chart" 
              :option="checkinStatsOption" 
              v-if="data?.checkin_statistics"
            />
            <div v-else class="no-data">暂无数据</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 考场利用率 -->
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card class="chart-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>考场利用率</span>
              <el-button size="small" @click="refreshData">刷新</el-button>
            </div>
          </template>
          <div class="chart-container">
            <v-chart 
              class="chart" 
              :option="venueUtilizationOption" 
              v-if="data?.venue_utilization?.length"
            />
            <div v-else class="no-data">暂无数据</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart, BarChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import VChart from 'vue-echarts'

// 注册ECharts组件
use([
  CanvasRenderer,
  PieChart,
  BarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
])

interface Props {
  data: {
    exam_statistics?: {
      total_exams: number
      passed_exams: number
      failed_exams: number
      pass_rate: number
    }
    checkin_statistics?: {
      total_checkins: number
      on_time: number
      late: number
      absent: number
    }
    venue_utilization?: Array<{
      venue_name: string
      utilization_rate: number
      total_sessions: number
      completed_sessions: number
    }>
  } | null
}

const props = defineProps<Props>()
const emit = defineEmits<{
  refresh: []
}>()

// 计算通过率
const passRate = computed(() => {
  return props.data?.exam_statistics?.pass_rate?.toFixed(1) || '0.0'
})

const passRateType = computed(() => {
  const rate = parseFloat(passRate.value)
  if (rate >= 80) return 'success'
  if (rate >= 60) return 'warning'
  return 'danger'
})

// 考试通过率饼图配置
const examPassRateOption = computed(() => {
  const stats = props.data?.exam_statistics
  if (!stats) return {}

  return {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '考试结果',
        type: 'pie',
        radius: '50%',
        data: [
          { value: stats.passed_exams, name: '通过', itemStyle: { color: '#67C23A' } },
          { value: stats.failed_exams, name: '未通过', itemStyle: { color: '#F56C6C' } }
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
})

// 签到统计柱状图配置
const checkinStatsOption = computed(() => {
  const stats = props.data?.checkin_statistics
  if (!stats) return {}

  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ['准时', '迟到', '缺席']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '人数',
        type: 'bar',
        data: [
          { value: stats.on_time, itemStyle: { color: '#67C23A' } },
          { value: stats.late, itemStyle: { color: '#E6A23C' } },
          { value: stats.absent, itemStyle: { color: '#F56C6C' } }
        ]
      }
    ]
  }
})

// 考场利用率配置
const venueUtilizationOption = computed(() => {
  const venues = props.data?.venue_utilization
  if (!venues?.length) return {}

  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: venues.map(v => v.venue_name),
      axisLabel: {
        rotate: 45
      }
    },
    yAxis: {
      type: 'value',
      max: 100,
      axisLabel: {
        formatter: '{value}%'
      }
    },
    series: [
      {
        name: '利用率',
        type: 'bar',
        data: venues.map(v => ({
          value: v.utilization_rate,
          itemStyle: {
            color: v.utilization_rate >= 80 ? '#67C23A' : 
                   v.utilization_rate >= 60 ? '#E6A23C' : '#F56C6C'
          }
        }))
      }
    ]
  }
})

const refreshData = () => {
  emit('refresh')
}
</script>

<style lang="scss" scoped>
.statistics-charts {
  .chart-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 600;
    }
  }

  .chart-container {
    height: 300px;
    display: flex;
    align-items: center;
    justify-content: center;

    .chart {
      height: 100%;
      width: 100%;
    }

    .no-data {
      color: #909399;
      font-size: 14px;
    }
  }
}
</style>