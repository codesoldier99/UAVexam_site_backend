#!/usr/bin/env python3
"""
测试导入脚本
"""

try:
    print("测试导入 schemas...")
    from app.schemas.wechat import WeChatLoginResponse, ExamScheduleInfo, QRCodeData, CheckInResponse
    print("✅ schemas 导入成功")
    
    print("测试导入 wechat_service...")
    from app.services.wechat_service import WeChatService
    print("✅ WeChatService 导入成功")
    
    print("测试导入 routes...")
    from app.routes.wechat import router
    print("✅ wechat routes 导入成功")
    
    print("🎉 所有导入测试通过！")
    
except Exception as e:
    print(f"❌ 导入失败: {e}")
    import traceback
    traceback.print_exc()