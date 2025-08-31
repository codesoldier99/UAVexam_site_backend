import request from '@/utils/request'

/**
 * 获取系统设置
 */
export function getSystemSettings() {
  return request({
    url: '/settings',
    method: 'get'
  })
}

/**
 * 更新基本设置
 * @param data 基本设置数据
 */
export function updateBasicSettings(data: {
  systemName: string
  version: string
  description: string
  maintenanceMode: boolean
}) {
  return request({
    url: '/settings/basic',
    method: 'put',
    data
  })
}

/**
 * 更新邮件设置
 * @param data 邮件设置数据
 */
export function updateEmailSettings(data: {
  smtpHost: string
  smtpPort: number
  fromEmail: string
  password: string
  enableSSL: boolean
}) {
  return request({
    url: '/settings/email',
    method: 'put',
    data
  })
}

/**
 * 更新安全设置
 * @param data 安全设置数据
 */
export function updateSecuritySettings(data: {
  minPasswordLength: number
  maxLoginAttempts: number
  lockoutDuration: number
  sessionTimeout: number
  forceHttps: boolean
}) {
  return request({
    url: '/settings/security',
    method: 'put',
    data
  })
}

/**
 * 测试邮件连接
 * @param data 邮件测试数据
 */
export function testEmailConnection(data: {
  smtpHost: string
  smtpPort: number
  fromEmail: string
  password: string
  enableSSL: boolean
  testEmail?: string
}) {
  return request({
    url: '/settings/email/test',
    method: 'post',
    data
  })
}

/**
 * 获取系统信息
 */
export function getSystemInfo() {
  return request({
    url: '/system/info',
    method: 'get'
  })
}