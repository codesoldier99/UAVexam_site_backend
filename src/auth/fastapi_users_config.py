from typing import Optional, List
from fastapi import Depends, Request, HTTPException
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users import exceptions
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.base import Base
from src.models.user import User
from src.db.session import get_async_session
from src.core.config import settings

# JWT 配置
SECRET_KEY = settings.SECRET_KEY  # 使用统一的密钥配置
LIFETIME_SECONDS = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60  # 使用统一的过期时间配置

class UserManager(BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_KEY
    verification_token_secret = SECRET_KEY

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")
    
    def parse_id(self, value: str) -> int:
        """解析用户ID"""
        return int(value)
    
    async def create(
        self,
        user_create,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> User:
        """重写用户创建方法以处理自定义字段"""
        await self.validate_password(user_create.password, user_create)
        
        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()
        
        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        
        # 处理自定义字段
        if hasattr(user_create, 'role_id') and user_create.role_id is not None:
            user_dict['role_id'] = user_create.role_id
        else:
            user_dict['role_id'] = 3  # 默认使用角色ID 3 (user)
            
        if hasattr(user_create, 'institution_id') and user_create.institution_id is not None:
            user_dict['institution_id'] = user_create.institution_id
        else:
            user_dict['institution_id'] = 7  # 默认使用机构ID 7 (中国民航大学)
        
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        
        created_user = await self.user_db.create(user_dict)
        
        await self.on_after_register(created_user, request)
        
        return created_user
    
    async def authenticate(
        self, credentials
    ) -> Optional[User]:
        """重写认证方法以支持用户名登录"""
        # OAuth2PasswordRequestForm 有 username 字段，我们用它作为 email 或 username
        username_or_email = credentials.username
        
        # 首先尝试通过 email 查找用户
        user = await self.user_db.get_by_email(username_or_email)
        if user is None:
            # 如果找不到，尝试通过用户名查找
            # 使用原始SQL查询来查找用户名
            from sqlalchemy import select
            from src.models.user import User as UserModel
            
            stmt = select(UserModel).where(UserModel.username == username_or_email)
            result = await self.user_db.session.execute(stmt)
            user = result.scalar_one_or_none()
        
        if user is None:
            return None
        
        if not self.password_helper.verify_and_update(credentials.password, user.hashed_password):
            return None
        
        return user
    
    async def get_user_permissions(self, user: User) -> List[str]:
        """
        获取用户权限列表
        
        Args:
            user: 用户对象
            
        Returns:
            权限列表
        """
        permissions = []
        
        # 超级管理员拥有所有权限
        if user.is_superuser:
            permissions.extend([
                "user:read", "user:write", "user:delete",
                "institution:read", "institution:create", "institution:update", "institution:delete",
                "exam_product:read", "exam_product:create", "exam_product:update", "exam_product:delete",
                "venue:read", "venue:create", "venue:update", "venue:delete",
                "exam:read", "exam:write", "exam:delete",
                "admin:all"
            ])
        else:
            # 根据用户角色获取权限
            if user.role_id:
                # 这里应该从数据库查询角色权限
                # 暂时使用硬编码的权限映射
                role_permissions = {
                    1: [  # 机构管理员
                        "user:read", "user:write",
                        "institution:read", "institution:create", "institution:update", "institution:delete",
                        "exam_product:read", "exam_product:create", "exam_product:update", "exam_product:delete",
                        "venue:read", "venue:create", "venue:update", "venue:delete",
                        "exam:read", "exam:write"
                    ],
                    2: [  # 普通用户
                        "user:read", "exam:read"
                    ],
                }
                permissions.extend(role_permissions.get(user.role_id, ["user:read"]))
            else:
                # 默认权限
                permissions.append("user:read")
        
        return permissions

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)

# 认证后端配置
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_KEY, lifetime_seconds=LIFETIME_SECONDS)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# FastAPI Users 实例
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# 当前用户依赖
current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)

# 添加简单的Bearer token认证
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """简单的Bearer token认证"""
    try:
        # 验证JWT令牌
        jwt_strategy = get_jwt_strategy()
        user = await jwt_strategy.read_token(credentials.credentials)
        if user and user.is_active:
            return user
        else:
            raise HTTPException(status_code=401, detail="无效的认证令牌")
    except Exception as e:
        raise HTTPException(status_code=401, detail="认证失败") 