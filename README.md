# 无人机驾驶员考试管理系统 (Drone Pilot Exam Management System)

一个基于微信小程序的无人机驾驶员考试管理系统，提供考生报名、签到、考试管理和实时监控等功能。

## 📋 项目概述

本系统是一个完整的考试管理解决方案，包含考生端、考官端和公共展示端三个主要模块，支持二维码签到、实时数据监控、考试进度跟踪等功能。

### 🎯 主要功能

#### 考生端 (Candidate Portal)
- **用户认证**: 安全的登录注册系统
- **个人资料**: 完整的考生信息管理
- **考试安排**: 查看考试时间、地点和详细信息
- **二维码生成**: 动态生成签到二维码
- **考试历史**: 查看历史考试记录和成绩

#### 考官端 (Staff Portal)
- **工作人员登录**: 专用的考官认证系统
- **二维码扫描**: 高效的考生签到管理
- **实时监控**: 考场状态和考生进度监控
- **手动操作**: 支持手动输入和特殊情况处理
- **统计报告**: 实时统计和历史数据分析

#### 公共展示端 (Public Dashboard)
- **实时仪表板**: 考试进度和统计数据展示
- **考场状态**: 各考场实时状态监控
- **排队信息**: 考生排队和等待状态
- **系统通知**: 重要通知和公告展示

## 🏗️ 技术架构

### 前端技术栈
- **框架**: 微信小程序原生开发
- **语言**: JavaScript (ES6+)
- **样式**: WXSS (支持响应式设计和暗黑模式)
- **组件**: 自定义组件库 (骨架屏、加载动画等)

### 后端集成
- **API通信**: RESTful API设计
- **数据格式**: JSON数据交换
- **认证机制**: Token-based身份验证
- **错误处理**: 完善的错误处理和回退机制

### 数据管理
- **本地存储**: 微信小程序Storage API
- **缓存策略**: 智能缓存和数据同步
- **模拟数据**: 完整的Mock数据系统用于开发测试

## 📁 项目结构

```
miniprogram/
├── app.js                          # 小程序入口文件
├── app.json                        # 小程序配置文件
├── app.wxss                        # 全局样式文件
├── custom-tab-bar/                 # 自定义底部导航栏
│   ├── index.js
│   ├── index.wxml
│   ├── index.wxss
│   └── index.json
├── pages/                          # 页面目录
│   ├── index/                      # 首页
│   ├── candidate/                  # 考生端页面
│   │   ├── login/                  # 考生登录
│   │   ├── dashboard/              # 考生仪表板
│   │   ├── profile/                # 个人资料
│   │   ├── schedule/               # 考试安排
│   │   └── qrcode/                 # 二维码页面
│   ├── staff/                      # 考官端页面
│   │   ├── login/                  # 考官登录
│   │   └── scan/                   # 扫码管理
│   └── public/                     # 公共页面
│       └── dashboard/              # 公共仪表板
├── components/                     # 自定义组件
│   ├── skeleton/                   # 骨架屏组件
│   └── loading-animation/          # 加载动画组件
├── utils/                          # 工具函数
│   ├── api.js                      # API接口封装
│   ├── cache.js                    # 缓存管理
│   ├── loading.js                  # 加载状态管理
│   └── performance.js              # 性能优化工具
├── mock-data/                      # 模拟数据系统
│   ├── index.js                    # 数据入口
│   ├── config.js                   # 配置文件
│   ├── api-mapping.js              # API映射
│   ├── dynamic-generator.js        # 动态数据生成
│   ├── data-loader.js              # 数据加载器
│   ├── auth/                       # 认证相关数据
│   ├── candidate/                  # 考生相关数据
│   ├── qrcode/                     # 二维码相关数据
│   └── realtime/                   # 实时数据
├── images/                         # 图片资源
└── docs/                           # 项目文档
```

## 🚀 快速开始

### 环境要求
- 微信开发者工具 (最新版本)
- Node.js 14.0+ (用于开发工具)
- 微信小程序开发账号

### 安装步骤

1. **克隆项目**
   ```bash
   git clone [项目地址]
   cd miniprogram-4
   ```

