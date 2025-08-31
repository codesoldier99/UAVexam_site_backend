import request from '@/utils/request'

/**
 * 获取考官列表
 * @param params 查询参数
 * @returns 考官列表
 */
export function getExaminers(params?: any) {
  return request({
    url: '/api/examiners',
    method: 'get',
    params
  })
}

/**
 * 获取考官详情
 * @param id 考官ID
 * @returns 考官详情
 */
export function getExaminerDetail(id: number) {
  return request({
    url: `/api/examiners/${id}`,
    method: 'get'
  })
}

/**
 * 创建考官
 * @param data 考官信息
 * @returns 创建结果
 */
export function createExaminer(data: any) {
  return request({
    url: '/api/examiners',
    method: 'post',
    data
  })
}

/**
 * 更新考官信息
 * @param id 考官ID
 * @param data 考官信息
 * @returns 更新结果
 */
export function updateExaminer(id: number, data: any) {
  return request({
    url: `/api/examiners/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除考官
 * @param id 考官ID
 * @returns 删除结果
 */
export function deleteExaminer(id: number) {
  return request({
    url: `/api/examiners/${id}`,
    method: 'delete'
  })
}

/**
 * 获取考生列表
 * @param params 查询参数
 * @returns 考生列表
 */
export function getCandidates(params?: any) {
  return request({
    url: '/api/candidates',
    method: 'get',
    params
  })
}

/**
 * 获取考生详情
 * @param id 考生ID
 * @returns 考生详情
 */
export function getCandidateDetail(id: number) {
  return request({
    url: `/api/candidates/${id}`,
    method: 'get'
  })
}

/**
 * 创建考生
 * @param data 考生信息
 * @returns 创建结果
 */
export function createCandidate(data: any) {
  return request({
    url: '/api/candidates',
    method: 'post',
    data
  })
}

/**
 * 更新考生信息
 * @param id 考生ID
 * @param data 考生信息
 * @returns 更新结果
 */
export function updateCandidate(id: number, data: any) {
  return request({
    url: `/api/candidates/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除考生
 * @param id 考生ID
 * @returns 删除结果
 */
export function deleteCandidate(id: number) {
  return request({
    url: `/api/candidates/${id}`,
    method: 'delete'
  })
}

/**
 * 批量导入考生
 * @param file 考生数据文件
 * @returns 导入结果
 */
export function importCandidates(file: File) {
  const formData = new FormData()
  formData.append('file', file)
  
  return request({
    url: '/api/candidates/import',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

/**
 * 导出考生数据
 * @param params 查询参数
 * @returns 导出结果
 */
export function exportCandidates(params?: any) {
  return request({
    url: '/api/candidates/export',
    method: 'get',
    params,
    responseType: 'blob'
  })
}

/**
 * 分配考官到考试
 * @param examId 考试ID
 * @param data 考官分配信息
 * @returns 分配结果
 */
export function assignExaminers(examId: number, data: any) {
  return request({
    url: `/api/exams/${examId}/examiners`,
    method: 'post',
    data
  })
}

/**
 * 分配考生到考试
 * @param examId 考试ID
 * @param data 考生分配信息
 * @returns 分配结果
 */
export function assignCandidates(examId: number, data: any) {
  return request({
    url: `/api/exams/${examId}/candidates`,
    method: 'post',
    data
  })
}

/**
 * 获取考试的考官列表
 * @param examId 考试ID
 * @returns 考官列表
 */
export function getExamExaminers(examId: number) {
  return request({
    url: `/api/exams/${examId}/examiners`,
    method: 'get'
  })
}

/**
 * 获取考试的考生列表
 * @param examId 考试ID
 * @param params 查询参数
 * @returns 考生列表
 */
export function getExamCandidates(examId: number, params?: any) {
  return request({
    url: `/api/exams/${examId}/candidates`,
    method: 'get',
    params
  })
}

/**
 * 移除考试的考官
 * @param examId 考试ID
 * @param examinerId 考官ID
 * @returns 移除结果
 */
export function removeExamExaminer(examId: number, examinerId: number) {
  return request({
    url: `/api/exams/${examId}/examiners/${examinerId}`,
    method: 'delete'
  })
}

/**
 * 移除考试的考生
 * @param examId 考试ID
 * @param candidateId 考生ID
 * @returns 移除结果
 */
export function removeExamCandidate(examId: number, candidateId: number) {
  return request({
    url: `/api/exams/${examId}/candidates/${candidateId}`,
    method: 'delete'
  })
}