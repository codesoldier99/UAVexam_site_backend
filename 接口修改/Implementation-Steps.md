# Implementation Steps - API Mock Integration
# 实施步骤 - API Mock数据集成

## 🎯 实施概览 (Implementation Overview)

本文档详细描述了将现有项目改造为使用Mock数据的具体实施步骤，以及后续对接真实后端的详细流程。

## 📋 前置准备 (Prerequisites)

### 当前项目状态检查
- [x] 项目结构完整
- [x] Mock数据文件存在
- [x] API调用层已实现
- [x] 前端页面基本完成

### 需要创建的新文件
```
miniprogram/mock-data/
├── index.js                    # Mock数据管理器
├── config.js                   # 配置管理
├── data-loader.js              # 数据加载器
├── dynamic-generator.js        # 动态数据生成器
└── api-mapping.js              # API路径映射
```

## 🚀 Phase 1: 创建Mock数据管理系统

### Step 1.1: 创建配置管理文件

**文件**: `miniprogram/mock-data/config.js`
```javascript
// 环境配置管理
const config = {
  // 全局Mock开关
  useMockData: true,
  
  // 模块级别控制
  moduleConfig: {
    auth: true,        // 认证模块
    candidate: true,   // 考生模块
    qrcode: true,      // 二维码模块
    realtime: true,    // 实时数据模块
    staff: true,       // 工作人员模块
    public: true       // 公共模块
  },
  
  // Mock行为配置
  mockBehavior: {
    networkDelay: 300,           // 模拟网络延迟(ms)
    errorRate: 0,                // 错误率 (0-1)
    enableDynamicData: true,     // 启用动态数据生成
    enableLogging: true,         // 启用Mock调用日志
    enableCache: true            // 启用Mock数据缓存
  },
  
  // 真实API配置
  realAPI: {
    baseURL: 'http://106.52.214.54',
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
  },
  
  // 动态数据配置
  dynamicData: {
    tokenPrefix: 'mock_token_',
    qrCodePrefix: 'candidate_checkin_',
    timestampFormat: 'ISO', // ISO | timestamp | custom
    idStart: 1000
  }
}

// 配置管理方法
const configManager = {
  // 获取配置
  get(key) {
    return key ? config[key] : config
  },
  
  // 设置全局Mock开关
  setGlobalMock(enabled) {
    config.useMockData = enabled
    this.log(`Global mock ${enabled ? 'enabled' : 'disabled'}`)
  },
  
  // 设置模块Mock开关
  setModuleConfig(module, enabled) {
    if (config.moduleConfig.hasOwnProperty(module)) {
      config.moduleConfig[module] = enabled
      this.log(`Module ${module} mock ${enabled ? 'enabled' : 'disabled'}`)
    }
  },
  
  // 检查是否使用Mock
  shouldUseMock(module = null) {
    if (!config.useMockData) return false
    if (module && config.moduleConfig.hasOwnProperty(module)) {
      return config.moduleConfig[module]
    }
    return true
  },
  
  // 日志输出
  log(message) {
    if (config.mockBehavior.enableLogging) {
      console.log(`[Mock Config] ${message}`)
    }
  }
}

module.exports = configManager
```

### Step 1.2: 创建API路径映射

