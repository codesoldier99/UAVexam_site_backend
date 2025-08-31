# UAV考点运营管理系统 - 数据库内容对照表

## 📊 数据概览
- **机构**: 5个 (北京、上海、深圳、广州、杭州)
- **考场**: 10个 (每机构2个考场)
- **考试产品**: 6个 (理论考试3个 + 实操考试3个)
- **用户**: 16人 (超级管理员1人 + 机构管理员5人 + 考生10人)
- **报名记录**: 18条 (每个考生1-3个报名)

---

## 🏢 机构数据 (institutions表)

| ID | 代码 | 名称 | 城市 | 联系人 | 地址 |
|----|------|------|------|--------|------|
| 1 | BUAV001 | 北京航空培训中心 | 北京 | 北京负责人 | 北京市航空路XXX号 |
| 2 | SUAV002 | 上海航空培训中心 | 上海 | 上海负责人 | 上海市航空路XXX号 |
| 3 | SUAV003 | 深圳航空培训中心 | 深圳 | 深圳负责人 | 深圳市航空路XXX号 |
| 4 | GUAV004 | 广州航空培训中心 | 广州 | 广州负责人 | 广州市航空路XXX号 |
| 5 | HUAV005 | 杭州航空培训中心 | 杭州 | 杭州负责人 | 杭州市航空路XXX号 |

**字段说明**:
- `type`: "培训学校"
- `province`: "{城市}市"
- `district`: "{城市}区"
- `contact_phone`: 138XXXXXXXX (随机生成)
- `contact_email`: {城市拼音}@example.com
- `is_active`: true
- `is_approved`: true

---

## 🏛️ 考场数据 (venues表)

| ID | 代码 | 名称 | 所属机构 | 容量 | 位置 |
|----|------|------|----------|------|------|
| 1 | BUAV001_VENUE_1 | 北京考场1 | 北京航空培训中心 | 20-50人 | 教学楼 X层 XXX室 |
| 2 | BUAV001_VENUE_2 | 北京考场2 | 北京航空培训中心 | 20-50人 | 教学楼 X层 XXX室 |
| 3 | SUAV002_VENUE_1 | 上海考场1 | 上海航空培训中心 | 20-50人 | 教学楼 X层 XXX室 |
| 4 | SUAV002_VENUE_2 | 上海考场2 | 上海航空培训中心 | 20-50人 | 教学楼 X层 XXX室 |
| 5 | SUAV003_VENUE_1 | 深圳考场1 | 深圳航空培训中心 | 20-50人 | 教学楼 X层 XXX室 |
| 6 | SUAV003_VENUE_2 | 深圳考场2 | 深圳航空培训中心 | 20-50人 | 教学楼 X层 XXX室 |
| 7 | GUAV004_VENUE_1 | 广州考场1 | 广州航空培训中心 | 20-50人 | 教学楼 X层 XXX室 |
| 8 | GUAV004_VENUE_2 | 广州考场2 | 广州航空培训中心 | 20-50人 | 教学楼 X层 XXX室 |
| 9 | HUAV005_VENUE_1 | 杭州考场1 | 杭州航空培训中心 | 20-50人 | 教学楼 X层 XXX室 |
| 10 | HUAV005_VENUE_2 | 杭州考场2 | 杭州航空培训中心 | 20-50人 | 教学楼 X层 XXX室 |

**字段说明**:
- `description`: "{城市}考试场地"
- `capacity`: random.randint(20, 50)
- `building`: "教学楼"
- `floor`: "1-3层" (随机)
- `room_number`: "101-399" (随机)
- `status`: "available"
- `is_active`: true

---

## 📋 考试产品 (exam_products表)

| ID | 代码 | 名称 | 类型 | 时长 |
|----|------|------|------|------|
| 1 | MULTI_THEORY | 多旋翼视距内驾驶员理论 | 理论 | 60分钟 |
| 2 | MULTI_PRACTICE | 多旋翼视距内驾驶员实操 | 实操 | 15分钟 |
| 3 | FIXED_THEORY | 固定翼视距内驾驶员理论 | 理论 | 60分钟 |
| 4 | FIXED_PRACTICE | 固定翼视距内驾驶员实操 | 实操 | 20分钟 |
| 5 | INSTRUCTOR_THEORY | 无人机教员资格理论 | 理论 | 90分钟 |
| 6 | INSTRUCTOR_PRACTICE | 无人机教员资格实操 | 实操 | 30分钟 |

**字段说明**:
- `description`: "{名称}，考试时长{时长}分钟"
- `is_active`: true

---

## 👥 用户数据 (users表)

### 超级管理员 (1人)
| ID | 用户名 | 姓名 | 邮箱 | 电话 | 角色 | 密码 |
|----|--------|------|------|------|------|------|
| 1 | admin | 系统管理员 | admin@uav-exam.com | 13800000001 | super_admin | admin123 |

