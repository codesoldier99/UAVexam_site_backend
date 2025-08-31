<template>
  <div class="monitoring-page">
    <div class="page-header">
      <h2>系统监控</h2>
      <p>实时监控系统运行状态</p>
    </div>
    
    <div class="stats-section">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon size="32" color="#409eff"><Monitor /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-number">{{ systemStats.cpuUsage }}</div>
                <div class="stat-label">CPU使用率</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon size="32" color="#67c23a"><DataBoard /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-number">{{ systemStats.memoryUsage }}</div>
                <div class="stat-label">内存使用率</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon size="32" color="#e6a23c"><FolderOpened /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-number">{{ systemStats.diskUsage }}</div>
                <div class="stat-label">磁盘使用率</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon size="32" color="#f56c6c"><Connection /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-number">{{ systemStats.networkUsage }}</div>
                <div class="stat-label">网络使用率</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <div class="content-card">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>实时日志</span>
            <div class="header-actions">
              <el-button size="small" @click="handleRefreshLogs">刷新</el-button>
              <el-button size="small" @click="handleClearLogs">清空</el-button>
            </div>
          </div>
        </template>
        
        <div class="log-container">
          <div v-for="log in systemLogs" :key="log.id" class="log-item" :class="getLogClass(log.level)">
            <span class="log-time">{{ log.timestamp }}</span>
            <span class="log-level">{{ log.level }}</span>
            <span class="log-message">{{ log.message }}</span>
          </div>
        </div>
      </el-card>
    </div>
    
    <div class="content-card">
      <el-card>
        <template #header>
          <span>在线用户</span>
        </template>
        
        <el-table :data="onlineUsers" style="width: 100%">
          <el-table-column prop="username" label="用户名" />
          <el-table-column prop="role" label="角色" />
          <el-table-column prop="ip" label="IP地址" />
          <el-table-column prop="location" label="地理位置" />
          <el-table-column prop="loginTime" label="登录时间" />
          <el-table-column prop="lastActivity" label="最后活动" />
          <el-table-column label="操作" width="100">
            <template #default="{ row }">
              <el-button 
                size="small" 
                type="danger" 
                @click="handleKickUser(row)"
              >
                踢出
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Monitor, DataBoard, FolderOpened, Connection } from '@element-plus/icons-vue'

const systemStats = ref({
  cpuUsage: '45%',
  memoryUsage: '62%',
  diskUsage: '38%',
  networkUsage: '12%'
})

const systemLogs = ref([
  {
    id: 1,
    timestamp: '2024-01-15 16:30:15',
    level: 'INFO',
    message: '用户 admin 登录系统'
  },
  {
    id: 2,
    timestamp: '2024-01-15 16:29:45',
    level: 'WARN',
    message: '数据库连接池使用率超过80%'
  },
  {
    id: 3,
    timestamp: '2024-01-15 16:28:30',
    level: 'ERROR',
    message: 'API请求失败: /api/users/list'
  },
  {
    id: 4,
    timestamp: '2024-01-15 16:27:20',
    level: 'INFO',
    message: '系统定时任务执行完成'
  }
])

const onlineUsers = ref([
  {
    id: 1,
    username: 'admin',
    role: '超级管理员',
    ip: '192.168.1.100',
    location: '北京市',
    loginTime: '2024-01-15 08:30:00',
    lastActivity: '2024-01-15 16:30:00'
  },
  {
    id: 2,
    username: 'examiner01',
    role: '考官',
    ip: '192.168.1.101',
    location: '上海市',
    loginTime: '2024-01-15 09:15:00',
    lastActivity: '2024-01-15 16:25:00'
  }
])

let refreshTimer: NodeJS.Timeout | null = null

const getLogClass = (level: string) => {
  const classes: Record<string, string> = {
    INFO: 'log-info',
    WARN: 'log-warn',
    ERROR: 'log-error'
  }
  return classes[level] || 'log-info'
}

const handleRefreshLogs = () => {
  ElMessage.success('日志已刷新')
  // 这里应该调用API刷新日志
}

const handleClearLogs = () => {
  systemLogs.value = []
  ElMessage.success('日志已清空')
}

const handleKickUser = (user: any) => {
  ElMessage.success(`用户 ${user.username} 已被踢出`)
  // 这里应该调用API踢出用户
}

const refreshStats = () => {
  // 模拟实时数据更新
  systemStats.value = {
    cpuUsage: Math.floor(Math.random() * 100) + '%',
    memoryUsage: Math.floor(Math.random() * 100) + '%',
    diskUsage: Math.floor(Math.random() * 100) + '%',
    networkUsage: Math.floor(Math.random() * 100) + '%'
  }
}

onMounted(() => {
  // 每5秒刷新一次统计数据
  refreshTimer = setInterval(refreshStats, 5000)
})

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})
</script>

<style lang="scss" scoped>
.monitoring-page {
  .page-header {
    margin-bottom: 20px;
    
    h2 {
      margin: 0 0 8px 0;
      color: #303133;
    }
    
    p {
      margin: 0;
      color: #909399;
    }
  }
  
  .stats-section {
    margin-bottom: 20px;
    
    .stat-card {
      .stat-content {
        display: flex;
        align-items: center;
        padding: 10px 0;
        
        .stat-icon {
          margin-right: 15px;
        }
        
        .stat-info {
          .stat-number {
            font-size: 24px;
            font-weight: bold;
            color: #303133;
            margin-bottom: 5px;
          }
          
          .stat-label {
            color: #606266;
            font-size: 14px;
          }
        }
      }
    }
  }
  
  .content-card {
    margin-bottom: 20px;
    
    &:last-child {
      margin-bottom: 0;
    }
    
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      .header-actions {
        display: flex;
        gap: 10px;
      }
    }
    
    .log-container {
      max-height: 400px;
      overflow-y: auto;
      
      .log-item {
        display: flex;
        padding: 8px 0;
        border-bottom: 1px solid #f0f0f0;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        
        &:last-child {
          border-bottom: none;
        }
        
        .log-time {
          width: 150px;
          color: #909399;
        }
        
        .log-level {
          width: 60px;
          font-weight: bold;
        }
        
        .log-message {
          flex: 1;
        }
        
        &.log-info .log-level {
          color: #409eff;
        }
        
        &.log-warn .log-level {
          color: #e6a23c;
        }
        
        &.log-error .log-level {
          color: #f56c6c;
        }
      }
    }
  }
}
</style>