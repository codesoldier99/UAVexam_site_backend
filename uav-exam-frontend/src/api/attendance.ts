import request from '@/utils/request'

/**
 * 获取考试签到记录列表
 * @param examId 考试ID
 * @param params 查询参数
 */
export function getExamAttendances(examId: number, params?: any) {
  return request({
    url: `/exams/${examId}/attendances`,
    method: 'get',
    params
  })
}

/**
 * 获取考官签到记录
 * @param examId 考试ID
 * @param params 查询参数
 */
export function getExaminerAttendances(examId: number, params?: any) {
  return request({
    url: `/exams/${examId}/examiners/attendances`,
    method: 'get',
    params
  })
}

/**
 * 获取考生签到记录
 * @param examId 考试ID
 * @param params 查询参数
 */
export function getCandidateAttendances(examId: number, params?: any) {
  return request({
    url: `/exams/${examId}/candidates/attendances`,
    method: 'get',
    params
  })
}

/**
 * 记录考官签到
 * @param examId 考试ID
 * @param examinerId 考官ID
 * @param data 签到数据
 */
export function recordExaminerAttendance(examId: number, examinerId: number, data: any) {
  return request({
    url: `/exams/${examId}/examiners/${examinerId}/attendance`,
    method: 'post',
    data
  })
}

/**
 * 记录考生签到
 * @param examId 考试ID
 * @param candidateId 考生ID
 * @param data 签到数据
 */
export function recordCandidateAttendance(examId: number, candidateId: number, data: any) {
  return request({
    url: `/exams/${examId}/candidates/${candidateId}/attendance`,
    method: 'post',
    data
  })
}

/**
 * 获取考试签到统计数据
 * @param examId 考试ID
 */
export function getExamAttendanceStats(examId: number) {
  return request({
    url: `/exams/${examId}/attendance/stats`,
    method: 'get'
  })
}

/**
 * 获取考官签到统计数据
 */
export function getExaminerAttendanceStats(params?: any) {
  return request({
    url: '/examiners/attendance/stats',
    method: 'get',
    params
  })
}

/**
 * 获取考生签到统计数据
 */
export function getCandidateAttendanceStats(params?: any) {
  return request({
    url: '/candidates/attendance/stats',
    method: 'get',
    params
  })
}

/**
 * 导出考试签到记录
 * @param examId 考试ID
 * @param params 导出参数
 */
export function exportExamAttendances(examId: number, params?: any) {
  return request({
    url: `/exams/${examId}/attendances/export`,
    method: 'get',
    params,
    responseType: 'blob'
  })
}