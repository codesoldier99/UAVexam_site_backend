import uvicorn
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("启动机构管理API服务器...")
    print("服务器将在 http://localhost:8000 运行")
    print("API文档地址: http://localhost:8000/docs")
    print("按 Ctrl+C 停止服务器")
    
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 