**文件**: `miniprogram/mock-data/api-mapping.js`
```javascript
// API路径到Mock数据文件的映射
const apiMapping = {
  // 认证模块
  'POST /wx/login-by-idcard': {
    success: 'auth/candidate-login-success.json',
    failure: 'auth/candidate-login-failure.json'
  },
  'POST /auth/jwt/login': {
    success: 'auth/staff-login-success.json',
    failure: 'auth/staff-login-failure.json'
  },
  'GET /auth/users/me': {
    success: 'auth/user-info.json'
  },
  
  // 考生模块
  'GET /wx-miniprogram/candidate-info': {
    success: 'candidate/candidate-info.json'
  },
  'GET /wx/candidate-info/:id': {
    success: 'candidate/candidate-detail.json'
  },
  'GET /wx-miniprogram/exam-schedule': {
    success: 'candidate/exam-schedule.json'
  },
  'GET /wx/my-qrcode/:id': {
    success: 'candidate/qrcode-data.json'
  },
  'GET /wx-miniprogram/checkin-history': {
    success: 'candidate/checkin-history.json'
  },
  
  // 二维码模块
  'GET /qrcode/generate-schedule-qr/:id': {
    success: 'qrcode/generate-qr-success.json'
  },
  'POST /qrcode/scan-checkin': {
    success: 'qrcode/scan-checkin-success.json',
    failure: 'qrcode/scan-checkin-failure.json'
  },
  'GET /qrcode/checkin-status/:id': {
    success: 'qrcode/checkin-status.json'
  },
  'POST /qrcode/manual-checkin': {
    success: 'qrcode/manual-checkin.json'
  },
  
  // 实时数据模块
  'GET /realtime/status': {
    success: 'realtime/realtime-status.json'
  },
  'GET /realtime/public-board': {
    success: 'realtime/public-board.json'
  },
  'GET /realtime/venue-status': {
    success: 'realtime/venue-status.json'
  },
  'GET /realtime/system-status': {
    success: 'realtime/system-status.json'
  },
  'GET /realtime/queue-status/:id': {
    success: 'realtime/queue-status.json'
  },
  'GET /realtime/venue-queue/:id': {
    success: 'realtime/venue-queue.json'
  },
  'GET /realtime/notifications': {
    success: 'realtime/notifications.json'
  }
}

// 路径匹配工具
const pathMatcher = {
  // 标准化API路径
  normalizePath(method, url) {
    // 移除查询参数
    const cleanUrl = url.split('?')[0]
    return `${method.toUpperCase()} ${cleanUrl}`
  },
  
  // 匹配API路径（支持参数路径）
  matchPath(method, url) {
    const normalizedPath = this.normalizePath(method, url)
    
    // 直接匹配
    if (apiMapping[normalizedPath]) {
      return apiMapping[normalizedPath]
    }
    
    // 参数路径匹配
    for (const [pattern, mapping] of Object.entries(apiMapping)) {
      if (this.isPatternMatch(normalizedPath, pattern)) {
        return mapping
      }
    }
    
    return null
  },
  
  // 检查路径模式匹配
  isPatternMatch(path, pattern) {
    // 将 :id 等参数转换为正则表达式
    const regexPattern = pattern
      .replace(/:[^/]+/g, '[^/]+')  // :id -> [^/]+
      .replace(/\//g, '\\/')        // / -> \/
    
    const regex = new RegExp(`^${regexPattern}$`)
    return regex.test(path)
  },
  
  // 提取路径参数
  extractParams(path, pattern) {
    const pathParts = path.split('/')
    const patternParts = pattern.split('/')
    const params = {}
    
    for (let i = 0; i < patternParts.length; i++) {
      if (patternParts[i].startsWith(':')) {
        const paramName = patternParts[i].substring(1)
        params[paramName] = pathParts[i]
      }
    }
    
    return params
  }
}

module.exports = {
  apiMapping,
  pathMatcher
}
```

### Step 1.3: 创建动态数据生成器

