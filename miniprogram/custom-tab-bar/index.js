Component({
  data: {
    selected: 0,
    color: "#646566",
    selectedColor: "#1989fa",
    userRole: 'candidate', // 默认为考生角色
    candidateList: [
      {
        pagePath: "/pages/candidate/qrcode/qrcode-enhanced",
        iconText: "⊞",
        text: "二维码"
      },
      {
        pagePath: "/pages/candidate/schedule/schedule",
        iconText: "☰",
        text: "考试安排"
      },
      {
        pagePath: "/pages/candidate/dashboard/dashboard",
        iconText: "◈",
        text: "实时看板"
      },
      {
        pagePath: "/pages/candidate/profile/profile",
        iconText: "◐",
        text: "个人信息"
      }
    ],
    staffList: [
      {
        pagePath: "/pages/staff/scan/scan",
        iconText: "📱",
        text: "签到"
      },
      {
        pagePath: "/pages/staff/dashboard/dashboard",
        iconText: "📊",
        text: "实时看板"
      }
    ],
    list: [] // 动态设置
  },
  
  attached() {
    // 初始化导航栏
    this.initTabBar();
  },
  
  methods: {
    // 初始化导航栏
    initTabBar() {
      try {
        // 获取用户角色
        const userRole = wx.getStorageSync('userRole') || 'candidate';
        const list = userRole === 'staff' ? this.data.staffList : this.data.candidateList;
        
        // 获取当前页面路径，设置对应的 selected 值
        const pages = getCurrentPages();
        let selected = 0;
        
        if (pages && pages.length > 0) {
          const currentPage = pages[pages.length - 1];
          if (currentPage && currentPage.route) {
            const currentPath = `/${currentPage.route}`;
            const foundIndex = list.findIndex(item => item.pagePath === currentPath);
            selected = foundIndex !== -1 ? foundIndex : 0;
          }
        }
        
        this.setData({
          userRole,
          list,
          selected
        });
      } catch (error) {
        console.warn('TabBar init error:', error);
        // 设置默认值
        this.setData({
          userRole: 'candidate',
          list: this.data.candidateList,
          selected: 0
        });
      }
    },
    
    // 更新用户角色
    updateUserRole(role) {
      const list = role === 'staff' ? this.data.staffList : this.data.candidateList;
      this.setData({
        userRole: role,
        list,
        selected: 0
      });
    },
    
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