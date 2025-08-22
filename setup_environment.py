#!/usr/bin/env python3
"""
环境设置脚本 - 为新部署设置环境配置
Environment Setup Script - Setup environment configuration for new deployment
"""

import os
import shutil
from pathlib import Path

def create_env_file():
    """创建环境配置文件"""
    env_content = """# 数据库配置
DATABASE_URL=mysql+pymysql://dev_user:a_good_password_for_dev@localhost:3307/exam_site_dev_db
MYSQL_USER=dev_user
MYSQL_PASSWORD=a_good_password_for_dev
MYSQL_DATABASE=exam_site_dev_db
MYSQL_ROOT_PASSWORD=a_very_strong_root_password
DB_HOST=localhost
DB_PORT=3307
DB_USER=dev_user
DB_PASSWORD=a_good_password_for_dev
DB_NAME=exam_site_dev_db
EXTERNAL_DB_PORT=3307

# Redis配置
REDIS_URL=redis://localhost:6379/0

# 应用配置
SECRET_KEY=your_secret_key_here_change_in_production
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=true

# 微信小程序配置
WECHAT_APP_ID=your_wechat_app_id
WECHAT_APP_SECRET=your_wechat_app_secret

# 文件上传配置
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760  # 10MB

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=app.log

# CORS配置
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# 邮件配置（可选）
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_email_password
SMTP_TLS=true"""

    backend_dir = Path("backend")
    if not backend_dir.exists():
        backend_dir.mkdir()
    
    env_path = backend_dir / ".env"
    
    if env_path.exists():
        print(f"⚠️  {env_path} 已存在，不会覆盖")
        return False
    
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print(f"✅ 创建环境配置文件: {env_path}")
    print("📝 请根据实际环境修改配置参数")
    return True

def main():
    """主函数"""
    print("🔧 UAV考试管理系统环境设置")
    print("=" * 40)
    
    create_env_file()
    
    print("\n📋 下一步操作:")
    print("1. 修改 backend/.env 中的配置参数")
    print("2. 运行 'docker-compose up -d' 启动服务")
    print("3. 运行 'python deployment_check.py' 验证部署")

if __name__ == "__main__":
    main()
