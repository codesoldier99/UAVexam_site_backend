@echo off
echo ========================================
echo         启动 ngrok 映射
echo ========================================

echo.
echo 正在启动 ngrok，映射端口 8000 到公网...
echo.
echo 请确保：
echo 1. 您已经配置了 authtoken
echo 2. 后端服务正在端口 8000 运行
echo.
echo 启动中...
echo.

ngrok http 8000

echo.
echo ngrok 已停止运行
pause