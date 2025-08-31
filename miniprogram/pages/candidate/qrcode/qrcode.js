// pages/candidate/qrcode/qrcode.js
// This file now redirects to the enhanced QR code implementation
const app = getApp();

Page({
  data: {
    redirecting: true
  },

  onLoad: function() {
    // Since TabBar uses qrcode-enhanced, redirect using switchTab
    wx.switchTab({
      url: '/pages/candidate/qrcode/qrcode-enhanced',
      fail: (error) => {
        console.error('Failed to redirect to enhanced QR code page:', error);
        this.setData({
          redirecting: false,
          errorMessage: '无法加载增强版二维码页面'
        });
      }
    });
  },

  onShow: function() {
    if (typeof this.getTabBar === 'function' && this.getTabBar()) {
      this.getTabBar().setData({
        selected: 0
      });
    }
  }
});
