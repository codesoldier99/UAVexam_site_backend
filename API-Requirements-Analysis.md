# UAV考点运营管理系统 - 小程序API需求分析

## 📊 **总体分析结果**

基于对61个后端API接口和小程序代码的详细分析，以下是小程序实际需要的接口分类和建议：

## 🎯 **核心必需接口 (26个)**

### **微信小程序专用模块 (7个) - 全部需要 ✅**
1. `POST /api/v1/wechat/login` - 考生身份证登录
2. `GET /api/v1/wechat/candidate/schedule` - 获取考生日程
3. `GET /api/v1/wechat/candidate/qrcode` - 获取考生二维码
4. `GET /api/v1/wechat/venues/status` - 获取考场状态
5. `POST /api/v1/wechat/checkin` - 扫码签到
6. `GET /api/v1/wechat/candidate/queue-position` - 获取排队位置
7. `GET /api/v1/wechat/dashboard` - 获取看板数据

### **认证授权模块 (4个)**
8. `POST /api/v1/auth/login` - 工作人员登录
9. `GET /api/v1/auth/me` - 获取当前用户信息
10. `POST /api/v1/auth/refresh` - 刷新令牌
11. `POST /api/v1/auth/logout` - 用户登出

### **考生管理模块 (4个)**
12. `GET /api/v1/candidates/` - 获取考生列表
13. `GET /api/v1/candidates/{id}` - 获取考生详情
14. `GET /api/v1/candidates/statistics` - 获取考生统计
15. `POST /api/v1/candidates/` - 创建考生 (工作人员功能)

### **日程管理模块 (5个)**
16. `GET /api/v1/schedules/` - 获取日程列表
17. `POST /api/v1/schedules/{id}/start` - 开始日程
18. `POST /api/v1/schedules/{id}/complete` - 完成日程
19. `GET /api/v1/schedules/venue/{id}/today` - 获取考场今日日程
20. `GET /api/v1/schedules/statistics/overview` - 获取日程统计

### **考场管理模块 (4个)**
21. `GET /api/v1/venues/` - 获取考场列表
22. `GET /api/v1/venues/{id}` - 获取考场详情
23. `GET /api/v1/venues/{id}/current-status` - 获取考场当前状态
24. `GET /api/v1/venues/{id}/schedules` - 获取考场日程

### **系统管理模块 (2个)**
25. `GET /api/v1/system/features` - 获取系统功能特性
26. `GET /api/v1/health/` - 健康检查

## 🚨 **发现的关键问题**

### **1. 缺少的关键接口 (需要补充4个)**

**A. 根据身份证获取考生信息**
```http
GET /api/v1/wechat/candidate/info-by-idcard?id_card={id_card}
```
**用途**: 考生登录时验证身份证号并获取基本信息
**优先级**: 🔴 高 (登录必需)

**B. 二维码刷新接口**
```http
POST /api/v1/wechat/candidate/qrcode/refresh
```
**用途**: 刷新考生动态二维码，防止过期
**优先级**: 🟡 中 (用户体验)

**C. 考生签到历史**
```http
GET /api/v1/wechat/candidate/checkin-history
```
**用途**: 查看考生的历史签到记录
**优先级**: 🟢 低 (信息查询)

**D. 考生考试结果查询**
```http
GET /api/v1/wechat/candidate/exam-results
```
**用途**: 查看考生的考试成绩和结果
**优先级**: 🟡 中 (核心功能)

### **2. 接口路径不匹配问题**

小程序当前使用的API路径需要更新为标准路径：

| 当前路径 | 标准路径 | 状态 |
|---------|---------|------|
| `/wx/login-by-idcard` | `/api/v1/wechat/login` | 🔄 需更新 |
| `/wx/my-qrcode/{id}` | `/api/v1/wechat/candidate/qrcode` | 🔄 需更新 |
| `/auth/jwt/login` | `/api/v1/auth/login` | 🔄 需更新 |
| `/auth/users/me` | `/api/v1/auth/me` | 🔄 需更新 |

### **3. 可选增强接口 (8个)**

这些接口可以提升用户体验，但不是核心必需：

27. `GET /api/v1/institutions/` - 获取机构列表
28. `GET /api/v1/exam-products/` - 获取考试产品列表
29. `GET /api/v1/system/config` - 获取系统配置
30. `GET /api/v1/system/status` - 获取系统状态
31. `POST /api/v1/schedules/batch` - 批量创建日程
32. `GET /api/v1/candidates/batch-import` - 批量导入考生
33. `POST /api/v1/venues/{id}/toggle-status` - 切换考场状态
34. `GET /api/v1/system/version` - 获取版本信息

## 📋 **实施建议**

### **阶段1: 核心功能 (优先级: 🔴 高)**
1. **立即补充4个缺失的关键接口**
2. **更新小程序API路径为标准格式**
3. **更新Mock数据系统映射**

### **阶段2: 功能完善 (优先级: 🟡 中)**
1. **实现考试结果查询功能**
2. **添加二维码刷新机制**
3. **完善错误处理和用户反馈**

### **阶段3: 体验优化 (优先级: 🟢 低)**
1. **添加签到历史查询**
2. **实现可选增强功能**
3. **性能优化和缓存策略**

## 🔧 **技术实施要点**

### **1. API路径标准化**
```javascript
// 更新 miniprogram/utils/api.js 中的接口调用
const authAPI = {
  candidateLogin(idNumber) {
    return request('/api/v1/wechat/login', {  // 标准路径
      method: 'POST',
      data: { id_card: idNumber },
      needAuth: false
    })
  }
}
```

### **2. Mock数据系统更新**
- ✅ 已更新 `api-mapping.js` 支持新的标准路径
- 🔄 需要创建缺失接口的Mock数据文件
- 🔄 保持向后兼容，逐步废弃旧路径

### **3. 错误处理增强**
```javascript
// 统一错误处理格式
{
  "error": {
    "code": "CANDIDATE_NOT_FOUND",
    "message": "未找到该身份证号对应的考生信息",
    "details": {
      "id_card": "110101199001011234"
    }
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## 📈 **接口使用统计**

| 模块 | 必需接口 | 可选接口 | 缺失接口 | 总计 |
|------|---------|---------|---------|------|
| 微信小程序 | 7 | 0 | 4 | 11 |
| 认证授权 | 4 | 0 | 0 | 4 |
| 考生管理 | 4 | 2 | 0 | 6 |
| 日程管理 | 5 | 1 | 0 | 6 |
| 考场管理 | 4 | 1 | 0 | 5 |
| 系统管理 | 2 | 3 | 0 | 5 |
| **总计** | **26** | **7** | **4** | **37** |

## 🎯 **结论**

1. **当前61个API接口中，小程序实际需要37个接口**
2. **其中26个是核心必需，7个是可选增强**
3. **需要补充4个关键缺失接口**
4. **需要更新API路径标准化**
5. **Mock数据系统已更新支持新路径**

## 🚀 **下一步行动**

1. **立即实施**: 补充4个缺失接口的后端实现
2. **同步更新**: 小程序API调用路径标准化
3. **测试验证**: 确保新接口与Mock数据系统兼容
4. **文档更新**: 同步更新API文档和使用说明

---
*分析完成时间: 2024-01-01*
*分析版本: v1.0*