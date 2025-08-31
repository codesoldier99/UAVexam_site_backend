#!/usr/bin/env python3
"""
后端服务连接测试脚本
测试8000端口的FastAPI服务是否正常运行
"""

import requests
import json
import time
from datetime import datetime

def test_backend_connection():
    """测试后端服务连接"""
    base_url = "http://127.0.0.1:8000"
    
    print("🚀 开始测试后端服务连接")
    print("=" * 60)
    print(f"📡 测试地址: {base_url}")
    print(f"🕐 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 测试项目列表
    tests = [
        {
            "name": "健康检查",
            "url": f"{base_url}/api/v1/health",
            "method": "GET",
            "expected_status": 200,
            "description": "检查服务基本状态"
        },
        {
            "name": "API文档访问",
            "url": f"{base_url}/docs",
            "method": "GET", 
            "expected_status": 200,
            "description": "检查Swagger文档是否可访问"
        },
        {
            "name": "OpenAPI规范",
            "url": f"{base_url}/openapi.json",
            "method": "GET",
            "expected_status": 200,
            "description": "检查OpenAPI规范文件"
        },
        {
            "name": "根路径访问",
            "url": f"{base_url}/",
            "method": "GET",
            "expected_status": 200,
            "description": "检查根路径重定向"
        },
        {
            "name": "身份证查询接口",
            "url": f"{base_url}/api/v1/wechat/candidate/info-by-idcard?id_card=110101199001011234",
            "method": "GET",
            "expected_status": [200, 404],
            "description": "测试新增的身份证查询接口"
        }
    ]
    
    results = []
    success_count = 0
    
    for i, test in enumerate(tests, 1):
        print(f"\n🔍 测试 {i}/{len(tests)}: {test['name']}")
        print(f"📋 描述: {test['description']}")
        print(f"🌐 URL: {test['url']}")
        
        try:
            # 发送请求
            start_time = time.time()
            response = None
            
            if test['method'] == 'GET':
                response = requests.get(test['url'], timeout=10)
            elif test['method'] == 'POST':
                response = requests.post(test['url'], timeout=10)
            
            if response is None:
                raise Exception(f"Unsupported method: {test['method']}")
            
            end_time = time.time()
            response_time = round((end_time - start_time) * 1000, 2)
            
            # 检查状态码
            expected_status = test['expected_status']
            if isinstance(expected_status, list):
                status_ok = response.status_code in expected_status
            else:
                status_ok = response.status_code == expected_status
            
            if status_ok:
                print(f"✅ 状态码: {response.status_code} (正常)")
                print(f"⏱️ 响应时间: {response_time}ms")
                
                # 尝试解析JSON响应
                try:
                    if response.headers.get('content-type', '').startswith('application/json'):
                        json_data = response.json()
                        print(f"📄 响应格式: JSON")
                        if isinstance(json_data, dict) and len(json_data) <= 5:
                            print(f"📝 响应内容: {json.dumps(json_data, ensure_ascii=False, indent=2)}")
                        else:
                            print(f"📝 响应大小: {len(str(json_data))} 字符")
                    else:
                        content_type = response.headers.get('content-type', 'unknown')
                        print(f"📄 响应格式: {content_type}")
                        if len(response.text) < 200:
                            print(f"📝 响应内容: {response.text[:100]}...")
                        else:
                            print(f"📝 响应大小: {len(response.text)} 字符")
                except:
                    print(f"📝 响应大小: {len(response.text)} 字符")
                
                success_count += 1
                results.append({"test": test['name'], "status": "SUCCESS", "code": response.status_code, "time": response_time})
            else:
                print(f"❌ 状态码: {response.status_code} (期望: {expected_status})")
                print(f"⏱️ 响应时间: {response_time}ms")
                print(f"📝 错误内容: {response.text[:200]}...")
                results.append({"test": test['name'], "status": "FAILED", "code": response.status_code, "time": response_time})
                
        except requests.exceptions.ConnectionError:
            print(f"❌ 连接失败: 无法连接到服务器")
            print(f"💡 请检查:")
            print(f"   - 后端服务是否已启动")
            print(f"   - 端口8000是否被占用")
            print(f"   - 防火墙是否阻止连接")
            results.append({"test": test['name'], "status": "CONNECTION_ERROR", "code": None, "time": None})
            
        except requests.exceptions.Timeout:
            print(f"❌ 请求超时: 服务器响应时间过长")
            results.append({"test": test['name'], "status": "TIMEOUT", "code": None, "time": None})
            
        except Exception as e:
            print(f"❌ 请求异常: {str(e)}")
            results.append({"test": test['name'], "status": "ERROR", "code": None, "time": None})
    
    # 输出测试总结
    print("\n" + "=" * 60)
    print("📊 测试结果总结")
    print("=" * 60)
    
    for result in results:
        status_icon = {
            "SUCCESS": "✅",
            "FAILED": "❌", 
            "CONNECTION_ERROR": "🔌",
            "TIMEOUT": "⏰",
            "ERROR": "💥"
        }.get(result['status'], "❓")
        
        time_str = f"{result['time']}ms" if result['time'] else "N/A"
        code_str = str(result['code']) if result['code'] else "N/A"
        
        print(f"{status_icon} {result['test']:<20} | 状态码: {code_str:<3} | 响应时间: {time_str}")
    
    print(f"\n🎯 成功率: {success_count}/{len(tests)} ({success_count/len(tests)*100:.1f}%)")
    
    # 给出建议
    if success_count == len(tests):
        print("\n🎉 所有测试通过！后端服务运行正常")
        print("💡 建议:")
        print("   - 可以开始进行API功能测试")
        print("   - 访问 http://127.0.0.1:8000/docs 查看完整API文档")
    elif success_count > 0:
        print(f"\n⚠️ 部分测试通过 ({success_count}/{len(tests)})")
        print("💡 建议:")
        print("   - 检查失败的接口是否需要认证")
        print("   - 确认数据库连接是否正常")
        print("   - 查看后端服务日志排查问题")
    else:
        print("\n🚨 所有测试失败！后端服务可能未正常启动")
        print("💡 建议:")
        print("   - 检查后端服务是否在运行")
        print("   - 确认端口8000是否被占用")
        print("   - 检查防火墙设置")
        print("   - 查看后端启动日志")
    
    print("\n🔗 相关链接:")
    print(f"   - API文档: {base_url}/docs")
    print(f"   - 健康检查: {base_url}/api/v1/health")
    print(f"   - OpenAPI规范: {base_url}/openapi.json")
    
    return success_count == len(tests)

def check_port_status():
    """检查端口状态"""
    import socket
    
    print("\n🔍 检查端口状态...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex(('127.0.0.1', 8000))
        sock.close()
        
        if result == 0:
            print("✅ 端口8000已开放，服务正在监听")
            return True
        else:
            print("❌ 端口8000未开放或服务未启动")
            return False
    except Exception as e:
        print(f"❌ 端口检查失败: {e}")
        return False

if __name__ == "__main__":
    print("🔧 UAV考点运营管理系统 - 后端连接测试")
    print("=" * 60)
    
    # 先检查端口状态
    port_ok = check_port_status()
    
    if port_ok:
        # 端口开放，进行详细测试
        success = test_backend_connection()
        
        if success:
            print(f"\n🎊 测试完成！后端服务运行正常，可以开始使用系统。")
        else:
            print(f"\n⚠️ 测试完成，但存在一些问题，请查看上述详细信息。")
    else:
        print("\n💡 启动后端服务的命令:")
        print("   cd backend")
        print("   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload")
        print("\n🔍 如果服务已启动但端口检查失败，可能的原因:")
        print("   - 服务绑定到了其他IP地址")
        print("   - 防火墙阻止了连接")
        print("   - 服务启动过程中出现错误")