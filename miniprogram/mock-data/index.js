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
    
    // 生成默认的用户数据
    const defaultUserData = {
      userId: 'CAND_1001',
      candidateId: 'CAND_1001', 
      idNumber: '110101199001011234',
      userType: 'candidate'
    }
    
    // 合并上下文
    const fullContext = {
      ...defaultUserData,
      ...context,
      ...params,
      ...urlParams,
      url,
      timestamp: new Date().toISOString()
    }
    
    console.log('Processing dynamic data with context:', fullContext)
    
    // 替换动态变量
    const result = this.dynamicGenerator.replaceDynamicVariables(data, fullContext)
    
    console.log('Dynamic data processing result:', result)
    
    return result
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