// 测试修复后的工作人员登录流程
const mockManager = require('./miniprogram/mock-data/index.js');

console.log('=== 测试工作人员登录修复 ===');

async function testStaffLoginFlow() {
  try {
    console.log('\n1. 测试工作人员登录API...');
    const loginResponse = await mockManager.getMockResponse('/auth/jwt/login', 'POST', {
      username: 'admin',
      password: '123456',
      user_type: 'staff'
    });
    
    console.log('登录响应:', JSON.stringify(loginResponse, null, 2));
    
    if (loginResponse && loginResponse.access_token) {
      console.log('✅ 登录API返回正确的token结构');
      console.log('Token:', loginResponse.access_token);
    } else {
      console.log('❌ 登录API返回结构异常');
      return;
    }
    
    console.log('\n2. 测试获取用户信息API...');
    const userInfoResponse = await mockManager.getMockResponse('/auth/user/info', 'GET');
    
    console.log('用户信息响应:', JSON.stringify(userInfoResponse, null, 2));
    
    if (userInfoResponse && userInfoResponse.data && userInfoResponse.data.role) {
      console.log('✅ 用户信息API返回正确结构');
      console.log('用户角色:', userInfoResponse.data.role);
      console.log('用户类型:', userInfoResponse.data.user_type);
    } else {
      console.log('❌ 用户信息API返回结构异常');
      return;
    }
    
    console.log('\n=== 工作人员登录流程测试完成 ===');
    console.log('✅ 登录API现在返回正确的token结构');
    console.log('✅ 用户信息API返回正确的用户数据');
    console.log('✅ 工作人员登录应该能正常工作了');
    
  } catch (error) {
    console.error('❌ 测试失败:', error.message);
    console.error('错误详情:', error);
  }
}

testStaffLoginFlow();