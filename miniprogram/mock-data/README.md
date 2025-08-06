# 微信小程序模拟数据系统

## 概述

这是一个为微信小程序考试管理系统设计的完整模拟数据系统，支持动态数据生成、配置管理、错误模拟等功能。

## 系统架构

```
mock-data/
├── index.js              # 主管理器
├── config.js             # 配置管理
├── api-mapping.js        # API路径映射
├── data-loader.js        # 数据加载器
├── dynamic-generator.js  # 动态数据生成器
├── auth/                 # 认证相关数据
├── candidate/            # 考生相关数据
├── qrcode/              # 二维码相关数据
└── realtime/            # 实时状态数据
```

## 核心功能

### 1. 智能API映射
- 支持路径参数匹配（如 `/candidate/:id`）
- 自动区分成功/失败响应
- 支持多种HTTP方法

### 2. 动态数据生成
- 自动生成时间戳、Token、二维码等
- 支持模板变量替换（如 `{{timestamp}}`）
- 上下文相关的数据生成

### 3. 灵活配置管理
- 全局/模块级别的Mock开关
- 网络延迟模拟
- 错误率配置
- 日志控制

### 4. 缓存机制
- 自动缓存加载的数据
- 支持缓存清理和重新加载

## 使用方法

### 基本使用

```javascript
const mockManager = require('./mock-data/index.js')

// 获取Mock响应
const response = await mockManager.getMockResponse(
  '/wx/login-by-idcard',  // URL
  'POST',                 // HTTP方法
  { idcard: '123456' },   // 参数
  { userId: 12345 }       // 上下文
)
```

### 配置管理

```javascript
// 全局启用/禁用Mock
mockManager.setGlobalMock(true)

// 模块级别控制
mockManager.setModuleMock('auth', false)  // 禁用认证模块Mock
mockManager.setModuleMock('candidate', true)  // 启用考生模块Mock

// 清除缓存
mockManager.clearCache()
```

### 动态数据变量

在数据文件中可以使用以下动态变量：

- `{{timestamp}}` - 当前时间戳
- `{{token}}` - 生成的Token
- `{{qr_content}}` - 二维码内容
- `{{qr_url}}` - 二维码URL
- `{{expiry_time}}` - 过期时间
- `{{random_id}}` - 随机ID

## API端点映射

### 认证模块
- `POST /wx/login-by-idcard` - 考生登录
- `POST /auth/jwt/login` - 工作人员登录
- `GET /auth/users/me` - 获取用户信息

### 考生模块
- `GET /wx-miniprogram/candidate-info` - 获取考生信息
- `GET /wx/candidate-info/:id` - 获取考生详情
- `GET /wx-miniprogram/exam-schedule` - 获取考试安排
- `GET /wx/my-qrcode/:id` - 获取考生二维码
- `GET /wx-miniprogram/checkin-history` - 获取签到历史
- `GET /wx-miniprogram/exam-results` - 获取考试结果

### 二维码模块
- `GET /qrcode/generate-schedule-qr/:id` - 生成考试二维码
- `POST /qrcode/scan-checkin` - 扫描签到
- `GET /qrcode/checkin-status/:id` - 获取签到状态
- `POST /qrcode/manual-checkin` - 手动签到

### 实时数据模块
- `GET /realtime/status` - 获取实时状态
- `GET /realtime/public-board` - 获取公告板
- `GET /realtime/venue-status` - 获取考场状态
- `GET /realtime/system-status` - 获取系统状态
- `GET /realtime/queue-status/:id` - 获取队列状态
- `GET /realtime/venue-queue/:id` - 获取考场队列
- `GET /realtime/notifications` - 获取通知

## 配置选项

### 全局配置 (config.js)

```javascript
{
  globalMock: true,           // 全局Mock开关
  modules: {                  // 模块级别配置
    auth: true,
    candidate: true,
    qrcode: true,
    realtime: true
  },
  mockBehavior: {
    networkDelay: 500,        // 网络延迟(ms)
    errorRate: 0.1,           // 错误率(0-1)
    enableDynamicData: true,  // 启用动态数据
    enableLogging: true       // 启用日志
  }
}
```

## 数据文件格式

每个数据文件都应该导出标准格式的响应：

```javascript
module.exports = {
  success: true,              // 成功标志
  message: "操作成功",        // 响应消息
  error_code: null,           // 错误代码
  data: {                     // 响应数据
    // 具体数据内容
  },
  timestamp: "{{timestamp}}"  // 时间戳（支持动态变量）
}
```

## 测试

运行测试脚本验证系统功能：

```bash
node test-mock-system.js
```

## 注意事项

1. **微信小程序兼容性**: 所有代码都已适配微信小程序环境，移除了Node.js特有的依赖
2. **动态数据**: 使用动态变量时确保上下文信息完整
3. **缓存管理**: 开发时可能需要清除缓存来获取最新数据
4. **错误处理**: 系统会自动处理文件不存在等错误情况
5. **性能优化**: 数据文件会被缓存，避免重复加载

## 扩展

### 添加新的API端点

1. 在对应模块目录下创建数据文件
2. 在 `api-mapping.js` 中添加路径映射
3. 在 `data-loader.js` 中添加导入和映射

### 自定义动态数据生成器

在 `dynamic-generator.js` 中添加新的生成方法，并在 `replaceStringVariables` 方法中添加对应的变量处理。

## 版本历史

- v1.0.0 - 初始版本，支持基本Mock功能
- v1.1.0 - 添加动态数据生成
- v1.2.0 - 完善配置管理和缓存机制
- v1.3.0 - 微信小程序兼容性优化