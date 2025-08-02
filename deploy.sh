#!/bin/bash

# 生产环境部署脚本
echo "🚀 开始部署考试系统后端到腾讯云CVM..."

# 检查环境变量
if [ -z "$MYSQL_ROOT_PASSWORD" ]; then
    echo "❌ 错误: 请设置 MYSQL_ROOT_PASSWORD 环境变量"
    exit 1
fi

if [ -z "$SECRET_KEY" ]; then
    echo "❌ 错误: 请设置 SECRET_KEY 环境变量"
    exit 1
fi

if [ -z "$MYSQL_DATABASE" ]; then
    export MYSQL_DATABASE=exam_site_db_prod
fi

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p logs/nginx
mkdir -p nginx/ssl
mkdir -p mysql/init

# 停止现有容器
echo "🛑 停止现有容器..."
docker-compose -f docker-compose.prod.yml down

# 构建并启动容器
echo "🔨 构建并启动容器..."
docker-compose -f docker-compose.prod.yml up -d --build

# 等待数据库启动
echo "⏳ 等待数据库启动..."
sleep 30

# 运行数据库迁移
echo "🗄️ 运行数据库迁移..."
docker-compose -f docker-compose.prod.yml exec app python -m alembic upgrade head

# 检查服务状态
echo "🔍 检查服务状态..."
docker-compose -f docker-compose.prod.yml ps

echo "✅ 部署完成！"
echo "📊 服务状态:"
echo "   - FastAPI应用: http://localhost"
echo "   - API文档: http://localhost/docs"
echo "   - 健康检查: http://localhost/health" 