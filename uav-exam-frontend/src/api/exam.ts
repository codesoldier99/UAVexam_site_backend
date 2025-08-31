import request from '@/utils/request'
import type { SearchParams } from '@/types/common'
import type { Exam, ExamDetail } from '@/types/exam'

// 获取考试列表
export function getExamList(params: SearchParams) {
  return request({
    url: '/exams',
    method: 'get',
    params
  })
}

// 获取考试详情
export function getExamDetail(id: number | string) {
  return request({
    url: `/exams/${id}`,
    method: 'get'
  })
}

// 创建考试
export function createExam(data: Partial<Exam>) {
  return request({
    url: '/exams',
    method: 'post',
    data
  })
}

// 更新考试
export function updateExam(id: number | string, data: Partial<Exam>) {
  return request({
    url: `/exams/${id}`,
    method: 'put',
    data
  })
}

// 删除考试
export function deleteExam(id: number | string) {
  return request({
    url: `/exams/${id}`,
    method: 'delete'
  })
}

// 发布考试
export function publishExam(id: number | string) {
  return request({
    url: `/exams/${id}/publish`,
    method: 'post'
  })
}

// 取消考试
export function cancelExam(id: number | string) {
  return request({
    url: `/exams/${id}/cancel`,
    method: 'post'
  })
}

// 获取考试场次列表
export function getExamSessions(examId: number | string) {
  return request({
    url: `/exams/${examId}/sessions`,
    method: 'get'
  })
}

// 创建考试场次
export function createExamSession(examId: number | string, data: any) {
  return request({
    url: `/exams/${examId}/sessions`,
    method: 'post',
    data
  })
}

// 更新考试场次
export function updateExamSession(examId: number | string, sessionId: number | string, data: any) {
  return request({
    url: `/exams/${examId}/sessions/${sessionId}`,
    method: 'put',
    data
  })
}

// 删除考试场次
export function deleteExamSession(examId: number | string, sessionId: number | string) {
  return request({
    url: `/exams/${examId}/sessions/${sessionId}`,
    method: 'delete'
  })
}

// 获取考试考生列表
export function getExamCandidates(examId: number | string, params?: any) {
  return request({
    url: `/exams/${examId}/candidates`,
    method: 'get',
    params
  })
}

// 添加考试考生
export function addExamCandidates(examId: number | string, data: { candidate_ids: number[] }) {
  return request({
    url: `/exams/${examId}/candidates`,
    method: 'post',
    data
  })
}

// 移除考试考生
export function removeExamCandidate(examId: number | string, candidateId: number | string) {
  return request({
    url: `/exams/${examId}/candidates/${candidateId}`,
    method: 'delete'
  })
}

// 获取考试考官列表
export function getExamExaminers(examId: number | string, params?: any) {
  return request({
    url: `/exams/${examId}/examiners`,
    method: 'get',
    params
  })
}

// 添加考试考官
export function addExamExaminers(examId: number | string, data: { examiner_ids: number[] }) {
  return request({
    url: `/exams/${examId}/examiners`,
    method: 'post',
    data
  })
}

// 移除考试考官
export function removeExamExaminer(examId: number | string, examinerId: number | string) {
  return request({
    url: `/exams/${examId}/examiners/${examinerId}`,
    method: 'delete'
  })
}