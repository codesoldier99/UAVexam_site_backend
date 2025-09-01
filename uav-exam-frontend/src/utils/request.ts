import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

// 创建axios实例
const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 15000
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    const userStore = useUserStore()
    
    console.log('发送请求:', {
      url: config.url,
      method: config.method,
      params: config.params,
      data: config.data,
      headers: config.headers
    })
    
    // 如果有token，添加到请求头
    if (userStore.token) {
      config.headers['Authorization'] = `Bearer ${userStore.token}`
    }
    
    return config
  },
  error => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data
    
    // 对于登录接口，直接返回数据
    if (response.config.url?.includes('/api/v1/pc/auth/login')) {
      return res
    }
    
    // 对于考试产品接口，直接返回数据（FastAPI直接返回数据，没有包装）
    if (response.config.url?.includes('/api/v1/pc/exam-products')) {
      console.log('考试产品接口响应数据:', res)
      return res
    }
    
    // 对于考生接口，直接返回数据
    if (response.config.url?.includes('/api/v1/pc/candidates')) {
      console.log('考生接口响应数据:', res)
      return res
    }
    
    // 如果返回的状态码不是200，说明接口请求有误
    if (res.code && res.code !== 200) {
      ElMessage({
        message: res.message || 'Error',
        type: 'error',
        duration: 5 * 1000
      })
      
      // 401: 未登录或token过期
      if (res.code === 401) {
        const userStore = useUserStore()
        userStore.logout()
        window.location.href = '/login'
      }
      
      return Promise.reject(new Error(res.message || 'Error'))
    } else {
      return res
    }
  },
  error => {
    console.error('Response error:', error)
    console.error('Error response data:', error.response?.data)
    console.error('Error response detail:', error.response?.data?.detail)
    if (error.response?.data?.detail && Array.isArray(error.response.data.detail)) {
      console.error('详细错误信息:', JSON.stringify(error.response.data.detail, null, 2))
    }
    console.error('Error response status:', error.response?.status)
    console.error('Error response headers:', error.response?.headers)
    
    // 处理网络错误
    let message = '网络错误，请稍后重试'
    
    if (error.response) {
      // 如果后端返回了具体的错误信息，优先使用
      if (error.response.data && error.response.data.detail) {
        // 如果 detail 是数组，取第一个错误信息
        if (Array.isArray(error.response.data.detail)) {
          const firstError = error.response.data.detail[0]
          if (typeof firstError === 'object' && firstError.msg) {
            message = firstError.msg
          } else if (typeof firstError === 'string') {
            message = firstError
          } else {
            message = JSON.stringify(firstError)
          }
        } else {
          message = error.response.data.detail
        }
      } else if (error.response.data && error.response.data.message) {
        message = error.response.data.message
      } else {
        switch (error.response.status) {
          case 400:
            message = '请求错误'
            break
          case 401:
            message = '未授权，请重新登录'
            // 清除用户信息并跳转到登录页
            const userStore = useUserStore()
            userStore.logout()
            window.location.href = '/login'
            break
          case 403:
            message = '拒绝访问'
            break
          case 404:
            message = '请求地址出错'
            break
          case 408:
            message = '请求超时'
            break
          case 422:
            message = '请求参数验证失败'
            break
          case 500:
            message = '服务器内部错误'
            break
          case 501:
            message = '服务未实现'
            break
          case 502:
            message = '网关错误'
            break
          case 503:
            message = '服务不可用'
            break
          case 504:
            message = '网关超时'
            break
          case 505:
            message = 'HTTP版本不受支持'
            break
          default:
            message = `连接错误${error.response.status}`
        }
      }
    }
    
    ElMessage({
      message: message,
      type: 'error',
      duration: 5 * 1000
    })
    
    return Promise.reject(error)
  }
)

export default service