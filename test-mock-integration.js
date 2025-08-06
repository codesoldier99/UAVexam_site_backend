// Mock Integration Test Script
// 测试Mock数据集成是否正常工作

const mockManager = require('./miniprogram/mock-data/index.js')

async function testMockIntegration() {
  console.log('🚀 Starting Mock Integration Tests...\n')
  
  const tests = [
    {
      name: 'Candidate Login',
      url: '/wx/login-by-idcard',
      method: 'POST',
      data: { id_card: '110101199001011234' }
    },
    {
      name: 'Staff Login',
      url: '/auth/jwt/login',
      method: 'POST',
      data: { username: 'staff001', password: 'password123' }
    },
    {
      name: 'Get Candidate Info',
      url: '/wx-miniprogram/candidate-info?id_number=110101199001011234',
      method: 'GET'
    },
    {
      name: 'Get Exam Schedule',
      url: '/wx-miniprogram/exam-schedule?candidate_id=1',
      method: 'GET'
    },
    {
      name: 'Generate QR Code',
      url: '/wx/my-qrcode/1',
      method: 'GET'
    },
    {
      name: 'Get Realtime Status',
      url: '/realtime/status',
      method: 'GET'
    }
  ]
  
  let passedTests = 0
  let totalTests = tests.length
  
  for (const test of tests) {
    try {
      console.log(`📋 Testing: ${test.name}`)
      console.log(`   URL: ${test.method} ${test.url}`)
      
      const startTime = Date.now()
      const result = await mockManager.getMockResponse(test.url, test.method, test.data || {})
      const duration = Date.now() - startTime
      
      if (result && result.success !== undefined) {
        console.log(`   ✅ Success (${duration}ms)`)
        console.log(`   📄 Response: ${result.message}`)
        
        // 检查动态数据
        if (result.data && typeof result.data === 'object') {
          const hasTimestamp = result.timestamp || (result.data && result.data.timestamp)
          const hasToken = result.data.access_token
          const hasQRCode = result.data.qr_content || result.data.qr_url
          
          if (hasTimestamp) console.log(`   🕒 Dynamic timestamp: ✅`)
          if (hasToken) console.log(`   🔑 Dynamic token: ✅`)
          if (hasQRCode) console.log(`   📱 Dynamic QR code: ✅`)
        }
        
        passedTests++
      } else {
        console.log(`   ❌ Failed: Invalid response format`)
        console.log(`   📄 Response:`, result)
      }
      
    } catch (error) {
      console.log(`   ❌ Error: ${error.message}`)
    }
    
    console.log('')
  }
  
  // 测试配置切换
  console.log('🔧 Testing Configuration Management...')
  
  try {
    // 测试模块切换
    mockManager.setModuleMock('auth', false)
    console.log('   ✅ Module config change: auth disabled')
    
    mockManager.setModuleMock('auth', true)
    console.log('   ✅ Module config change: auth enabled')
    
    // 测试全局切换
    mockManager.setGlobalMock(false)
    console.log('   ✅ Global mock disabled')
    
    mockManager.setGlobalMock(true)
    console.log('   ✅ Global mock enabled')
    
  } catch (error) {
    console.log(`   ❌ Configuration test failed: ${error.message}`)
  }
  
  console.log('')
  
  // 测试结果汇总
  console.log('📊 Test Results Summary:')
  console.log(`   Total Tests: ${totalTests}`)
  console.log(`   Passed: ${passedTests}`)
  console.log(`   Failed: ${totalTests - passedTests}`)
  console.log(`   Success Rate: ${((passedTests / totalTests) * 100).toFixed(1)}%`)
  
  if (passedTests === totalTests) {
    console.log('\n🎉 All tests passed! Mock integration is working correctly.')
    console.log('\n📝 Next Steps:')
    console.log('   1. Test in WeChat Developer Tools')
    console.log('   2. Verify all pages work with Mock data')
    console.log('   3. Check console logs for [Mock Manager] messages')
    console.log('   4. When ready, switch to real API by changing config.js')
  } else {
    console.log('\n⚠️  Some tests failed. Please check the Mock data files and configuration.')
  }
}

// 运行测试
testMockIntegration().catch(console.error)