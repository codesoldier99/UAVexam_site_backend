<template>
  <div class="dashboard-container">
    <el-card class="welcome-card">
      <template #header>
        <div class="card-header">
          <h3>欢迎使用无人机考试管理系统</h3>
        </div>
      </template>
      <div class="welcome-content">
        <p>您已成功登录系统，请从左侧菜单选择功能模块。</p>
        <p v-if="userStore.userInfo">
          当前用户: {{ userStore.userInfo.real_name }} ({{ getRoleName(userStore.userInfo.role) }})
        </p>
      </div>
    </el-card>

    <div class="dashboard-stats">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="stat-card">
            <div class="stat-icon">
              <el-icon><User /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ dashboardData.total_candidates || 0 }}</div>
              <div class="stat-label">考生总数</div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="stat-card">
            <div class="stat-icon">
              <el-icon><OfficeBuilding /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ dashboardData.total_venues || 0 }}</div>
              <div class="stat-label">考场总数</div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="stat-card">
            <div class="stat-icon">
              <el-icon><Calendar /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ dashboardData.today_exams || 0 }}</div>
              <div class="stat-label">今日考试</div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="stat-card">
            <div class="stat-icon">
              <el-icon><Check /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ dashboardData.completed_exams || 0 }}</div>
              <div class="stat-label">已完成考试</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <!-- 管理员和操作员可见的内容 -->
    <permission-guard :roles="['SUPER_ADMIN', 'ADMIN', 'OPERATOR']">
      <el-card class="mt-20">
        <template #header>
          <div class="card-header">
            <h3>管理员功能</h3>
          </div>
        </template>
        <div class="admin-functions">
          <el-row :gutter="20">
            <el-col :xs="24" :sm="12" :md="8" :lg="6">
              <el-card shadow="hover" class="function-card" @click="navigateTo('/admin/candidates')">
                <el-icon><Avatar /></el-icon>
                <span>考生管理</span>
              </el-card>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="8" :lg="6">
              <el-card shadow="hover" class="function-card" @click="navigateTo('/admin/exams')">
                <el-icon><Document /></el-icon>
                <span>考试管理</span>
              </el-card>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="8" :lg="6">
              <el-card shadow="hover" class="function-card" @click="navigateTo('/admin/schedules')">
                <el-icon><Calendar /></el-icon>
                <span>日程管理</span>
              </el-card>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="8" :lg="6" v-permission="['SUPER_ADMIN', 'ADMIN']">
              <el-card shadow="hover" class="function-card" @click="navigateTo('/admin/venues')">
                <el-icon><OfficeBuilding /></el-icon>
                <span>考场管理</span>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </el-card>
    </permission-guard>
    
    <!-- 考生可见的内容 -->
    <permission-guard :roles="['CANDIDATE']">
      <el-card class="mt-20">
        <template #header>
          <div class="card-header">
            <h3>考生功能</h3>
          </div>
        </template>
        <div class="candidate-functions">
          <el-row :gutter="20">
            <el-col :xs="24" :sm="12" :md="8" :lg="6">
              <el-card shadow="hover" class="function-card" @click="navigateTo('/candidate/exams')">
                <el-icon><Document /></el-icon>
                <span>我的考试</span>
              </el-card>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="8" :lg="6">
              <el-card shadow="hover" class="function-card" @click="navigateTo('/candidate/results')">
                <el-icon><DataAnalysis /></el-icon>
                <span>考试成绩</span>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </el-card>
    </permission-guard>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { User, OfficeBuilding, Calendar, Check, Avatar, Document, DataAnalysis } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import type { UserRole } from '@/types/user'

const router = useRouter()
const userStore = useUserStore()

interface DashboardData {
  total_candidates: number
  total_venues: number
  today_exams: number
  completed_exams: number
  pending_exams: number
  system_status: string
}

const dashboardData = ref<DashboardData>({
  total_candidates: 0,
  total_venues: 0,
  today_exams: 0,
  completed_exams: 0,
  pending_exams: 0,
  system_status: 'normal'
})

const getRoleName = (role: UserRole): string => {
  const roleMap: Record<string, string> = {
    'SUPER_ADMIN': '超级管理员',
    'ADMIN': '管理员',
    'OPERATOR': '操作员',
    'CANDIDATE': '考生'
  }
  return roleMap[role] || role
}

const navigateTo = (path: string) => {
  router.push(path)
}

onMounted(async () => {
  // 这里应该调用API获取仪表板数据
  // 暂时使用模拟数据
  dashboardData.value = {
    total_candidates: 1250,
    total_venues: 15,
    today_exams: 45,
    completed_exams: 38,
    pending_exams: 7,
    system_status: 'normal'
  }
})
</script>

<style lang="scss" scoped>
.dashboard-container {
  padding: 20px;
}

.welcome-card {
  margin-bottom: 20px;
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .welcome-content {
    line-height: 1.6;
  }
}

.dashboard-stats {
  margin-bottom: 30px;
  
  .stat-card {
    display: flex;
    align-items: center;
    padding: 20px;
    margin-bottom: 20px;
    
    .stat-icon {
      font-size: 48px;
      color: var(--primary-color);
      margin-right: 20px;
    }
    
    .stat-info {
      .stat-value {
        font-size: 28px;
        font-weight: bold;
        color: var(--text-color-primary);
      }
      
      .stat-label {
        font-size: 14px;
        color: var(--text-color-secondary);
        margin-top: 5px;
      }
    }
  }
}

.function-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  margin-bottom: 20px;
  cursor: pointer;
  transition: all 0.3s;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
  
  .el-icon {
    font-size: 32px;
    color: var(--primary-color);
    margin-bottom: 10px;
  }
  
  span {
    font-size: 16px;
  }
}
</style>