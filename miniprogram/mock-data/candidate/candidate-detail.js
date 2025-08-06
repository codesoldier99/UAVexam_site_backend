// 考生详细信息响应数据
module.exports = {
  "success": true,
  "message": "获取考生详细信息成功",
  "data": {
    "id": "{{user_id}}",
    "personal_info": {
      "name": "张三",
      "id_number": "{{id_number}}",
      "phone": "13800138001",
      "email": "zhangsan@example.com",
      "gender": "男",
      "birth_date": "1990-01-01",
      "address": "北京市朝阳区xxx街道xxx号"
    },
    "institution_info": {
      "institution_name": "北京航空培训中心",
      "department": "无人机驾驶培训部",
      "exam_type": "无人机驾驶员理论考试",
      "registration_date": "2025-07-01"
    },
    "exam_history": [
      {
        "exam_id": "EXAM001",
        "exam_name": "无人机驾驶理论考试",
        "exam_date": "2025-08-15",
        "status": "已报名",
        "venue": "北京考试中心"
      }
    ],
    "certificates": [
      {
        "cert_id": "CERT001",
        "cert_name": "航空法规证书",
        "issue_date": "2025-07-25",
        "valid_until": "2028-07-25",
        "status": "有效"
      }
    ],
    "payment_records": [
      {
        "payment_id": "PAY001",
        "amount": 500.00,
        "payment_date": "2025-07-15",
        "status": "已支付",
        "exam_name": "无人机驾驶理论考试"
      }
    ]
  },
  "timestamp": "{{timestamp}}"
}