import mysql.connector
from datetime import datetime

# 数据库配置 - 请根据你的实际配置修改
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',  # 替换为你的数据库用户名
    'password': 'root',  # 替换为你的数据库密码
    'database': 'exam_site_dev_db'  # 替换为你的数据库名
}

def check_test_data():
    """检查测试所需的数据"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        print("=== 检查测试数据 ===")
        
        # 1. 检查考生数据
        print("\n1. 考生数据:")
        cursor.execute("""
            SELECT id, username, real_name, id_card, phone, is_active 
            FROM users 
            WHERE role = 'candidate' 
            LIMIT 5
        """)
        candidates = cursor.fetchall()
        
        if candidates:
            for candidate in candidates:
                print(f"  ID: {candidate['id']}, 姓名: {candidate['real_name']}, 身份证: {candidate['id_card']}")
        else:
            print("  ❌ 没有找到考生数据")
        
        # 2. 检查考务人员数据
        print("\n2. 考务人员数据:")
        cursor.execute("""
            SELECT id, username, real_name 
            FROM users 
            WHERE role = 'examiner' 
            LIMIT 3
        """)
        examiners = cursor.fetchall()
        
        if examiners:
            for examiner in examiners:
                print(f"  ID: {examiner['id']}, 姓名: {examiner['real_name']}")
        else:
            print("  ❌ 没有找到考务人员数据")
        
        # 3. 检查考场数据
        print("\n3. 考场数据:")
        cursor.execute("""
            SELECT id, name, building, floor, room_number, capacity 
            FROM venues 
            LIMIT 3
        """)
        venues = cursor.fetchall()
        
        if venues:
            for venue in venues:
                print(f"  ID: {venue['id']}, 名称: {venue['name']}, 位置: {venue['building']} {venue['floor']} {venue['room_number']}")
        else:
            print("  ❌ 没有找到考场数据")
        
        # 4. 检查考试安排数据
        print("\n4. 考试安排数据:")
        cursor.execute("""
            SELECT s.id, s.exam_date, s.start_time, s.end_time, s.status,
                   v.name as venue_name, v.id as venue_id
            FROM schedules s
            JOIN venues v ON s.venue_id = v.id
            WHERE s.status = 'scheduled'
            LIMIT 3
        """)
        schedules = cursor.fetchall()
        
        if schedules:
            for schedule in schedules:
                print(f"  ID: {schedule['id']}, 日期: {schedule['exam_date']}, 时间: {schedule['start_time']}-{schedule['end_time']}, 考场: {schedule['venue_name']}")
        else:
            print("  ❌ 没有找到考试安排数据")
        
        # 5. 检查考生报名数据
        print("\n5. 考生报名数据:")
        cursor.execute("""
            SELECT er.id, er.user_id, er.schedule_id, er.status,
                   u.real_name, u.id_card,
                   s.exam_date, s.start_time
            FROM exam_registrations er
            JOIN users u ON er.user_id = u.id
            JOIN schedules s ON er.schedule_id = s.id
            WHERE er.status = 'registered'
            LIMIT 5
        """)
        registrations = cursor.fetchall()
        
        if registrations:
            for reg in registrations:
                print(f"  考生: {reg['real_name']} ({reg['id_card']}) -> 考试: {reg['exam_date']} {reg['start_time']}")
        else:
            print("  ❌ 没有找到考生报名数据")
        
        # 6. 生成测试建议
        print("\n=== 测试建议 ===")
        if candidates and schedules and registrations:
            test_candidate = candidates[0]
            print(f"建议使用考生进行测试:")
            print(f"  身份证号: {test_candidate['id_card']}")
            print(f"  考生ID: {test_candidate['id']}")
            
            if examiners:
                test_examiner = examiners[0]
                print(f"建议使用考务人员进行测试:")
                print(f"  考务人员ID: {test_examiner['id']}")
        else:
            print("❌ 缺少必要的测试数据，请先运行数据初始化脚本")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        print(f"数据库连接错误: {e}")
        print("请检查数据库配置和连接")

if __name__ == "__main__":
    check_test_data()