<template>
  <div class="dashboard">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>仪表板</h1>
      <div class="header-actions">
        <el-button 
          type="primary" 
          :icon="Refresh" 
          @click="refreshAllData"
          :loading="dashboardStore.loading"
        >
          刷新数据
        </el-button>
        <span class="last-updated" v-if="dashboardStore.lastUpdated">
          最后更新: {{ formatUpdateTime(dashboardStore.lastUpdated) }}
        </span>
      </div>
    </div>

    <!-- 概览卡片 -->
    <OverviewCards :data="dashboardStore.overviewData" />

    <!-- 统计图表 -->
    <StatisticsCharts 
      :data="dashboardStore.statisticsData" 
      @refresh="refreshStatistics"
    />

    <!-- 最近活动 -->
    <div style="margin-top: 20px;">
      <RecentActivities 
        :activities="dashboardStore.recentActivities" 
        @refresh="refreshActivities"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import { useDashboardStore } from '@/stores/dashboard'
import OverviewCards from '@/components/dashboard/OverviewCards.vue'
import StatisticsCharts from '@/components/dashboard/StatisticsCharts.vue'
import RecentActivities from '@/components/dashboard/RecentActivities.vue'
import dayjs from 'dayjs'

const dashboardStore = useDashboardStore()

// 刷新所有数据
const refreshAllData = async () => {
  try {
    await dashboardStore.refreshAll()
    ElMessage.success('数据刷新成功')
  } catch (error) {
    console.error('刷新数据失败:', error)
    ElMessage.error('数据刷新失败')
  }
}

// 刷新统计数据
const refreshStatistics = async () => {
  try {
    await dashboardStore.fetchStatistics()
    ElMessage.success('统计数据刷新成功')
  } catch (error) {
    console.error('刷新统计数据失败:', error)
    ElMessage.error('统计数据刷新失败')
  }
}

// 刷新活动日志
const refreshActivities = async () => {
  try {
    await dashboardStore.fetchRecentActivities()
    ElMessage.success('活动日志刷新成功')
  } catch (error) {
    console.error('刷新活动日志失败:', error)
    ElMessage.error('活动日志刷新失败')
  }
}

// 格式化更新时间
const formatUpdateTime = (timestamp: string) => {
  return dayjs(timestamp).format('YYYY-MM-DD HH:mm:ss')
}

// 页面加载时获取数据
onMounted(() => {
  refreshAllData()
})
</script>

<style lang="scss" scoped>
.dashboard {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  
  h1 {
    margin: 0;
    color: #303133;
  }
  
  .header-actions {
    display: flex;
    align-items: center;
    gap: 16px;
    
    .last-updated {
      font-size: 12px;
      color: #909399;
    }
  }
}
</style>