**文件**: `miniprogram/mock-data/dynamic-generator.js`
```javascript
// 动态数据生成器
const configManager = require('./config.js')

class DynamicGenerator {
  constructor() {
    this.config = configManager.get('dynamicData')
  }
  
  // 生成当前时间戳
  generateTimestamp(format = null) {
    const now = new Date()
    const targetFormat = format || this.config.timestampFormat
    
    switch (targetFormat) {
      case 'ISO':
        return now.toISOString()
      case 'timestamp':
        return Math.floor(now.getTime() / 1000)
      case 'datetime':
        return now.toLocaleString('zh-CN')
      default:
        return now.toISOString()
    }
  }
  
  // 生成Mock Token
  generateToken(userId = null, userType = 'candidate') {
    const timestamp = Date.now()
    const random = Math.random().toString(36).substr(2, 9)
    const userInfo = userId ? `_${userId}` : ''
    return `${this.config.tokenPrefix}${userType}${userInfo}_${timestamp}_${random}`
  }
  
  // 生成二维码内容
  generateQRContent(candidateId, scheduleId = null) {
    const timestamp = Math.floor(Date.now() / 1000)
    const scheduleInfo = scheduleId ? `_${scheduleId}` : ''
    return `${this.config.qrCodePrefix}${candidateId}${scheduleInfo}_${timestamp}`
  }
  
  // 生成二维码URL
  generateQRUrl(content, size = '200x200') {
    return `https://api.qrserver.com/v1/create-qr-code/?size=${size}&data=${encodeURIComponent(content)}`
  }
  
  // 生成随机ID
  generateId(prefix = '') {
    const random = Math.floor(Math.random() * 9000) + this.config.idStart
    return prefix ? `${prefix}_${random}` : random
  }
  
  // 生成过期时间
  generateExpiryTime(hoursFromNow = 24) {
    const expiry = new Date()
    expiry.setHours(expiry.getHours() + hoursFromNow)
    return expiry.toISOString()
  }
  
  // 替换模板中的动态变量
  replaceDynamicVariables(data, context = {}) {
    if (typeof data === 'string') {
      return this.replaceStringVariables(data, context)
    } else if (Array.isArray(data)) {
      return data.map(item => this.replaceDynamicVariables(item, context))
    } else if (typeof data === 'object' && data !== null) {
      const result = {}
      for (const [key, value] of Object.entries(data)) {
        result[key] = this.replaceDynamicVariables(value, context)
      }
      return result
    }
    return data
  }
  
  // 替换字符串中的动态变量
  replaceStringVariables(str, context) {
    return str.replace(/\{\{(\w+)\}\}/g, (match, variable) => {
      switch (variable) {
        case 'timestamp':
          return this.generateTimestamp()
        case 'token':
          return this.generateToken(context.userId, context.userType)
        case 'qr_content':
          return this.generateQRContent(context.candidateId, context.scheduleId)
        case 'qr_url':
          const content = this.generateQRContent(context.candidateId, context.scheduleId)
          return this.generateQRUrl(content)
        case 'expiry_time':
          return this.generateExpiryTime()
        case 'random_id':
          return this.generateId()
        default:
          return context[variable] || match
      }
    })
  }
  
  // 生成考试相关的动态数据
  generateExamData(candidateId, scheduleId) {
    return {
      candidate_id: candidateId,
      schedule_id: scheduleId,
      qr_content: this.generateQRContent(candidateId, scheduleId),
      qr_url: this.generateQRUrl(this.generateQRContent(candidateId, scheduleId)),
      checkin_time: this.generateTimestamp(),
      expires_at: this.generateExpiryTime(2), // 2小时后过期
      token: this.generateToken(candidateId, 'candidate')
    }
  }
}

module.exports = new DynamicGenerator()
```

### Step 1.4: 创建数据加载器

**文件**: `miniprogram/mock-data/data-loader.js`
```javascript
// Mock数据加载器
const fs = require('fs')
const path = require('path')

class DataLoader {
  constructor() {
    this.cache = new Map()
    this.basePath = path.join(__dirname)
  }
  
  // 加载JSON文件
  loadJsonFile(filePath) {
    try {
      const fullPath = path.join(this.basePath, filePath)
      
      // 检查缓存
      if (this.cache.has(fullPath)) {
        return this.cache.get(fullPath)
      }
      
      // 读取文件
      const fileContent = fs.readFileSync(fullPath, 'utf8')
      const data = JSON.parse(fileContent)
      
      // 缓存数据
      this.cache.set(fullPath, data)
      
      return data
    } catch (error) {
      console.error(`Failed to load mock data file: ${filePath}`, error)
      return this.getDefaultErrorResponse()
    }
  }
  
  // 获取默认错误响应
  getDefaultErrorResponse() {
    return {
      success: false,
      message: "Mock数据加载失败",
      error_code: "MOCK_DATA_ERROR",
      data: null,
      timestamp: new Date().toISOString()
    }
  }
  
  // 清除缓存
  clearCache() {
    this.cache.clear()
  }
  
  // 重新加载文件（清除缓存后重新加载）
  reloadFile(filePath) {
    const fullPath = path.join(this.basePath, filePath)
    this.cache.delete(fullPath)
    return this.loadJsonFile(filePath)
  }
}

module.exports = new DataLoader()
```

### Step 1.5: 创建Mock数据管理器主文件

**文件**: `miniprogram/mock-data/index.js`
```javascript
// Mock数据管理器主文件
const configManager = require('./config.js')
const { pathMatcher } = require('./api-mapping.js')
const dataLoader = require('./data-loader.js')
const dynamicGenerator = require('./dynamic-generator.js')

class MockDataManager {
  constructor() {
    this.config = configManager
    this.pathMatcher = pathMatcher
    this.dataLoader = dataLoader
    this.dynamicGenerator = dynamicGenerator
  }
  
