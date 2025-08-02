# 🚀 快速开始指南

## 📋 环境准备

### 1. 激活虚拟环境
```bash
# 在 exam_site_backend 目录下
venv\Scripts\activate
```

### 2. 安装依赖
```bash
pip install requests
```

## 🚀 启动服务器

### 方法1：使用简单启动脚本
```bash
python start_server_simple.py
```

### 方法2：直接启动
```bash
python start_dev.py
```

## 🧪 测试API

### 方法1：交互式测试工具
```bash
python simple_api_test.py
```

选择菜单中的选项：
- `1` - 管理员登录
- `2` - 创建机构
- `3` - 获取机构列表
- `4` - 创建考试产品
- `5` - 创建考场资源
- `6` - 无权限访问测试
- `0` - 退出

### 方法2：自动测试
```bash
python auto_test.py
```

### 方法3：手动测试
参考 `SIMPLE_API_TEST_GUIDE.md` 文件进行手动测试

## 📊 测试流程

1. **启动服务器**
   ```bash
   python start_dev.py
   ```

2. **打开新终端，激活虚拟环境**
   ```bash
   venv\Scripts\activate
   ```

3. **运行测试工具**
   ```bash
   python simple_api_test.py
   ```

4. **按顺序测试**
   - 先选择 `1` 进行管理员登录
   - 然后选择其他选项测试各个功能

## 🔍 检查服务器状态

访问以下地址检查服务器是否正常运行：
- API文档：http://localhost:8000/docs
- 管理界面：http://localhost:8000/redoc

## 🚨 常见问题

### 1. 模块缺失错误
```bash
pip install requests
```

### 2. 虚拟环境未激活
```bash
venv\Scripts\activate
```

### 3. 服务器启动失败
- 检查端口8000是否被占用
- 检查数据库配置
- 查看错误日志

## 📝 测试记录

使用测试工具时，会显示：
- 请求详情
- 响应状态码
- 响应时间
- 响应内容

现在您可以开始测试API了！ 