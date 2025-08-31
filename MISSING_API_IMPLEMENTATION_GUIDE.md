# 缺失API功能实现指南

## 📋 **概述**

通过组合现有的后端接口，可以在前端实现三个缺失的功能：
1. 考试日程查询
2. 二维码生成  
3. 公共看板

---

## 🎯 **1. 考试日程查询功能实现**

### **目标接口**: `GET /api/v1/wechat/candidate/schedule`

### **实现方案**: 组合多个现有接口

#### **步骤1: 获取考生信息**
```javascript
// 使用现有接口获取当前考生信息
const userInfo = await request({
  url: '/api/v1/auth/me',
  method: 'GET',
  headers: { 'Authorization': `Bearer ${token}` }
});

const candidateId = userInfo.id;
```

#### **步骤2: 获取考生的报名记录**
```javascript
// 可以通过身份证查询获取考生基本信息
const candidateInfo = await request({
  url: '/api/v1/wechat/candidate/info-by-idcard',
  method: 'GET',
  params: { id_card: userInfo.id_card }
});
```

#### **步骤3: 获取签到历史来推断考试安排**
```javascript
// 使用签到历史接口获取相关考试信息
const checkinHistory = await request({
  url: '/api/v1/wechat/candidate/checkin-history',
  method: 'GET',
  headers: { 'Authorization': `Bearer ${token}` }
});
```

#### **前端组合实现**:
```javascript
// 前端实现考试日程查询
async function getCandidateSchedule() {
  try {
    // 1. 获取用户信息
    const userInfo = await getUserInfo();
    
    // 2. 获取考生详细信息
    const candidateInfo = await getCandidateByIdCard(userInfo.id_card);
    
    // 3. 获取签到历史（包含考试安排信息）
    const checkinHistory = await getCheckinHistory();
    
    // 4. 组合数据生成日程
    const schedule = {
      upcoming_exams: extractUpcomingExams(checkinHistory),
      completed_exams: extractCompletedExams(checkinHistory),
      candidate_info: candidateInfo.data
    };
    
    return {
      success: true,
      message: "获取考试日程成功",
      data: schedule,
      timestamp: new Date().toISOString()
    };
    
  } catch (error) {
    return {
      success: false,
      message: "获取考试日程失败",
      error_code: "SCHEDULE_FETCH_ERROR",
      data: null
    };
  }
}

// 辅助函数：从签到历史中提取即将到来的考试
function extractUpcomingExams(checkinHistory) {
  const now = new Date();
  return checkinHistory.data
    .filter(item => new Date(item.exam_time) > now)
    .map(item => ({
      id: item.schedule_id,
      exam_name: item.exam_name || "考试",
      exam_time: item.exam_time,
      venue: item.venue_name,
      address: item.venue_address,
      status: "待签到",
      exam_type: item.exam_type
    }));
}
```

---

## 📱 **2. 二维码生成功能实现**

### **目标接口**: `GET /api/v1/wechat/candidate/qrcode`

### **实现方案**: 前端生成 + 后端验证

#### **方案A: 纯前端生成二维码**
```javascript
// 使用前端二维码库生成
import QRCode from 'qrcode';

async function generateCandidateQRCode() {
  try {
    // 1. 获取当前用户信息
    const userInfo = await getUserInfo();
    
    // 2. 构造二维码数据
    const qrData = {
      t: "CHK",                    // 类型：签到
      c: userInfo.id,              // 考生ID
      s: getCurrentScheduleId(),    // 当前考试安排ID
      ts: Date.now(),              // 时间戳
      exp: Date.now() + 30 * 60 * 1000  // 30分钟后过期
    };
    
    // 3. 生成二维码
    const qrCodeDataURL = await QRCode.toDataURL(JSON.stringify(qrData));
    
    // 4. 生成备用码（6位数字）
    const backupCode = Math.floor(100000 + Math.random() * 900000).toString();
    
    return {
      success: true,
      message: "二维码生成成功",
      data: {
        qr_code: qrCodeDataURL,
        qr_data: qrData,
        expires_at: new Date(qrData.exp).toISOString(),
        backup_code: backupCode,
        refresh_interval: 30
      },
      timestamp: new Date().toISOString()
    };
    
  } catch (error) {
    return {
      success: false,
      message: "二维码生成失败",
      error_code: "QR_GENERATION_ERROR",
      data: null
    };
  }
}

// 获取当前考试安排ID的辅助函数
function getCurrentScheduleId() {
  // 从本地存储或全局状态中获取当前考试安排
  return wx.getStorageSync('currentScheduleId') || 'DEFAULT_SCHEDULE';
}
```

