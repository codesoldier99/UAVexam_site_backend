# Quick Reference Guide - API Mock Integration
# 快速参考指南 - API Mock数据集成

## 🚀 快速开始 (Quick Start)

### 1. 立即启用Mock模式
```javascript
// 在 miniprogram/mock-data/config.js 中
module.exports = {
  useMockData: true,  // 启用Mock模式
  // ... 其他配置
}
```

### 2. 验证Mock功能
```bash
# 运行测试脚本
node test-mock-integration.js
```

### 3. 前端页面测试
- 打开小程序开发者工具
- 测试所有页面功能
- 检查控制台日志确认使用Mock数据

## 🔧 常用操作 (Common Operations)

### 配置切换
```javascript
const mockManager = require('./miniprogram/mock-data/index.js')

// 全局切换
mockManager.setGlobalMock(true)   // 启用Mock
mockManager.setGlobalMock(false)  // 禁用Mock

// 模块切换
mockManager.setModuleMock('auth', false)      // 认证模块使用真实API
mockManager.setModuleMock('candidate', true)  // 考生模块使用Mock
```

### 调试和监控
```javascript
// 查看Mock调用日志
// 在浏览器控制台查看 [Mock Manager] 开头的日志

// 清除Mock数据缓存
mockManager.clearCache()

// 检查当前配置
const config = require('./miniprogram/mock-data/config.js')
console.log('Current config:', config.get())
```

## 📋 API接口映射表 (API Mapping Table)

### 认证模块 (Auth Module)
| API路径 | 方法 | Mock文件 | 说明 |
|---------|------|----------|------|
| `/wx/login-by-idcard` | POST | `auth/candidate-login-success.json` | 考生登录 |
| `/auth/jwt/login` | POST | `auth/staff-login-success.json` | 工作人员登录 |
| `/auth/users/me` | GET | `auth/user-info.json` | 获取用户信息 |

### 考生模块 (Candidate Module)
| API路径 | 方法 | Mock文件 | 说明 |
|---------|------|----------|------|
| `/wx-miniprogram/candidate-info` | GET | `candidate/candidate-info.json` | 考生信息 |
| `/wx/candidate-info/:id` | GET | `candidate/candidate-detail.json` | 考生详情 |
| `/wx-miniprogram/exam-schedule` | GET | `candidate/exam-schedule.json` | 考试安排 |
| `/wx/my-qrcode/:id` | GET | `candidate/qrcode-data.json` | 考生二维码 |

### 二维码模块 (QR Code Module)
| API路径 | 方法 | Mock文件 | 说明 |
|---------|------|----------|------|
| `/qrcode/generate-schedule-qr/:id` | GET | `qrcode/generate-qr-success.json` | 生成考试二维码 |
| `/qrcode/scan-checkin` | POST | `qrcode/scan-checkin-success.json` | 扫码签到 |
| `/qrcode/checkin-status/:id` | GET | `qrcode/checkin-status.json` | 签到状态 |

### 实时数据模块 (Realtime Module)
| API路径 | 方法 | Mock文件 | 说明 |
|---------|------|----------|------|
| `/realtime/status` | GET | `realtime/realtime-status.json` | 实时状态 |
| `/realtime/public-board` | GET | `realtime/public-board.json` | 公共看板 |
| `/realtime/venue-status` | GET | `realtime/venue-status.json` | 考场状态 |

## 🔄 切换到真实API的步骤 (Switch to Real API)

### 方法1: 全局切换 (一键切换)
```javascript
// 修改 miniprogram/mock-data/config.js
const config = {
  useMockData: false,  // 改为false
  // ... 其他配置保持不变
}
```

### 方法2: 模块级切换 (渐进式切换)
```javascript
// 修改 miniprogram/mock-data/config.js
const config = {
  useMockData: true,
  moduleConfig: {
    auth: false,       // ✅ 认证模块使用真实API
    candidate: true,   // 🔄 考生模块仍使用Mock
    qrcode: true,      // 🔄 二维码模块仍使用Mock
    realtime: false    // ✅ 实时数据使用真实API
  }
}
```

### 方法3: 运行时切换
```javascript
// 在小程序中动态切换
const mockManager = require('./mock-data/index.js')

// 切换单个模块
mockManager.setModuleMock('auth', false)

// 全局切换
mockManager.setGlobalMock(false)
```

## 🛠️ 故障排除 (Troubleshooting)

