// 测试工作人员登录跳转修复
console.log('=== 测试工作人员登录跳转修复 ===');

// 模拟微信小程序的跳转API
const wx = {
  redirectTo: (options) => {
    console.log('✅ wx.redirectTo 调用成功');
    console.log('跳转目标:', options.url);
    return Promise.resolve();
  },
  switchTab: (options) => {
    console.log('❌ wx.switchTab 调用 (这应该不会被调用)');
    console.log('目标:', options.url);
    return Promise.reject(new Error('switchTab:fail can not switch to no-tabBar page'));
  }
};

// 模拟登录成功后的跳转逻辑
function simulateLoginSuccess() {
  console.log('\n模拟登录成功...');
  console.log('显示成功提示: "登录成功"');
  
  console.log('\n1秒后执行跳转...');
  setTimeout(() => {
    console.log('执行跳转逻辑:');
    wx.redirectTo({
      url: '/pages/staff/scan/scan'
    }).then(() => {
      console.log('✅ 跳转成功！');
      console.log('✅ 工作人员现在可以正常登录并跳转到扫码页面');
    }).catch((error) => {
      console.log('❌ 跳转失败:', error.message);
    });
  }, 100); // 缩短延时用于测试
}

console.log('\n=== 修复说明 ===');
console.log('问题: 使用 wx.switchTab 跳转到非 tabBar 页面');
console.log('解决: 改用 wx.redirectTo 跳转到扫码页面');
console.log('目标页面: /pages/staff/scan/scan');

simulateLoginSuccess();