#### **方案B: 结合现有接口增强**
```javascript
async function generateEnhancedQRCode() {
  try {
    // 1. 获取考生信息
    const userInfo = await getUserInfo();
    const candidateInfo = await getCandidateByIdCard(userInfo.id_card);
    
    // 2. 获取最近的签到记录作为参考
    const checkinHistory = await getCheckinHistory();
    const latestCheckin = checkinHistory.data[0];
    
    // 3. 构造增强的二维码数据
    const enhancedQrData = {
      candidate: {
        id: userInfo.id,
        name: candidateInfo.data.name,
        id_card: candidateInfo.data.id_card
      },
      schedule: latestCheckin ? {
        id: latestCheckin.schedule_id,
        venue_id: latestCheckin.venue_id
      } : null,
      timestamp: Date.now(),
      expires: Date.now() + 30 * 60 * 1000
    };
    
    // 4. 生成二维码
    const qrCodeDataURL = await QRCode.toDataURL(JSON.stringify(enhancedQrData));
    
    return {
      success: true,
      data: {
        qr_code: qrCodeDataURL,
        qr_data: enhancedQrData,
        expires_at: new Date(enhancedQrData.expires).toISOString()
      }
    };
    
  } catch (error) {
    console.error('Enhanced QR generation failed:', error);
    // 降级到基础二维码生成
    return await generateCandidateQRCode();
  }
}
```

---

## 🏢 **3. 公共看板功能实现**

### **目标接口**: `GET /api/v1/wechat/dashboard`

### **实现方案**: 组合现有接口数据

#### **可用的数据源接口**:
1. `GET /api/v1/wechat/venues/status` - 考场状态
2. `GET /api/v1/health` - 系统状态
3. `GET /api/v1/auth/me` - 当前用户信息
4. `GET /api/v1/wechat/candidate/checkin-history` - 签到历史

#### **实现代码**:
```javascript
async function getDashboardData() {
  try {
    // 并行获取各种数据
    const [venuesStatus, systemHealth, userInfo, checkinHistory] = await Promise.all([
      getVenuesStatus(),
      getSystemHealth(),
      getUserInfo(),
      getCheckinHistory()
    ]);
    
    // 处理考场数据
    const venues = venuesStatus.data.map(venue => ({
      id: venue.id,
      name: venue.name,
      capacity: venue.capacity || 100,
      occupied: venue.current_occupancy || 0,
      status: venue.status === 'AVAILABLE' ? '可用' : 
              venue.status === 'OCCUPIED' ? '使用中' : '维护中'
    }));
    
    // 统计数据（基于签到历史推算）
    const stats = calculateStats(checkinHistory.data);
    
    // 构造看板数据
    const dashboardData = {
      // 统计信息
      total_candidates: stats.totalCandidates,
      checked_in: stats.checkedIn,
      in_progress: stats.inProgress,
      completed: stats.completed,
      
      // 考场信息
      venues: venues,
      
      // 系统公告（可以是静态的或从其他地方获取）
      announcements: [
        {
          id: "ANN_001",
          title: "考试注意事项",
          content: "请考生提前30分钟到达考场",
          type: "notice",
          created_at: new Date().toISOString()
        }
      ],
      
      // 个人信息
      current_user: {
        name: userInfo.real_name,
        id_card: userInfo.id_card,
        status: userInfo.is_active ? 'active' : 'inactive'
      }
    };
    
    return {
      success: true,
      message: "获取看板数据成功",
      data: dashboardData,
      timestamp: new Date().toISOString()
    };
    
  } catch (error) {
    return {
      success: false,
      message: "获取看板数据失败",
      error_code: "DASHBOARD_ERROR",
      data: null
    };
  }
}

// 统计计算辅助函数
function calculateStats(checkinData) {
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  
  // 基于签到历史数据进行统计
  const todayCheckins = checkinData.filter(item => 
    new Date(item.checkin_time) >= today
  );
  
  return {
    totalCandidates: checkinData.length,
    checkedIn: todayCheckins.filter(item => item.status === 'SUCCESS').length,
    inProgress: todayCheckins.filter(item => 
      item.status === 'SUCCESS' && 
      new Date(item.exam_end_time) > now
    ).length,
    completed: todayCheckins.filter(item => 
      item.status === 'SUCCESS' && 
      new Date(item.exam_end_time) <= now
    ).length
  };
}

// 获取考场状态
async function getVenuesStatus() {
  return await request({
    url: '/api/v1/wechat/venues/status',
    method: 'GET',
    headers: { 'Authorization': `Bearer ${getToken()}` }
  });
}

// 获取系统健康状态
async function getSystemHealth() {
  return await request({
    url: '/api/v1/health',
    method: 'GET'
  });
}
```

