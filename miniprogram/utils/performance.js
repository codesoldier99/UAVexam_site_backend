/**
 * 性能监控工具
 * 提供性能指标收集、分析和优化建议
 */

class PerformanceMonitor {
  constructor() {
    this.metrics = new Map();
    this.observers = [];
    this.config = {
      // 是否启用性能监控
      enabled: true,
      // 采样率 (0-1)
      sampleRate: 0.1,
      // 性能阈值配置
      thresholds: {
        apiResponse: 3000,    // API响应时间阈值 (ms)
        pageLoad: 2000,       // 页面加载时间阈值 (ms)
        renderTime: 1000,     // 渲染时间阈值 (ms)
        memoryUsage: 50       // 内存使用率阈值 (%)
      },
      // 自动上报配置
      autoReport: {
        enabled: false,
        interval: 30000,      // 上报间隔 (ms)
        batchSize: 10         // 批量上报大小
      }
    };
    
    this.initMonitoring();
  }

  /**
   * 初始化监控
   */
  initMonitoring() {
    if (!this.config.enabled) return;

    // 监听小程序生命周期
    this.observeAppLifecycle();
    
    // 监听页面性能
    this.observePagePerformance();
    
    // 监听网络状态
    this.observeNetworkStatus();
    
    // 启动自动上报
    if (this.config.autoReport.enabled) {
      this.startAutoReport();
    }
  }

  /**
   * 开始性能计时
   */
  startTiming(name, category = 'custom') {
    if (!this.shouldSample()) return null;

    const timingId = `${category}_${name}_${Date.now()}`;
    const timing = {
      id: timingId,
      name,
      category,
      startTime: Date.now(),
      startMemory: this.getMemoryUsage()
    };

    this.metrics.set(timingId, timing);
    return timingId;
  }

  /**
   * 结束性能计时
   */
  endTiming(timingId, metadata = {}) {
    if (!timingId) return null;

    const timing = this.metrics.get(timingId);
    if (!timing) return null;

    const endTime = Date.now();
    const duration = endTime - timing.startTime;
    const endMemory = this.getMemoryUsage();

    const result = {
      ...timing,
      endTime,
      duration,
      endMemory,
      memoryDelta: endMemory - timing.startMemory,
      metadata,
      timestamp: new Date().toISOString()
    };

    // 检查性能阈值
    this.checkThreshold(result);
    
    // 存储结果
    this.storeMetric(result);
    
    // 清理临时数据
    this.metrics.delete(timingId);

    return result;
  }

  /**
   * 记录API性能
   */
  recordAPI(url, method, duration, status, size = 0) {
    if (!this.shouldSample()) return;

    const metric = {
      type: 'api',
      url,
      method,
      duration,
      status,
      size,
      timestamp: new Date().toISOString(),
      isSlowRequest: duration > this.config.thresholds.apiResponse
    };

    this.storeMetric(metric);
    
    // 检查慢请求
    if (metric.isSlowRequest) {
      this.reportSlowAPI(metric);
    }
  }

  /**
   * 记录页面性能
   */
  recordPageLoad(pagePath, loadTime, renderTime, dataSize = 0) {
    if (!this.shouldSample()) return;

    const metric = {
      type: 'page',
      pagePath,
      loadTime,
      renderTime,
      totalTime: loadTime + renderTime,
      dataSize,
      timestamp: new Date().toISOString(),
      isSlowPage: (loadTime + renderTime) > this.config.thresholds.pageLoad
    };

    this.storeMetric(metric);
    
    // 检查慢页面
    if (metric.isSlowPage) {
      this.reportSlowPage(metric);
    }
  }

  /**
   * 记录错误信息
   */
  recordError(error, context = {}) {
    const metric = {
      type: 'error',
      message: error.message || error,
      stack: error.stack,
      context,
      timestamp: new Date().toISOString(),
      userAgent: wx.getSystemInfoSync()
    };

    this.storeMetric(metric);
    console.error('性能监控捕获错误:', metric);
  }

