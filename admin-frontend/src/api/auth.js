import apiClient from './config'

export const login = async (username, password) => {
  const formData = new FormData()
  formData.append('username', username)
  formData.append('password', password)
  
  return apiClient.post('/auth/login', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export const getCurrentUser = async () => {
  return apiClient.get('/auth/me')
}

export const logout = async () => {
  return apiClient.post('/auth/logout')
}