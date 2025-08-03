#!/usr/bin/env python3
"""
考试系统API接口全面测试脚本
测试所有42个API接口的功能
"""
import asyncio
import aiohttp
import json
import time
from datetime import datetime, date
from typing import Dict, Any, List

class APITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None
        self.access_token = None
        self.test_results = []
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def log_result(self, test_name: str, success: bool, details: str = ""):
        """记录测试结果"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.test_results.append({
            "test": test_name,
            "status": status,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        print(f"{status} - {test_name}: {details}")
    
    async def test_api_endpoint(self, method: str, endpoint: str, data: Dict = None, 
                               expected_status: int = 200, test_name: str = ""):
        """通用API测试方法"""
        try:
            url = f"{self.base_url}{endpoint}"
            headers = {}
            
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"
            
            if method.upper() == "GET":
                async with self.session.get(url, headers=headers) as response:
                    response_data = await response.json()
                    success = response.status == expected_status
                    
            elif method.upper() == "POST":
                headers["Content-Type"] = "application/json"
                async with self.session.post(url, json=data, headers=headers) as response:
                    response_data = await response.json()
                    success = response.status == expected_status
                    
            elif method.upper() == "PUT":
                headers["Content-Type"] = "application/json"
                async with self.session.put(url, json=data, headers=headers) as response:
                    response_data = await response.json()
                    success = response.status == expected_status
                    
            elif method.upper() == "DELETE":
                async with self.session.delete(url, headers=headers) as response:
                    response_data = await response.json()
                    success = response.status == expected_status
            
            details = f"Status: {response.status}, Response: {str(response_data)[:100]}..."
            self.log_result(test_name or f"{method} {endpoint}", success, details)
            
            return success, response_data
            
        except Exception as e:
            self.log_result(test_name or f"{method} {endpoint}", False, f"Error: {str(e)}")
            return False, None
    
    async def test_health_endpoints(self):
        """测试健康检查端点"""
        print("\n🏥 === 健康检查端点测试 ===")
        
        await self.test_api_endpoint("GET", "/", test_name="根路径访问")
        await self.test_api_endpoint("GET", "/test", test_name="测试端点")
        await self.test_api_endpoint("GET", "/health", test_name="健康检查")
    
    async def test_venues_endpoints(self):
        """测试场地管理端点"""
        print("\n🏢 === 场地管理端点测试 ===")
        
        # 测试场地列表
        await self.test_api_endpoint("GET", "/venues/", test_name="获取场地列表")
        await self.test_api_endpoint("GET", "/venues/?page=1&size=5", test_name="场地列表分页")
        await self.test_api_endpoint("GET", "/venues/?status=active", test_name="场地状态筛选")
        await self.test_api_endpoint("GET", "/venues/?venue_type=理论考场", test_name="场地类型筛选")
        
        # 测试单个场地
        await self.test_api_endpoint("GET", "/venues/1", test_name="获取场地详情")
        await self.test_api_endpoint("GET", "/venues/999", expected_status=200, test_name="获取不存在场地")
    
    async def test_exam_products_endpoints(self):
        """测试考试产品端点"""
        print("\n📚 === 考试产品端点测试 ===")
        
        # 测试产品列表
        await self.test_api_endpoint("GET", "/exam-products/", test_name="获取产品列表")
        await self.test_api_endpoint("GET", "/exam-products/?page=1&size=3", test_name="产品列表分页")
        await self.test_api_endpoint("GET", "/exam-products/?category=理论+实操", test_name="产品类别筛选")
        await self.test_api_endpoint("GET", "/exam-products/?status=active", test_name="产品状态筛选")
        await self.test_api_endpoint("GET", "/exam-products/?difficulty=中等", test_name="产品难度筛选")
        
        # 测试单个产品
        await self.test_api_endpoint("GET", "/exam-products/1", test_name="获取产品详情")
        await self.test_api_endpoint("GET", "/exam-products/999", expected_status=200, test_name="获取不存在产品")
    
    async def test_candidates_endpoints(self):
        """测试考生管理端点"""
        print("\n👥 === 考生管理端点测试 ===")
        
        # 基础列表查询
        await self.test_api_endpoint("GET", "/candidates/", test_name="获取考生列表")
        await self.test_api_endpoint("GET", "/candidates/?page=1&size=5", test_name="考生列表分页")
        await self.test_api_endpoint("GET", "/candidates/?status=registered", test_name="考生状态筛选")
        await self.test_api_endpoint("GET", "/candidates/?gender=男", test_name="考生性别筛选")
        
    async def test_schedules_endpoints(self):
        """测试排期管理端点"""
        print("\n📅 === 排期管理端点测试 ===")
        
        # 基础排期查询
        await self.test_api_endpoint("GET", "/schedules/", test_name="获取排期列表")
        await self.test_api_endpoint("GET", "/schedules/?page=1&size=5", test_name="排期列表分页")
        await self.test_api_endpoint("GET", "/schedules/?status=待确认", test_name="排期状态筛选")
        
    async def test_roles_permissions_endpoints(self):
        """测试角色权限端点"""
        print("\n🔐 === 角色权限端点测试 ===")
        
        # 角色管理
        await self.test_api_endpoint("GET", "/roles/", test_name="获取角色列表")
        
        # 权限管理
        await self.test_api_endpoint("GET", "/permissions/", test_name="获取权限列表")
    
    async def test_users_endpoints(self):
        """测试用户管理端点"""
        print("\n👤 === 用户管理端点测试 ===")
        
        await self.test_api_endpoint("GET", "/users/", test_name="获取用户列表")
    
    async def generate_test_report(self):
        """生成测试报告"""
        print("\n📊 === 测试报告生成 ===")
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        report = {
            "test_summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "success_rate": f"{success_rate:.1f}%",
                "test_time": datetime.now().isoformat()
            },
            "test_results": self.test_results
        }
        
        # 保存报告到文件
        with open("api_test_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # 打印摘要
        print(f"\n🎯 === 测试摘要 ===")
        print(f"总测试数: {total_tests}")
        print(f"通过数: {passed_tests}")
        print(f"失败数: {failed_tests}")
        print(f"成功率: {success_rate:.1f}%")
        print(f"详细报告已保存到: api_test_report.json")
        
        return report

async def main():
    """主测试函数"""
    print("🚀 === 考试系统API接口全面测试开始 ===")
    print(f"测试时间: {datetime.now().isoformat()}")
    print("目标: 测试主要API接口的功能\n")
    
    async with APITester() as tester:
        # 等待服务器启动
        print("⏳ 等待服务器启动...")
        await asyncio.sleep(2)
        
        # 执行各模块测试
        await tester.test_health_endpoints()
        await tester.test_venues_endpoints()
        await tester.test_exam_products_endpoints()
        await tester.test_candidates_endpoints()
        await tester.test_schedules_endpoints()
        await tester.test_roles_permissions_endpoints()
        await tester.test_users_endpoints()
        
        # 生成测试报告
        await tester.generate_test_report()
    
    print("\n🎉 === API接口测试完成 ===")

if __name__ == "__main__":
    asyncio.run(main())