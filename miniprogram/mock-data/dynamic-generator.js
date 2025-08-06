// 动态数据生成器 - 微信小程序版本
class DynamicGenerator {
  constructor() {
    // 直接定义配置，避免依赖外部配置文件
    this.config = {
      timestampFormat: 'ISO',
      tokenPrefix: 'mock_',
      qrCodePrefix: 'CANDIDATE_',
      idStart: 1000
    }
  }
  
  // 生成当前时间戳
  generateTimestamp(format = null) {
    const now = new Date()
    const targetFormat = format || this.config.timestampFormat
    
    switch (targetFormat) {
      case 'ISO':
        return now.toISOString()
      case 'timestamp':
        return Math.floor(now.getTime() / 1000)
      case 'datetime':
        return now.toLocaleString('zh-CN')
      default:
        return now.toISOString()
    }
  }
  
  // 生成Mock Token
  generateToken(userId = null, userType = 'candidate') {
    const timestamp = Date.now()
    const random = Math.random().toString(36).substr(2, 9)
    const userInfo = userId ? `_${userId}` : ''
    return `${this.config.tokenPrefix}${userType}${userInfo}_${timestamp}_${random}`
  }
  
  // 生成二维码内容
  generateQRContent(candidateId, scheduleId = null) {
    const timestamp = Math.floor(Date.now() / 1000)
    const scheduleInfo = scheduleId ? `_${scheduleId}` : ''
    return `${this.config.qrCodePrefix}${candidateId}${scheduleInfo}_${timestamp}`
  }
  
  // 生成二维码URL
  generateQRUrl(content, size = '200x200') {
    return `https://api.qrserver.com/v1/create-qr-code/?size=${size}&data=${encodeURIComponent(content)}`
  }
  
  // 生成随机ID
  generateId(prefix = '') {
    const random = Math.floor(Math.random() * 9000) + this.config.idStart
    return prefix ? `${prefix}_${random}` : random
  }
  
  // 生成过期时间
  generateExpiryTime(hoursFromNow = 24) {
    const expiry = new Date()
    expiry.setHours(expiry.getHours() + hoursFromNow)
    return expiry.toISOString()
  }
  
  // 替换模板中的动态变量
  replaceDynamicVariables(data, context = {}) {
    if (typeof data === 'string') {
      return this.replaceStringVariables(data, context)
    } else if (Array.isArray(data)) {
      return data.map(item => this.replaceDynamicVariables(item, context))
    } else if (typeof data === 'object' && data !== null) {
      const result = {}
      for (const [key, value] of Object.entries(data)) {
        result[key] = this.replaceDynamicVariables(value, context)
      }
      return result
    }
    return data
  }
  
  // 替换字符串中的动态变量
  replaceStringVariables(str, context) {
    return str.replace(/\{\{(\w+)\}\}/g, (match, variable) => {
      switch (variable) {
        case 'timestamp':
          return this.generateTimestamp()
        case 'token':
          return this.generateToken(context.userId, context.userType)
        case 'qr_content':
          return this.generateQRContent(context.candidateId, context.scheduleId)
        case 'qr_url':
          const content = this.generateQRContent(context.candidateId, context.scheduleId)
          return this.generateQRUrl(content)
        case 'expiry_time':
          return this.generateExpiryTime()
        case 'random_id':
          return this.generateId()
        case 'user_id':
          return context.userId || context.candidateId || 'CAND_' + this.generateId()
        case 'id_number':
          return context.idNumber || this.generateIdNumber()
        default:
          return context[variable] || match
      }
    })
  }

  // 生成身份证号码（模拟）
  generateIdNumber() {
    const year = 1990 + Math.floor(Math.random() * 30) // 1990-2020年
    const month = String(Math.floor(Math.random() * 12) + 1).padStart(2, '0')
    const day = String(Math.floor(Math.random() * 28) + 1).padStart(2, '0')
    const area = '110101' // 北京市东城区
    const sequence = String(Math.floor(Math.random() * 999) + 1).padStart(3, '0')
    const gender = Math.floor(Math.random() * 2) // 0=女, 1=男
    
    const base = area + year + month + day + sequence + gender
    
    // 简化的校验码计算
    const checkCode = Math.floor(Math.random() * 10)
    
    return base + checkCode
  }
  
  // 生成考试相关的动态数据
  generateExamData(candidateId, scheduleId) {
    return {
      candidate_id: candidateId,
      schedule_id: scheduleId,
      qr_content: this.generateQRContent(candidateId, scheduleId),
      qr_url: this.generateQRUrl(this.generateQRContent(candidateId, scheduleId)),
      checkin_time: this.generateTimestamp(),
      expires_at: this.generateExpiryTime(2), // 2小时后过期
      token: this.generateToken(candidateId, 'candidate')
    }
  }
}

module.exports = new DynamicGenerator()