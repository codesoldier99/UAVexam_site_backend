#!/bin/bash

echo "考试产品接口测试脚本"
echo "========================"

# 检查Python环境
echo "检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "错误：未找到Python3，请先安装Python3"
    exit 1
fi

python3 --version

# 安装依赖
echo ""
echo "安装依赖包..."
pip3 install requests

# 运行测试
echo ""
echo "运行完整测试..."
python3 test_exam_products_api.py

echo ""
echo "测试完成"