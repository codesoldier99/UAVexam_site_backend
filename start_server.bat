@echo off
echo 启动考试系统后端服务器...
echo.

REM 设置Python路径
set PYTHONPATH=%cd%

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请确保Python已安装并添加到PATH
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 检查依赖...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo 安装依赖...
    pip install -r requirements.txt
)

echo 启动服务器...
echo 服务器将在 http://localhost:8000 启动
echo Swagger UI 将在 http://localhost:8000/docs 可用
echo.

REM 使用修复的启动脚本
python run_server.py

pause 