import request from '@/utils/request'

/**
 * 获取考场列表
 * @param params 查询参数
 */
export function getVenues(params?: any) {
  return request({
    url: '/api/venues',
    method: 'get',
    params
  })
}

/**
 * 获取考场详情
 * @param id 考场ID
 */
export function getVenueDetail(id: number) {
  return request({
    url: `/api/venues/${id}`,
    method: 'get'
  })
}

/**
 * 创建考场
 * @param data 考场信息
 */
export function createVenue(data: any) {
  return request({
    url: '/api/venues',
    method: 'post',
    data
  })
}

/**
 * 更新考场信息
 * @param id 考场ID
 * @param data 考场信息
 */
export function updateVenue(id: number, data: any) {
  return request({
    url: `/api/venues/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除考场
 * @param id 考场ID
 */
export function deleteVenue(id: number) {
  return request({
    url: `/api/venues/${id}`,
    method: 'delete'
  })
}

/**
 * 获取考场的考试安排
 * @param id 考场ID
 * @param params 查询参数
 */
export function getVenueExams(id: number, params?: any) {
  return request({
    url: `/api/venues/${id}/exams`,
    method: 'get',
    params
  })
}

/**
 * 分配考场到考试
 * @param examId 考试ID
 * @param venueId 考场ID
 * @param data 分配信息
 */
export function assignVenueToExam(examId: number, venueId: number, data?: any) {
  return request({
    url: `/api/exams/${examId}/venues/${venueId}`,
    method: 'post',
    data
  })
}

/**
 * 移除考试的考场分配
 * @param examId 考试ID
 * @param venueId 考场ID
 */
export function removeVenueFromExam(examId: number, venueId: number) {
  return request({
    url: `/api/exams/${examId}/venues/${venueId}`,
    method: 'delete'
  })
}