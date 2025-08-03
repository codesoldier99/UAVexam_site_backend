@echo off
echo 🚀 考试系统后端部署测试
echo ========================

echo.
echo 📝 请先尝试以下SSH连接（选择一个）:
echo 1. ssh root@106.52.214.54
echo 2. ssh ubuntu@106.52.214.54  
echo 3. ssh admin@106.52.214.54
echo.

echo 💡 连接成功后，在服务器上运行：
echo git clone https://github.com/codesoldier99/UAVexam_site_backend.git
echo cd UAVexam_site_backend
echo sudo bash 一键部署脚本.sh
echo.

echo 🧪 部署完成后测试：
echo curl http://106.52.214.54/health
echo.

pause