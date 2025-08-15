# 无人机考点运营与流程管理系统

## 项目简介

本系统是一个专注于无人机考点现场后勤与流程管理的综合解决方案，旨在解决考点现场管理混乱、信息不透明、考生焦虑以及运营效率低下的问题。

## 系统架构

```
uav-exam-complete/
├── backend/               # FastAPI后端服务
│   ├── app/
│   │   ├── api/          # API路由
│   │   ├── core/         # 核心配置
│   │   ├── db/           # 数据库相关
│   │   ├── models/       # 数据模型
│   │   ├── schemas/      # Pydantic模式
│   │   └── services/     # 业务逻辑
│   ├── alembic/          # 数据库迁移
│   └── requirements.txt  # Python依赖
│
├── admin-frontend/        # Vue 3 PC管理后台
│   ├── src/
│   │   ├── views/        # 页面组件
│   │   ├── components/   # 通用组件
│   │   ├── api/          # API接口
│   │   └── router/       # 路由配置
│   └── package.json
│
├── miniprogram/          # 微信小程序
│   ├── pages/            # 页面
│   ├── components/       # 组件
│   └── utils/            # 工具函数
│
└── docker-compose.yml    # Docker配置
```

## 核心功能

### 1. PC管理后台
- **超级管理员**：用户管理、系统配置
- **考务管理员**：考场管理、排期管理、考务监控
- **培训机构**：考生报名、批量导入、信息管理

### 2. 微信小程序
- **考生端**：查看日程、显示二维码、查看排队状态
- **考务人员端**：扫码签到、流程确认
- **公共看板**：实时考场动态

### 3. 后端服务
- RESTful API设计
- JWT认证授权
- RBAC权限管理
- 实时数据同步

## 技术栈

- **后端**：Python 3.10+, FastAPI, SQLAlchemy, MySQL 8.0
- **PC前端**：Vue 3, Element Plus, Axios
- **小程序**：原生微信小程序框架
- **部署**：Docker, Nginx, PM2

## 快速开始

### 1. 环境准备

```bash
# 安装Python依赖
cd backend
pip install -r requirements.txt

# 安装前端依赖
cd ../admin-frontend
npm install

# 配置数据库
cp .env.example .env
# 编辑.env文件，配置数据库连接
```

### 2. 启动服务

```bash
# 启动后端服务
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 启动PC管理后台
cd admin-frontend
npm run dev

# 小程序开发
# 使用微信开发者工具打开miniprogram目录
```

### 3. Docker部署

```bash
docker-compose up -d
```

## 默认账号

- 超级管理员：admin / admin123
- 考务管理员：examadmin / exam123
- 培训机构：institution / inst123
- 考务人员：staff / staff123

## API文档

启动后端服务后访问：http://localhost:8000/docs

## 部署说明

详见 [部署指南](./docs/deployment.md)

## 许可证

MIT License

## 联系方式

如有问题，请联系项目维护团队。