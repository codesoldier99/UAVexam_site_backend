# 考试系统后端 (Exam Site Backend)

## 🚀 快速开始

### 一键启动
```bash
python quick_start.py
```

### 手动启动
```bash
# 1. 启动数据库
docker-compose up -d db

# 2. 等待数据库启动 (15秒)
Start-Sleep 15

# 3. 运行迁移
alembic upgrade head

# 4. 创建测试用户
python create_test_user.py

# 5. 启动服务器
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## 📋 项目状态

✅ **数据库连接** - 完全正常  
✅ **JWT认证** - 工作正常  
✅ **API服务** - 响应正常  
✅ **测试工具** - 可用  

## 🔧 技术栈

- **后端框架**: FastAPI
- **数据库**: MySQL 8.0 (Docker)
- **ORM**: SQLAlchemy
- **认证**: FastAPI-Users (JWT)
- **迁移**: Alembic
- **容器**: Docker

## 📊 测试信息

- **API地址**: http://localhost:8000
- **文档地址**: http://localhost:8000/docs
- **测试用户**: admin@exam.com / admin123

## 📁 重要文件

- `PROJECT_STATUS.md` - 详细项目状态
- `quick_start.py` - 一键启动脚本
- `simple_api_test.py` - API测试工具

## 🎯 下一步

查看 `PROJECT_STATUS.md` 了解详细进度和下一步开发计划。

---

*项目状态: 基础功能完整，可继续开发*
