# UAV考点运营管理系统 - 公网API地址

## 🌐 ngrok公网部署成功！

**公网基础地址**: `https://5583860500fb.ngrok-free.app`  
**部署时间**: 2025-08-26 10:42  
**区域**: Japan (jp)  
**状态**: ✅ 在线

---

## 📋 核心API接口

### 系统接口
| 接口名称 | 方法 | 公网地址 |
|---------|------|----------|
| 系统首页 | GET | https://5583860500fb.ngrok-free.app/ |
| 健康检查 | GET | https://5583860500fb.ngrok-free.app/api/v1/health |
| 系统信息 | GET | https://5583860500fb.ngrok-free.app/api/v1/system/info |
| API文档 | GET | https://5583860500fb.ngrok-free.app/docs |

### 认证接口
| 接口名称 | 方法 | 公网地址 |
|---------|------|----------|
| 管理员登录 | POST | https://5583860500fb.ngrok-free.app/api/v1/auth/login |

### 微信小程序接口
| 接口名称 | 方法 | 公网地址 |
|---------|------|----------|
| 微信登录 | POST | https://5583860500fb.ngrok-free.app/api/v1/wechat/login |
| 考生信息查询 | GET | https://5583860500fb.ngrok-free.app/api/v1/wechat/candidate/info-by-idcard?id_card=110101199001011234 |
| 看板数据 | GET | https://5583860500fb.ngrok-free.app/api/v1/wechat/dashboard |
| 考生日程 | GET | https://5583860500fb.ngrok-free.app/api/v1/wechat/candidate/schedule |
| 考生二维码 | GET | https://5583860500fb.ngrok-free.app/api/v1/wechat/candidate/qrcode |
| 考场状态 | GET | https://5583860500fb.ngrok-free.app/api/v1/wechat/venues/status |

### 公共接口（无需认证）
| 接口名称 | 方法 | 公网地址 |
|---------|------|----------|
| 公共考场状态 | GET | https://5583860500fb.ngrok-free.app/api/v1/public/venues/status |
| 微信小程序看板 | GET | https://5583860500fb.ngrok-free.app/api/v1/wechat/venues/dashboard |

---

## 🧪 API测试示例

### 1. 健康检查
```bash
curl https://5583860500fb.ngrok-free.app/api/v1/health
```

### 2. 管理员登录
```bash
curl -X POST https://5583860500fb.ngrok-free.app/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### 3. 查询考生信息（张三）
```bash
curl "https://5583860500fb.ngrok-free.app/api/v1/wechat/candidate/info-by-idcard?id_card=110101199001011234"
```

### 4. 获取微信看板数据
```bash
curl https://5583860500fb.ngrok-free.app/api/v1/wechat/dashboard
```

### 5. 获取公共考场状态
```bash
curl https://5583860500fb.ngrok-free.app/api/v1/public/venues/status
```

---

## 📱 微信小程序配置

### 小程序API配置文件更新
在 `miniprogram/utils/api.js` 中更新baseURL：

```javascript
// 开发环境使用ngrok公网地址
const baseURL = 'https://5583860500fb.ngrok-free.app/api/v1'

// 或者根据环境自动切换
const baseURL = process.env.NODE_ENV === 'production' 
  ? 'https://your-production-domain.com/api/v1'
  : 'https://5583860500fb.ngrok-free.app/api/v1'
```

### 微信小程序域名配置
在微信开发者工具中，需要将以下域名添加到合法域名列表：
- **request合法域名**: `https://5583860500fb.ngrok-free.app`

---

## 🔧 测试数据

### 测试账号
| 角色 | 用户名 | 密码 | 说明 |
|------|--------|------|------|
| 超级管理员 | admin | admin123 | 全部权限 |
| 机构管理员 | beijing_admin | 123456 | 北京机构 |
| 机构管理员 | shanghai_admin | 123456 | 上海机构 |
| 机构管理员 | shenzhen_admin | 123456 | 深圳机构 |

### 测试考生
| 姓名 | 身份证号 | 用户名 | 密码 |
|------|----------|--------|------|
| 张三 | 110101199001011234 | candidate_011234 | 011234 |
| 李四 | 110101199002022345 | candidate_022345 | 022345 |
| 王五 | 110101199003033456 | candidate_033456 | 033456 |

---

## 🚀 快速验证

### 方法1: 浏览器访问
直接在浏览器中打开：
- API文档: https://5583860500fb.ngrok-free.app/docs
- 健康检查: https://5583860500fb.ngrok-free.app/api/v1/health
- 系统信息: https://5583860500fb.ngrok-free.app/api/v1/system/info

### 方法2: 使用测试脚本
```bash
python complete_test_solution.py
# 然后输入: https://5583860500fb.ngrok-free.app
```

### 方法3: 微信开发者工具
1. 打开微信开发者工具
2. 修改 `miniprogram/utils/api.js` 中的baseURL
3. 编译并预览小程序
4. 测试各个功能模块

---

## ⚠️ 注意事项

### ngrok限制
- **免费版限制**: 每月40GB流量，最多1个并发隧道
- **会话时间**: 8小时后需要重新启动
- **域名变化**: 每次重启ngrok域名会变化

### 安全提醒
- 这是测试环境，不要在生产环境使用
- 公网地址可能被其他人访问，注意数据安全
- 建议只在开发测试期间使用

### 稳定性
- 如果连接中断，重新运行 `ngrok http 8000`
- 新的域名需要更新小程序配置
- 建议使用ngrok付费版获得固定域名

---

## 📞 技术支持

如果遇到问题：
1. 检查后端服务是否在8000端口运行
2. 确认ngrok连接状态正常
3. 验证API接口返回数据
4. 检查微信小程序域名配置

**当前部署状态**: ✅ 成功  
**最后更新**: 2025-08-26 10:42  
**有效期**: 直到ngrok会话结束