  /**
   * 获取内存使用情况
   */
  getMemoryUsage() {
    try {
      const systemInfo = wx.getSystemInfoSync();
      return {
        used: systemInfo.memorySize || 0,
        total: systemInfo.totalMemorySize || 0,
        usage: systemInfo.memorySize && systemInfo.totalMemorySize 
          ? (systemInfo.memorySize / systemInfo.totalMemorySize * 100).toFixed(2)
          : 0
      };
    } catch (error) {
      return { used: 0, total: 0, usage: 0 };
    }
  }

  /**
   * 获取网络状态
   */
  getNetworkStatus() {
    return new Promise((resolve) => {
      wx.getNetworkType({
        success: (res) => {
          resolve({
            networkType: res.networkType,
            isConnected: res.networkType !== 'none'
          });
        },
        fail: () => {
          resolve({
            networkType: 'unknown',
            isConnected: true
          });
        }
      });
    });
  }

  /**
   * 监听应用生命周期
   */
  observeAppLifecycle() {
    const app = getApp();
    if (!app) return;

    // 记录应用启动时间
    const originalOnLaunch = app.onLaunch;
    app.onLaunch = function(options) {
      const startTime = Date.now();
      
      if (originalOnLaunch) {
        originalOnLaunch.call(this, options);
      }
      
      // 记录启动性能
      setTimeout(() => {
        const launchTime = Date.now() - startTime;
        this.recordPageLoad('app_launch', launchTime, 0);
      }, 0);
    }.bind(this);
  }

  /**
   * 监听页面性能
   */
  observePagePerformance() {
    // 这里可以通过页面生命周期钩子来监控页面性能
    // 由于小程序的限制，需要在具体页面中调用相关方法
  }

  /**
   * 监听网络状态
   */
  observeNetworkStatus() {
    wx.onNetworkStatusChange((res) => {
      this.storeMetric({
        type: 'network',
        networkType: res.networkType,
        isConnected: res.isConnected,
        timestamp: new Date().toISOString()
      });
    });
  }

  /**
   * 检查性能阈值
   */
  checkThreshold(metric) {
    const { category, duration } = metric;
    const threshold = this.config.thresholds[category];
    
    if (threshold && duration > threshold) {
      console.warn(`性能警告: ${category} 耗时 ${duration}ms 超过阈值 ${threshold}ms`);
      
      // 触发性能警告事件
      this.notifyObservers('threshold_exceeded', metric);
    }
  }

  /**
   * 存储性能指标
   */
  storeMetric(metric) {
    try {
      // 获取现有指标
      const existingMetrics = wx.getStorageSync('performance_metrics') || [];
      
      // 添加新指标
      existingMetrics.push(metric);
      
      // 限制存储数量，保留最新的1000条
      if (existingMetrics.length > 1000) {
        existingMetrics.splice(0, existingMetrics.length - 1000);
      }
      
      // 存储到本地
      wx.setStorageSync('performance_metrics', existingMetrics);
      
      // 通知观察者
      this.notifyObservers('metric_recorded', metric);
    } catch (error) {
      console.warn('存储性能指标失败:', error);
    }
  }

  /**
   * 获取性能报告
   */
  getPerformanceReport(timeRange = 24 * 60 * 60 * 1000) {
    try {
      const metrics = wx.getStorageSync('performance_metrics') || [];
      const cutoffTime = Date.now() - timeRange;
      
      // 过滤时间范围内的指标
      const filteredMetrics = metrics.filter(metric => 
        new Date(metric.timestamp).getTime() > cutoffTime
      );

      // 分类统计
      const report = {
        summary: {
          totalMetrics: filteredMetrics.length,
          timeRange: timeRange,
          generatedAt: new Date().toISOString()
        },
        api: this.analyzeAPIMetrics(filteredMetrics),
        page: this.analyzePageMetrics(filteredMetrics),
        error: this.analyzeErrorMetrics(filteredMetrics),
        network: this.analyzeNetworkMetrics(filteredMetrics)
      };

      return report;
    } catch (error) {
      console.error('生成性能报告失败:', error);
      return null;
    }
  }

