# 环境要求和版本一致性

## Python版本要求
**必须使用 Python 3.11.9**

### 版本检查
在开始开发前，请确认Python版本：
```bash
python --version
# 应该显示: Python 3.11.9
```

### 如果版本不匹配
1. 使用pyenv安装正确版本：
```bash
pyenv install 3.11.9
pyenv local 3.11.9
```

2. 或者下载官方Python 3.11.9：
https://www.python.org/downloads/release/python-3119/

## Docker环境
项目使用Docker确保环境一致性，Dockerfile已指定Python 3.11版本：
```dockerfile
FROM python:3.11-slim
```

## 依赖管理
- `backend/requirements.txt` - 主要依赖包和版本范围
- `backend/requirements.lock` - **完整锁定版本文件（推荐团队使用）**

### 使用锁定版本（推荐）
```bash
pip install -r backend/requirements.lock
```

### 使用主要依赖文件
```bash
pip install -r backend/requirements.txt
```

## 快速环境验证
运行以下命令验证环境：
```bash
# 检查Python版本
python --version

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r backend/requirements.txt

# 验证安装
python -c "import fastapi; print('FastAPI version:', fastapi.__version__)"
```

## 团队协作建议
1. 使用Docker进行开发和部署，确保环境完全一致
2. 提交前运行 `pip freeze > requirements.txt` 更新依赖版本
3. 使用 `.python-version` 文件确保pyenv用户使用正确版本
