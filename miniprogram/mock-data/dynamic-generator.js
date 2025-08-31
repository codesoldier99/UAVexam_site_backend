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
        case 'qr_code':
          const qrContent = this.generateQRContent(context.candidateId, context.scheduleId)
          return this.generateQRUrl(qrContent)
        case 'expires_at':
        case 'expiry_time':
          return this.generateExpiryTime()
        case 'schedule_id':
          return context.scheduleId || context.id || 'SCH_' + this.generateId()
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

  // 生成考生信息
  generateCandidateInfo(context = {}) {
    const candidates = [
      { name: '张三', idCard: '110101199001011234', phone: '13800138001', institution: '北京航空培训中心' },
      { name: '李四', idCard: '110101199002022345', phone: '13800138002', institution: '上海飞行学院' },
      { name: '王五', idCard: '110101199003033456', phone: '13800138003', institution: '广州航空学校' },
      { name: '赵六', idCard: '110101199004044567', phone: '13800138004', institution: '深圳无人机培训中心' },
      { name: '孙七', idCard: '110101199005055678', phone: '13800138005', institution: '成都航空技术学院' }
    ]
    
    const candidate = candidates[Math.floor(Math.random() * candidates.length)]
    
    return {
      candidateId: context.candidateId || `CAND_${Math.floor(Math.random() * 9000 + 1000)}`,
      candidateName: context.candidateName || candidate.name,
      idNumber: context.idNumber || candidate.idCard,
      phone: candidate.phone,
      institution: candidate.institution,
      examName: context.examName || this.generateExamName(),
      examTime: context.examTime || this.generateExamTime(),
      venue: context.venue || this.generateVenue()
    }
  }

  // 生成工作人员信息
  generateStaffInfo(context = {}) {
    const staffNames = ['张老师', '李老师', '王老师', '赵老师', '孙老师']
    const departments = ['教务处', '考务中心', '监考部', '技术支持部', '质量管理部']
    
    return {
      staffId: context.staffId || `STAFF_${Math.floor(Math.random() * 9000 + 1000)}`,
      staffName: context.staffName || staffNames[Math.floor(Math.random() * staffNames.length)],
      department: departments[Math.floor(Math.random() * departments.length)],
      role: context.role || 'staff'
    }
  }

  // 生成扫码结果
  generateScanResult(context = {}) {
    const candidateInfo = this.generateCandidateInfo(context)
    const staffInfo = this.generateStaffInfo(context)
    
    // 根据二维码内容判断扫码结果
    const qrCode = context.qrCode || ''
    let success = true
    let errorMessage = ''
    let errorCode = ''
    let reason = ''
    
    // 模拟各种扫码失败情况
    if (qrCode.includes('expired') || qrCode.includes('old')) {
      success = false
      errorMessage = '二维码已过期，请刷新后重试'
      errorCode = 'QR_EXPIRED'
      reason = '二维码过期'
    } else if (qrCode.includes('invalid') || qrCode.length < 10) {
      success = false
      errorMessage = '无效的二维码，请确认二维码正确'
      errorCode = 'QR_INVALID'
      reason = '二维码无效'
    } else if (qrCode.includes('duplicate')) {
      success = false
      errorMessage = '该考生已完成签到，请勿重复签到'
      errorCode = 'ALREADY_CHECKED_IN'
      reason = '重复签到'
    } else if (Math.random() < 0.1) { // 10%概率随机失败
      success = false
      errorMessage = '签到失败，请重试'
      errorCode = 'CHECKIN_FAILED'
      reason = '系统错误'
    }
    
    return {
      success,
      candidateId: candidateInfo.candidateId,
      candidateName: candidateInfo.candidateName,
      examName: candidateInfo.examName,
      examTime: candidateInfo.examTime,
      venue: candidateInfo.venue,
      scheduleId: `SCH_${Math.floor(Math.random() * 9000 + 1000)}`,
      staffId: staffInfo.staffId,
      staffName: staffInfo.staffName,
      qrCode: qrCode,
      errorMessage,
      errorCode,
      reason
    }
  }

  // 生成考试名称
  generateExamName() {
    const examTypes = [
      '无人机驾驶员理论考试',
      '无人机驾驶员实操考试',
      '航空法规考试',
      '飞行安全考试',
      '无人机维修考试'
    ]
    return examTypes[Math.floor(Math.random() * examTypes.length)]
  }

  // 生成考试时间
  generateExamTime() {
    const now = new Date()
    const examDate = new Date(now.getTime() + Math.random() * 7 * 24 * 60 * 60 * 1000) // 未来7天内
    return examDate.toISOString()
  }

  // 生成考场
  generateVenue() {
    const venues = ['考场A101', '考场A102', '考场B201', '考场B202', '考场C301', '考场C302']
    return venues[Math.floor(Math.random() * venues.length)]
  }
}

module.exports = new DynamicGenerator()