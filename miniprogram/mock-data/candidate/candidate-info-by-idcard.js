// 考生身份证验证Mock数据 - 临时回退用
module.exports = {
  success: true,
  message: '考生信息获取成功',
  data: {
    candidate_id: 1,
    name: '张三',
    id_card: '{{id_card}}',
    phone: '13800138001',
    institution: {
      id: 1,
      name: '北京航空培训中心',
      code: 'BJAV001'
    },
    status: 'active',
    has_pending_exams: true,
    next_exam_date: '2024-01-15'
  },
  timestamp: '{{timestamp}}'
}