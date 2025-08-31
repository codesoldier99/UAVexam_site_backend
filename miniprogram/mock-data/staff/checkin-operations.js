// 工作人员签到操作Mock数据
module.exports = {
  // 签到成功
  performCheckInSuccess: (context) => {
    const { candidateId, scheduleId, staffId, staffName } = context;
    
    const checkinId = `CHECKIN_${Date.now()}`;
    const checkinTime = new Date().toISOString();
    
    return {
      success: true,
      message: '签到成功',
      data: {
        checkin_id: checkinId,
        candidate_id: candidateId || 'CAND_1001',
        candidate_name: '张三',
        schedule_id: scheduleId || 'SCH002',
        exam_name: '无人机驾驶实操考试',
        staff_id: staffId || 'STAFF_1001',
        staff_name: staffName || '张老师',
        checkin_time: checkinTime,
        checkin_method: 'qr_code', // qr_code, manual_code
        location: '考试现场',
        status: 'success',
        notes: '',
        // 签到后的考试状态更新
        exam_status_updated: {
          old_status: '待签到',
          new_status: '已签到',
          checkin_status: '已签到'
        },
        // 生成签到凭证
        checkin_receipt: {
          receipt_id: `RECEIPT_${Date.now()}`,
          qr_code: `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=CHECKIN_${checkinId}`,
          valid_until: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString() // 24小时有效
        }
      },
      timestamp: checkinTime
    };
  },

  // 签到失败 - 网络错误
  performCheckInNetworkError: (context) => {
    return {
      success: false,
      message: '网络连接失败，请检查网络后重试',
      error_code: 'NETWORK_ERROR',
      data: null,
      timestamp: new Date().toISOString()
    };
  },

  // 签到失败 - 服务器错误
  performCheckInServerError: (context) => {
    return {
      success: false,
      message: '服务器繁忙，请稍后重试',
      error_code: 'SERVER_ERROR',
      data: null,
      timestamp: new Date().toISOString()
    };
  },

  // 签到失败 - 权限不足
  performCheckInPermissionDenied: (context) => {
    return {
      success: false,
      message: '您没有执行签到操作的权限',
      error_code: 'PERMISSION_DENIED',
      data: null,
      timestamp: new Date().toISOString()
    };
  },

  // 签到失败 - 考试时间未到
  performCheckInTooEarly: (context) => {
    return {
      success: false,
      message: '考试签到时间未到，请在考试开始前30分钟内签到',
      error_code: 'CHECKIN_TOO_EARLY',
      data: {
        exam_start_time: '2025-08-20T14:00:00.000Z',
        checkin_start_time: '2025-08-20T13:30:00.000Z',
        current_time: new Date().toISOString()
      },
      timestamp: new Date().toISOString()
    };
  },

  // 签到失败 - 考试已结束
  performCheckInTooLate: (context) => {
    return {
      success: false,
      message: '考试签到时间已过，无法完成签到',
      error_code: 'CHECKIN_TOO_LATE',
      data: {
        exam_start_time: '2025-08-20T14:00:00.000Z',
        checkin_end_time: '2025-08-20T14:15:00.000Z',
        current_time: new Date().toISOString()
      },
      timestamp: new Date().toISOString()
    };
  }
};