2. **打开微信开发者工具**
   - 选择"导入项目"
   - 选择项目目录
   - 填入AppID (测试可使用测试号)

3. **配置项目**
   - 检查 `project.config.json` 配置
   - 确认 `app.json` 中的页面路径
   - 配置服务器域名 (开发阶段可跳过)

4. **启动项目**
   - 点击"编译"按钮
   - 选择不同的编译模式测试各个功能

### 测试账号

#### 考生测试账号
- **用户名**: `candidate001`
- **密码**: `123456`
- **姓名**: 张三
- **考试**: 无人机驾驶员理论考试

#### 考官测试账号
- **用户名**: `staff001`
- **密码**: `123456`
- **姓名**: 监考老师
- **部门**: 教务处

## 🔧 开发指南

### API接口

系统使用统一的API接口管理，位于 `utils/api.js`：

```javascript
// 考生API
const candidateAPI = {
  login: (username, password) => {},
  getProfile: () => {},
  getSchedule: () => {},
  generateQRCode: () => {}
}

// 考官API
const staffAPI = {
  login: (username, password) => {},
  scanQRCode: (qrCode) => {},
  getStats: () => {}
}

// 公共API
const publicAPI = {
  getDashboard: () => {},
  getVenueStatus: () => {},
  getNotifications: () => {}
}
```

### 模拟数据系统

项目包含完整的模拟数据系统，支持：
- 动态数据生成
- API请求模拟
- 网络状态模拟
- 错误场景测试

使用方式：
```javascript
// 在 mock-data/config.js 中配置
const config = {
  enabled: true,  // 启用模拟数据
  delay: 1000,    // 模拟网络延迟
  errorRate: 0.1  // 模拟错误率
}
```

### 自定义组件

#### 骨架屏组件
```xml
<skeleton loading="{{loading}}" rows="3" />
```

#### 加载动画组件
```xml
<loading-animation show="{{loading}}" type="ring" />
```

### 样式规范

项目采用统一的设计系统：
- **颜色**: 主色调 #1890ff，辅助色 #52c41a
- **字体**: 系统默认字体栈
- **间距**: 8px基础间距单位
- **圆角**: 4px基础圆角
- **阴影**: 统一的卡片阴影效果

## 📱 功能特性

### 🔐 安全特性
- Token-based身份验证
- 请求加密和签名验证
- 敏感数据本地加密存储
- 会话超时自动登出

### 🎨 用户体验
- 响应式设计，适配各种屏幕尺寸
- 暗黑模式支持
- 流畅的页面转场动画
- 智能加载状态和错误提示

### ⚡ 性能优化
- 图片懒加载和压缩
- 数据缓存和预加载
- 组件按需加载
- 网络请求优化和重试机制

### 🔄 实时功能
- 实时数据更新
- WebSocket连接支持
- 推送通知集成
- 离线数据同步

## 🧪 测试

### 功能测试
项目包含多个测试文件：
- `test-mock-integration.js` - 模拟数据集成测试
- `test-candidate-login-fix.js` - 考生登录功能测试
- `test-staff-login-final.js` - 考官登录功能测试
- `test-dashboard-final.js` - 仪表板功能测试

### 运行测试
```bash
# 在项目根目录运行
node test-mock-integration.js
node test-dashboard-final.js
```

## 📊 监控和分析

### 性能监控
- 页面加载时间统计
- API请求性能分析
- 用户行为数据收集
- 错误日志记录

### 数据分析
- 用户活跃度统计
- 功能使用情况分析
- 考试通过率统计
- 系统稳定性监控

## 🔄 版本更新

### v1.0.0 (当前版本)
- ✅ 基础功能完整实现
- ✅ 三端界面优化完成
- ✅ 模拟数据系统完善
- ✅ 性能优化和错误处理

### 计划功能
- 📋 考试成绩管理
- 📊 高级数据分析
- 🔔 消息推送系统
- 📱 多平台支持

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- 项目维护者: [维护者姓名]
- 邮箱: [联系邮箱]
- 项目地址: [GitHub地址]

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和测试人员。

---

**注意**: 这是一个演示项目，包含模拟数据用于开发和测试。在生产环境中使用前，请确保配置真实的后端API接口。