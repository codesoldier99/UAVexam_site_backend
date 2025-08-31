#!/usr/bin/env python3
"""
测试简单的修改密码接口
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class SimplePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

@app.post("/test-change-password")
async def test_change_password(request: SimplePasswordRequest):
    """测试修改密码接口"""
    
    # 基本验证
    if request.new_password != request.confirm_password:
        raise HTTPException(status_code=400, detail="密码不匹配")
    
    if len(request.new_password) < 6:
        raise HTTPException(status_code=400, detail="密码太短")
    
    return {
        "success": True,
        "message": "测试成功",
        "data": {
            "current_password": request.current_password,
            "new_password": request.new_password,
            "confirm_password": request.confirm_password
        }
    }

if __name__ == "__main__":
    print("启动测试服务器在端口8001...")
    uvicorn.run(app, host="127.0.0.1", port=8001)