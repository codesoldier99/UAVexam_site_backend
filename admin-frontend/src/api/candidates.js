import apiClient from './config'

export const getCandidates = async (params = {}) => {
  return apiClient.get('/candidates', { params })
}

export const getCandidate = async (id) => {
  return apiClient.get(`/candidates/${id}`)
}

export const createCandidate = async (data) => {
  return apiClient.post('/candidates', data)
}

export const updateCandidate = async (id, data) => {
  return apiClient.put(`/candidates/${id}`, data)
}

export const deleteCandidate = async (id) => {
  return apiClient.delete(`/candidates/${id}`)
}

export const importCandidates = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  
  return apiClient.post('/candidates/batch', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}