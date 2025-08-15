#!/bin/bash

# 无人机考点管理系统部署脚本

set -e

echo "========================================="
echo "无人机考点管理系统 - 自动部署脚本"
echo "========================================="

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "Docker未安装，请先安装Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 创建环境配置文件
if [ ! -f backend/.env ]; then
    echo "创建环境配置文件..."
    cp backend/.env.example backend/.env
    echo "请编辑 backend/.env 文件配置数据库和其他参数"
    read -p "配置完成后按Enter继续..."
fi

# 构建前端
echo "构建前端应用..."
cd admin-frontend
npm install
npm run build
cd ..

# 启动Docker容器
echo "启动Docker容器..."
docker-compose down
docker-compose up -d --build

# 等待数据库启动
echo "等待数据库启动..."
sleep 10

# 初始化数据库
echo "初始化数据库..."
docker-compose exec backend python -c "
from app.db.init_db import init_db
init_db()
print('数据库初始化完成')
"

# 显示服务状态
echo ""
echo "========================================="
echo "部署完成！"
echo "========================================="
echo "服务访问地址："
echo "- 管理后台: http://localhost:3000"
echo "- API文档: http://localhost:8000/docs"
echo "- 数据库: localhost:3306"
echo "- Redis: localhost:6379"
echo ""
echo "默认账号："
echo "- 超级管理员: admin / admin123"
echo "- 考务管理员: examadmin / exam123"
echo "- 培训机构: institution / inst123"
echo "========================================="

# 查看容器状态
docker-compose ps