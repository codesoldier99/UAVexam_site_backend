#!/usr/bin/env python3
"""
部署检查脚本 - 验证系统是否能够正常部署和运行
Deployment Check Script - Verify system can be properly deployed and run
"""

import os
import sys
import subprocess
import time
import requests
import json
from pathlib import Path

def check_file_exists(file_path):
    """检查文件是否存在"""
    if os.path.exists(file_path):
        print(f"✅ {file_path} 存在")
        return True
    else:
        print(f"❌ {file_path} 不存在")
        return False

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major == 3 and version.minor == 11:
        print(f"✅ Python版本正确: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python版本不正确: {version.major}.{version.minor}.{version.micro} (需要3.11)")
        return False

def check_docker_installation():
    """检查Docker是否安装"""
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker已安装: {result.stdout.strip()}")
            return True
        else:
            print("❌ Docker未安装或无法运行")
            return False
    except FileNotFoundError:
        print("❌ Docker未安装")
        return False

def check_docker_compose():
    """检查docker-compose是否可用"""
    try:
        result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker Compose已安装: {result.stdout.strip()}")
            return True
        else:
            # 尝试新版本的命令
            result = subprocess.run(['docker', 'compose', 'version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Docker Compose已安装: {result.stdout.strip()}")
                return True
            else:
                print("❌ Docker Compose未安装或无法运行")
                return False
    except FileNotFoundError:
        print("❌ Docker Compose未安装")
        return False

def check_required_files():
    """检查必需的部署文件"""
    required_files = [
        'docker-compose.yml',
        'backend/Dockerfile',
        'backend/requirements.txt',
        'backend/app/main.py',
        'backend/app/config/settings.py',
        'docker/mysql/init.sql',
        'docker/nginx/nginx.conf',
        '.gitignore'
    ]
    
    all_exist = True
    for file_path in required_files:
        if not check_file_exists(file_path):
            all_exist = False
    
    return all_exist

def check_environment_template():
    """检查环境配置模板"""
    env_example_path = 'backend/.env.example'
    if check_file_exists(env_example_path):
        print("✅ 发现环境配置模板")
        return True
    else:
        print("⚠️  未发现.env.example，需要手动配置环境变量")
        return False

def test_docker_build():
    """测试Docker镜像构建"""
    print("\n🔨 测试Docker镜像构建...")
    try:
        # 构建backend镜像
        result = subprocess.run([
            'docker', 'build', '-t', 'uav-exam-backend-test', './backend'
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Backend Docker镜像构建成功")
            
            # 清理测试镜像
            subprocess.run(['docker', 'rmi', 'uav-exam-backend-test'], 
                          capture_output=True, text=True)
            return True
        else:
            print(f"❌ Backend Docker镜像构建失败: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Docker构建超时")
        return False
    except Exception as e:
        print(f"❌ Docker构建出错: {e}")
        return False

def check_requirements_compatibility():
    """检查requirements.txt的兼容性"""
    requirements_path = 'backend/requirements.txt'
    if not os.path.exists(requirements_path):
        print("❌ requirements.txt不存在")
        return False
    
    with open(requirements_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否包含主要依赖
    required_packages = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'pymysql',
        'redis',
        'pydantic'
    ]
    
    missing_packages = []
    for package in required_packages:
        if package not in content.lower():
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ requirements.txt缺少关键依赖: {', '.join(missing_packages)}")
        return False
    else:
        print("✅ requirements.txt包含所有关键依赖")
        return True

def create_deployment_guide():
    """创建部署指南"""
    guide_content = """# UAV考试管理系统部署指南

## 前置要求
- Python 3.11
- Docker & Docker Compose
- Git

## 快速部署步骤

### 1. 克隆项目
```bash
git clone <repository-url>
cd UAV_EXAMv8
```

### 2. 环境配置
```bash
# 复制环境配置模板
cp backend/.env.example backend/.env

# 根据需要修改环境变量
# 编辑 backend/.env 文件
```

### 3. 启动服务
```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f backend
```

### 4. 初始化数据
```bash
# 等待数据库启动完成后，运行初始化脚本
docker-compose exec backend python init_test_data.py
```

### 5. 验证部署
访问以下URL验证部署：
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health
- 前端应用: http://localhost:3000

## 故障排除

### 数据库连接问题
```bash
# 检查数据库容器状态
docker-compose logs db

# 重启数据库服务
docker-compose restart db
```

### 后端服务问题
```bash
# 查看后端日志
docker-compose logs backend

# 重新构建后端镜像
docker-compose build backend
```

## 生产部署注意事项
1. 修改所有默认密码
2. 配置HTTPS证书
3. 设置适当的环境变量
4. 配置日志轮转
5. 设置监控和备份
"""
    
    with open('DEPLOYMENT_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("✅ 创建了部署指南: DEPLOYMENT_GUIDE.md")

def main():
    """主检查函数"""
    print("🚀 UAV考试管理系统部署检查")
    print("=" * 50)
    
    checks_passed = 0
    total_checks = 7
    
    # 检查Python版本
    if check_python_version():
        checks_passed += 1
    
    # 检查Docker安装
    if check_docker_installation():
        checks_passed += 1
    
    # 检查Docker Compose
    if check_docker_compose():
        checks_passed += 1
    
    # 检查必需文件
    if check_required_files():
        checks_passed += 1
    
    # 检查环境配置
    if check_environment_template():
        checks_passed += 1
    
    # 检查依赖兼容性
    if check_requirements_compatibility():
        checks_passed += 1
    
    # 测试Docker构建
    if test_docker_build():
        checks_passed += 1
    
    print("\n" + "=" * 50)
    print(f"检查完成: {checks_passed}/{total_checks} 项通过")
    
    if checks_passed == total_checks:
        print("🎉 系统部署检查通过！可以安全提交代码。")
        create_deployment_guide()
        return True
    else:
        print("⚠️  存在问题需要解决后再提交代码。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
