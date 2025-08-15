# 无人机考点管理系统 - 部署指南

## 系统要求

### 服务器配置
- **操作系统**: Ubuntu 20.04 LTS 或 CentOS 7+ 
- **CPU**: 2核心以上
- **内存**: 4GB以上
- **硬盘**: 20GB以上可用空间
- **带宽**: 5Mbps以上

### 软件依赖
- Docker 20.10+
- Docker Compose 1.29+
- Node.js 18+ (开发环境)
- Python 3.10+ (开发环境)
- MySQL 8.0+
- Redis 7.0+
- Nginx 1.20+

## 腾讯云部署步骤

### 1. 服务器准备

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 验证安装
docker --version
docker-compose --version
```

### 2. 项目部署

```bash
# 克隆项目
git clone https://github.com/your-repo/uav-exam-complete.git
cd uav-exam-complete

# 配置环境变量
cp backend/.env.example backend/.env
# 编辑 backend/.env 文件，设置数据库密码、SECRET_KEY等

# 设置权限
chmod +x deploy.sh
chmod +x start-dev.sh

# 执行部署
./deploy.sh
```

### 3. 配置域名和SSL

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 获取SSL证书
sudo certbot --nginx -d your-domain.com

# 配置Nginx
sudo nano /etc/nginx/sites-available/uav-exam
```

Nginx配置示例：
```nginx
server {
    listen 80;
    listen [::]:80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # 管理后台
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4. 数据库配置

```sql
-- 创建数据库
CREATE DATABASE IF NOT EXISTS uav_exam CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户
CREATE USER 'uav_user'@'%' IDENTIFIED BY 'your_secure_password';

-- 授权
GRANT ALL PRIVILEGES ON uav_exam.* TO 'uav_user'@'%';
FLUSH PRIVILEGES;
```

### 5. 防火墙配置

```bash
# 开放必要端口
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 3306/tcp  # MySQL (仅内网)
sudo ufw allow 6379/tcp  # Redis (仅内网)
sudo ufw enable
```

## 微信小程序配置

### 1. 注册小程序
1. 访问 [微信公众平台](https://mp.weixin.qq.com/)
2. 注册小程序账号
3. 获取 AppID 和 AppSecret

### 2. 配置服务器域名
在小程序管理后台配置：
- 请求域名: `https://your-domain.com`
- socket域名: `wss://your-domain.com`
- uploadFile域名: `https://your-domain.com`
- downloadFile域名: `https://your-domain.com`

### 3. 上传代码
1. 使用微信开发者工具打开 `miniprogram` 目录
2. 修改 `app.js` 中的 `baseUrl` 为实际服务器地址
3. 上传代码并提交审核

## 监控和维护

### 查看日志
```bash
# Docker日志
docker-compose logs -f backend
docker-compose logs -f admin-frontend

# PM2日志（开发环境）
pm2 logs
```

### 备份数据库
```bash
# 备份
docker exec uav_exam_mysql mysqldump -u root -p uav_exam > backup_$(date +%Y%m%d).sql

# 恢复
docker exec -i uav_exam_mysql mysql -u root -p uav_exam < backup.sql
```

### 更新部署
```bash
# 拉取最新代码
git pull

# 重新构建并部署
docker-compose down
docker-compose up -d --build
```

## 性能优化

### 1. 数据库优化
- 添加适当的索引
- 配置查询缓存
- 定期清理过期数据

### 2. Redis缓存
- 缓存热点数据
- 设置合理的过期时间
- 使用Redis集群提高可用性

### 3. 前端优化
- 启用Gzip压缩
- 配置CDN加速
- 图片懒加载

## 故障排查

### 常见问题

1. **数据库连接失败**
   - 检查数据库服务是否启动
   - 验证连接字符串是否正确
   - 确认防火墙规则

2. **前端无法访问后端API**
   - 检查CORS配置
   - 验证Nginx代理配置
   - 查看后端日志

3. **小程序无法登录**
   - 检查AppID和AppSecret配置
   - 验证服务器域名配置
   - 查看小程序错误日志

## 技术支持

如遇到问题，请：
1. 查看项目Wiki
2. 提交Issue
3. 联系技术支持团队

## 安全建议

1. 定期更新系统和依赖包
2. 使用强密码和密钥
3. 启用防火墙和入侵检测
4. 定期备份数据
5. 监控系统日志
6. 限制数据库远程访问