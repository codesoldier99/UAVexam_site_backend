// Mock数据配置管理
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
    timestampFormat: 'ISO',
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