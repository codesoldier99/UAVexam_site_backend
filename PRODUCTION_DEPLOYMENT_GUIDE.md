# 腾讯云CVM生产环境部署指南

## 架构概述

根据系统架构图，生产环境采用以下架构：
```
用户设备 → 腾讯云CVM → Nginx反向代理 → FastAPI应用 → MySQL数据库
```

## 部署前准备

### 1. 腾讯云CVM配置
- 操作系统：Ubuntu 20.04 LTS 或 CentOS 8
- 配置：2核4GB内存（推荐）
- 带宽：5Mbps以上
- 安全组：开放80、443端口

### 2. 域名配置
- 购买域名并解析到CVM公网IP
- 申请SSL证书（推荐使用腾讯云SSL证书）

### 3. 环境变量设置
在CVM上设置以下环境变量：
```bash
export MYSQL_ROOT_PASSWORD="your_secure_password"
export SECRET_KEY="your_secret_key_here"
export MYSQL_DATABASE="exam_site_db_prod"
export WECHAT_APP_ID="your_wechat_app_id"
export WECHAT_APP_SECRET="your_wechat_app_secret"
```

## 部署步骤

### 1. 安装Docker和Docker Compose
```bash
# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. 上传代码到CVM
```bash
# 在本地打包代码
tar -czf exam_site_backend.tar.gz exam_site_backend/

# 上传到CVM
scp exam_site_backend.tar.gz root@your_cvm_ip:/root/

# 在CVM上解压
cd /root
tar -xzf exam_site_backend.tar.gz
cd exam_site_backend
```

### 3. 配置SSL证书
```bash
# 创建SSL证书目录
mkdir -p nginx/ssl

# 将SSL证书文件复制到nginx/ssl目录
# cert.pem 和 key.pem
```

### 4. 修改Nginx配置
编辑 `nginx/nginx.conf`，将域名替换为实际域名：
```nginx
server_name your-domain.com www.your-domain.com;
```

### 5. 运行部署脚本
```bash
# 给部署脚本执行权限
chmod +x deploy.sh

# 运行部署
./deploy.sh
```

## 服务管理

### 启动服务
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 停止服务
```bash
docker-compose -f docker-compose.prod.yml down
```

### 查看日志
```bash
# 查看所有服务日志
docker-compose -f docker-compose.prod.yml logs

# 查看特定服务日志
docker-compose -f docker-compose.prod.yml logs app
docker-compose -f docker-compose.prod.yml logs nginx
```

### 重启服务
```bash
docker-compose -f docker-compose.prod.yml restart
```

## 监控和维护

### 1. 健康检查
访问 `https://your-domain.com/health` 检查服务状态

### 2. 日志监控
```bash
# 查看Nginx访问日志
tail -f logs/nginx/access.log

# 查看应用日志
docker-compose -f docker-compose.prod.yml logs -f app
```

### 3. 数据库备份
```bash
# 备份数据库
docker-compose -f docker-compose.prod.yml exec db mysqldump -u root -p exam_site_db_prod > backup.sql

# 恢复数据库
docker-compose -f docker-compose.prod.yml exec -T db mysql -u root -p exam_site_db_prod < backup.sql
```

## 性能优化

### 1. Nginx优化
- 启用Gzip压缩
- 配置静态文件缓存
- 启用HTTP/2

### 2. FastAPI优化
- 使用多进程模式（--workers 4）
- 启用连接池
- 配置缓存

### 3. MySQL优化
- 调整innodb_buffer_pool_size
- 启用查询缓存
- 优化索引

## 安全配置

### 1. 防火墙设置
```bash
# 只开放必要端口
ufw allow 22    # SSH
ufw allow 80    # HTTP
ufw allow 443   # HTTPS
ufw enable
```

### 2. SSL证书配置
- 使用Let's Encrypt免费证书
- 配置自动续期
- 启用HSTS

### 3. 数据库安全
- 使用强密码
- 限制数据库访问IP
- 定期备份

## 故障排除

### 1. 服务无法访问
```bash
# 检查容器状态
docker-compose -f docker-compose.prod.yml ps

# 检查端口占用
netstat -tlnp | grep :80
netstat -tlnp | grep :443
```

### 2. 数据库连接失败
```bash
# 检查数据库容器
docker-compose -f docker-compose.prod.yml logs db

# 测试数据库连接
docker-compose -f docker-compose.prod.yml exec app python -c "from src.db.session import SessionLocal; db = SessionLocal(); print('数据库连接正常')"
```

### 3. Nginx配置错误
```bash
# 检查Nginx配置
docker-compose -f docker-compose.prod.yml exec nginx nginx -t

# 查看Nginx错误日志
docker-compose -f docker-compose.prod.yml logs nginx
```

## 更新部署

### 1. 代码更新
```bash
# 停止服务
docker-compose -f docker-compose.prod.yml down

# 拉取最新代码
git pull origin main

# 重新构建并启动
docker-compose -f docker-compose.prod.yml up -d --build
```

### 2. 数据库迁移
```bash
# 运行数据库迁移
docker-compose -f docker-compose.prod.yml exec app python -m alembic upgrade head
```

## 总结

通过以上配置，您的考试系统后端将在腾讯云CVM上稳定运行，支持：
- ✅ 高可用性部署
- ✅ HTTPS安全访问
- ✅ 负载均衡和缓存
- ✅ 完整的监控和日志
- ✅ 自动化部署和更新 