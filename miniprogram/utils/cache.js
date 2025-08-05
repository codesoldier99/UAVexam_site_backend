/**
 * 缓存管理工具
 * 提供多层级缓存策略和智能缓存管理
 */

class CacheManager {
  constructor() {
    this.memoryCache = new Map();
    this.cacheConfig = {
      // 缓存过期时间配置（毫秒）
      expireTime: {
        short: 5 * 60 * 1000,      // 5分钟
        medium: 30 * 60 * 1000,    // 30分钟
        long: 2 * 60 * 60 * 1000,  // 2小时
        persistent: 24 * 60 * 60 * 1000 // 24小时
      },
      // 最大缓存条目数
      maxMemoryItems: 100,
      // 存储键前缀
      storagePrefix: 'exam_cache_'
    };
  }

  /**
   * 生成缓存键
   */
  generateKey(namespace, key, params = {}) {
    const paramStr = Object.keys(params).length > 0 
      ? '_' + JSON.stringify(params).replace(/[{}":,]/g, '') 
      : '';
    return `${this.cacheConfig.storagePrefix}${namespace}_${key}${paramStr}`;
  }

  /**
   * 设置内存缓存
   */
  setMemoryCache(key, data, expireTime = this.cacheConfig.expireTime.short) {
    // 检查内存缓存大小限制
    if (this.memoryCache.size >= this.cacheConfig.maxMemoryItems) {
      // 删除最旧的缓存项
      const firstKey = this.memoryCache.keys().next().value;
      this.memoryCache.delete(firstKey);
    }

    this.memoryCache.set(key, {
      data,
      timestamp: Date.now(),
      expireTime
    });
  }

  /**
   * 获取内存缓存
   */
  getMemoryCache(key) {
    const cached = this.memoryCache.get(key);
    if (!cached) return null;

    // 检查是否过期
    if (Date.now() - cached.timestamp > cached.expireTime) {
      this.memoryCache.delete(key);
      return null;
    }

    return cached.data;
  }

  /**
   * 设置本地存储缓存
   */
  setStorageCache(key, data, expireTime = this.cacheConfig.expireTime.medium) {
    try {
      const cacheData = {
        data,
        timestamp: Date.now(),
        expireTime
      };
      wx.setStorageSync(key, JSON.stringify(cacheData));
    } catch (error) {
      console.warn('设置存储缓存失败:', error);
    }
  }

  /**
   * 获取本地存储缓存
   */
  getStorageCache(key) {
    try {
      const cached = wx.getStorageSync(key);
      if (!cached) return null;

      const cacheData = JSON.parse(cached);
      
      // 检查是否过期
      if (Date.now() - cacheData.timestamp > cacheData.expireTime) {
        wx.removeStorageSync(key);
        return null;
      }

      return cacheData.data;
    } catch (error) {
      console.warn('获取存储缓存失败:', error);
      return null;
    }
  }

  /**
   * 智能缓存获取（优先内存，后存储）
   */
  get(namespace, key, params = {}) {
    const cacheKey = this.generateKey(namespace, key, params);
    
    // 先尝试内存缓存
    let data = this.getMemoryCache(cacheKey);
    if (data) return data;

    // 再尝试存储缓存
    data = this.getStorageCache(cacheKey);
    if (data) {
      // 将存储缓存提升到内存缓存
      this.setMemoryCache(cacheKey, data);
      return data;
    }

    return null;
  }

  /**
   * 智能缓存设置
   */
  set(namespace, key, data, options = {}) {
    const {
      params = {},
      level = 'medium', // short, medium, long, persistent
      memoryOnly = false
    } = options;

    const cacheKey = this.generateKey(namespace, key, params);
    const expireTime = this.cacheConfig.expireTime[level];

    // 设置内存缓存
    this.setMemoryCache(cacheKey, data, expireTime);

    // 根据配置决定是否设置存储缓存
    if (!memoryOnly && level !== 'short') {
      this.setStorageCache(cacheKey, data, expireTime);
    }
  }

  /**
   * 删除缓存
   */
  remove(namespace, key, params = {}) {
    const cacheKey = this.generateKey(namespace, key, params);
    
    // 删除内存缓存
    this.memoryCache.delete(cacheKey);
    
    // 删除存储缓存
    try {
      wx.removeStorageSync(cacheKey);
    } catch (error) {
      console.warn('删除存储缓存失败:', error);
    }
  }

  /**
   * 清空指定命名空间的缓存
   */
  clearNamespace(namespace) {
    const prefix = `${this.cacheConfig.storagePrefix}${namespace}_`;
    
    // 清空内存缓存
    for (const key of this.memoryCache.keys()) {
      if (key.startsWith(prefix)) {
        this.memoryCache.delete(key);
      }
    }

    // 清空存储缓存
    try {
      const storageInfo = wx.getStorageInfoSync();
      storageInfo.keys.forEach(key => {
        if (key.startsWith(prefix)) {
          wx.removeStorageSync(key);
        }
      });
    } catch (error) {
      console.warn('清空存储缓存失败:', error);
    }
  }

  /**
   * 清空所有缓存
   */
  clearAll() {
    // 清空内存缓存
    this.memoryCache.clear();

    // 清空存储缓存
    try {
      const storageInfo = wx.getStorageInfoSync();
      storageInfo.keys.forEach(key => {
        if (key.startsWith(this.cacheConfig.storagePrefix)) {
          wx.removeStorageSync(key);
        }
      });
    } catch (error) {
      console.warn('清空所有存储缓存失败:', error);
    }
  }

  /**
   * 获取缓存统计信息
   */
  getStats() {
    const memorySize = this.memoryCache.size;
    let storageSize = 0;

    try {
      const storageInfo = wx.getStorageInfoSync();
      storageSize = storageInfo.keys.filter(key => 
        key.startsWith(this.cacheConfig.storagePrefix)
      ).length;
    } catch (error) {
      console.warn('获取存储统计失败:', error);
    }

    return {
      memorySize,
      storageSize,
      totalSize: memorySize + storageSize,
      maxMemoryItems: this.cacheConfig.maxMemoryItems
    };
  }

  /**
   * 缓存预热 - 预加载常用数据
   */
  async preload(preloadList = []) {
    for (const item of preloadList) {
      try {
        if (typeof item.loader === 'function') {
          const data = await item.loader();
          this.set(item.namespace, item.key, data, {
            level: item.level || 'medium',
            params: item.params || {}
          });
        }
      } catch (error) {
        console.warn(`预加载缓存失败 ${item.namespace}:${item.key}`, error);
      }
    }
  }
}

// 创建全局缓存管理器实例
const cacheManager = new CacheManager();

// 导出缓存管理器和便捷方法
module.exports = {
  cacheManager,
  
  // 便捷方法
  cache: {
    get: (namespace, key, params) => cacheManager.get(namespace, key, params),
    set: (namespace, key, data, options) => cacheManager.set(namespace, key, data, options),
    remove: (namespace, key, params) => cacheManager.remove(namespace, key, params),
    clear: (namespace) => cacheManager.clearNamespace(namespace),
    clearAll: () => cacheManager.clearAll(),
    stats: () => cacheManager.getStats(),
    preload: (list) => cacheManager.preload(list)
  }
};