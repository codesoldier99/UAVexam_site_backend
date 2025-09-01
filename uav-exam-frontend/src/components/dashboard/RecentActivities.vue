<template>
  <div class="recent-activities">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>最近活动</span>
          <el-button size="small" @click="refreshActivities">刷新</el-button>
        </div>
      </template>
      
      <div class="activities-list" v-if="activities.length">
        <div 
          class="activity-item" 
          v-for="activity in activities" 
          :key="activity.id"
        >
          <div class="activity-icon">
            <el-icon :class="getActivityIconClass(activity.type)">
              <component :is="getActivityIcon(activity.type)" />
            </el-icon>
          </div>
          <div class="activity-content">
            <div class="activity-description">{{ activity.description }}</div>
            <div class="activity-meta">
              <span class="activity-user">{{ activity.user }}</span>
              <span class="activity-location" v-if="activity.venue">
                <el-icon><Location /></el-icon>
                {{ activity.venue }}
              </span>
              <span class="activity-product" v-if="activity.exam_product">
                <el-icon><Document /></el-icon>
                {{ activity.exam_product }}
              </span>
            </div>
          </div>
          <div class="activity-time">
            <div class="time-text">{{ formatTime(activity.timestamp) }}</div>
            <el-tag 
              :type="getStatusType(activity.status)" 
              size="small"
            >
              {{ getStatusText(activity.status) }}
            </el-tag>
          </div>
        </div>
      </div>
      
      <el-empty 
        v-else 
        description="暂无活动记录" 
        :image-size="100"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { 
  CircleCheck, 
  UserFilled, 
  Calendar, 
  Clock, 
  Location, 
  Document,
  Warning,
  InfoFilled
} from '@element-plus/icons-vue'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/zh-cn'

dayjs.extend(relativeTime)
dayjs.locale('zh-cn')

interface ActivityLog {
  id: number
  type: string
  description: string
  user: string
  venue?: string
  exam_product?: string
  timestamp: string
  status: string
}

interface Props {
  activities: ActivityLog[]
}

const props = defineProps<Props>()
const emit = defineEmits<{
  refresh: []
}>()

// 获取活动图标
const getActivityIcon = (type: string) => {
  const iconMap: Record<string, any> = {
    'checkin': CircleCheck,
    'registration': UserFilled,
    'exam': Calendar,
    'schedule': Clock,
    'default': InfoFilled
  }
  return iconMap[type] || iconMap.default
}

// 获取活动图标样式类
const getActivityIconClass = (type: string) => {
  const classMap: Record<string, string> = {
    'checkin': 'icon-success',
    'registration': 'icon-primary',
    'exam': 'icon-warning',
    'schedule': 'icon-info',
    'default': 'icon-default'
  }
  return classMap[type] || classMap.default
}

// 获取状态类型
const getStatusType = (status: string) => {
  const typeMap: Record<string, string> = {
    'success': 'success',
    'pending': 'warning',
    'failed': 'danger',
    'cancelled': 'info'
  }
  return typeMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status: string) => {
  const textMap: Record<string, string> = {
    'success': '成功',
    'pending': '待处理',
    'failed': '失败',
    'cancelled': '已取消'
  }
  return textMap[status] || status
}

// 格式化时间
const formatTime = (timestamp: string) => {
  return dayjs(timestamp).fromNow()
}

const refreshActivities = () => {
  emit('refresh')
}
</script>

<style lang="scss" scoped>
.recent-activities {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 600;
  }
}

.activities-list {
  max-height: 400px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
  
  &:last-child {
    border-bottom: none;
  }
}

.activity-icon {
  margin-right: 12px;
  margin-top: 2px;
  
  .el-icon {
    font-size: 20px;
    
    &.icon-success {
      color: #67C23A;
    }
    
    &.icon-primary {
      color: #409EFF;
    }
    
    &.icon-warning {
      color: #E6A23C;
    }
    
    &.icon-info {
      color: #909399;
    }
    
    &.icon-default {
      color: #C0C4CC;
    }
  }
}

.activity-content {
  flex: 1;
  margin-right: 12px;
}

.activity-description {
  font-size: 14px;
  color: #303133;
  margin-bottom: 4px;
  line-height: 1.4;
}

.activity-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 12px;
  color: #909399;
  
  .activity-user {
    font-weight: 500;
  }
  
  .activity-location,
  .activity-product {
    display: flex;
    align-items: center;
    gap: 2px;
  }
}

.activity-time {
  text-align: right;
  min-width: 80px;
}

.time-text {
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}
</style>