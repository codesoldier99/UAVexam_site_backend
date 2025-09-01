<template>
  <div class="overview-cards">
    <el-row :gutter="20">
      <el-col :xs="24" :sm="12" :md="6" v-for="card in cards" :key="card.key">
        <el-card class="overview-card" shadow="hover">
          <div class="card-content">
            <div class="card-icon" :style="{ backgroundColor: card.color }">
              <el-icon :size="24">
                <component :is="card.icon" />
              </el-icon>
            </div>
            <div class="card-info">
              <div class="card-title">{{ card.title }}</div>
              <div class="card-value">{{ formatValue(card.value) }}</div>
              <div class="card-trend" v-if="card.trend">
                <el-icon :class="card.trend > 0 ? 'trend-up' : 'trend-down'">
                  <ArrowUp v-if="card.trend > 0" />
                  <ArrowDown v-else />
                </el-icon>
                <span>{{ Math.abs(card.trend) }}%</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { User, Location, Calendar, Clock, CircleCheck, Clock as PendingCircle, ArrowUp, ArrowDown } from '@element-plus/icons-vue'

interface Props {
  data: {
    total_candidates?: number
    total_venues?: number
    total_exams?: number
    active_schedules?: number
    today_checkins?: number
    pending_registrations?: number
  } | null
}

const props = defineProps<Props>()

import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const cards = computed(() => {
  const userRole = userStore.userInfo?.role?.toUpperCase()
  
  // 根据用户角色返回不同的卡片配置
  const baseCards = [
    {
      key: 'candidates',
      title: getRoleBasedTitle('candidates', userRole),
      value: props.data?.total_candidates || 0,
      icon: User,
      color: '#409EFF',
      trend: 12.5
    },
    {
      key: 'venues',
      title: getRoleBasedTitle('venues', userRole),
      value: props.data?.total_venues || 0,
      icon: Location,
      color: '#67C23A',
      trend: 0
    },
    {
      key: 'exams',
      title: getRoleBasedTitle('exams', userRole),
      value: props.data?.total_exams || 0,
      icon: Calendar,
      color: '#E6A23C',
      trend: 8.3
    },
    {
      key: 'schedules',
      title: getRoleBasedTitle('schedules', userRole),
      value: props.data?.active_schedules || 0,
      icon: Clock,
      color: '#F56C6C',
      trend: -2.1
    },
    {
      key: 'checkins',
      title: getRoleBasedTitle('checkins', userRole),
      value: props.data?.today_checkins || 0,
      icon: CircleCheck,
      color: '#909399',
      trend: 15.7
    },
    {
      key: 'pending',
      title: getRoleBasedTitle('pending', userRole),
      value: props.data?.pending_registrations || 0,
      icon: PendingCircle,
      color: '#B88230',
      trend: -5.2
    }
  ]
  
  // 根据角色过滤显示的卡片
  return filterCardsByRole(baseCards, userRole)
})

// 根据角色获取卡片标题
const getRoleBasedTitle = (cardType: string, role?: string) => {
  const titleMap: Record<string, Record<string, string>> = {
    'candidates': {
      'SUPER_ADMIN': '总考生数',
      'ADMIN': '机构考生数',
      'OPERATOR': '机构考生数',
      'EXAMINER': '我的考生数',
      'CANDIDATE': '我的状态',
      'default': '考生数'
    },
    'venues': {
      'SUPER_ADMIN': '总考场数',
      'ADMIN': '可用考场',
      'OPERATOR': '可用考场',
      'EXAMINER': '分配考场',
      'CANDIDATE': '考试考场',
      'default': '考场数'
    },
    'exams': {
      'SUPER_ADMIN': '总考试场次',
      'ADMIN': '机构考试',
      'OPERATOR': '机构考试',
      'EXAMINER': '我的考试',
      'CANDIDATE': '我的考试',
      'default': '考试场次'
    },
    'schedules': {
      'SUPER_ADMIN': '活跃排期',
      'ADMIN': '机构排期',
      'OPERATOR': '机构排期',
      'EXAMINER': '我的排期',
      'CANDIDATE': '我的排期',
      'default': '排期数'
    },
    'checkins': {
      'SUPER_ADMIN': '今日签到',
      'ADMIN': '今日签到',
      'OPERATOR': '今日签到',
      'EXAMINER': '我的签到',
      'CANDIDATE': '签到状态',
      'default': '签到数'
    },
    'pending': {
      'SUPER_ADMIN': '待处理报名',
      'ADMIN': '待处理报名',
      'OPERATOR': '待处理报名',
      'EXAMINER': '待分配考生',
      'CANDIDATE': '待确认事项',
      'default': '待处理'
    }
  }
  
  return titleMap[cardType]?.[role || 'default'] || titleMap[cardType]?.['default'] || '数据'
}

// 根据角色过滤卡片
const filterCardsByRole = (cards: any[], role?: string) => {
  switch (role) {
    case 'CANDIDATE':
      // 考生只看到与自己相关的卡片
      return cards.filter(card => 
        ['candidates', 'exams', 'schedules', 'checkins'].includes(card.key)
      )
    case 'EXAMINER':
      // 考官看到分配给自己的数据
      return cards.filter(card => 
        ['candidates', 'venues', 'exams', 'schedules', 'checkins'].includes(card.key)
      )
    case 'OPERATOR':
      // 操作员看到机构相关数据
      return cards.filter(card => 
        ['candidates', 'venues', 'exams', 'schedules', 'checkins', 'pending'].includes(card.key)
      )
    default:
      // 管理员和超级管理员看到所有卡片
      return cards
  }
}

const formatValue = (value: number): string => {
  if (value >= 1000) {
    return (value / 1000).toFixed(1) + 'K'
  }
  return value.toString()
}
</script>

<style lang="scss" scoped>
.overview-cards {
  margin-bottom: 20px;
}

.overview-card {
  height: 120px;
  
  :deep(.el-card__body) {
    padding: 20px;
    height: 100%;
  }
}

.card-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.card-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  color: white;
}

.card-info {
  flex: 1;
}

.card-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.card-value {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.card-trend {
  display: flex;
  align-items: center;
  font-size: 12px;
  
  .trend-up {
    color: #67C23A;
  }
  
  .trend-down {
    color: #F56C6C;
  }
  
  span {
    margin-left: 4px;
  }
}
</style>