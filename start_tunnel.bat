@echo off
chcp 65001
echo 🚀 启动考试系统后端API内网穿透
echo ================================================

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装，请先安装Python
    pause
    exit /b 1
)

REM 检查FastAPI服务是否运行
echo 🔍 检查FastAPI服务...
curl -s http://localhost:8000/ >nul 2>&1
if errorlevel 1 (
    echo ❌ FastAPI服务未运行
    echo 正在启动FastAPI服务...
    start "FastAPI服务" cmd /k "python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload"
    timeout /t 5 /nobreak >nul
)

REM 检查ngrok是否安装
ngrok version >nul 2>&1
if errorlevel 1 (
    echo ❌ ngrok未安装
    echo 正在安装ngrok...
    winget install Ngrok.Ngrok
    timeout /t 10 /nobreak >nul
)

REM 启动ngrok隧道
echo 🚀 启动ngrok隧道...
echo 正在启动隧道，请稍候...
start "ngrok隧道" cmd /k "ngrok http 8000"

REM 等待隧道启动
timeout /t 5 /nobreak >nul

REM 获取隧道URL
echo 🔍 获取隧道地址...
for /f "tokens=*" %%i in ('curl -s http://localhost:4040/api/tunnels ^| findstr "public_url"') do (
    set tunnel_url=%%i
)

echo.
echo 🎉 隧道启动成功！
echo.
echo 📋 分享给队友的信息：
echo API基础地址: 请查看上面的ngrok窗口
echo 示例接口: 基础地址 + /
echo API文档: 基础地址 + /docs
echo 测试接口: 基础地址 + /test
echo.
echo ⚠️  注意事项：
echo 1. 此地址仅在ngrok运行时有效
echo 2. 免费版ngrok每次重启地址会变化
echo 3. 建议使用付费版获得固定域名
echo.
echo 📄 API文档已生成: API_DOCUMENTATION.md
echo.
echo 🔄 按任意键停止隧道
pause

REM 停止所有相关进程
taskkill /f /im ngrok.exe >nul 2>&1
taskkill /f /im uvicorn.exe >nul 2>&1
echo ✅ 隧道已停止
pause 