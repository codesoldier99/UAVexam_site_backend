// 考试成绩响应数据
module.exports = {
  "success": true,
  "message": "获取考试成绩成功",
  "data": [
    {
      "id": "RESULT001",
      "exam_id": "EXAM003",
      "exam_name": "航空法规考试",
      "exam_type": "理论",
      "exam_date": "2025-07-20",
      "score": 85,
      "total_marks": 100,
      "grade": "良好",
      "status": "已发布",
      "pass_status": "通过",
      "details": {
        "section_scores": [
          {
            "section": "基础法规",
            "score": 28,
            "total": 30
          },
          {
            "section": "飞行安全",
            "score": 32,
            "total": 35
          },
          {
            "section": "应急处理",
            "score": 25,
            "total": 35
          }
        ],
        "correct_answers": 85,
        "total_questions": 100,
        "accuracy_rate": "85%"
      },
      "certificate_info": {
        "certificate_number": "CERT2025001",
        "issue_date": "2025-07-25",
        "valid_until": "2028-07-25",
        "status": "已颁发"
      }
    },
    {
      "id": "RESULT002",
      "exam_id": "EXAM001",
      "exam_name": "无人机驾驶理论考试",
      "exam_type": "理论",
      "exam_date": "2025-08-10",
      "score": null,
      "total_marks": 100,
      "grade": null,
      "status": "待发布",
      "pass_status": "待定",
      "details": null,
      "certificate_info": null
    }
  ],
  "timestamp": "{{timestamp}}"
}