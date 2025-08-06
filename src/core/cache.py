"""
Redis缓存机制
提供高性能的数据缓存功能
"""

import json
import pickle
from typing import Any, Optional, Union, Callable
from functools import wraps
import redis
from redis import ConnectionPool
import hashlib
import logging
from src.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

class CacheManager:
    """缓存管理器"""
    
    def __init__(self):
        self.redis_client = None
        self._connect()
    
    def _connect(self):
        """连接Redis"""
        try:
            # 创建连接池
            pool = ConnectionPool(
                host=getattr(settings, 'REDIS_HOST', 'localhost'),
                port=getattr(settings, 'REDIS_PORT', 6379),
                db=getattr(settings, 'REDIS_DB', 0),
                password=getattr(settings, 'REDIS_PASSWORD', None),
                decode_responses=True,
                max_connections=20,
            )
            self.redis_client = redis.Redis(connection_pool=pool)
            
            # 测试连接
            self.redis_client.ping()
            logger.info("Redis连接成功")
            
        except Exception as e:
            logger.warning(f"Redis连接失败: {e}, 将使用内存缓存")
            self.redis_client = None
    
    def _generate_cache_key(self, prefix: str, *args, **kwargs) -> str:
        """生成缓存键"""
        # 将参数转换为字符串并生成哈希
        key_data = f"{prefix}:{str(args)}:{str(sorted(kwargs.items()))}"
        return f"venue_api:{hashlib.md5(key_data.encode()).hexdigest()}"
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if not self.redis_client:
            return None
        
        try:
            data = self.redis_client.get(key)
            if data:
                return json.loads(data)
        except Exception as e:
            logger.error(f"获取缓存失败: {e}")
        return None
    
    def set(self, key: str, value: Any, expire: int = 300) -> bool:
        """设置缓存"""
        if not self.redis_client:
            return False
        
        try:
            serialized_data = json.dumps(value, ensure_ascii=False, default=str)
            return self.redis_client.setex(key, expire, serialized_data)
        except Exception as e:
            logger.error(f"设置缓存失败: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """删除缓存"""
        if not self.redis_client:
            return False
        
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            logger.error(f"删除缓存失败: {e}")
            return False
    
    def delete_pattern(self, pattern: str) -> int:
        """删除匹配模式的缓存"""
        if not self.redis_client:
            return 0
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
        except Exception as e:
            logger.error(f"批量删除缓存失败: {e}")
        return 0
    
    def clear_venue_cache(self):
        """清除所有场地相关缓存"""
        try:
            return self.delete_pattern("venue_api:*")
        except Exception as e:
            logger.error(f"清除场地缓存失败: {e}")
            return 0

# 全局缓存管理器实例
cache_manager = CacheManager()

def cache_result(expire: int = 300, key_prefix: str = "default"):
    """
    缓存装饰器
    
    Args:
        expire: 过期时间（秒）
        key_prefix: 缓存键前缀
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = cache_manager._generate_cache_key(
                f"{key_prefix}:{func.__name__}", *args, **kwargs
            )
            
            # 尝试从缓存获取
            cached_result = cache_manager.get(cache_key)
            if cached_result is not None:
                logger.info(f"缓存命中: {cache_key}")
                return cached_result
            
            # 执行函数
            result = await func(*args, **kwargs)
            
            # 存储到缓存
            if result is not None:
                cache_manager.set(cache_key, result, expire)
                logger.info(f"结果已缓存: {cache_key}")
            
            return result
        
        return wrapper
    return decorator

def invalidate_cache_on_change(cache_patterns: list):
    """
    数据变更时清除缓存的装饰器
    
    Args:
        cache_patterns: 要清除的缓存模式列表
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 执行函数
            result = await func(*args, **kwargs)
            
            # 清除相关缓存
            for pattern in cache_patterns:
                deleted_count = cache_manager.delete_pattern(f"venue_api:*{pattern}*")
                if deleted_count > 0:
                    logger.info(f"已清除 {deleted_count} 个相关缓存 (模式: {pattern})")
            
            return result
        
        return wrapper
    return decorator

# 常用缓存配置
class CacheConfig:
    """缓存配置常量"""
    VENUE_LIST = {"expire": 300, "key": "venue_list"}      # 5分钟
    VENUE_DETAIL = {"expire": 600, "key": "venue_detail"}  # 10分钟
    VENUE_STATS = {"expire": 600, "key": "venue_stats"}    # 10分钟
    USER_PERMISSIONS = {"expire": 1800, "key": "user_perm"}  # 30分钟