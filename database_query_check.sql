-- 数据库查询代码 - 检查签到相关的时间数据

-- 1. 查看所有考试安排的时间信息
SELECT 
    s.id as schedule_id,
    s.schedule_date,
    s.start_time,
    s.end_time,
    s.status,
    u.real_name as candidate_name,
    u.id_card,
    v.name as venue_name,
    ep.name as exam_name
FROM schedules s
LEFT JOIN exam_registrations er ON s.registration_id = er.id
LEFT JOIN users u ON er.user_id = u.id
LEFT JOIN venues v ON s.venue_id = v.id
LEFT JOIN exam_products ep ON er.exam_product_id = ep.id
ORDER BY s.schedule_date, s.start_time;

-- 2. 查看schedule_id=1的具体信息（问题中涉及的考试安排）
SELECT 
    s.*,
    u.real_name as candidate_name,
    u.id_card,
    v.name as venue_name
FROM schedules s
LEFT JOIN exam_registrations er ON s.registration_id = er.id
LEFT JOIN users u ON er.user_id = u.id
LEFT JOIN venues v ON s.venue_id = v.id
WHERE s.id = 1;

-- 3. 查看candidate_id=5（张三）的所有考试安排
SELECT 
    s.id as schedule_id,
    s.schedule_date,
    s.start_time,
    s.end_time,
    s.status,
    v.name as venue_name,
    ep.name as exam_name
FROM schedules s
JOIN exam_registrations er ON s.registration_id = er.id
JOIN users u ON er.user_id = u.id
JOIN venues v ON s.venue_id = v.id
JOIN exam_products ep ON er.exam_product_id = ep.id
WHERE u.id = 5
ORDER BY s.schedule_date, s.start_time;

-- 4. 查看所有签到记录
SELECT 
    c.id,
    c.schedule_id,
    c.checkin_time,
    c.status,
    u.real_name as candidate_name,
    u.id_card,
    s.schedule_date,
    s.start_time,
    s.end_time
FROM checkins c
LEFT JOIN users u ON c.user_id = u.id
LEFT JOIN schedules s ON c.schedule_id = s.id
ORDER BY c.checkin_time DESC;

-- 5. 检查今天的考试安排（如果有的话）
SELECT 
    s.id as schedule_id,
    s.schedule_date,
    s.start_time,
    s.end_time,
    s.status,
    u.real_name as candidate_name,
    v.name as venue_name
FROM schedules s
LEFT JOIN exam_registrations er ON s.registration_id = er.id
LEFT JOIN users u ON er.user_id = u.id
LEFT JOIN venues v ON s.venue_id = v.id
WHERE s.schedule_date = CURDATE()
ORDER BY s.start_time;

-- 6. 查看数据库当前时间
SELECT NOW() as current_database_time;

-- 7. 计算签到时间窗口（基于schedule_id=1）
SELECT 
    s.schedule_date,
    s.start_time,
    s.end_time,
    DATE_SUB(CONCAT(s.schedule_date, ' ', s.start_time), INTERVAL 30 MINUTE) as checkin_start_time,
    DATE_ADD(CONCAT(s.schedule_date, ' ', IFNULL(s.end_time, TIME_ADD(s.start_time, INTERVAL 2 HOUR))), INTERVAL 30 MINUTE) as checkin_end_time,
    NOW() as current_time,
    CASE 
        WHEN NOW() < DATE_SUB(CONCAT(s.schedule_date, ' ', s.start_time), INTERVAL 30 MINUTE) THEN '签到时间未到'
        WHEN NOW() > DATE_ADD(CONCAT(s.schedule_date, ' ', IFNULL(s.end_time, TIME_ADD(s.start_time, INTERVAL 2 HOUR))), INTERVAL 30 MINUTE) THEN '签到时间已过'
        ELSE '可以签到'
    END as checkin_status
FROM schedules s
WHERE s.id = 1;