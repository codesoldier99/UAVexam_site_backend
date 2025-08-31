@echo off
echo ========================================
echo         ngrok 设置脚本
echo ========================================

echo.
echo 1. 请手动完成以下步骤：
echo.
echo 步骤1: 下载ngrok
echo   - 打开浏览器访问: https://ngrok.com/download
echo   - 点击 "Windows (64-bit)" 下载
echo   - 或直接访问: https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip
echo.
echo 步骤2: 解压ngrok
echo   - 将下载的zip文件解压到当前目录
echo   - 确保 ngrok.exe 在当前文件夹中
echo.
echo 步骤3: 注册ngrok账号
echo   - 访问: https://ngrok.com/signup
echo   - 注册免费账号并登录
echo   - 在Dashboard页面复制你的authtoken
echo.
echo 步骤4: 配置authtoken
echo   - 下载完成后，运行: ngrok config add-authtoken YOUR_TOKEN_HERE
echo   - 将 YOUR_TOKEN_HERE 替换为你的实际token
echo.
echo 步骤5: 启动ngrok
echo   - 确保你的后端服务运行在端口8000
echo   - 运行: ngrok http 8000
echo.
echo ========================================
echo 完成后，ngrok会显示公网地址，类似：
echo https://abc123.ngrok.io
echo ========================================

pause