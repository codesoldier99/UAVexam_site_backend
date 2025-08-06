Component({
  data: {
    selected: 0,
    color: "#646566",
    selectedColor: "#1989fa",
    list: [
      {
        pagePath: "/pages/candidate/qrcode/qrcode",
        iconText: "⊞",
        text: "二维码"
      },
      {
        pagePath: "/pages/candidate/schedule/schedule",
        iconText: "☰",
        text: "考试安排"
      },
      {
        pagePath: "/pages/public/dashboard/dashboard",
        iconText: "◈",
        text: "实时看板"
      },
      {
        pagePath: "/pages/candidate/profile/profile",
        iconText: "◐",
        text: "个人信息"
      }
    ]
  },
  
  attached() {
    // 获取当前页面路径，设置对应的 selected 值
    const pages = getCurrentPages();
    const currentPage = pages[pages.length - 1];
    const currentPath = `/${currentPage.route}`;
    
    const selected = this.data.list.findIndex(item => item.pagePath === currentPath);
    this.setData({
      selected: selected !== -1 ? selected : 0
    });
  },
  
  methods: {
    switchTab(e) {
      const data = e.currentTarget.dataset;
      const url = data.path;
      
      // 添加点击动画效果
      this.setData({
        selected: data.index
      });
      
      // 使用 wx.switchTab 进行页面切换
      wx.switchTab({
        url,
        success: () => {
          // 切换成功后的回调
          this.triggerEvent('tabchange', {
            index: data.index,
            pagePath: url
          });
        },
        fail: (err) => {
          console.error('Tab switch failed:', err);
        }
      });
    }
  }
});