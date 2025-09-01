#!/usr/bin/env python3
"""
考试产品接口测试脚本
测试 /api/v1/pc/exam-products 相关接口
"""

import requests
import json
import time
from datetime import datetime

# 配置
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

# 测试用户凭据
TEST_USER = {
    "username": "admin",  # 根据实际情况修改
    "password": "admin123"  # 根据实际情况修改
}

class ExamProductsAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.headers = {"Content-Type": "application/json"}
        
    def login(self):
        """登录获取token"""
        print("🔐 正在登录...")
        login_url = f"{API_BASE}/pc/auth/login"
        
        try:
            response = self.session.post(
                login_url, 
                json=TEST_USER,
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                if self.token:
                    self.headers["Authorization"] = f"Bearer {self.token}"
                    print("✅ 登录成功")
                    return True
                else:
                    print("❌ 登录失败：未获取到token")
                    return False
            else:
                print(f"❌ 登录失败：{response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 登录异常：{str(e)}")
            return False
    
    def test_get_exam_products_list(self):
        """测试获取考试产品列表"""
        print("\n📋 测试获取考试产品列表...")
        
        # 测试不同的路径格式
        test_urls = [
            f"{API_BASE}/pc/exam-products",      # 无斜杠
            f"{API_BASE}/pc/exam-products/",     # 有斜杠
            f"{API_BASE}/pc/exam-products?skip=0&limit=20",  # 带参数
            f"{API_BASE}/pc/exam-products/?skip=0&limit=10", # 带斜杠和参数
        ]
        
        for i, url in enumerate(test_urls, 1):
            print(f"\n  测试 {i}: {url}")
            try:
                response = self.session.get(url, headers=self.headers)
                print(f"    状态码: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, dict) and "items" in data:
                        print(f"    ✅ 成功 - 返回 {len(data['items'])} 条记录")
                        print(f"    总数: {data.get('total', 'N/A')}")
                        print(f"    页数: {data.get('pages', 'N/A')}")
                    elif isinstance(data, list):
                        print(f"    ✅ 成功 - 返回 {len(data)} 条记录（旧格式）")
                    else:
                        print(f"    ⚠️  返回格式异常: {type(data)}")
                elif response.status_code == 307:
                    print(f"    🔄 重定向到: {response.headers.get('Location', 'N/A')}")
                elif response.status_code == 422:
                    print(f"    ❌ 参数错误: {response.text}")
                else:
                    print(f"    ❌ 失败: {response.text}")
                    
            except Exception as e:
                print(f"    ❌ 异常: {str(e)}")
    
    def test_search_exam_products(self):
        """测试搜索考试产品"""
        print("\n🔍 测试搜索考试产品...")
        
        search_terms = ["无人机", "驾驶员", "多旋翼", "test"]
        
        for term in search_terms:
            print(f"\n  搜索关键词: '{term}'")
            url = f"{API_BASE}/pc/exam-products?search={term}&limit=5"
            
            try:
                response = self.session.get(url, headers=self.headers)
                print(f"    状态码: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, dict) and "items" in data:
                        items = data["items"]
                        print(f"    ✅ 找到 {len(items)} 条匹配记录")
                        for item in items[:2]:  # 只显示前2条
                            print(f"      - {item.get('name', 'N/A')} ({item.get('code', 'N/A')})")
                    else:
                        print(f"    ⚠️  返回格式异常")
                else:
                    print(f"    ❌ 搜索失败: {response.text}")
                    
            except Exception as e:
                print(f"    ❌ 异常: {str(e)}")
    
    def test_filter_exam_products(self):
        """测试过滤考试产品"""
        print("\n🎯 测试过滤考试产品...")
        
        filters = [
            {"is_active": True, "desc": "活跃产品"},
            {"is_active": False, "desc": "非活跃产品"},
        ]
        
        for filter_config in filters:
            is_active = filter_config["is_active"]
            desc = filter_config["desc"]
            
            print(f"\n  过滤条件: {desc}")
            url = f"{API_BASE}/pc/exam-products?is_active={str(is_active).lower()}&limit=10"
            
            try:
                response = self.session.get(url, headers=self.headers)
                print(f"    状态码: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, dict) and "items" in data:
                        items = data["items"]
                        print(f"    ✅ 找到 {len(items)} 条{desc}")
                        # 验证过滤结果
                        for item in items[:3]:
                            actual_status = item.get('is_active', None)
                            status_match = actual_status == is_active
                            print(f"      - {item.get('name', 'N/A')}: {'✅' if status_match else '❌'} {actual_status}")
                    else:
                        print(f"    ⚠️  返回格式异常")
                else:
                    print(f"    ❌ 过滤失败: {response.text}")
                    
            except Exception as e:
                print(f"    ❌ 异常: {str(e)}")
    
    def test_get_exam_product_detail(self):
        """测试获取考试产品详情"""
        print("\n📄 测试获取考试产品详情...")
        
        # 先获取一个产品ID
        list_url = f"{API_BASE}/pc/exam-products?limit=1"
        try:
            response = self.session.get(list_url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and "items" in data and data["items"]:
                    product_id = data["items"][0]["id"]
                    print(f"  使用产品ID: {product_id}")
                    
                    # 测试详情接口
                    detail_url = f"{API_BASE}/pc/exam-products/{product_id}/"
                    detail_response = self.session.get(detail_url, headers=self.headers)
                    
                    print(f"    状态码: {detail_response.status_code}")
                    if detail_response.status_code == 200:
                        detail_data = detail_response.json()
                        print(f"    ✅ 获取详情成功")
                        print(f"      名称: {detail_data.get('name', 'N/A')}")
                        print(f"      代码: {detail_data.get('code', 'N/A')}")
                        print(f"      状态: {detail_data.get('is_active', 'N/A')}")
                    else:
                        print(f"    ❌ 获取详情失败: {detail_response.text}")
                else:
                    print("    ⚠️  没有找到可用的产品ID")
            else:
                print(f"    ❌ 获取产品列表失败: {response.text}")
                
        except Exception as e:
            print(f"    ❌ 异常: {str(e)}")
    
    def test_get_statistics(self):
        """测试获取统计信息"""
        print("\n📊 测试获取统计信息...")
        
        stats_url = f"{API_BASE}/pc/exam-products/statistics/"
        
        try:
            response = self.session.get(stats_url, headers=self.headers)
            print(f"    状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"    ✅ 获取统计成功")
                print(f"      总产品数: {data.get('total_products', 'N/A')}")
                print(f"      活跃产品: {data.get('active_products', 'N/A')}")
                print(f"      非活跃产品: {data.get('inactive_products', 'N/A')}")
            else:
                print(f"    ❌ 获取统计失败: {response.text}")
                
        except Exception as e:
            print(f"    ❌ 异常: {str(e)}")
    
    def test_pagination(self):
        """测试分页功能"""
        print("\n📖 测试分页功能...")
        
        pagination_tests = [
            {"skip": 0, "limit": 5, "desc": "第1页，每页5条"},
            {"skip": 5, "limit": 5, "desc": "第2页，每页5条"},
            {"skip": 0, "limit": 1, "desc": "第1页，每页1条"},
            {"skip": 0, "limit": 100, "desc": "第1页，每页100条"},
        ]
        
        for test in pagination_tests:
            skip = test["skip"]
            limit = test["limit"]
            desc = test["desc"]
            
            print(f"\n  {desc}")
            url = f"{API_BASE}/pc/exam-products?skip={skip}&limit={limit}"
            
            try:
                response = self.session.get(url, headers=self.headers)
                print(f"    状态码: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, dict) and "items" in data:
                        items_count = len(data["items"])
                        total = data.get("total", 0)
                        page = data.get("page", 0)
                        pages = data.get("pages", 0)
                        
                        print(f"    ✅ 返回 {items_count} 条记录")
                        print(f"      总数: {total}, 当前页: {page}, 总页数: {pages}")
                        
                        # 验证分页逻辑
                        expected_page = (skip // limit) + 1 if limit > 0 else 1
                        if page == expected_page:
                            print(f"      ✅ 分页计算正确")
                        else:
                            print(f"      ❌ 分页计算错误，期望: {expected_page}")
                    else:
                        print(f"    ⚠️  返回格式异常")
                else:
                    print(f"    ❌ 分页测试失败: {response.text}")
                    
            except Exception as e:
                print(f"    ❌ 异常: {str(e)}")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始测试考试产品接口")
        print("=" * 50)
        
        # 登录
        if not self.login():
            print("❌ 登录失败，无法继续测试")
            return
        
        # 运行各项测试
        try:
            self.test_get_exam_products_list()
            time.sleep(1)
            
            self.test_search_exam_products()
            time.sleep(1)
            
            self.test_filter_exam_products()
            time.sleep(1)
            
            self.test_get_exam_product_detail()
            time.sleep(1)
            
            self.test_get_statistics()
            time.sleep(1)
            
            self.test_pagination()
            
        except KeyboardInterrupt:
            print("\n⏹️  测试被用户中断")
        except Exception as e:
            print(f"\n❌ 测试过程中发生异常: {str(e)}")
        
        print("\n" + "=" * 50)
        print("🏁 测试完成")

def main():
    """主函数"""
    print("考试产品接口测试脚本")
    print(f"测试目标: {BASE_URL}")
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 检查服务器连接
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ 服务器连接正常")
        else:
            print(f"⚠️  服务器响应异常: {response.status_code}")
    except Exception as e:
        print(f"❌ 无法连接到服务器: {str(e)}")
        print("请确保后端服务正在运行")
        return
    
    # 运行测试
    tester = ExamProductsAPITester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()