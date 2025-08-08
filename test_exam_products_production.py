#!/usr/bin/env python3
"""
考试产品API生产级别测试脚本
包含完整的认证、错误处理、日志记录等功能
"""

import requests
import json
import time
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('exam_products_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class TestConfig:
    """测试配置"""
    base_url: str = "http://localhost:8000"
    username: str = "admin"
    password: str = "admin123"
    timeout: int = 30
    retry_count: int = 3

class ExamProductAPITester:
    """考试产品API测试器"""
    
    def __init__(self, config: TestConfig):
        self.config = config
        self.session = requests.Session()
        self.auth_token: Optional[str] = None
        self.test_results = []
        
    def log_test_result(self, test_name: str, success: bool, details: str = ""):
        """记录测试结果"""
        result = {
            "test_name": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        if success:
            logger.info(f"✅ {test_name}: 通过")
        else:
            logger.error(f"❌ {test_name}: 失败 - {details}")
    
    def authenticate(self) -> bool:
        """获取认证token"""
        try:
            # 这里需要根据实际的认证API进行调整
            auth_data = {
                "username": self.config.username,
                "password": self.config.password
            }
            
            response = self.session.post(
                f"{self.config.base_url}/auth/login",
                json=auth_data,
                timeout=self.config.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get("access_token")
                if self.auth_token:
                    self.session.headers.update({
                        "Authorization": f"Bearer {self.auth_token}"
                    })
                    logger.info("认证成功")
                    return True
                else:
                    logger.error("认证响应中没有token")
                    return False
            else:
                logger.error(f"认证失败: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"认证异常: {e}")
            return False
    
    def make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """发送HTTP请求"""
        url = f"{self.config.base_url}{endpoint}"
        
        for attempt in range(self.config.retry_count):
            try:
                response = self.session.request(
                    method, url, timeout=self.config.timeout, **kwargs
                )
                return response
            except requests.exceptions.RequestException as e:
                if attempt == self.config.retry_count - 1:
                    raise
                logger.warning(f"请求失败，重试 {attempt + 1}/{self.config.retry_count}: {e}")
                time.sleep(1)
    
    def test_get_exam_products(self) -> bool:
        """测试获取考试产品列表"""
        try:
            response = self.make_request("GET", "/exam-products/")
            
            if response.status_code == 200:
                data = response.json()
                total = data.get("total", 0)
                items = data.get("items", [])
                
                logger.info(f"获取考试产品列表成功: 共 {total} 个产品")
                for item in items[:3]:  # 显示前3个产品
                    logger.info(f"  - {item.get('name')} (ID: {item.get('id')})")
                
                self.log_test_result("获取考试产品列表", True, f"共 {total} 个产品")
                return True
            else:
                self.log_test_result("获取考试产品列表", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("获取考试产品列表", False, str(e))
            return False
    
    def test_get_exam_product_stats(self) -> bool:
        """测试获取考试产品统计信息"""
        try:
            response = self.make_request("GET", "/exam-products/stats/summary")
            
            if response.status_code == 200:
                data = response.json()
                total = data.get("total_products", 0)
                active = data.get("active_products", 0)
                
                logger.info(f"获取统计信息成功: 总数 {total}, 激活 {active}")
                
                self.log_test_result("获取考试产品统计", True, f"总数 {total}, 激活 {active}")
                return True
            else:
                self.log_test_result("获取考试产品统计", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("获取考试产品统计", False, str(e))
            return False
    
    def test_create_exam_product(self) -> Optional[int]:
        """测试创建考试产品"""
        try:
            test_product = {
                "name": f"测试产品 {datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "description": "这是一个测试用的考试产品",
                "code": f"TEST_{int(time.time())}",
                "category": "VLOS",
                "exam_type": "MULTIROTOR",
                "exam_class": "AGRICULTURE",
                "exam_level": "PILOT",
                "duration_minutes": 120,
                "theory_pass_score": 80,
                "practical_pass_score": 80,
                "training_hours": 40,
                "price": 1500.0,
                "training_price": 3000.0,
                "theory_content": "测试理论内容",
                "practical_content": "测试实操内容",
                "requirements": "测试要求"
            }
            
            response = self.make_request(
                "POST", 
                "/exam-products/",
                json=test_product
            )
            
            if response.status_code == 201:
                data = response.json()
                product_id = data.get("id")
                product_name = data.get("name")
                
                logger.info(f"创建考试产品成功: {product_name} (ID: {product_id})")
                self.log_test_result("创建考试产品", True, f"ID: {product_id}")
                return product_id
            else:
                self.log_test_result("创建考试产品", False, f"HTTP {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            self.log_test_result("创建考试产品", False, str(e))
            return None
    
    def test_get_exam_product_detail(self, product_id: int) -> bool:
        """测试获取考试产品详情"""
        try:
            response = self.make_request("GET", f"/exam-products/{product_id}")
            
            if response.status_code == 200:
                data = response.json()
                product_name = data.get("name")
                
                logger.info(f"获取产品详情成功: {product_name}")
                self.log_test_result("获取考试产品详情", True, f"产品: {product_name}")
                return True
            else:
                self.log_test_result("获取考试产品详情", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("获取考试产品详情", False, str(e))
            return False
    
    def test_update_exam_product(self, product_id: int) -> bool:
        """测试更新考试产品"""
        try:
            update_data = {
                "name": f"更新后的测试产品 {datetime.now().strftime('%H%M%S')}",
                "description": "这是更新后的描述",
                "price": 2000.0,
                "training_price": 4000.0
            }
            
            response = self.make_request(
                "PUT",
                f"/exam-products/{product_id}",
                json=update_data
            )
            
            if response.status_code == 200:
                data = response.json()
                product_name = data.get("name")
                
                logger.info(f"更新考试产品成功: {product_name}")
                self.log_test_result("更新考试产品", True, f"产品: {product_name}")
                return True
            else:
                self.log_test_result("更新考试产品", False, f"HTTP {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            self.log_test_result("更新考试产品", False, str(e))
            return False
    
    def test_delete_exam_product(self, product_id: int) -> bool:
        """测试删除考试产品"""
        try:
            response = self.make_request("DELETE", f"/exam-products/{product_id}")
            
            if response.status_code == 204:
                logger.info(f"删除考试产品成功: ID {product_id}")
                self.log_test_result("删除考试产品", True, f"ID: {product_id}")
                return True
            else:
                self.log_test_result("删除考试产品", False, f"HTTP {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            self.log_test_result("删除考试产品", False, str(e))
            return False
    
    def test_search_and_filter(self) -> bool:
        """测试搜索和筛选功能"""
        try:
            # 测试按类别筛选
            response = self.make_request("GET", "/exam-products/?category=VLOS&page=1&size=5")
            
            if response.status_code == 200:
                data = response.json()
                total = data.get("total", 0)
                logger.info(f"VLOS类别筛选成功: 找到 {total} 个产品")
                
                # 测试价格筛选
                response2 = self.make_request("GET", "/exam-products/?min_price=1000&max_price=3000&page=1&size=5")
                
                if response2.status_code == 200:
                    data2 = response2.json()
                    total2 = data2.get("total", 0)
                    logger.info(f"价格筛选成功: 找到 {total2} 个产品")
                    
                    self.log_test_result("搜索和筛选功能", True, f"类别筛选: {total}, 价格筛选: {total2}")
                    return True
                else:
                    self.log_test_result("搜索和筛选功能", False, f"价格筛选失败: HTTP {response2.status_code}")
                    return False
            else:
                self.log_test_result("搜索和筛选功能", False, f"类别筛选失败: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result("搜索和筛选功能", False, str(e))
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """运行所有测试"""
        logger.info("=" * 60)
        logger.info("开始考试产品API生产级别测试")
        logger.info("=" * 60)
        
        # 1. 认证
        if not self.authenticate():
            logger.error("认证失败，无法继续测试")
            return {"success": False, "error": "认证失败"}
        
        # 2. 基础功能测试
        self.test_get_exam_products()
        self.test_get_exam_product_stats()
        
        # 3. CRUD功能测试
        product_id = self.test_create_exam_product()
        if product_id:
            self.test_get_exam_product_detail(product_id)
            self.test_update_exam_product(product_id)
            self.test_delete_exam_product(product_id)
        
        # 4. 高级功能测试
        self.test_search_and_filter()
        
        # 5. 生成测试报告
        success_count = sum(1 for result in self.test_results if result["success"])
        total_count = len(self.test_results)
        
        logger.info("=" * 60)
        logger.info("测试完成")
        logger.info(f"总测试数: {total_count}")
        logger.info(f"成功数: {success_count}")
        logger.info(f"失败数: {total_count - success_count}")
        logger.info(f"成功率: {success_count/total_count*100:.1f}%")
        logger.info("=" * 60)
        
        return {
            "success": success_count == total_count,
            "total_tests": total_count,
            "passed_tests": success_count,
            "failed_tests": total_count - success_count,
            "success_rate": success_count/total_count*100,
            "results": self.test_results
        }

def main():
    """主函数"""
    config = TestConfig()
    tester = ExamProductAPITester(config)
    
    try:
        result = tester.run_all_tests()
        
        # 保存测试报告
        with open("exam_products_test_report.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        if result["success"]:
            logger.info("🎉 所有测试通过！")
            exit(0)
        else:
            logger.error("❌ 部分测试失败")
            exit(1)
            
    except Exception as e:
        logger.error(f"测试执行异常: {e}")
        exit(1)

if __name__ == "__main__":
    main() 