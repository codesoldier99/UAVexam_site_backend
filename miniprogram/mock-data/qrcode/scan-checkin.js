// 扫码签到成功Mock数据
module.exports = {
  success: true,
  message: '签到成功！',
  data: {
    candidate_id: 'CAND_{{candidateId}}',
    candidate_name: '{{candidateName}}',
    exam_name: '{{examName}}',
    exam_time: '{{examTime}}',
    venue: '{{venue}}',
    check_in_time: '{{timestamp}}',
    schedule_id: 'SCH_{{scheduleId}}',
    staff_id: '{{staffId}}',
    status: 'checked_in'
  },
  timestamp: '{{timestamp}}'
}