### 常见问题

#### 1. Mock数据不生效
```javascript
// 检查配置
const config = require('./miniprogram/mock-data/config.js')
console.log('Mock enabled:', config.shouldUseMock())

// 检查模块配置
console.log('Auth mock:', config.shouldUseMock('auth'))
```

#### 2. 动态数据不更新
```javascript
// 清除缓存
const mockManager = require('./miniprogram/mock-data/index.js')
mockManager.clearCache()

// 检查动态数据配置
const config = require('./miniprogram/mock-data/config.js')
console.log('Dynamic data enabled:', config.get('mockBehavior').enableDynamicData)
```

#### 3. API路径不匹配
```javascript
// 检查路径映射
const { pathMatcher } = require('./miniprogram/mock-data/api-mapping.js')
const mapping = pathMatcher.matchPath('GET', '/your-api-path')
console.log('Path mapping:', mapping)
```

#### 4. 网络延迟过长
```javascript
// 调整延迟设置
// 在 miniprogram/mock-data/config.js 中
mockBehavior: {
  networkDelay: 100,  // 减少延迟到100ms
  // ...
}
```

### 调试技巧

#### 1. 启用详细日志
```javascript
// 在 miniprogram/mock-data/config.js 中
mockBehavior: {
  enableLogging: true,  // 启用日志
  // ...
}
```

#### 2. 检查Mock数据文件
```bash
# 验证JSON文件格式
node -e "console.log(JSON.parse(require('fs').readFileSync('./miniprogram/mock-data/auth/candidate-login-success.json', 'utf8')))"
```

#### 3. 测试特定API
```javascript
// 创建测试脚本
const mockManager = require('./miniprogram/mock-data/index.js')

async function testAPI() {
  const result = await mockManager.getMockResponse('/wx/login-by-idcard', 'POST', {
    id_card: '123456'
  })
  console.log('Test result:', result)
}

testAPI()
```

## 📊 性能优化 (Performance Optimization)

### 缓存管理
```javascript
// 启用缓存
mockBehavior: {
  enableCache: true,
  // ...
}

// 手动清除缓存
mockManager.clearCache()
```

### 网络延迟调优
```javascript
// 根据需要调整延迟
mockBehavior: {
  networkDelay: 200,  // 生产环境建议200-500ms
  // ...
}
```

## 🔒 安全注意事项 (Security Notes)

### 1. 生产环境配置
```javascript
// 生产环境必须关闭Mock
if (process.env.NODE_ENV === 'production') {
  config.useMockData = false
}
```

### 2. 敏感数据处理
```javascript
// Mock数据中不要包含真实的敏感信息
// 使用虚拟的身份证号、手机号等
```

### 3. Token安全
```javascript
// Mock Token应该有明显标识
tokenPrefix: 'mock_token_',  // 便于识别Mock数据
```

## 📝 最佳实践 (Best Practices)

### 1. Mock数据维护
- 定期同步API文档更新Mock数据
- 保持Mock数据结构与真实API一致
- 使用有意义的测试数据

### 2. 开发流程
- 开发阶段：100% 使用Mock
- 联调阶段：渐进式切换
- 测试阶段：混合模式验证
- 生产阶段：关闭Mock，保留备用能力

### 3. 团队协作
- 统一Mock数据格式
- 及时同步配置变更
- 建立Mock数据版本管理

## 🚨 应急处理 (Emergency Procedures)

### 真实API故障时快速切换到Mock
```javascript
// 紧急情况下快速启用Mock
const mockManager = require('./miniprogram/mock-data/index.js')
mockManager.setGlobalMock(true)

// 或者修改配置文件
// useMockData: true
```

### 回滚到之前的配置
```bash
# 恢复备份配置
cp miniprogram/mock-data/config.backup.js miniprogram/mock-data/config.js
```

## 📞 支持联系 (Support Contact)

如果遇到问题，请检查：
1. 配置文件是否正确
2. Mock数据文件是否存在
3. 控制台是否有错误日志
4. API路径映射是否正确

---

## 总结 (Summary)

这个Mock集成系统提供了：
- ✅ 完整的Mock数据管理
- ✅ 灵活的配置切换
- ✅ 动态数据生成
- ✅ 详细的调试信息
- ✅ 渐进式API对接
- ✅ 应急备用方案

通过这个系统，开发团队可以独立进行前端开发，并在需要时平滑切换到真实API。