from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.dependencies.get_db import get_db
from src.models.user import User
from src.auth.service import create_access_token, get_password_hash
from datetime import timedelta

router = APIRouter(
    prefix="/social",
    tags=["social authentication"],
    responses={404: {"description": "Not found"}},
)

class SocialAuthProvider:
    """社交认证提供者基类"""
    
    def __init__(self, name: str):
        self.name = name
    
    async def authenticate(self, token: str, db: Session) -> Optional[User]:
        """认证用户"""
        raise NotImplementedError
    
    def create_or_update_user(self, social_data: Dict[str, Any], db: Session) -> User:
        """创建或更新用户"""
        # 根据社交平台返回的数据创建或更新用户
        social_id = social_data.get("id")
        email = social_data.get("email")
        username = social_data.get("username", f"{self.name}_user_{social_id}")
        
        # 查找现有用户
        user = db.query(User).filter(
            (User.email == email) | (User.username == username)
        ).first()
        
        if user:
            # 更新现有用户信息
            user.email = email or user.email
            user.username = username or user.username
            db.commit()
            db.refresh(user)
            return user
        else:
            # 创建新用户
            hashed_password = get_password_hash(f"{self.name}_{social_id}_password")
            user = User(
                email=email,
                username=username,
                hashed_password=hashed_password,
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            return user

class WeChatAuthProvider(SocialAuthProvider):
    """微信认证提供者"""
    
    def __init__(self):
        super().__init__("wechat")
    
    async def authenticate(self, code: str, db: Session) -> Optional[User]:
        """微信认证"""
        # 这里需要实现微信 OAuth 认证逻辑
        # 1. 使用 code 换取 access_token
        # 2. 使用 access_token 获取用户信息
        # 3. 创建或更新用户
        
        # 示例实现（需要根据微信 API 文档完善）
        try:
            # 这里应该调用微信 API
            # social_data = await self.get_wechat_user_info(code)
            # return self.create_or_update_user(social_data, db)
            
            # 临时返回 None，等待微信 API 集成
            return None
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"微信认证失败: {str(e)}"
            )
    
    async def get_wechat_user_info(self, code: str) -> Dict[str, Any]:
        """获取微信用户信息"""
        # 这里需要实现微信 API 调用
        # 返回用户信息字典
        pass

# 创建微信认证提供者实例
wechat_provider = WeChatAuthProvider()

@router.post("/wechat/login")
async def wechat_login(code: str, db: Session = Depends(get_db)):
    """微信登录"""
    user = await wechat_provider.authenticate(code, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="微信认证失败"
        )
    
    # 生成访问令牌
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser
        }
    } 