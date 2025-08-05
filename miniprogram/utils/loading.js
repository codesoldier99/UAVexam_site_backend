/**
 * 加载状态管理工具
 * 提供统一的加载状态管理和用户体验优化
 */

class LoadingManager {
  constructor() {
    this.loadingStates = new Map();
    this.globalLoading = false;
    this.loadingQueue = [];
    this.config = {
      // 最小显示时间，避免闪烁
      minShowTime: 300,
      // 延迟显示时间，避免快速请求的加载闪烁
      delayShowTime: 100,
      // 默认加载文案
      defaultTitle: '加载中...',
      // 骨架屏配置
      skeleton: {
        enabled: true,
        minHeight: 100
      }
    };
  }

  /**
   * 显示全局加载
   */
  showGlobal(title = this.config.defaultTitle, mask = true) {
    this.globalLoading = true;
    
    // 延迟显示，避免快速请求的闪烁
    setTimeout(() => {
      if (this.globalLoading) {
        wx.showLoading({
          title,
          mask
        });
      }
    }, this.config.delayShowTime);

    return this.createLoadingPromise('global');
  }

  /**
   * 隐藏全局加载
   */
  hideGlobal() {
    this.globalLoading = false;
    wx.hideLoading();
    this.resolveLoading('global');
  }

  /**
   * 显示页面级加载
   */
  showPage(pageId, options = {}) {
    const {
      title = this.config.defaultTitle,
      skeleton = this.config.skeleton.enabled,
      minShowTime = this.config.minShowTime
    } = options;

    const loadingState = {
      id: pageId,
      startTime: Date.now(),
      title,
      skeleton,
      minShowTime,
      visible: false
    };

    this.loadingStates.set(pageId, loadingState);

    // 延迟显示
    setTimeout(() => {
      const state = this.loadingStates.get(pageId);
      if (state && !state.hidden) {
        state.visible = true;
        this.updatePageLoading(pageId, true);
      }
    }, this.config.delayShowTime);

    return this.createLoadingPromise(pageId);
  }

  /**
   * 隐藏页面级加载
   */
  async hidePage(pageId) {
    const loadingState = this.loadingStates.get(pageId);
    if (!loadingState) return;

    const elapsedTime = Date.now() - loadingState.startTime;
    const remainingTime = Math.max(0, loadingState.minShowTime - elapsedTime);

    loadingState.hidden = true;

    // 确保最小显示时间
    setTimeout(() => {
      if (loadingState.visible) {
        this.updatePageLoading(pageId, false);
      }
      this.loadingStates.delete(pageId);
      this.resolveLoading(pageId);
    }, remainingTime);
  }

  /**
   * 更新页面加载状态
   */
  updatePageLoading(pageId, show) {
    const pages = getCurrentPages();
    const currentPage = pages[pages.length - 1];
    
    if (currentPage && currentPage.setData) {
      const updateData = {};
      updateData[`loading_${pageId}`] = show;
      
      // 如果启用骨架屏
      const loadingState = this.loadingStates.get(pageId);
      if (loadingState && loadingState.skeleton) {
        updateData[`skeleton_${pageId}`] = show;
      }
      
      currentPage.setData(updateData);
    }
  }

  /**
   * 创建加载Promise
   */
  createLoadingPromise(id) {
    return new Promise((resolve) => {
      this.loadingQueue.push({ id, resolve });
    });
  }

  /**
   * 解析加载Promise
   */
  resolveLoading(id) {
    const index = this.loadingQueue.findIndex(item => item.id === id);
    if (index !== -1) {
      const { resolve } = this.loadingQueue[index];
      this.loadingQueue.splice(index, 1);
      resolve();
    }
  }

  /**
   * 显示Toast加载
   */
  showToast(title, duration = 2000, icon = 'loading') {
    wx.showToast({
      title,
      icon,
      duration,
      mask: true
    });

    return new Promise((resolve) => {
      setTimeout(resolve, duration);
    });
  }

