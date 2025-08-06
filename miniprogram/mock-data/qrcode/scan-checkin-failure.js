// 二维码扫描签到失败响应
module.exports = {
  success: false,
  message: "签到失败",
  error_code: "CHECKIN_FAILED",
  data: null,
  timestamp: "{{timestamp}}",
  details: {
    error_type: "qr_scan_error",
    possible_reasons: [
      "二维码已过期",
      "二维码格式错误",
      "考生信息不匹配",
      "不在签到时间范围内",
      "已经完成签到"
    ],
    retry_allowed: true,
    help_text: "请确认二维码有效性或联系工作人员"
  }
}