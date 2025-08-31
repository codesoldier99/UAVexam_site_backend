// 工作人员统计信息Mock数据
module.exports = {
  success: true,
  message: '获取统计信息成功',
  data: {
    today: {
      scanned: Math.floor(Math.random() * 50 + 10),
      checked_in: Math.floor(Math.random() * 45 + 8),
      failed: Math.floor(Math.random() * 5 + 1),
      manual_checkin: Math.floor(Math.random() * 3)
    },
    this_week: {
      scanned: Math.floor(Math.random() * 300 + 50),
      checked_in: Math.floor(Math.random() * 280 + 45),
      failed: Math.floor(Math.random() * 20 + 5),
      manual_checkin: Math.floor(Math.random() * 15 + 2)
    },
    current_session: {
      start_time: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(), // 4小时前
      scanned: Math.floor(Math.random() * 20 + 5),
      checked_in: Math.floor(Math.random() * 18 + 4),
      failed: Math.floor(Math.random() * 2),
      last_scan_time: new Date(Date.now() - 10 * 60 * 1000).toISOString() // 10分钟前
    }
  },
  timestamp: new Date().toISOString()
}