  /**
   * 分析API指标
   */
  analyzeAPIMetrics(metrics) {
    const apiMetrics = metrics.filter(m => m.type === 'api');
    
    if (apiMetrics.length === 0) {
      return { count: 0, avgDuration: 0, slowRequests: 0 };
    }

    const durations = apiMetrics.map(m => m.duration);
    const slowRequests = apiMetrics.filter(m => m.isSlowRequest).length;

    return {
      count: apiMetrics.length,
      avgDuration: Math.round(durations.reduce((a, b) => a + b, 0) / durations.length),
      minDuration: Math.min(...durations),
      maxDuration: Math.max(...durations),
      slowRequests,
      slowRequestRate: ((slowRequests / apiMetrics.length) * 100).toFixed(2) + '%'
    };
  }

  /**
   * 分析页面指标
   */
  analyzePageMetrics(metrics) {
    const pageMetrics = metrics.filter(m => m.type === 'page');
    
    if (pageMetrics.length === 0) {
      return { count: 0, avgLoadTime: 0, slowPages: 0 };
    }

    const loadTimes = pageMetrics.map(m => m.totalTime || m.loadTime);
    const slowPages = pageMetrics.filter(m => m.isSlowPage).length;

    return {
      count: pageMetrics.length,
      avgLoadTime: Math.round(loadTimes.reduce((a, b) => a + b, 0) / loadTimes.length),
      minLoadTime: Math.min(...loadTimes),
      maxLoadTime: Math.max(...loadTimes),
      slowPages,
      slowPageRate: ((slowPages / pageMetrics.length) * 100).toFixed(2) + '%'
    };
  }

  /**
   * 分析错误指标
   */
  analyzeErrorMetrics(metrics) {
    const errorMetrics = metrics.filter(m => m.type === 'error');
    
    if (errorMetrics.length === 0) {
      return { count: 0, errorRate: '0%' };
    }

    // 按错误类型分组
    const errorTypes = {};
    errorMetrics.forEach(error => {
      const type = error.message || 'unknown';
      errorTypes[type] = (errorTypes[type] || 0) + 1;
    });

    return {
      count: errorMetrics.length,
      errorRate: ((errorMetrics.length / metrics.length) * 100).toFixed(2) + '%',
      topErrors: Object.entries(errorTypes)
        .sort(([,a], [,b]) => b - a)
        .slice(0, 5)
        .map(([type, count]) => ({ type, count }))
    };
  }

  /**
   * 分析网络指标
   */
  analyzeNetworkMetrics(metrics) {
    const networkMetrics = metrics.filter(m => m.type === 'network');
    
    if (networkMetrics.length === 0) {
      return { changes: 0, currentType: 'unknown' };
    }

    const networkTypes = {};
    networkMetrics.forEach(metric => {
      const type = metric.networkType;
      networkTypes[type] = (networkTypes[type] || 0) + 1;
    });

    const latestNetwork = networkMetrics[networkMetrics.length - 1];

    return {
      changes: networkMetrics.length,
      currentType: latestNetwork.networkType,
      isConnected: latestNetwork.isConnected,
      typeDistribution: networkTypes
    };
  }

  /**
   * 报告慢API
   */
  reportSlowAPI(metric) {
    console.warn('慢API检测:', {
      url: metric.url,
      method: metric.method,
      duration: metric.duration,
      threshold: this.config.thresholds.apiResponse
    });
  }

  /**
   * 报告慢页面
   */
  reportSlowPage(metric) {
    console.warn('慢页面检测:', {
      pagePath: metric.pagePath,
      totalTime: metric.totalTime,
      threshold: this.config.thresholds.pageLoad
    });
  }

  /**
   * 判断是否应该采样
   */
  shouldSample() {
    return Math.random() < this.config.sampleRate;
  }

  /**
   * 添加观察者
   */
  addObserver(callback) {
    this.observers.push(callback);
  }

  /**
   * 移除观察者
   */
  removeObserver(callback) {
    const index = this.observers.indexOf(callback);
    if (index > -1) {
      this.observers.splice(index, 1);
    }
  }

