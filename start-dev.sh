#!/bin/bash

# 开发环境启动脚本

echo "========================================="
echo "无人机考点管理系统 - 开发环境启动"
echo "========================================="

# 使用PM2管理进程
if ! command -v pm2 &> /dev/null; then
    echo "安装PM2..."
    npm install -g pm2
fi

# 创建PM2配置文件
cat > ecosystem.config.js << 'EOF'
module.exports = {
  apps: [
    {
      name: 'uav-backend',
      cwd: './backend',
      script: 'uvicorn',
      args: 'app.main:app --reload --host 0.0.0.0 --port 8000',
      interpreter: 'python3',
      env: {
        DATABASE_URL: 'mysql+aiomysql://root:password@localhost:3306/uav_exam',
        SYNC_DATABASE_URL: 'mysql+pymysql://root:password@localhost:3306/uav_exam',
        SECRET_KEY: 'dev-secret-key-change-in-production',
        DEBUG: 'true'
      }
    },
    {
      name: 'uav-admin',
      cwd: './admin-frontend',
      script: 'npm',
      args: 'run dev -- --host 0.0.0.0 --port 3000',
      env: {
        VITE_API_BASE_URL: 'http://localhost:8000/api/v1'
      }
    }
  ]
}
EOF

# 安装依赖
echo "安装后端依赖..."
cd backend
pip install -r requirements.txt
cd ..

echo "安装前端依赖..."
cd admin-frontend
npm install
cd ..

# 启动MySQL和Redis（如果使用Docker）
echo "启动数据库服务..."
docker-compose up -d mysql redis

# 等待数据库启动
sleep 5

# 初始化数据库
echo "初始化数据库..."
cd backend
python -c "
from app.db.session import sync_engine
from app.db.base import Base
Base.metadata.create_all(bind=sync_engine)
print('数据库表创建完成')
"
cd ..

# 使用PM2启动服务
echo "启动服务..."
pm2 delete all 2>/dev/null || true
pm2 start ecosystem.config.js

# 显示服务状态
pm2 status

echo ""
echo "========================================="
echo "开发环境启动完成！"
echo "========================================="
echo "服务访问地址："
echo "- 管理后台: http://localhost:3000"
echo "- API文档: http://localhost:8000/docs"
echo ""
echo "查看日志："
echo "- pm2 logs uav-backend"
echo "- pm2 logs uav-admin"
echo ""
echo "停止服务："
echo "- pm2 stop all"
echo "========================================="