  // 主要方法：获取Mock响应
  async getMockResponse(url, method = 'GET', params = {}, context = {}) {
    try {
      // 检查是否应该使用Mock
      const module = this.extractModuleFromUrl(url)
      if (!this.config.shouldUseMock(module)) {
        return null // 返回null表示应该使用真实API
      }
      
      // 记录日志
      this.log(`Mock request: ${method} ${url}`)
      
      // 模拟网络延迟
      await this.simulateDelay()
      
      // 获取Mock数据文件路径
      const mapping = this.pathMatcher.matchPath(method, url)
      if (!mapping) {
        return this.getNotFoundResponse(url)
      }
      
      // 决定返回成功还是失败响应
      const shouldReturnError = this.shouldReturnError()
      const dataFile = shouldReturnError && mapping.failure ? mapping.failure : mapping.success
      
      // 加载Mock数据
      let mockData = this.dataLoader.loadJsonFile(dataFile)
      
      // 处理动态数据
      if (this.config.get('mockBehavior').enableDynamicData) {
        mockData = this.processDynamicData(mockData, url, params, context)
      }
      
      // 处理参数替换
      mockData = this.processParameters(mockData, url, params)
      
      return mockData
      
    } catch (error) {
      console.error('Mock data manager error:', error)
      return this.getErrorResponse(error.message)
    }
  }
  
  // 从URL提取模块名
  extractModuleFromUrl(url) {
    if (url.includes('/auth/') || url.includes('/wx/login')) return 'auth'
    if (url.includes('/wx-miniprogram/') || url.includes('/wx/candidate')) return 'candidate'
    if (url.includes('/qrcode/')) return 'qrcode'
    if (url.includes('/realtime/')) return 'realtime'
    if (url.includes('/staff/')) return 'staff'
    return 'public'
  }
  
  // 模拟网络延迟
  async simulateDelay() {
    const delay = this.config.get('mockBehavior').networkDelay
    if (delay > 0) {
      await new Promise(resolve => setTimeout(resolve, delay))
    }
  }
  
  // 判断是否应该返回错误
  shouldReturnError() {
    const errorRate = this.config.get('mockBehavior').errorRate
    return Math.random() < errorRate
  }
  
  // 处理动态数据
  processDynamicData(data, url, params, context) {
    // 提取URL参数
    const urlParams = this.extractUrlParams(url)
    
    // 合并上下文
    const fullContext = {
      ...context,
      ...params,
      ...urlParams,
      url,
      timestamp: new Date().toISOString()
    }
    
    // 替换动态变量
    return this.dynamicGenerator.replaceDynamicVariables(data, fullContext)
  }
  
  // 提取URL参数
  extractUrlParams(url) {
    const params = {}
    
    // 提取路径参数 (如 /candidate/123 中的 123)
    const pathParts = url.split('/')
    pathParts.forEach((part, index) => {
      if (/^\d+$/.test(part)) {
        params.id = part
        params.candidateId = part
        params.scheduleId = part
      }
    })
    
    // 提取查询参数
    const [, queryString] = url.split('?')
    if (queryString) {
      queryString.split('&').forEach(param => {
        const [key, value] = param.split('=')
        params[key] = decodeURIComponent(value)
      })
    }
    
    return params
  }
  
  // 处理参数替换
  processParameters(data, url, params) {
    // 如果数据是数组，可能需要根据参数过滤
    if (Array.isArray(data.data)) {
      return this.filterArrayData(data, params)
    }
    
    // 如果是对象，可能需要根据参数修改某些字段
    if (typeof data.data === 'object' && data.data !== null) {
      return this.updateObjectData(data, params)
    }
    
    return data
  }
  
  // 过滤数组数据
  filterArrayData(data, params) {
    if (params.candidate_id) {
      // 过滤与特定考生相关的数据
      data.data = data.data.filter(item => 
        item.candidate_id == params.candidate_id || 
        item.id == params.candidate_id
      )
    }
    
    if (params.venue_id) {
      // 过滤与特定考场相关的数据
      data.data = data.data.filter(item => 
        item.venue_id == params.venue_id
      )
    }
    
    return data
  }
  
  // 更新对象数据
  updateObjectData(data, params) {
    if (params.id && data.data.id) {
      data.data.id = parseInt(params.id)
    }
    
    if (params.candidate_id && data.data.candidate_id) {
      data.data.candidate_id = parseInt(params.candidate_id)
    }
    
    return data
  }
  
