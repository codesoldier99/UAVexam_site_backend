@echo off
echo 正在启动ngrok...
echo 如果遇到连接问题，请按Ctrl+C停止，然后重新运行此脚本

REM 确保停止之前的ngrok进程
taskkill /f /im ngrok.exe >nul 2>&1

REM 等待1秒
timeout /t 1 /nobreak >nul

REM 启动ngrok
echo 启动ngrok HTTP隧道到端口8000...
ngrok http 8000

pause