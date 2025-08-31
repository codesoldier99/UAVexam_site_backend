// 工作人员扫码验证Mock数据
module.exports = {
  // 二维码验证成功
  validateQRCodeSuccess: (context) => {
    const { candidateId, scheduleId, staffId } = context;
    
    return {
      success: true,
      message: '二维码验证成功',
      data: {
        candidate: {
          id: candidateId || 'CAND_1001',
          name: '张三',
          id_number: '110101199001011234',
          phone: '13800138001',
          status: 'active'
        },
        exam: {
          schedule_id: scheduleId || 'SCH002',
          exam_id: 'EXAM002',
          exam_name: '无人机驾驶实操考试',
          exam_type: '实操考试',
          exam_time: '2025-08-20T14:00:00.000Z',
          exam_date: '2025-08-20',
          venue: '北京考试中心 实操场地',
          location: '北京考试中心 实操场地',
          venue_info: {
            address: '北京市朝阳区xxx路xxx号',
            room: '实操场地',
            floor: '1楼',
            capacity: 20
          },
          duration: 180,
          status: '待签到',
          checkin_status: '未签到'
        },
        validation: {
          qr_valid: true,
          qr_expired: false,
          candidate_eligible: true,
          exam_available: true,
          already_checkedin: false,
          validation_time: new Date().toISOString()
        }
      },
      timestamp: new Date().toISOString()
    };
  },

  // 二维码验证失败 - 已过期
  validateQRCodeExpired: (context) => {
    return {
      success: false,
      message: '二维码已过期，请考生刷新后重试',
      error_code: 'QR_EXPIRED',
      data: null,
      timestamp: new Date().toISOString()
    };
  },

  // 二维码验证失败 - 格式错误
  validateQRCodeInvalid: (context) => {
    return {
      success: false,
      message: '无效的二维码格式',
      error_code: 'QR_INVALID_FORMAT',
      data: null,
      timestamp: new Date().toISOString()
    };
  },

  // 二维码验证失败 - 考生不存在
  validateQRCodeCandidateNotFound: (context) => {
    return {
      success: false,
      message: '考生信息不存在',
      error_code: 'CANDIDATE_NOT_FOUND',
      data: null,
      timestamp: new Date().toISOString()
    };
  },

  // 二维码验证失败 - 已签到
  validateQRCodeAlreadyCheckedIn: (context) => {
    return {
      success: false,
      message: '该考生已完成签到',
      error_code: 'ALREADY_CHECKED_IN',
      data: {
        checkin_time: '2025-08-20T13:45:00.000Z',
        checkin_staff: '李老师'
      },
      timestamp: new Date().toISOString()
    };
  },

  // 手动签到码验证成功
  validateManualCodeSuccess: (context) => {
    const { checkinCode } = context;
    
    return {
      success: true,
      message: '签到码验证成功',
      data: {
        candidate: {
          id: 'CAND_1002',
          name: '李四',
          id_number: '110101199001011235',
          phone: '13800138002',
          status: 'active'
        },
        exam: {
          schedule_id: 'SCH003',
          exam_id: 'EXAM003',
          exam_name: '航空法规考试',
          exam_type: '理论考试',
          exam_time: '2025-08-25T10:00:00.000Z',
          exam_date: '2025-08-25',
          venue: '北京考试中心 B201',
          location: '北京考试中心 B201',
          venue_info: {
            address: '北京市朝阳区xxx路xxx号',
            room: 'B201',
            floor: '2楼',
            capacity: 50
          },
          duration: 120,
          status: '待签到',
          checkin_status: '未签到'
        },
        validation: {
          code_valid: true,
          candidate_eligible: true,
          exam_available: true,
          already_checkedin: false,
          validation_time: new Date().toISOString(),
          checkin_code: checkinCode
        }
      },
      timestamp: new Date().toISOString()
    };
  },

  // 手动签到码验证失败
  validateManualCodeFailed: (context) => {
    return {
      success: false,
      message: '签到码无效或已过期',
      error_code: 'MANUAL_CODE_INVALID',
      data: null,
      timestamp: new Date().toISOString()
    };
  }
};