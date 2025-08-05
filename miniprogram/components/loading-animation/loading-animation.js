Component({
  properties: {
    // 是否显示加载动画
    show: {
      type: Boolean,
      value: false
    },
    
    // 动画类型: pulse, spinner, wave, progress
    type: {
      type: String,
      value: 'pulse'
    },
    
    // 加载文本
    text: {
      type: String,
      value: ''
    },
    
    // 进度值 (0-100)，仅在 type='progress' 时有效
    progress: {
      type: Number,
      value: 0
    },
    
    // 是否显示进度文本
    showText: {
      type: Boolean,
      value: true
    },
    
    // 自定义样式类
    customClass: {
      type: String,
      value: ''
    }
  },

  data: {
    // 内部状态
  },

  methods: {
    // 显示加载动画
    showLoading(options = {}) {
      const { type = 'pulse', text = '', progress = 0 } = options;
      
      this.setData({
        show: true,
        type,
        text,
        progress
      });
    },

    // 隐藏加载动画
    hideLoading() {
      this.setData({
        show: false
      });
    },

    // 更新进度
    updateProgress(progress) {
      if (this.data.type === 'progress') {
        this.setData({
          progress: Math.max(0, Math.min(100, progress))
        });
      }
    },

    // 更新文本
    updateText(text) {
      this.setData({
        text
      });
    }
  },

  observers: {
    // 监听进度变化，自动隐藏当进度达到100%
    'progress': function(newProgress) {
      if (this.data.type === 'progress' && newProgress >= 100) {
        setTimeout(() => {
          this.hideLoading();
        }, 500); // 延迟500ms隐藏，让用户看到完成状态
      }
    }
  },

  lifetimes: {
    attached() {
      // 组件实例被放入页面节点树后执行
    },

    detached() {
      // 组件实例被从页面节点树移除后执行
    }
  }
});