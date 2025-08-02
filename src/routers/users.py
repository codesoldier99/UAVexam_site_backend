from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.auth.fastapi_users_config import current_active_user, fastapi_users
from src.models.user import User
from src.models.role import Role
from src.models.permission import Permission, RolePermission
from src.schemas.user import UserRead, UserCreate, UserUpdate, UserStatus, UserLogin
from src.schemas.role import RoleRead, RoleWithPermissions
from src.dependencies.permissions import require_user_read
from src.db.session import get_db
from typing import List
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead

@router.post("/login", response_model=LoginResponse)
async def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    用户登录端点
    """
    # 查找用户
    user = db.query(User).filter(User.username == login_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # 验证密码
    from src.auth.fastapi_users_config import get_user_manager
    from src.db.session import get_async_session
    
    async for session in get_async_session():
        user_manager = await anext(get_user_manager(session))
        if not user_manager.password_helper.verify_and_update(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误"
            )
        break
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # 生成访问令牌
    from src.auth.fastapi_users_config import SECRET_KEY
    import jwt
    from datetime import datetime, timedelta
    
    access_token_expires = timedelta(minutes=30)
    access_token = jwt.encode(
        {"sub": str(user.id), "exp": datetime.utcnow() + access_token_expires},
        SECRET_KEY,
        algorithm="HS256"
    )
    
    # 更新最后登录时间
    user.last_login = datetime.utcnow()
    db.commit()
    
    return LoginResponse(
        access_token=access_token,
        user=UserRead(
            id=user.id,
            username=user.username,
            email=user.email,
            status=user.status,
            role_id=user.role_id,
            institution_id=user.institution_id,
            last_login=user.last_login,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    )

@router.get("/me", response_model=UserRead)
async def get_current_user_info(user: User = Depends(current_active_user), db: Session = Depends(get_db)):
    """
    获取当前登录用户的详细信息
    """
    # 获取用户角色信息
    role = db.query(Role).filter(Role.id == user.role_id).first()
    
    # 获取用户权限
    permissions = db.query(Permission).join(RolePermission).filter(
        RolePermission.role_id == user.role_id
    ).all()
    
    # 构建响应数据
    user_data = {
        "id": user.id,
        "username": user.username,
        "status": user.status,
        "role_id": user.role_id,
        "institution_id": user.institution_id,
        "last_login": user.last_login,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }
    
    return UserRead(**user_data)

@router.get("/", response_model=List[UserRead])
async def get_users_list(user: User = Depends(require_user_read), db: Session = Depends(get_db)):
    """
    获取用户列表（需要用户读取权限）
    """
    users = db.query(User).all()
    return users

@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
    user_id: int, 
    current_user: User = Depends(require_user_read),
    db: Session = Depends(get_db)
):
    """
    根据ID获取用户信息（需要用户读取权限）
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return user

@router.post("/", response_model=UserRead)
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(require_user_read),
    db: Session = Depends(get_db)
):
    """
    创建新用户
    """
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 创建新用户
    new_user = User(
        username=user_data.username,
        hashed_password=fastapi_users._user_manager.password_helper.hash(user_data.password),
        role_id=user_data.role_id,
        institution_id=user_data.institution_id,
        status=UserStatus.active
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(require_user_read),
    db: Session = Depends(get_db)
):
    """
    更新用户信息
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 更新字段
    update_data = user_data.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = fastapi_users._user_manager.password_helper.hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return user

@router.get("/roles/", response_model=List[RoleRead])
async def get_roles_list(db: Session = Depends(get_db)):
    """
    获取角色列表
    """
    roles = db.query(Role).all()
    return roles

@router.get("/roles/{role_id}", response_model=RoleWithPermissions)
async def get_role_with_permissions(role_id: int, db: Session = Depends(get_db)):
    """
    获取角色及其权限信息
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    # 获取角色权限
    permissions = db.query(Permission).join(RolePermission).filter(
        RolePermission.role_id == role_id
    ).all()
    
    role_data = {
        "id": role.id,
        "name": role.name,
        "created_at": role.created_at,
        "updated_at": role.updated_at,
        "permissions": [perm.name for perm in permissions]
    }
    
    return RoleWithPermissions(**role_data)
