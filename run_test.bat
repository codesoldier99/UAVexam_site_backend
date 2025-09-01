@echo off
echo 考试产品接口测试脚本
echo ========================

echo 检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo 错误：未找到Python，请先安装Python
    pause
    exit /b 1
)

echo.
echo 安装依赖包...
pip install requests

echo.
echo 运行完整测试...
python test_exam_products_api.py

echo.
echo 按任意键退出...
pause