### 机构管理员 (5人)
| ID | 用户名 | 姓名 | 邮箱 | 电话 | 所属机构 | 密码 |
|----|--------|------|------|------|----------|------|
| 2 | beijing_admin | 北京管理员 | beijing_admin@example.com | 13800000002 | 北京航空培训中心 | 123456 |
| 3 | shanghai_admin | 上海管理员 | shanghai_admin@example.com | 13800000003 | 上海航空培训中心 | 123456 |
| 4 | shenzhen_admin | 深圳管理员 | shenzhen_admin@example.com | 13800000004 | 深圳航空培训中心 | 123456 |
| 5 | guangzhou_admin | 广州管理员 | guangzhou_admin@example.com | 13800000005 | 广州航空培训中心 | 123456 |
| 6 | hangzhou_admin | 杭州管理员 | hangzhou_admin@example.com | 13800000006 | 杭州航空培训中心 | 123456 |

### 考生用户 (10人)
| ID | 用户名 | 姓名 | 身份证 | 电话 | 邮箱 | 所属机构 | 密码 |
|----|--------|------|--------|------|------|----------|------|
| 7 | candidate_XXXX | 张三 | 110101199001XXXX | 13800010001 | candidate1@example.com | 随机机构 | 身份证后6位 |
| 8 | candidate_XXXX | 李四 | 110101199002XXXX | 13800010002 | candidate2@example.com | 随机机构 | 身份证后6位 |
| 9 | candidate_XXXX | 王五 | 110101199003XXXX | 13800010003 | candidate3@example.com | 随机机构 | 身份证后6位 |
| 10 | candidate_XXXX | 赵六 | 110101199004XXXX | 13800010004 | candidate4@example.com | 随机机构 | 身份证后6位 |
| 11 | candidate_XXXX | 钱七 | 110101199005XXXX | 13800010005 | candidate5@example.com | 随机机构 | 身份证后6位 |
| 12 | candidate_XXXX | 孙八 | 110101199006XXXX | 13800010006 | candidate6@example.com | 随机机构 | 身份证后6位 |
| 13 | candidate_XXXX | 周九 | 110101199007XXXX | 13800010007 | candidate7@example.com | 随机机构 | 身份证后6位 |
| 14 | candidate_XXXX | 吴十 | 110101199008XXXX | 13800010008 | candidate8@example.com | 随机机构 | 身份证后6位 |
| 15 | candidate_XXXX | 郑十一 | 110101199009XXXX | 13800010009 | candidate9@example.com | 随机机构 | 身份证后6位 |
| 16 | candidate_XXXX | 王十二 | 110101199010XXXX | 13800010010 | candidate10@example.com | 随机机构 | 身份证后6位 |

**考生字段说明**:
- `id_card`: 格式为 "11010119900{序号:02d}{随机4位数字}"
- `username`: "candidate_{身份证后6位}"
- `password_hash`: 身份证后6位的哈希值
- `role`: "candidate"
- `institution_id`: 随机分配到5个机构中的一个
- `is_active`: true
- `is_verified`: true
- `wechat_openid`: "wx_{18位随机数字}"

---

## 📝 报名记录 (exam_registrations表)

**总数**: 18条记录

**生成规则**:
- 每个考生随机报名1-3个考试产品
- 报名编号格式: "REG{日期YYYYMMDD}{考生ID:03d}{序号:02d}"
- 报名日期: 当前时间往前推0-30天随机
- 状态: 全部为 "approved" (已批准)
- 备注: "考生{姓名}报名{考试产品名称}"

**示例记录**:
```
报名号: REG20250127007001
考生ID: 7 (张三)
考试产品ID: 随机选择的产品
状态: approved
创建时间: 2025-01-XX (随机日期)
备注: 考生张三报名多旋翼视距内驾驶员理论
```

---

## 🔍 验证方法

### 1. 检查数据统计
```bash
python -c "
from app.config.database import SessionLocal
from app.models.user import User, UserRole
from app.models.institution import Institution
from app.models.venue import Venue
from app.models.exam import ExamProduct, ExamRegistration

session = SessionLocal()
print(f'机构: {session.query(Institution).count()}个')
print(f'考场: {session.query(Venue).count()}个')
print(f'考试产品: {session.query(ExamProduct).count()}个')
print(f'用户: {session.query(User).count()}人')
print(f'报名记录: {session.query(ExamRegistration).count()}条')
session.close()
"
```

### 2. 查看具体数据
```bash
# 查看考生身份证信息
python -c "
from app.config.database import SessionLocal
from app.models.user import User, UserRole
session = SessionLocal()
candidates = session.query(User).filter(User.role == UserRole.CANDIDATE).all()
for c in candidates:
    print(f'{c.real_name}: {c.username} | 身份证: {c.id_card}')
session.close()
"
```

---

## 📋 注意事项

1. **随机数据**: 身份证后4位、电话号码、考场容量、房间号等都是随机生成的
2. **机构分配**: 考生随机分配到5个机构中
3. **报名数量**: 每个考生报名1-3个考试，所以总报名数在10-30条之间
4. **密码**: 所有考生密码都是身份证后6位
5. **时间**: 报名时间是当前时间往前推0-30天的随机时间

你可以用上面的验证方法来对照检查数据是否符合预期！