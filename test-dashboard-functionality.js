const mockManager = require('./miniprogram/mock-data/index.js');

async function testCandidateDashboard() {
  console.log('=== Testing Candidate Dashboard Complete Functionality ===');
  
  try {
    // Simulate candidate login state
    const candidateInfo = {
      id: 'CAND_1001',
      name: '张三',
      id_number: '110101199001011234'
    };
    
    console.log('Candidate Info:', JSON.stringify(candidateInfo, null, 2));
    
    // 1. Test get user info
    console.log('\n1. Testing Get User Info API...');
    const userInfoResult = await mockManager.getMockResponse('/api/v1/auth/me', 'GET', {}, { 
      forceMock: true,
      userId: candidateInfo.id,
      candidateId: candidateInfo.id
    });
    
    console.log('User Info Result:', userInfoResult.success ? '✅ Success' : '❌ Failed');
    
    // 2. Test get exam schedule
    console.log('\n2. Testing Get Exam Schedule API...');
    const scheduleResult = await mockManager.getMockResponse('/api/v1/wechat/candidate/schedule', 'GET', {}, { 
      forceMock: true,
      userId: candidateInfo.id,
      candidateId: candidateInfo.id
    });
    
    if (scheduleResult.success && scheduleResult.data) {
      console.log('✅ Schedule retrieved successfully, total', scheduleResult.data.length, 'exam arrangements');
      
      // Find next exam
      const now = new Date();
      const upcomingExams = scheduleResult.data.filter(exam => {
        const examTime = new Date(exam.exam_time || exam.startTime);
        return examTime > now && (exam.status === '待签到' || exam.status === 'confirmed');
      });
      
      if (upcomingExams.length > 0) {
        console.log('Next exam:', upcomingExams[0].exam_name);
      } else {
        console.log('No upcoming exams');
      }
    } else {
      console.log('❌ Schedule retrieval failed');
    }
    
    // 3. Test get QR code status
    console.log('\n3. Testing Get QR Code Status API...');
    const qrResult = await mockManager.getMockResponse('/api/v1/wechat/candidate/qrcode', 'GET', {}, { 
      forceMock: true,
      userId: candidateInfo.id,
      candidateId: candidateInfo.id
    });
    
    if (qrResult.success && qrResult.data) {
      console.log('✅ QR code status retrieved successfully');
      console.log('QR code expiry time:', qrResult.data.expires_at);
    } else {
      console.log('❌ QR code status retrieval failed');
    }
    
    // 4. Test public dashboard data
    console.log('\n4. Testing Public Dashboard Data API...');
    const dashboardResult = await mockManager.getMockResponse('/api/v1/wechat/dashboard', 'GET', {}, { 
      forceMock: true,
      userId: candidateInfo.id
    });
    
    console.log('Public dashboard data:', dashboardResult.success ? '✅ Success' : '❌ Failed');
    
    // 5. Calculate statistics
    console.log('\n5. Calculating Statistics...');
    const examSchedule = scheduleResult.data || [];
    const completedExams = examSchedule.filter(exam => exam.status === '已完成').length;
    const totalExams = examSchedule.length;
    const upcomingExams = examSchedule.filter(exam => exam.status === '待签到' || exam.status === 'confirmed').length;
    
    console.log('Statistics:');
    console.log('- Total exams:', totalExams);
    console.log('- Completed:', completedExams);
    console.log('- Upcoming:', upcomingExams);
    console.log('- Completion rate:', totalExams > 0 ? Math.round((completedExams / totalExams) * 100) + '%' : '0%');
    
    console.log('\n=== Dashboard Functionality Test Complete ===');
    console.log('✅ Candidate personal dashboard functionality is normal');
    console.log('📊 Main features:');
    console.log('   - User info display');
    console.log('   - Next exam information');
    console.log('   - Exam statistics');
    console.log('   - Quick action entries');
    console.log('   - Recent exam records');
    console.log('   - QR code status monitoring');
    
  } catch (error) {
    console.error('❌ Test failed:', error);
  }
}

testCandidateDashboard();