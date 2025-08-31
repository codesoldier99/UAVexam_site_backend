<template>
  <div class="exam-schedule page-container">
    <div class="page-header">
      <h2 class="page-title">考试日程</h2>
      <p class="page-description">查看和管理所有考试日程安排</p>
    </div>
    
    <!-- 日历视图 -->
    <el-card>
      <template #header>
        <div class="card-header">
          <div class="calendar-title">
            <el-button-group>
              <el-button @click="changeView('month')" :type="calendarView === 'month' ? 'primary' : ''">月视图</el-button>
              <el-button @click="changeView('week')" :type="calendarView === 'week' ? 'primary' : ''">周视图</el-button>
              <el-button @click="changeView('day')" :type="calendarView === 'day' ? 'primary' : ''">日视图</el-button>
            </el-button-group>
          </div>
          
          <div class="calendar-nav">
            <el-button @click="prev">
              <el-icon><ArrowLeft /></el-icon>
            </el-button>
            <span class="current-date">{{ currentDateTitle }}</span>
            <el-button @click="next">
              <el-icon><ArrowRight /></el-icon>
            </el-button>
            <el-button @click="today">今天</el-button>
          </div>
        </div>
      </template>
      
      <div class="calendar-container">
        <!-- 月视图 -->
        <div v-if="calendarView === 'month'" class="month-view">
          <!-- 星期标题 -->
          <div class="week-header">
            <div v-for="day in weekDays" :key="day" class="week-day">{{ day }}</div>
          </div>
          
          <!-- 日历单元格 -->
          <div class="month-grid">
            <div
              v-for="(day, index) in monthDays"
              :key="index"
              class="day-cell"
              :class="{
                'other-month': day.otherMonth,
                'today': day.isToday,
                'has-events': day.events.length > 0
              }"
            >
              <div class="day-header">
                <span class="day-number">{{ day.date.getDate() }}</span>
              </div>
              
              <div class="day-events">
                <div
                  v-for="event in day.events.slice(0, 3)"
                  :key="event.id"
                  class="event-item"
                  :class="getEventClass(event)"
                  @click="showEventDetail(event)"
                >
                  {{ event.title }}
                </div>
                
                <div v-if="day.events.length > 3" class="more-events" @click="showMoreEvents(day)">
                  还有 {{ day.events.length - 3 }} 个考试
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 周视图 -->
        <div v-else-if="calendarView === 'week'" class="week-view">
          <!-- 星期标题 -->
          <div class="week-header">
            <div class="time-column"></div>
            <div v-for="day in weekViewDays" :key="day.date" class="week-day">
              <div class="day-name">{{ day.dayName }}</div>
              <div class="day-number" :class="{ 'today': day.isToday }">{{ day.dayNumber }}</div>
            </div>
          </div>
          
          <!-- 时间格子 -->
          <div class="week-grid">
            <div class="time-column">
              <div v-for="hour in 24" :key="hour" class="time-cell">
                {{ hour - 1 }}:00
              </div>
            </div>
            
            <div v-for="day in weekViewDays" :key="day.date" class="day-column">
              <div
                v-for="hour in 24"
                :key="hour"
                class="hour-cell"
                :class="{ 'current-hour': day.isToday && currentHour === hour - 1 }"
              >
                <!-- 事件 -->
                <template v-for="event in getEventsForHour(day.date, hour - 1)" :key="event.id">
                  <div
                    class="week-event-item"
                    :class="getEventClass(event)"
                    :style="{
                      top: `${getEventTop(event, hour - 1)}%`,
                      height: `${getEventHeight(event)}%`
                    }"
                    @click="showEventDetail(event)"
                  >
                    {{ event.title }}
                    <div class="event-time">{{ formatEventTime(event) }}</div>
                  </div>
                </template>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 日视图 -->
        <div v-else class="day-view">
          <div class="day-header">
            <div class="day-title" :class="{ 'today': isToday(currentDate) }">
              {{ formatDate(currentDate, 'YYYY年MM月DD日') }}
            </div>
          </div>
          
          <div class="day-grid">
            <div class="time-column">
              <div v-for="hour in 24" :key="hour" class="time-cell">
                {{ hour - 1 }}:00
              </div>
            </div>
            
            <div class="events-column">
              <div
                v-for="hour in 24"
                :key="hour"
                class="hour-cell"
                :class="{ 'current-hour': isToday(currentDate) && currentHour === hour - 1 }"
              >
                <!-- 事件 -->
                <template v-for="event in getEventsForHour(currentDate, hour - 1)" :key="event.id">
                  <div
                    class="day-event-item"
                    :class="getEventClass(event)"
                    :style="{
                      top: `${getEventTop(event, hour - 1)}%`,
                      height: `${getEventHeight(event)}%`
                    }"
                    @click="showEventDetail(event)"
                  >
                    <div class="event-title">{{ event.title }}</div>
                    <div class="event-time">{{ formatEventTime(event) }}</div>
                    <div class="event-venue">{{ event.venue }}</div>
                  </div>
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
  
  <!-- 事件详情对话框 -->
  <el-dialog
    v-model="eventDetailVisible"
    :title="selectedEvent?.title || '考试详情'"
    width="500px"
  >
    <div v-if="selectedEvent" class="event-detail">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="考试名称">{{ selectedEvent.title }}</el-descriptions-item>
        <el-descriptions-item label="考场">{{ selectedEvent.venue }}</el-descriptions-item>
        <el-descriptions-item label="开始时间">{{ formatDate(selectedEvent.start, 'YYYY-MM-DD HH:mm') }}</el-descriptions-item>
        <el-descriptions-item label="结束时间">{{ formatDate(selectedEvent.end, 'YYYY-MM-DD HH:mm') }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getEventStatusType(selectedEvent.status)">
            {{ getEventStatusText(selectedEvent.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="考生人数">{{ selectedEvent.candidatesCount }}</el-descriptions-item>
        <el-descriptions-item label="考官">{{ selectedEvent.examiners.join(', ') }}</el-descriptions-item>
      </el-descriptions>
      
      <div class="dialog-footer">
        <el-button @click="eventDetailVisible = false">关闭</el-button>
        <el-button type="primary" @click="viewExamDetail(selectedEvent.examId)">查看详情</el-button>
      </div>
    </div>
  </el-dialog>
  
  <!-- 更多事件对话框 -->
  <el-dialog
    v-model="moreEventsVisible"
    :title="`${selectedDay ? formatDate(selectedDay.date, 'YYYY年MM月DD日') : ''} 的考试`"
    width="500px"
  >
    <div v-if="selectedDay" class="more-events-list">
      <el-table :data="selectedDay.events" style="width: 100%">
        <el-table-column prop="title" label="考试名称" min-width="150" />
        <el-table-column prop="venue" label="考场" width="120" />
        <el-table-column label="时间" width="180">
          <template #default="scope">
            {{ formatEventTime(scope.row) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="80" fixed="right">
          <template #default="scope">
            <el-button link type="primary" @click="showEventDetail(scope.row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </el-dialog>
</template>