---

## 🛠️ **前端集成实现**

### **在 miniprogram/utils/api.js 中添加**:

```javascript
// 考试日程查询（组合实现）
export const getCandidateSchedule = () => {
  return new Promise(async (resolve, reject) => {
    try {
      const userInfo = await getUserInfo();
      const candidateInfo = await getCandidateByIdCard(userInfo.id_card);
      const checkinHistory = await getCheckinHistory();
      
      // 组合数据逻辑...
      const scheduleData = combineScheduleData(userInfo, candidateInfo, checkinHistory);
      resolve(scheduleData);
    } catch (error) {
      reject(error);
    }
  });
};

// 二维码生成（前端实现）
export const generateQRCode = () => {
  return new Promise(async (resolve, reject) => {
    try {
      const qrData = await generateCandidateQRCode();
      resolve(qrData);
    } catch (error) {
      reject(error);
    }
  });
};

// 看板数据（组合实现）
export const getDashboard = () => {
  return new Promise(async (resolve, reject) => {
    try {
      const dashboardData = await getDashboardData();
      resolve(dashboardData);
    } catch (error) {
      reject(error);
    }
  });
};
```

---

## 📦 **需要的前端依赖**

### **二维码生成库**:
```bash
# 在小程序中使用
npm install --save qrcode
```

### **或者使用小程序原生API**:
```javascript
// 使用小程序canvas生成二维码
wx.createCanvasContext('qrcode-canvas')
```

---

## 🎯 **实现优势**

### **1. 无需后端修改**
- 完全基于现有接口实现
- 不需要后端开发新接口
- 快速上线功能

### **2. 数据一致性**
- 使用相同的数据源
- 保证数据的准确性
- 实时性较好

### **3. 渐进式增强**
- 可以先实现基础功能
- 后续可以优化和增强
- 如果后端提供专用接口，可以无缝切换

### **4. 离线能力**
- 二维码可以离线生成
- 部分数据可以缓存
- 提升用户体验

---

## ⚠️ **注意事项**

### **1. 性能考虑**
- 多个接口并行调用可能增加延迟
- 需要做好加载状态处理
- 考虑数据缓存策略

### **2. 错误处理**
- 任一接口失败都要有降级方案
- 提供友好的错误提示
- 保证核心功能可用

### **3. 数据准确性**
- 组合数据可能不如专用接口准确
- 需要做好数据验证
- 定期与后端数据同步

通过这种方式，可以在不修改后端的情况下，快速实现三个缺失的功能，为用户提供完整的使用体验！