  /**
   * 通知观察者
   */
  notifyObservers(event, data) {
    this.observers.forEach(callback => {
      try {
        callback(event, data);
      } catch (error) {
        console.error('观察者回调执行失败:', error);
      }
    });
  }

  /**
   * 启动自动上报
   */
  startAutoReport() {
    setInterval(() => {
      this.uploadMetrics();
    }, this.config.autoReport.interval);
  }

  /**
   * 上传性能指标
   */
  async uploadMetrics() {
    try {
      const metrics = wx.getStorageSync('performance_metrics') || [];
      
      if (metrics.length === 0) return;

      // 批量上传
      const batchSize = this.config.autoReport.batchSize;
      const batches = [];
      
      for (let i = 0; i < metrics.length; i += batchSize) {
        batches.push(metrics.slice(i, i + batchSize));
      }

      for (const batch of batches) {
        // 这里可以调用API上传到服务器
        console.log('上传性能指标批次:', batch.length);
        
        // 上传成功后清理本地数据
        // wx.setStorageSync('performance_metrics', []);
      }
    } catch (error) {
      console.error('上传性能指标失败:', error);
    }
  }

  /**
   * 清理过期数据
   */
  cleanup(maxAge = 7 * 24 * 60 * 60 * 1000) {
    try {
      const metrics = wx.getStorageSync('performance_metrics') || [];
      const cutoffTime = Date.now() - maxAge;
      
      const validMetrics = metrics.filter(metric => 
        new Date(metric.timestamp).getTime() > cutoffTime
      );

      wx.setStorageSync('performance_metrics', validMetrics);
      
      console.log(`清理性能数据: 删除 ${metrics.length - validMetrics.length} 条过期记录`);
    } catch (error) {
      console.error('清理性能数据失败:', error);
    }
  }

  /**
   * 获取性能建议
   */
  getOptimizationSuggestions() {
    const report = this.getPerformanceReport();
    if (!report) return [];

    const suggestions = [];

    // API性能建议
    if (report.api.slowRequestRate > 20) {
      suggestions.push({
        type: 'api',
        level: 'high',
        message: `API慢请求率过高 (${report.api.slowRequestRate})，建议优化接口性能或增加缓存`
      });
    }

    // 页面性能建议
    if (report.page.slowPageRate > 15) {
      suggestions.push({
        type: 'page',
        level: 'medium',
        message: `页面加载慢比率过高 (${report.page.slowPageRate})，建议优化页面渲染逻辑`
      });
    }

    // 错误率建议
    if (parseFloat(report.error.errorRate) > 5) {
      suggestions.push({
        type: 'error',
        level: 'high',
        message: `错误率过高 (${report.error.errorRate})，需要及时修复相关问题`
      });
    }

    return suggestions;
  }
}

// 创建全局性能监控实例
const performanceMonitor = new PerformanceMonitor();

// 导出性能监控器和便捷方法
module.exports = {
  performanceMonitor,
  
  // 便捷方法
  perf: {
    // 计时
    start: (name, category) => performanceMonitor.startTiming(name, category),
    end: (timingId, metadata) => performanceMonitor.endTiming(timingId, metadata),
    
    // 记录
    recordAPI: (url, method, duration, status, size) => 
      performanceMonitor.recordAPI(url, method, duration, status, size),
    recordPage: (pagePath, loadTime, renderTime, dataSize) => 
      performanceMonitor.recordPageLoad(pagePath, loadTime, renderTime, dataSize),
    recordError: (error, context) => performanceMonitor.recordError(error, context),
    
    // 报告
    getReport: (timeRange) => performanceMonitor.getPerformanceReport(timeRange),
    getSuggestions: () => performanceMonitor.getOptimizationSuggestions(),
    
    // 工具
    getMemory: () => performanceMonitor.getMemoryUsage(),
    getNetwork: () => performanceMonitor.getNetworkStatus(),
    
    // 管理
    cleanup: (maxAge) => performanceMonitor.cleanup(maxAge),
    addObserver: (callback) => performanceMonitor.addObserver(callback),
    removeObserver: (callback) => performanceMonitor.removeObserver(callback)
  }
};
