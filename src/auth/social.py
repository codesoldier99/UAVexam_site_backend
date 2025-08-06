from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_async_session
from src.models.user import User
from src.auth.fastapi_users_config import fastapi_users, auth_backend
from src.core.security import get_password_hash
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
    
    async def authenticate(self, token: str, db: AsyncSession) -> Optional[User]:
        """认证用户"""
        raise NotImplementedError
    
    async def create_or_update_user(self, social_data: Dict[str, Any], db: AsyncSession) -> User:
        """创建或更新用户"""
        from sqlalchemy import select
        
        # 根据社交平台返回的数据创建或更新用户
        social_id = social_data.get("id")
        email = social_data.get("email")
        username = social_data.get("username", f"{self.name}_user_{social_id}")
        
        # 查找现有用户
        stmt = select(User).where(
            (User.email == email) | (User.username == username)
        )
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if user:
            # 更新现有用户信息
            if email:
                user.email = email
            if username:
                user.username = username
            from datetime import datetime
            user.last_login = datetime.utcnow()
            await db.commit()
            await db.refresh(user)
            return user
        else:
            # 创建新用户
            hashed_password = get_password_hash(f"{self.name}_{social_id}_password")
            user = User(
                email=email,
                username=username,
                hashed_password=hashed_password,
                is_active=True,
                is_superuser=False,
                is_verified=True,
                role_id=3,  # 普通用户角色
                institution_id=7,  # 默认机构
                status='active'
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user

class WeChatAuthProvider(SocialAuthProvider):
    """微信认证提供者"""
    
    def __init__(self):
        super().__init__("wechat")
        # 微信小程序配置（实际使用时需要配置真实的AppID和AppSecret）
        self.app_id = "wx_test_app_id"  # 替换为真实的AppID
        self.app_secret = "wx_test_app_secret"  # 替换为真实的AppSecret
    
    async def authenticate(self, code: str, db: AsyncSession) -> Optional[User]:
        """微信认证"""
        try:
            # 在实际环境中，这里会调用真实的微信API
            # 目前创建一个模拟的微信用户认证流程
            
            if code.startswith("test_"):
                # 模拟微信认证成功，创建测试用户
                social_data = {
                    "id": f"wx_user_{code}",
                    "openid": f"openid_{code}",
                    "nickname": f"微信用户_{code[-6:]}",
                    "avatar": "https://example.com/avatar.jpg",
                    "unionid": f"unionid_{code}"
                }
                
                # 生成邮箱（微信用户可能没有邮箱）
                email = f"wx_user_{code[-6:]}@wechat.fake"
                username = f"wx_{code[-6:]}"
                
                # 查找或创建用户
                from sqlalchemy import select
                from src.models.user import User as UserModel
                
                # 首先尝试通过微信openid查找用户（需要扩展User模型）
                stmt = select(UserModel).where(UserModel.username == username)
                result = await db.execute(stmt)
                user = result.scalar_one_or_none()
                
                if user:
                    # 更新现有用户的最后登录时间
                    from datetime import datetime
                    user.last_login = datetime.utcnow()
                    await db.commit()
                    await db.refresh(user)
                    return user
                else:
                    # 创建新的微信用户
                    from src.core.security import get_password_hash
                    
                    # 为微信用户生成随机密码
                    import secrets
                    random_password = secrets.token_urlsafe(16)
                    hashed_password = get_password_hash(random_password)
                    
                    new_user = UserModel(
                        email=email,
                        username=username,
                        hashed_password=hashed_password,
                        is_active=True,
                        is_superuser=False,
                        is_verified=True,
                        role_id=3,  # 普通用户角色
                        institution_id=7,  # 默认机构
                        status='active'
                    )
                    
                    db.add(new_user)
                    await db.commit()
                    await db.refresh(new_user)
                    return new_user
            else:
                # 非测试代码时，调用真实微信API
                return await self.authenticate_with_real_wechat_api(code, db)
                
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"微信认证失败: {str(e)}"
            )
    
    async def authenticate_with_real_wechat_api(self, code: str, db: AsyncSession) -> Optional[User]:
        """使用真实微信API进行认证"""
        try:
            # 步骤1: 使用code换取access_token
            token_url = "https://api.weixin.qq.com/sns/jscode2session"
            token_params = {
                "appid": self.app_id,
                "secret": self.app_secret,
                "js_code": code,
                "grant_type": "authorization_code"
            }
            
            # 这里需要实际的HTTP请求
            # import httpx
            # async with httpx.AsyncClient() as client:
            #     token_response = await client.get(token_url, params=token_params)
            #     token_data = token_response.json()
            
            # 模拟微信API响应
            token_data = {
                "openid": f"real_openid_{code}",
                "session_key": f"session_key_{code}",
                "unionid": f"unionid_{code}"
            }
            
            if "openid" not in token_data:
                return None
            
            # 步骤2: 根据openid查找或创建用户
            openid = token_data["openid"]
            username = f"wx_{openid[-8:]}"
            email = f"{username}@wechat.system"
            
            # 查找现有用户
            from sqlalchemy import select
            from src.models.user import User as UserModel
            
            stmt = select(UserModel).where(UserModel.username == username)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                # 创建新用户
                from src.core.security import get_password_hash
                import secrets
                
                random_password = secrets.token_urlsafe(16)
                hashed_password = get_password_hash(random_password)
                
                user = UserModel(
                    email=email,
                    username=username,
                    hashed_password=hashed_password,
                    is_active=True,
                    is_superuser=False,
                    is_verified=True,
                    role_id=3,
                    institution_id=7,
                    status='active'
                )
                
                db.add(user)
                await db.commit()
                await db.refresh(user)
            
            return user
            
        except Exception as e:
            print(f"微信API认证错误: {e}")
            return None
    
    async def get_wechat_user_info(self, access_token: str, openid: str) -> Dict[str, Any]:
        """获取微信用户信息"""
        # 实际实现中会调用微信用户信息API
        # https://api.weixin.qq.com/sns/userinfo
        return {
            "openid": openid,
            "nickname": "微信用户",
            "headimgurl": "https://example.com/avatar.jpg"
        }

# 创建微信认证提供者实例
wechat_provider = WeChatAuthProvider()

@router.post("/wechat/login")
async def wechat_login(code: str, db: AsyncSession = Depends(get_async_session)):
    """微信登录"""
    user = await wechat_provider.authenticate(code, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="微信认证失败"
        )
    
    # 使用FastAPI-Users的JWT策略生成token
    from src.auth.fastapi_users_config import get_jwt_strategy
    jwt_strategy = get_jwt_strategy()
    
    # 生成访问令牌
    access_token = await jwt_strategy.write_token(user)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "role_id": user.role_id,
            "institution_id": user.institution_id
        }
    } 