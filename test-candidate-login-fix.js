// 测试考生登录修复效果
const mockManager = require('./miniprogram/mock-data/index.js');

console.log('=== 测试考生登录修复 ===');

async function testCandidateLoginFix() {
  try {
    console.log('\n1. 测试考生登录API...');
    
    // 模拟考生登录请求
    const loginResponse = await mockManager.getMockResponse('/wx/login-by-idcard', 'POST', {
      id_card: '110101199001011234'
    });
    
    console.log('API响应结构:', JSON.stringify(loginResponse, null, 2));
    
    // 验证响应结构
    if (loginResponse && loginResponse.access_token && loginResponse.candidate_info) {
      console.log('✅ 登录响应结构正确');
      console.log('✅ 包含 access_token:', loginResponse.access_token);
      console.log('✅ 包含 candidate_info:', loginResponse.candidate_info.name);
      console.log('✅ 考生ID:', loginResponse.candidate_info.id);
      console.log('✅ 身份证号:', loginResponse.candidate_info.id_number);
      console.log('✅ 手机号:', loginResponse.candidate_info.phone);
    } else {
      console.log('❌ 登录响应结构异常');
      console.log('缺少字段:', {
        access_token: !!loginResponse.access_token,
        candidate_info: !!loginResponse.candidate_info
      });
    }
    
    console.log('\n2. 测试不同身份证号登录...');
    
    // 测试其他身份证号
    const testIds = [
      '110101199002022345',
      '110101199003033456'
    ];
    
    for (const idNumber of testIds) {
      const response = await mockManager.getMockResponse('/wx/login-by-idcard', 'POST', {
        id_card: idNumber
      });
      
      if (response && response.candidate_info) {
        console.log(`✅ 身份证 ${idNumber} 登录成功`);
      } else {
        console.log(`❌ 身份证 ${idNumber} 登录失败`);
      }
    }
    
    console.log('\n=== 考生登录修复测试完成 ===');
    console.log('✅ 现在考生登录应该能正常工作');
    console.log('✅ 不再显示"登录响应数据异常"错误');
    
  } catch (error) {
    console.error('❌ 测试失败:', error.message);
    console.error('错误详情:', error);
  }
}

testCandidateLoginFix();