  // 获取404响应
  getNotFoundResponse(url) {
    return {
      success: false,
      message: `Mock数据未找到: ${url}`,
      error_code: "MOCK_NOT_FOUND",
      data: null,
      timestamp: new Date().toISOString()
    }
  }
  
  // 获取错误响应
  getErrorResponse(message) {
    return {
      success: false,
      message: message || "Mock数据处理错误",
      error_code: "MOCK_ERROR",
      data: null,
      timestamp: new Date().toISOString()
    }
  }
  
  // 日志输出
  log(message) {
    if (this.config.get('mockBehavior').enableLogging) {
      console.log(`[Mock Manager] ${message}`)
    }
  }
  
  // 配置管理方法
  setGlobalMock(enabled) {
    this.config.setGlobalMock(enabled)
  }
  
  setModuleMock(module, enabled) {
    this.config.setModuleConfig(module, enabled)
  }
  
  // 清除缓存
  clearCache() {
    this.dataLoader.clearCache()
  }
}

module.exports = new MockDataManager()
```

## 🔄 Phase 2: 修改API调用层

### Step 2.1: 修改主API文件

**文件**: `miniprogram/utils/api.js` (修改现有文件)

在文件顶部添加Mock管理器引用：
```javascript
// 在文件顶部添加
const mockManager = require('../mock-data/index.js')
```

修改request函数：
```javascript
// 修改现有的request函数
async function request(url, options = {}) {
  const {
    method = 'GET',
    data = {},
    header = {},
    timeout = 10000,
    enableCache = true,
    showLoading = true,
    loadingText = '加载中...'
  } = options

  // 检查是否使用Mock数据
  try {
    const mockResponse = await mockManager.getMockResponse(url, method, data, {
      userInfo: getCurrentUser(), // 如果有当前用户信息
      timestamp: Date.now()
    })
    
    if (mockResponse !== null) {
      // 使用Mock数据
      console.log('[API] Using mock data for:', method, url)
      
      // 模拟加载状态
      if (showLoading) {
        wx.showLoading({ title: loadingText })
        setTimeout(() => wx.hideLoading(), 100)
      }
      
      // 返回Mock响应
      return mockResponse
    }
  } catch (mockError) {
    console.error('[API] Mock data error:', mockError)
    // 如果Mock出错，继续使用真实API
  }

  // 使用真实API（保持原有逻辑）
  return realAPIRequest(url, options)
}

// 保持原有的真实API请求逻辑
async function realAPIRequest(url, options = {}) {
  // 这里是原有的request函数逻辑
  // ... 保持不变
}
```

### Step 2.2: 确保所有API接口调用保持不变

验证以下接口调用方式无需修改：
```javascript
// 这些调用方式保持完全不变
authAPI.candidateLogin({ id_card: '123456' })
authAPI.staffLogin({ username: 'staff001', password: 'password' })
candidateAPI.getCandidateInfo({ id_number: '123456' })
candidateAPI.getExamSchedule({ candidate_id: 1 })
qrcodeAPI.generateScheduleQR(scheduleId)
realtimeAPI.getRealtimeStatus()
```

## 🧪 Phase 3: 测试和验证

### Step 3.1: 创建测试脚本

**文件**: `test-mock-integration.js`
```javascript
// Mock集成测试脚本
const mockManager = require('./miniprogram/mock-data/index.js')

async function testMockIntegration() {
  console.log('=== Mock Integration Test ===')
  
  // 测试认证接口
  console.log('\n1. Testing Auth APIs...')
  const loginResult = await mockManager.getMockResponse('/wx/login-by-idcard', 'POST', {
    id_card: '110101199001011234'
  })
  console.log('Login result:', loginResult.success ? '✅' : '❌')
  
  // 测试考生接口
  console.log('\n2. Testing Candidate APIs...')
  const candidateInfo = await mockManager.getMockResponse('/wx-miniprogram/candidate-info', 'GET', {
    id_number: '110101199001011234'
  })
  console.log('Candidate info:', candidateInfo.success ? '✅' : '❌')
  
  // 测试二维码接口
  console.log('\n3. Testing QR Code APIs...')
  const qrCode = await mockManager.getMockResponse('/wx/my-qrcode/1', 'GET')
  console.log('QR Code generation:', qrCode.success ? '✅' : '❌')
  
  // 测试实时数据接口
  console.log('\n4. Testing Realtime APIs...')
  const realtimeStatus = await mockManager.getMockResponse('/realtime/status', 'GET')
  console.log('Realtime status:', realtimeStatus.success ? '✅' : '❌')
  
  // 测试配置切换
  console.log('\n5. Testing Configuration Switch...')
  mockManager.setModuleMock('auth', false)
  const authAfterDisable = await mockManager.getMockResponse('/wx/login-by-idcard', 'POST', {})
  console.log('Auth disabled:', authAfterDisable === null ? '✅' : '❌')
  
  console.log('\n=== Test Complete ===')
}

