<template>
  <div class="exam-info-page">
    <div class="page-header">
      <h2>考试信息</h2>
      <p>查看我的考试安排和相关信息</p>
    </div>
    
    <div class="content-card">
      <el-card>
        <template #header>
          <span>我的考试安排</span>
        </template>
        
        <div class="exam-list">
          <div v-for="exam in examList" :key="exam.id" class="exam-item">
            <el-card class="exam-card">
              <div class="exam-header">
                <h3>{{ exam.name }}</h3>
                <el-tag :type="getExamStatusType(exam.status)">
                  {{ getExamStatusText(exam.status) }}
                </el-tag>
              </div>
              
              <div class="exam-details">
                <el-row :gutter="20">
                  <el-col :span="12">
                    <div class="detail-item">
                      <span class="label">考试类型：</span>
                      <span class="value">{{ exam.type }}</span>
                    </div>
                    <div class="detail-item">
                      <span class="label">考试日期：</span>
                      <span class="value">{{ exam.date }}</span>
                    </div>
                    <div class="detail-item">
                      <span class="label">考试时间：</span>
                      <span class="value">{{ exam.time }}</span>
                    </div>
                  </el-col>
                  <el-col :span="12">
                    <div class="detail-item">
                      <span class="label">考试地点：</span>
                      <span class="value">{{ exam.venue }}</span>
                    </div>
                    <div class="detail-item">
                      <span class="label">考试地址：</span>
                      <span class="value">{{ exam.address }}</span>
                    </div>
                    <div class="detail-item">
                      <span class="label">联系电话：</span>
                      <span class="value">{{ exam.contact }}</span>
                    </div>
                  </el-col>
                </el-row>
              </div>
              
              <div class="exam-actions">
                <el-button 
                  v-if="exam.status === 'upcoming'" 
                  type="primary"
                  @click="handleViewDetails(exam)"
                >
                  查看详情
                </el-button>
                <el-button 
                  v-if="exam.status === 'completed'" 
                  type="success"
                  @click="handleViewResult(exam)"
                >
                  查看成绩
                </el-button>
              </div>
            </el-card>
          </div>
        </div>
        
        <div v-if="examList.length === 0" class="empty-state">
          <el-empty description="暂无考试安排" />
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const examList = ref([
  {
    id: 1,
    name: '2024年第一期无人机驾驶员考试',
    type: '无人机驾驶员',
    date: '2024-02-15',
    time: '09:00-12:00',
    venue: '北京考试中心',
    address: '北京市朝阳区建国路88号',
    contact: '010-12345678',
    status: 'upcoming'
  },
  {
    id: 2,
    name: '2024年第二期无人机教员考试',
    type: '无人机教员',
    date: '2024-01-20',
    time: '14:00-17:00',
    venue: '上海考试中心',
    address: '上海市浦东新区世纪大道100号',
    contact: '021-87654321',
    status: 'completed'
  }
])

const getExamStatusType = (status: string) => {
  const types: Record<string, string> = {
    upcoming: 'warning',
    ongoing: 'primary',
    completed: 'success',
    cancelled: 'danger'
  }
  return types[status] || 'info'
}

const getExamStatusText = (status: string) => {
  const texts: Record<string, string> = {
    upcoming: '即将开始',
    ongoing: '进行中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return texts[status] || '未知'
}

const handleViewDetails = (exam: any) => {
  ElMessage.info(`查看考试详情: ${exam.name}`)
}

const handleViewResult = (exam: any) => {
  ElMessage.info(`查看考试成绩: ${exam.name}`)
}

onMounted(() => {
  // 加载考试信息数据
})
</script>

<style lang="scss" scoped>
.exam-info-page {
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
  
  .exam-list {
    .exam-item {
      margin-bottom: 20px;
      
      &:last-child {
        margin-bottom: 0;
      }
      
      .exam-card {
        .exam-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 20px;
          
          h3 {
            margin: 0;
            color: #303133;
          }
        }
        
        .exam-details {
          margin-bottom: 20px;
          
          .detail-item {
            display: flex;
            margin-bottom: 10px;
            
            .label {
              width: 80px;
              color: #606266;
              font-weight: 500;
            }
            
            .value {
              color: #303133;
            }
          }
        }
        
        .exam-actions {
          text-align: right;
        }
      }
    }
  }
  
  .empty-state {
    text-align: center;
    padding: 40px 0;
  }
}
</style>