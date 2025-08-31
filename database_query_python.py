#!/usr/bin/env python3
"""
Python版本的数据库查询代码
"""

import mysql.connector
from datetime import datetime, timedelta
import json

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3307,
    'user': 'dev_user',
    'password': 'a_good_password_for_dev',
    'database': 'exam_site_dev_db'
}

def connect_database():
    """连接数据库"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None

def query_schedule_info():
    """查询考试安排信息"""
    conn = connect_database()
    if not conn:
        return
    
    cursor = conn.cursor(dictionary=True)
    
    print("=" * 60)
    print("1. 查询schedule_id=1的详细信息")
    print("=" * 60)
    
    query = """
    SELECT 
        s.*,
        u.real_name as candidate_name,
        u.id_card,
        v.name as venue_name,
        ep.name as exam_name
    FROM schedules s
    LEFT JOIN exam_registrations er ON s.registration_id = er.id
    LEFT JOIN users u ON er.user_id = u.id
    LEFT JOIN venues v ON s.venue_id = v.id
    LEFT JOIN exam_products ep ON er.exam_product_id = ep.id
    WHERE s.id = 1
    """
    
    cursor.execute(query)
    result = cursor.fetchone()
    
    if result:
        print(f"考试安排ID: {result['id']}")
        print(f"考试日期: {result['schedule_date']}")
        print(f"开始时间: {result['start_time']}")
        print(f"结束时间: {result['end_time']}")
        print(f"状态: {result['status']}")
        print(f"考生姓名: {result['candidate_name']}")
        print(f"身份证: {result['id_card']}")
        print(f"考场: {result['venue_name']}")
        print(f"考试项目: {result['exam_name']}")
        
        # 计算签到时间窗口
        if result['schedule_date'] and result['start_time']:
            exam_datetime = datetime.combine(result['schedule_date'], result['start_time'])
            end_time = result['end_time'] if result['end_time'] else (datetime.combine(result['schedule_date'], result['start_time']) + timedelta(hours=2)).time()
            exam_end_datetime = datetime.combine(result['schedule_date'], end_time)
            
            checkin_start = exam_datetime - timedelta(minutes=30)
            checkin_end = exam_end_datetime + timedelta(minutes=30)
            current_time = datetime.now()
            
            print(f"\n时间分析:")
            print(f"考试时间: {exam_datetime}")
            print(f"考试结束: {exam_end_datetime}")
            print(f"签到开始: {checkin_start}")
            print(f"签到结束: {checkin_end}")
            print(f"当前时间: {current_time}")
            
            if current_time < checkin_start:
                print(f"状态: ❌ 签到时间未到")
            elif current_time > checkin_end:
                print(f"状态: ❌ 签到时间已过")
            else:
                print(f"状态: ✅ 可以签到")
    
    print("\n" + "=" * 60)
    print("2. 查询所有考试安排")
    print("=" * 60)
    
    query2 = """
    SELECT 
        s.id,
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
    ORDER BY s.schedule_date, s.start_time
    """
    
    cursor.execute(query2)
    results = cursor.fetchall()
    
    for row in results:
        print(f"ID:{row['id']} | 日期:{row['schedule_date']} | 时间:{row['start_time']}-{row['end_time']} | 考生:{row['candidate_name']} | 考场:{row['venue_name']}")
    
    print("\n" + "=" * 60)
    print("3. 查询签到记录")
    print("=" * 60)
    
    query3 = """
    SELECT 
        c.id,
        c.schedule_id,
        c.checkin_time,
        c.status,
        u.real_name as candidate_name
    FROM checkins c
    LEFT JOIN users u ON c.user_id = u.id
    ORDER BY c.checkin_time DESC
    """
    
    cursor.execute(query3)
    checkins = cursor.fetchall()
    
    for checkin in checkins:
        print(f"签到ID:{checkin['id']} | 考试:{checkin['schedule_id']} | 时间:{checkin['checkin_time']} | 状态:{checkin['status']} | 考生:{checkin['candidate_name']}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    print("数据库查询 - 签到时间问题分析")
    query_schedule_info()