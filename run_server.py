#!/usr/bin/env python3
"""
修复事件循环问题的FastAPI启动脚本
"""
import asyncio
import uvicorn
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """主函数，确保事件循环正确启动"""
    try:
        # 检查是否已有事件循环
        try:
            loop = asyncio.get_running_loop()
            print(f"检测到运行中的事件循环: {loop}")
        except RuntimeError:
            print("没有运行中的事件循环，将创建新的")
            loop = None
        
        # 启动uvicorn服务器
        uvicorn.run(
            "src.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            reload_dirs=["src"],
            log_level="info",
            access_log=True,
            loop="asyncio"
        )
        
    except Exception as e:
        print(f"启动服务器时出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 