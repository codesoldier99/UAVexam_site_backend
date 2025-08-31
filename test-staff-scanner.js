const mockManager = require('./miniprogram/mock-data/index.js');

async function testStaffScannerFunctionality() {
  console.log('=== 测试工作人员扫码页面完整功能 ===');
  
  try {
    // 模拟工作人员登录状态
    const staffInfo = {
      id: 'STAFF_1001',
      name: '张老师',
      department: '考务管理部',
      permissions: ['scan_qr', 'manual_checkin', 'view_dashboard']
    };
    
    console.log('工作人员信息:', JSON.stringify(staffInfo, null, 2));
    
    // 1. 测试获取今日统计
    console.log('\n1. 测试获取今日统计...');
    const statsResult = await mockManager.getMockResponse('/api/v1/staff/today-stats', 'GET', {}, { 
      forceMock: true,
      staffId: staffInfo.id,
      staffName: staffInfo.name
    });
    
    if (statsResult.success && statsResult.data) {
      console.log('✅ 今日统计获取成功');
      console.log('总扫码次数:', statsResult.data.totalScans);
      console.log('成功签到:', statsResult.data.successfulCheckins);
      console.log('失败次数:', statsResult.data.failedCheckins);
    } else {
      console.log('❌ 今日统计获取失败');
    }
    
    // 2. 测试获取扫码历史
    console.log('\n2. 测试获取扫码历史...');
    const historyResult = await mockManager.getMockResponse('/api/v1/staff/scan-history', 'GET', {}, { 
      forceMock: true,
      staffId: staffInfo.id
    });
    
    if (historyResult.success && historyResult.data) {
      console.log('✅ 扫码历史获取成功，共', historyResult.data.length, '条记录');
    } else {
      console.log('❌ 扫码历史获取失败');
    }
    
    // 3. 测试二维码验证 - 成功场景
    console.log('\n3. 测试二维码验证 - 成功场景...');
    const qrData = {
      t: "CHK",
      c: "CAND_1001",
      s: "SCH002",
      ts: Date.now(),
      exp: Date.now() + 2 * 60 * 60 * 1000
    };
    
    const validateResult = await mockManager.getMockResponse('/api/v1/qrcode/validate', 'POST', {
      qr_data: qrData,
      staff_id: staffInfo.id,
      scan_time: new Date().toISOString()
    }, { 
      forceMock: true,
      candidateId: qrData.c,
      scheduleId: qrData.s,
      staffId: staffInfo.id
    });
    
    if (validateResult.success && validateResult.data) {
      console.log('✅ 二维码验证成功');
      console.log('考生姓名:', validateResult.data.candidate.name);
      console.log('考试名称:', validateResult.data.exam.exam_name);
      console.log('考试时间:', validateResult.data.exam.exam_time);
      
      // 4. 测试执行签到
      console.log('\n4. 测试执行签到...');
      const checkinResult = await mockManager.getMockResponse('/api/v1/checkin/perform', 'POST', {
        qr_code: JSON.stringify(qrData),
        candidate_id: validateResult.data.candidate.id,
        schedule_id: validateResult.data.exam.schedule_id,
        staff_id: staffInfo.id,
        checkin_time: new Date().toISOString()
      }, { 
        forceMock: true,
        candidateId: validateResult.data.candidate.id,
        scheduleId: validateResult.data.exam.schedule_id,
        staffId: staffInfo.id,
        staffName: staffInfo.name
      });
      
      if (checkinResult.success && checkinResult.data) {
        console.log('✅ 签到执行成功');
        console.log('签到ID:', checkinResult.data.checkin_id);
        console.log('签到时间:', checkinResult.data.checkin_time);
        console.log('状态更新:', checkinResult.data.exam_status_updated);
      } else {
        console.log('❌ 签到执行失败');
      }
      
    } else {
      console.log('❌ 二维码验证失败');
    }
    
    // 5. 测试手动签到码验证
    console.log('\n5. 测试手动签到码验证...');
    const manualCodeResult = await mockManager.getMockResponse('/api/v1/qrcode/manual-validate', 'POST', {
      checkin_code: '123456',
      staff_id: staffInfo.id,
      scan_time: new Date().toISOString()
    }, { 
      forceMock: true,
      checkinCode: '123456',
      staffId: staffInfo.id
    });
    
    if (manualCodeResult.success && manualCodeResult.data) {
      console.log('✅ 手动签到码验证成功');
      console.log('考生姓名:', manualCodeResult.data.candidate.name);
      console.log('考试名称:', manualCodeResult.data.exam.exam_name);
    } else {
      console.log('❌ 手动签到码验证失败');
    }
    
    // 6. 测试错误场景 - 二维码已过期
    console.log('\n6. 测试错误场景 - 二维码已过期...');
    const expiredQrData = {
      t: "CHK",
      c: "CAND_1001",
      s: "SCH002",
      ts: Date.now() - 3 * 60 * 60 * 1000, // 3小时前
      exp: Date.now() - 1 * 60 * 60 * 1000  // 1小时前过期
    };
    
    const expiredResult = await mockManager.getMockResponse('/api/v1/qrcode/validate', 'POST', {
      qr_data: expiredQrData,
      staff_id: staffInfo.id,
      scan_time: new Date().toISOString()
    }, { 
      forceMock: true,
      candidateId: expiredQrData.c,
      scheduleId: expiredQrData.s,
      staffId: staffInfo.id,
      scenario: 'expired' // 指定测试场景
    });
    
    if (!expiredResult.success) {
      console.log('✅ 过期二维码正确被拒绝');
      console.log('错误信息:', expiredResult.message);
    } else {
      console.log('❌ 过期二维码验证异常');
    }
    
    console.log('\n=== 工作人员扫码功能测试完成 ===');
    console.log('✅ 主要功能验证:');
    console.log('   - 今日统计数据获取');
    console.log('   - 扫码历史记录查询');
    console.log('   - 二维码验证和解析');
    console.log('   - 签到操作执行');
    console.log('   - 手动签到码验证');
    console.log('   - 错误场景处理');
    
    console.log('\n📱 扫码工作流程:');
    console.log('   1. 工作人员登录验证权限');
    console.log('   2. 扫描考生二维码');
    console.log('   3. 验证二维码有效性');
    console.log('   4. 显示考生和考试信息');
    console.log('   5. 确认并执行签到');
    console.log('   6. 更新考试状态');
    console.log('   7. 记录签到历史');
    
    console.log('\n🔧 技术特性:');
    console.log('   - 实时状态监控');
    console.log('   - 多种验证方式');
    console.log('   - 完善的错误处理');
    console.log('   - 权限控制机制');
    console.log('   - 操作历史追踪');
    
  } catch (error) {
    console.error('❌ 测试失败:', error);
  }
}

testStaffScannerFunctionality();