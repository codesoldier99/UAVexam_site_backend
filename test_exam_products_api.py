import requests
import json
from datetime import datetime

# API基础URL
BASE_URL = "http://localhost:8000"

# 测试数据
test_exam_product = {
    "name": "测试考试产品",
    "description": "这是一个测试用的考试产品",
    "code": "TEST_001",
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

def test_exam_products_api():
    """测试考试产品API的完整CRUD功能"""
    
    print("=" * 50)
    print("开始测试考试产品API")
    print("=" * 50)
    
    # 1. 测试获取考试产品列表
    print("\n1. 测试获取考试产品列表")
    try:
        response = requests.get(f"{BASE_URL}/exam-products/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取列表成功，共 {data.get('total', 0)} 个产品")
            print(f"   分页信息: 第{data.get('page', 1)}页，每页{data.get('size', 20)}条")
        else:
            print(f"❌ 获取列表失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
    except Exception as e:
        print(f"❌ 请求异常: {e}")
    
    # 2. 测试获取统计信息
    print("\n2. 测试获取统计信息")
    try:
        response = requests.get(f"{BASE_URL}/exam-products/stats/summary")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取统计成功")
            print(f"   总产品数: {data.get('total_products', 0)}")
            print(f"   激活产品: {data.get('active_products', 0)}")
            print(f"   未激活产品: {data.get('inactive_products', 0)}")
        else:
            print(f"❌ 获取统计失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 请求异常: {e}")
    
    # 3. 测试创建考试产品
    print("\n3. 测试创建考试产品")
    try:
        response = requests.post(
            f"{BASE_URL}/exam-products/",
            json=test_exam_product,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 201:
            data = response.json()
            product_id = data.get('id')
            print(f"✅ 创建产品成功，ID: {product_id}")
            print(f"   产品名称: {data.get('name')}")
            print(f"   产品代码: {data.get('code')}")
        else:
            print(f"❌ 创建产品失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
            product_id = None
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        product_id = None
    
    # 4. 测试获取单个考试产品
    if product_id:
        print(f"\n4. 测试获取单个考试产品 (ID: {product_id})")
        try:
            response = requests.get(f"{BASE_URL}/exam-products/{product_id}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 获取产品详情成功")
                print(f"   产品名称: {data.get('name')}")
                print(f"   产品描述: {data.get('description')}")
                print(f"   考试时长: {data.get('duration_minutes')}分钟")
                print(f"   考试费用: {data.get('price')}元")
            else:
                print(f"❌ 获取产品详情失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 请求异常: {e}")
    
    # 5. 测试更新考试产品
    if product_id:
        print(f"\n5. 测试更新考试产品 (ID: {product_id})")
        update_data = {
            "name": "更新后的测试考试产品",
            "description": "这是更新后的描述",
            "price": 2000.0,
            "training_price": 4000.0
        }
        try:
            response = requests.put(
                f"{BASE_URL}/exam-products/{product_id}",
                json=update_data,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 更新产品成功")
                print(f"   更新后名称: {data.get('name')}")
                print(f"   更新后价格: {data.get('price')}元")
            else:
                print(f"❌ 更新产品失败: {response.status_code}")
                print(f"   错误信息: {response.text}")
        except Exception as e:
            print(f"❌ 请求异常: {e}")
    
    # 6. 测试删除考试产品
    if product_id:
        print(f"\n6. 测试删除考试产品 (ID: {product_id})")
        try:
            response = requests.delete(f"{BASE_URL}/exam-products/{product_id}")
            if response.status_code == 204:
                print(f"✅ 删除产品成功")
            else:
                print(f"❌ 删除产品失败: {response.status_code}")
                print(f"   错误信息: {response.text}")
        except Exception as e:
            print(f"❌ 请求异常: {e}")
    
    # 7. 测试筛选功能
    print("\n7. 测试筛选功能")
    try:
        # 测试按类别筛选
        response = requests.get(f"{BASE_URL}/exam-products/?category=VLOS&page=1&size=5")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ VLOS类别筛选成功，找到 {data.get('total', 0)} 个产品")
        
        # 测试按状态筛选
        response = requests.get(f"{BASE_URL}/exam-products/?status=active&page=1&size=5")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 激活状态筛选成功，找到 {data.get('total', 0)} 个产品")
            
    except Exception as e:
        print(f"❌ 筛选测试异常: {e}")
    
    print("\n" + "=" * 50)
    print("考试产品API测试完成")
    print("=" * 50)

def test_with_auth():
    """测试带认证的API调用"""
    print("\n" + "=" * 50)
    print("测试带认证的API调用")
    print("=" * 50)
    
    # 这里需要先获取认证token
    # 由于认证系统复杂，这里只做基础测试
    print("注意: 需要有效的认证token才能测试完整的CRUD功能")
    print("建议先运行初始化脚本添加测试数据")

if __name__ == "__main__":
    # 运行基础测试
    test_exam_products_api()
    
    # 运行认证测试
    test_with_auth() 