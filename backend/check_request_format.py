#!/usr/bin/env python3
"""
检查请求格式问题
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json

app = FastAPI()

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """记录所有请求"""
    
    # 读取请求体
    body = await request.body()
    
    print(f"\n=== 请求信息 ===")
    print(f"方法: {request.method}")
    print(f"URL: {request.url}")
    print(f"头部: {dict(request.headers)}")
    print(f"请求体 (bytes): {body}")
    
    if body:
        try:
            body_str = body.decode('utf-8')
            print(f"请求体 (string): {body_str}")
            
            # 尝试解析JSON
            try:
                body_json = json.loads(body_str)
                print(f"请求体 (JSON): {json.dumps(body_json, indent=2, ensure_ascii=False)}")
                
                # 检查字段类型
                for key, value in body_json.items():
                    print(f"字段 '{key}': 值='{value}', 类型={type(value).__name__}")
                    
            except json.JSONDecodeError as e:
                print(f"JSON解析失败: {e}")
                
        except UnicodeDecodeError:
            print("请求体不是UTF-8编码")
    
    print("=" * 50)
    
    # 继续处理请求
    response = await call_next(request)
    return response

@app.post("/debug-change-password")
async def debug_change_password(request: Request):
    """调试修改密码请求"""
    
    try:
        body = await request.json()
        
        print(f"\n=== FastAPI解析结果 ===")
        print(f"解析后的数据: {body}")
        print(f"数据类型: {type(body)}")
        
        # 检查必需字段
        required_fields = ["current_password", "new_password", "confirm_password"]
        missing_fields = []
        
        for field in required_fields:
            if field not in body:
                missing_fields.append(field)
            else:
                value = body[field]
                print(f"字段 '{field}': 值='{value}', 类型={type(value).__name__}, 是否为空={value is None or value == ''}")
        
        if missing_fields:
            return {"error": f"缺少字段: {missing_fields}"}
        
        # 模拟Pydantic验证
        from pydantic import BaseModel, ValidationError
        
        class TestModel(BaseModel):
            current_password: str
            new_password: str
            confirm_password: str
        
        try:
            model = TestModel(**body)
            return {"success": True, "message": "验证通过", "data": model.model_dump()}
        except ValidationError as e:
            return {"error": "Pydantic验证失败", "details": e.errors()}
            
    except Exception as e:
        return {"error": f"处理异常: {str(e)}"}

if __name__ == "__main__":
    print("启动调试服务器在端口8002...")
    print("请将前端请求发送到: http://localhost:8002/debug-change-password")
    uvicorn.run(app, host="127.0.0.1", port=8002)