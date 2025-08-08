#!/usr/bin/env python3
"""
场地API完整测试脚本
测试场地CRUD操作并验证数据库数据
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/venues"

def print_result(operation: str, response: requests.Response):
    """打印操作结果"""
    print(f"\n{'='*50}")
    print(f"操作: {operation}")
    print(f"状态码: {response.status_code}")
    print(f"响应内容:")
    try:
        data = response.json()
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except:
        print(response.text)
    print(f"{'='*50}")

def test_create_venue():
    """测试创建考场"""
    print("\n🏗️ 测试创建考场...")
    
    venues_data = [
        {
            "name": "北京理论考场A",
            "type": "理论考场"
        },
        {
            "name": "北京实操考场B",
            "type": "实操考场"
        },
        {
            "name": "上海理论考场C",
            "type": "理论考场"
        }
    ]
    
    created_venues = []
    for venue_data in venues_data:
        response = requests.post(API_URL, json=venue_data)
        print_result(f"创建考场: {venue_data['name']}", response)
        
        if response.status_code == 201:
            data = response.json()
            created_venues.append(data.get('data', {}).get('id'))
    
    return created_venues

def test_get_venues():
    """测试获取考场列表"""
    print("\n📋 测试获取考场列表...")
    
    # 测试基本列表
    response = requests.get(API_URL)
    print_result("获取考场列表", response)
    
    # 测试带分页
    response = requests.get(f"{API_URL}?page=1&size=2")
    print_result("分页获取考场列表", response)
    
    # 测试筛选
    response = requests.get(f"{API_URL}?status=active")
    print_result("筛选激活状态考场", response)
    
    # 测试搜索
    response = requests.get(f"{API_URL}?search=北京")
    print_result("搜索北京考场", response)

def test_get_venue_by_id(venue_id: int):
    """测试根据ID获取考场"""
    print(f"\n🔍 测试获取考场详情 (ID: {venue_id})...")
    
    response = requests.get(f"{API_URL}/{venue_id}")
    print_result(f"获取考场详情 (ID: {venue_id})", response)
    
    return response.status_code == 200

def test_update_venue(venue_id: int):
    """测试更新考场"""
    print(f"\n✏️ 测试更新考场 (ID: {venue_id})...")
    
    update_data = {
        "name": "北京理论考场A - 已升级",
        "status": "active"
    }
    
    response = requests.put(f"{API_URL}/{venue_id}", json=update_data)
    print_result(f"更新考场 (ID: {venue_id})", response)
    
    return response.status_code == 200

def test_venue_stats():
    """测试考场统计"""
    print("\n📊 测试考场统计信息...")
    
    response = requests.get(f"{API_URL}/stats/overview")
    print_result("获取考场统计信息", response)

def test_batch_update():
    """测试批量更新"""
    print("\n🔄 测试批量更新考场状态...")
    
    # 获取前两个考场的ID进行批量更新
    response = requests.get(f"{API_URL}?size=2")
    if response.status_code == 200:
        data = response.json()
        venue_ids = [item["id"] for item in data.get("data", {}).get("items", [])]
        
        if venue_ids:
            batch_data = {
                "venue_ids": venue_ids,
                "new_status": "inactive"
            }
            
            response = requests.patch(f"{API_URL}/batch/status", json=batch_data)
            print_result("批量更新考场状态", response)

def test_delete_venue(venue_id: int):
    """测试删除考场"""
    print(f"\n🗑️ 测试删除考场 (ID: {venue_id})...")
    
    response = requests.delete(f"{API_URL}/{venue_id}")
    print_result(f"删除考场 (ID: {venue_id})", response)
    
    return response.status_code == 200

def test_error_cases():
    """测试错误情况"""
    print("\n❌ 测试错误情况...")
    
    # 测试获取不存在的考场
    response = requests.get(f"{API_URL}/99999")
    print_result("获取不存在的考场", response)
    
    # 测试更新不存在的考场
    response = requests.put(f"{API_URL}/99999", json={"name": "test"})
    print_result("更新不存在的考场", response)
    
    # 测试删除不存在的考场
    response = requests.delete(f"{API_URL}/99999")
    print_result("删除不存在的考场", response)

def main():
    """主测试函数"""
    print("🚀 开始场地API完整测试")
    print(f"目标服务器: {BASE_URL}")
    
    try:
        # 检查服务器状态
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✅ 服务器状态正常 (状态码: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法连接到服务器: {e}")
        return
    
    # 执行测试
    created_venue_ids = test_create_venue()
    test_get_venues()
    
    if created_venue_ids:
        # 使用第一个创建的考场进行详细测试
        first_venue_id = created_venue_ids[0]
        
        test_get_venue_by_id(first_venue_id)
        test_update_venue(first_venue_id)
        test_venue_stats()
        test_batch_update()
        
        # 删除最后一个考场进行删除测试
        if len(created_venue_ids) > 1:
            test_delete_venue(created_venue_ids[-1])
    
    test_error_cases()
    
    print("\n🎉 测试完成!")
    print("请检查SwaggerUI界面: http://localhost:8000/docs")
    print("请检查数据库中的venues表以验证数据持久化")

if __name__ == "__main__":
    main()