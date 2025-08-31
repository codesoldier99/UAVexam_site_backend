// 更新考生信息响应数据
module.exports = {
  "success": true,
  "message": "考生信息更新成功",
  "data": {
    "id": "{{candidateId}}",
    "name": "{{name}}",
    "phone": "{{phone}}",
    "email": "{{email}}",
    "institution": "{{institution}}",
    "updated_at": "{{timestamp}}",
    "version": 2
  },
  "timestamp": "{{timestamp}}"
}