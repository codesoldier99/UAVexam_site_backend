// 工作人员签到历史Mock数据
module.exports = {
  success: true,
  message: '获取签到历史成功',
  data: {
    total: 156,
    page: 1,
    size: 20,
    records: [
      {
        id: 'CHK_001',
        candidate_name: '张三',
        candidate_id: 'CAND_1001',
        exam_name: '无人机驾驶员理论考试',
        venue: '考场A101',
        check_in_time: new Date(Date.now() - 30 * 60 * 1000).toISOString(), // 30分钟前
        method: 'qr_scan',
        status: 'success',
        staff_name: '{{staffName}}',
        notes: null
      },
      {
        id: 'CHK_002',
        candidate_name: '李四',
        candidate_id: 'CAND_1002',
        exam_name: '无人机驾驶员实操考试',
        venue: '考场B201',
        check_in_time: new Date(Date.now() - 45 * 60 * 1000).toISOString(), // 45分钟前
        method: 'manual',
        status: 'success',
        staff_name: '{{staffName}}',
        notes: '考生忘记带身份证，核实信息后手动签到'
      },
      {
        id: 'CHK_003',
        candidate_name: '王五',
        candidate_id: 'CAND_1003',
        exam_name: '无人机驾驶员理论考试',
        venue: '考场A102',
        check_in_time: new Date(Date.now() - 60 * 60 * 1000).toISOString(), // 1小时前
        method: 'qr_scan',
        status: 'success',
        staff_name: '{{staffName}}',
        notes: null
      },
      {
        id: 'CHK_004',
        candidate_name: '赵六',
        candidate_id: 'CAND_1004',
        exam_name: '无人机驾驶员实操考试',
        venue: '考场C301',
        check_in_time: new Date(Date.now() - 90 * 60 * 1000).toISOString(), // 1.5小时前
        method: 'qr_scan',
        status: 'failed',
        staff_name: '{{staffName}}',
        notes: '二维码已过期，需要重新生成'
      },
      {
        id: 'CHK_005',
        candidate_name: '孙七',
        candidate_id: 'CAND_1005',
        exam_name: '无人机驾驶员理论考试',
        venue: '考场A103',
        check_in_time: new Date(Date.now() - 120 * 60 * 1000).toISOString(), // 2小时前
        method: 'qr_scan',
        status: 'success',
        staff_name: '{{staffName}}',
        notes: null
      }
    ]
  },
  timestamp: new Date().toISOString()
}