  /**
   * 显示成功Toast
   */
  showSuccess(title = '操作成功', duration = 1500) {
    return this.showToast(title, duration, 'success');
  }

  /**
   * 显示错误Toast
   */
  showError(title = '操作失败', duration = 2000) {
    return this.showToast(title, duration, 'error');
  }

  /**
   * 批量加载管理
   */
  async batchLoading(tasks, options = {}) {
    const {
      concurrent = 3,
      showProgress = false,
      progressTitle = '加载中'
    } = options;

    let completed = 0;
    const total = tasks.length;
    const results = [];

    if (showProgress) {
      this.showGlobal(`${progressTitle} 0/${total}`);
    }

    // 分批执行任务
    for (let i = 0; i < tasks.length; i += concurrent) {
      const batch = tasks.slice(i, i + concurrent);
      const batchPromises = batch.map(async (task, index) => {
        try {
          const result = await task();
          completed++;
          
          if (showProgress) {
            wx.showLoading({
              title: `${progressTitle} ${completed}/${total}`,
              mask: true
            });
          }
          
          return { success: true, data: result, index: i + index };
        } catch (error) {
          completed++;
          
          if (showProgress) {
            wx.showLoading({
              title: `${progressTitle} ${completed}/${total}`,
              mask: true
            });
          }
          
          return { success: false, error, index: i + index };
        }
      });

      const batchResults = await Promise.all(batchPromises);
      results.push(...batchResults);
    }

    if (showProgress) {
      this.hideGlobal();
    }

    return results;
  }

  /**
   * 获取加载状态
   */
  getLoadingState(pageId) {
    return this.loadingStates.get(pageId) || null;
  }

  /**
   * 检查是否正在加载
   */
  isLoading(pageId) {
    if (pageId) {
      const state = this.loadingStates.get(pageId);
      return state && state.visible && !state.hidden;
    }
    return this.globalLoading || this.loadingStates.size > 0;
  }

  /**
   * 清空所有加载状态
   */
  clearAll() {
    this.globalLoading = false;
    this.loadingStates.clear();
    this.loadingQueue.forEach(item => item.resolve());
    this.loadingQueue = [];
    wx.hideLoading();
  }

  /**
   * 创建骨架屏数据
   */
  createSkeletonData(config = {}) {
    const {
      rows = 3,
      avatar = false,
      title = true,
      paragraph = true
    } = config;

    const skeletonItems = [];
    
    for (let i = 0; i < rows; i++) {
      skeletonItems.push({
        id: i,
        avatar: avatar && i === 0,
        title: title,
        paragraph: paragraph,
        lines: Math.floor(Math.random() * 3) + 1
      });
    }

    return skeletonItems;
  }
}

// 创建全局加载管理器实例
const loadingManager = new LoadingManager();

// 导出加载管理器和便捷方法
module.exports = {
  loadingManager,
  
  // 便捷方法
  loading: {
    // 全局加载
    show: (title, mask) => loadingManager.showGlobal(title, mask),
    hide: () => loadingManager.hideGlobal(),
    
    // 页面加载
    showPage: (pageId, options) => loadingManager.showPage(pageId, options),
    hidePage: (pageId) => loadingManager.hidePage(pageId),
    
    // Toast
    success: (title, duration) => loadingManager.showSuccess(title, duration),
    error: (title, duration) => loadingManager.showError(title, duration),
    toast: (title, duration, icon) => loadingManager.showToast(title, duration, icon),
    
    // 批量加载
    batch: (tasks, options) => loadingManager.batchLoading(tasks, options),
    
    // 状态查询
    isLoading: (pageId) => loadingManager.isLoading(pageId),
    getState: (pageId) => loadingManager.getLoadingState(pageId),
    
    // 骨架屏
    skeleton: (config) => loadingManager.createSkeletonData(config),
    
    // 清理
    clear: () => loadingManager.clearAll()
  }
};