// 运行测试
testMockIntegration().catch(console.error)
```

### Step 3.2: 验证前端页面功能

创建验证清单：
- [ ] 考生登录页面正常工作
- [ ] 工作人员登录页面正常工作
- [ ] 考生信息页面显示正确
- [ ] 考试安排页面显示正确
- [ ] 二维码生成和显示正常
- [ ] 实时数据看板正常更新
- [ ] 所有页面加载速度合理

## 🔄 Phase 4: 对接真实后端的详细步骤

### Step 4.1: 准备阶段

#### 4.1.1 API文档对比
```markdown
# API对比检查清单
- [ ] 请求URL格式一致
- [ ] 请求方法一致
- [ ] 请求参数格式一致
- [ ] 响应数据结构一致
- [ ] 错误码定义一致
- [ ] 认证方式一致
```

#### 4.1.2 环境配置准备
```javascript
// 在 mock-data/config.js 中准备真实API配置
realAPI: {
  development: {
    baseURL: 'http://dev-api.example.com',
    timeout: 15000
  },
  staging: {
    baseURL: 'http://staging-api.example.com',
    timeout: 10000
  },
  production: {
    baseURL: 'https://api.example.com',
    timeout: 8000
  }
}
```

### Step 4.2: 渐进式切换策略

#### 策略A: 按模块切换（推荐）
```javascript
// 第1周：切换认证模块
mockManager.setModuleMock('auth', false)

// 第2周：切换考生模块
mockManager.setModuleMock('candidate', false)

// 第3周：切换二维码模块
mockManager.setModuleMock('qrcode', false)

// 第4周：切换实时数据模块
mockManager.setModuleMock('realtime', false)
```

#### 策略B: 按接口切换
```javascript
// 在 api-mapping.js 中添加接口级别控制
const apiConfig = {
  'POST /wx/login-by-idcard': 'real',      // 使用真实API
  'GET /wx-miniprogram/candidate-info': 'mock',  // 仍使用Mock
  // ... 其他接口配置
}
```

### Step 4.3: 切换执行步骤

#### Step 4.3.1: 单模块切换流程
```bash
# 1. 备份当前配置
cp miniprogram/mock-data/config.js miniprogram/mock-data/config.backup.js

# 2. 修改配置文件
# 将目标模块的Mock开关设为false

# 3. 测试验证
npm run test:integration

# 4. 前端功能测试
# 手动测试所有相关页面功能

# 5. 性能测试
# 检查响应时间是否在可接受范围内

# 6. 错误处理测试
# 测试网络异常、服务器错误等场景

