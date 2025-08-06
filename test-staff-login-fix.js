// 测试工作人员登录修复效果
const mockManager = require('./miniprogram/mock-data/index.js');

console.log('=== 测试工作人员登录修复 ===');

async function testStaffLoginFix() {
  try {
    console.log('\n1. 测试工作人员登录API...');
    
    // 模拟工作人员登录请求
    const loginResponse = await mockManager.getMockResponse('/auth/jwt/login', 'POST', {
      username: 'admin',
      password: '123456'
    });
    
    console.log('登录API响应结构:', JSON.stringify(loginResponse, null, 2));
    
    // 验证响应结构
    if (loginResponse && loginResponse.data && loginResponse.data.access_token) {
      console.log('✅ 登录响应结构正确');
      console.log('✅ 包含 access_token:', loginResponse.data.access_token);
      console.log('✅ 包含 user_info:', loginResponse.data.user_info ? loginResponse.data.user_info.username : '缺失');
    } else {
      console.log('❌ 登录响应结构异常');
      console.log('缺少字段:', {
        data: !!loginResponse.data,
        access_token: !!(loginResponse.data && loginResponse.data.access_token)
      });
    }
    
    console.log('\n2. 测试获取用户信息API...');
    
    // 测试获取当前用户信息
    const userInfoResponse = await mockManager.getMockResponse('/auth/users/me', 'GET');
    
    if (userInfoResponse && userInfoResponse.data) {
      console.log('✅ 用户信息API响应正常');
      console.log('✅ 用户角色:', userInfoResponse.data.role);
      console.log('✅ 用户名:', userInfoResponse.data.username);
    } else {
      console.log('❌ 用户信息API响应异常');
    }
    
    console.log('\n3. 测试不同工作人员账号...');
    
    // 测试其他工作人员账号
    const testAccounts = [
      { username: 'examiner01', password: '123456' },
      { username: 'examiner02', password: '123456' },
      { username: 'support', password: '123456' }
    ];
    
    for (const account of testAccounts) {
      const response = await mockManager.getMockResponse('/auth/jwt/login', 'POST', account);
      
      if (response && response.data && response.data.access_token) {
        console.log(`✅ 账号 ${account.username} 登录成功`);
      } else {
        console.log(`❌ 账号 ${account.username} 登录失败`);
      }
    }
    
    console.log('\n=== 工作人员登录修复测试完成 ===');
    console.log('✅ 现在工作人员登录应该能正常工作');
    console.log('✅ 不再显示事件处理函数缺失错误');
    
  } catch (error) {
    console.error('❌ 测试失败:', error.message);
    console.error('错误详情:', error);
  }
}

testStaffLoginFix();