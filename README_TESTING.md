# 🧪 考试系统后端测试工具

## 📋 测试工具概览

本项目提供了完整的API测试环境，包括Postman测试集合、自动测试脚本和测试报告工具。

## 🚀 快速开始

### 1. 启动测试环境

```bash
# 进入项目目录
cd exam_site_backend

# 启动服务器
python start_dev.py

# 或者使用快速启动脚本
python quick_start_test.py
```

### 2. 检查环境状态

```bash
# 检查测试环境
python check_test_environment.py
```

### 3. 运行自动测试

```bash
# 运行自动API测试
python auto_test.py
```

## 📁 测试文件说明

### Postman测试文件
- `exam_site_backend.postman_collection.json` - Postman测试集合
- `exam_site_backend.postman_environment.json` - Postman环境配置
- `COMPLETE_POSTMAN_TEST_GUIDE.md` - 完整测试指南
- `POSTMAN_TEST_GUIDE.md` - 基础测试指南

### 自动测试脚本
- `auto_test.py` - 自动API测试脚本
- `quick_start_test.py` - 快速启动脚本
- `check_test_environment.py` - 环境检查脚本

### 测试报告模板
- `TEST_REPORT_TEMPLATE.md` - 测试报告模板

## 🔧 测试环境配置

### 环境变量
```bash
# 数据库配置
DATABASE_URL=mysql+pymysql://root:password@localhost:3307/exam_site_db
DB_HOST=localhost
DB_PORT=3307
DB_USER=root
DB_PASSWORD=password
DB_NAME=exam_site_db

# 应用配置
PROJECT_NAME=Exam Site Backend
DEBUG=True

# 安全配置
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 默认用户凭据
- **管理员:** admin@exam.com / admin123
- **普通用户:** user@exam.com / user123

## 📊 测试覆盖范围

### 认证管理
- ✅ 管理员登录
- ✅ 用户登录
- ✅ Token验证
- ✅ 权限检查

### 机构管理
- ✅ 创建机构
- ✅ 获取机构列表
- ✅ 获取机构详情
- ✅ 更新机构信息
- ✅ 删除机构
- ✅ 获取机构统计

### 考试产品管理
- ✅ 创建考试产品
- ✅ 获取产品列表
- ✅ 获取产品详情
- ✅ 更新产品信息
- ✅ 删除考试产品

### 考场资源管理
- ✅ 创建考场资源
- ✅ 获取资源列表
- ✅ 获取资源详情
- ✅ 更新资源信息
- ✅ 删除考场资源

### 权限测试
- ✅ 无权限访问测试
- ✅ 无效Token测试
- ✅ 过期Token测试

## 🎯 测试目标

### 功能完整性
- [ ] 所有CRUD操作正常
- [ ] 权限控制有效
- [ ] 数据验证正确
- [ ] 错误处理完善

### 接口规范
- [ ] RESTful API设计
- [ ] 标准HTTP状态码
- [ ] 统一响应格式
- [ ] 文档完整

### 安全性
- [ ] JWT认证有效
- [ ] 权限检查正确
- [ ] 数据保护到位
- [ ] 输入验证有效

## 📝 使用Postman测试

### 1. 导入文件
1. 打开Postman
2. 点击 "Import" 按钮
3. 选择 `exam_site_backend.postman_collection.json`
4. 再次点击 "Import" 按钮
5. 选择 `exam_site_backend.postman_environment.json`

### 2. 配置环境
1. 在右上角选择 "Exam Site Backend Environment" 环境
2. 确认环境变量已正确设置

### 3. 开始测试
1. 首先执行管理员登录
2. 按顺序测试各个功能模块
3. 记录测试结果

## 🔍 自动测试脚本

### auto_test.py
自动运行所有API测试，包括：
- 服务器状态检查
- 管理员登录测试
- 机构管理测试
- 考试产品测试
- 考场资源测试
- 权限测试

### 运行方式
```bash
python auto_test.py
```

### 输出结果
- 实时测试结果
- 响应时间统计
- 成功率统计
- 详细测试报告

## 📊 测试报告

### 生成测试报告
自动测试脚本会生成详细的JSON格式测试报告，包含：
- 测试用例名称
- 测试状态（PASS/FAIL/SKIP）
- 响应时间
- HTTP状态码
- 详细信息
- 时间戳

### 报告模板
使用 `TEST_REPORT_TEMPLATE.md` 模板记录手动测试结果。

## 🚨 常见问题

### 1. 服务器启动失败
```bash
# 检查依赖
pip install -r requirements.txt

# 检查数据库
python init_db.py

# 检查环境变量
cp env.example .env
```

### 2. 认证失败
- 确认用户凭据正确
- 检查数据库是否已初始化
- 验证JWT配置

### 3. 权限错误
- 确认用户角色设置
- 检查接口权限要求
- 验证Token格式

### 4. 连接错误
- 检查服务器是否运行
- 确认端口配置
- 检查防火墙设置

## 📞 技术支持

### 检查环境状态
```bash
python check_test_environment.py
```

### 查看服务器日志
```bash
python start_dev.py
```

### 重置数据库
```bash
python init_db.py
```

## 🎉 测试完成

测试完成后，您应该能够：
- ✅ 验证所有API功能正常
- ✅ 确认权限控制有效
- ✅ 检查数据验证正确
- ✅ 确保安全性符合要求

如果遇到任何问题，请检查：
1. 服务器日志输出
2. 数据库连接状态
3. 网络连接情况
4. 环境配置正确性 