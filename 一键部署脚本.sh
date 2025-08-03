#!/bin/bash

echo "🚀 考试系统后端一键部署脚本"
echo "================================"

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    echo "❌ 请使用root权限运行此脚本"
    echo "请执行: sudo bash 一键部署脚本.sh"
    exit 1
fi

# 设置变量
PROJECT_DIR="/opt/exam_site_backend"
GITHUB_REPO="https://github.com/codesoldier99/UAVexam_site_backend.git"

echo "📍 开始部署考试系统后端..."

# 1. 更新系统
echo "🔄 更新系统包..."
apt update

# 2. 安装必要软件
echo "📦 安装必要软件..."
apt install -y git python3 python3-pip python3-venv curl

# 3. 安装Docker (如果没有)
if ! command -v docker &> /dev/null; then
    echo "🐳 安装Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    systemctl start docker
    systemctl enable docker
fi

# 4. 创建项目目录
echo "📁 创建项目目录..."
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# 5. 克隆项目 (如果不存在)
if [ ! -d ".git" ]; then
    echo "📥 克隆项目代码..."
    git clone $GITHUB_REPO .
else
    echo "🔄 更新项目代码..."
    git pull origin main
fi

# 6. 停止现有服务 (如果有)
echo "🛑 停止现有服务..."
pkill -f "python.*start_server.py" || true
docker-compose down 2>/dev/null || true

# 7. 设置环境变量
echo "⚙️ 设置环境变量..."
export HOST=0.0.0.0
export PORT=80
export DEBUG=False

# 8. 方案A: 直接Python部署 (简单快速)
echo "🐍 尝试Python直接部署..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 启动服务
echo "🚀 启动API服务..."
nohup python3 start_server.py > /var/log/exam_api.log 2>&1 &

# 等待启动
sleep 10

# 9. 测试服务
echo "🧪 测试服务..."
if curl -s http://localhost/health | grep -q "healthy"; then
    echo "✅ Python部署成功!"
    echo "📊 服务状态:"
    echo "   - API地址: http://106.52.214.54/"
    echo "   - API文档: http://106.52.214.54/docs"
    echo "   - 健康检查: http://106.52.214.54/health"
    echo "   - 日志文件: /var/log/exam_api.log"
else
    echo "❌ Python部署失败，尝试Docker部署..."
    
    # 方案B: Docker部署
    echo "🐳 尝试Docker部署..."
    docker-compose up -d --build
    
    sleep 20
    
    if curl -s http://localhost/health | grep -q "healthy"; then
        echo "✅ Docker部署成功!"
        echo "📊 服务状态:"
        echo "   - API地址: http://106.52.214.54/"
        echo "   - API文档: http://106.52.214.54/docs"
        echo "   - 容器状态: docker-compose ps"
        docker-compose ps
    else
        echo "❌ 部署失败，请检查错误日志"
        echo "📋 可用命令:"
        echo "   - 查看Python日志: tail -f /var/log/exam_api.log"
        echo "   - 查看Docker日志: docker-compose logs"
        echo "   - 检查端口占用: netstat -tlpn | grep :80"
        exit 1
    fi
fi

echo ""
echo "🎉 部署完成!"
echo "📝 重要信息:"
echo "   - 项目目录: $PROJECT_DIR"
echo "   - 访问地址: http://106.52.214.54/"
echo "   - API文档: http://106.52.214.54/docs"
echo ""
echo "🔧 管理命令:"
echo "   - 重启服务: systemctl restart docker 或 pkill python3 && cd $PROJECT_DIR && python3 start_server.py &"
echo "   - 查看日志: tail -f /var/log/exam_api.log"
echo "   - 更新代码: cd $PROJECT_DIR && git pull && 重启服务"