# 7. 回退准备
# 如果出现问题，立即恢复备份配置
```

#### Step 4.3.2: 问题排查流程
```javascript
// 创建调试工具
const debugTool = {
  // 对比Mock和真实API响应
  async compareResponses(url, method, params) {
    const mockResponse = await mockManager.getMockResponse(url, method, params)
    const realResponse = await realAPIRequest(url, { method, data: params })
    
    console.log('Mock Response:', mockResponse)
    console.log('Real Response:', realResponse)
    console.log('Differences:', this.findDifferences(mockResponse, realResponse))
  },
  
  // 查找数据差异
  findDifferences(mock, real) {
    // 实现数据结构对比逻辑
  }
}
```

### Step 4.4: 完全切换后的配置

#### 最终配置状态
```javascript
// mock-data/config.js - 生产环境配置
module.exports = {
  // 全局关闭Mock（但保留能力）
  useMockData: false,
  
  // 所有模块使用真实API
  moduleConfig: {
    auth: false,
    candidate: false,
    qrcode: false,
    realtime: false,
    staff: false,
    public: false
  },
  
  // 保留Mock能力用于演示和测试
  demoMode: {
    enabled: false,  // 可以通过管理界面开启
    modules: ['auth', 'candidate', 'qrcode', 'realtime']
  }
}
```

## 📊 监控和维护

### Step 5.1: 创建监控脚本

**文件**: `monitoring/api-health-check.js`
```javascript
// API健康检查脚本
const healthCheck = {
  async checkAllAPIs() {
    const apis = [
      { name: 'Auth Login', url: '/wx/login-by-idcard', method: 'POST' },
      { name: 'Candidate Info', url: '/wx-miniprogram/candidate-info', method: 'GET' },
      { name: 'QR Generate', url: '/qrcode/generate-schedule-qr/1', method: 'GET' },
      { name: 'Realtime Status', url: '/realtime/status', method: 'GET' }
    ]
    
    for (const api of apis) {
      const startTime = Date.now()
      try {
        const response = await this.testAPI(api.url, api.method)
        const responseTime = Date.now() - startTime
        console.log(`✅ ${api.name}: ${responseTime}ms`)
      } catch (error) {
        console.log(`❌ ${api.name}: ${error.message}`)
      }
    }
  }
}
```

### Step 5.2: 创建切换工具

**文件**: `tools/mock-switch-tool.js`
```javascript
// Mock切换工具
const switchTool = {
  // 快速切换到Mock模式
  enableMockMode() {
    const config = require('../miniprogram/mock-data/config.js')
    config.setGlobalMock(true)
    console.log('✅ Mock mode enabled')
  },
  
  // 快速切换到真实API模式
  enableRealAPIMode() {
    const config = require('../miniprogram/mock-data/config.js')
    config.setGlobalMock(false)
    console.log('✅ Real API mode enabled')
  },
  
  // 模块级别切换
  switchModule(module, useMock) {
    const config = require('../miniprogram/mock-data/config.js')
    config.setModuleConfig(module, useMock)
    console.log(`✅ Module ${module} switched to ${useMock ? 'Mock' : 'Real API'}`)
  }
}

module.exports = switchTool
```

## 🎯 验收标准

### 开发阶段验收
- [ ] 所有前端页面使用Mock数据正常运行
- [ ] Mock数据覆盖所有API接口
- [ ] 动态数据生成正常（时间戳、Token、二维码等）
- [ ] 配置切换机制正常工作
- [ ] 错误场景模拟正常
- [ ] 性能满足要求（响应时间<500ms）

### 对接阶段验收
- [ ] 单模块切换成功率100%
- [ ] 混合模式稳定运行
- [ ] 数据格式完全一致
- [ ] 错误处理机制正常
- [ ] 回退机制可靠
- [ ] 性能指标达到预期

### 生产阶段验收
- [ ] 所有功能使用真实API正常运行
- [ ] 系统稳定性达到要求
- [ ] 监控和告警机制完善
- [ ] 文档和维护流程完整
- [ ] 应急预案可执行

## 📝 注意事项和最佳实践

### 开发阶段注意事项
1. **数据一致性**：确保Mock数据与API文档完全一致
2. **动态数据**：重要的动态字段（时间戳、Token）必须实时生成
3. **错误模拟**：适当模拟各种错误场景
4. **性能考虑**：Mock响应时间应该接近真实API

### 对接阶段注意事项
1. **渐进切换**：避免一次性切换所有接口
2. **充分测试**：每个模块切换后都要进行全面测试
3. **监控告警**：建立完善的监控和告警机制
4. **回退准备**：随时准备回退到Mock模式

### 维护阶段注意事项
1. **版本同步**：Mock数据要与API版本保持同步
2. **文档更新**：及时更新相关文档
3. **定期检查**：定期检查Mock和真实API的一致性
4. **备用方案**：保持Mock模式作为备用方案

---

## 总结

这个实施方案提供了完整的、分阶段的、风险可控的API Mock数据集成解决方案。通过这种方式，我们可以：

1. **立即开始开发**：使用完善的Mock数据系统
2. **平滑过渡**：通过配置轻松切换Mock和真实API
3. **降低风险**：渐进式切换和可靠的回退机制
4. **长期维护**：保持Mock能力用于演示和测试

整个方案既满足了当前开发需求，又为未来的扩展和维护提供了充分的灵活性和可靠性。
