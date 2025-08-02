# API测试用例总结

## 概述

本项目已为核心API编写了完整的自动化测试用例，确保代码质量和功能稳定性。

## 测试文件结构

```
src/tests/
├── test_auth.py              # 认证API测试
├── test_candidates_api.py    # 考生管理API测试
├── test_schedules_api.py     # 排期管理API测试
├── test_exam_products_api.py # 考试产品API测试
└── test_main.py              # 主应用测试
```

## 测试覆盖范围

### 1. 认证API测试 (`test_auth.py`)
- ✅ JWT登录成功/失败测试
- ✅ 用户信息获取测试
- ✅ 权限验证测试
- ✅ Token有效性测试

### 2. 考生管理API测试 (`test_candidates_api.py`)
- ✅ 考生CRUD操作测试
- ✅ 批量导入功能测试
- ✅ 权限控制测试
- ✅ 数据验证测试
- ✅ 跨机构访问限制测试

### 3. 排期管理API测试 (`test_schedules_api.py`)
- ✅ 排期CRUD操作测试
- ✅ 批量创建排期测试
- ✅ 扫码签到功能测试
- ✅ 批量签到测试
- ✅ 签到统计测试

### 4. 考试产品API测试 (`test_exam_products_api.py`)
- ✅ 考试产品CRUD操作测试
- ✅ 数据验证测试
- ✅ 筛选功能测试
- ✅ 重复代码检查测试

## 测试特性

### 🔐 认证与权限
- 所有API端点都经过认证测试
- 权限控制严格验证
- 跨机构访问限制测试
- Token有效性验证

### 📊 数据验证
- 输入数据格式验证
- 业务规则验证
- 边界条件测试
- 错误处理测试

### 🔄 CRUD操作
- 完整的增删改查测试
- 分页功能测试
- 筛选功能测试
- 数据完整性验证

### 📁 文件处理
- Excel文件导入测试
- 模板下载测试
- 文件格式验证
- 错误文件处理

## 运行测试

### 运行所有测试
```bash
cd exam_site_backend
python run_tests.py
```

### 运行特定测试
```bash
# 运行认证测试
python run_tests.py run test_auth.py

# 运行考生API测试
python run_tests.py run test_candidates_api.py

# 运行排期API测试
python run_tests.py run test_schedules_api.py

# 运行考试产品API测试
python run_tests.py run test_exam_products_api.py
```

### 列出所有测试文件
```bash
python run_tests.py list
```

### 直接使用pytest
```bash
# 运行所有测试
pytest src/tests/ -v

# 运行特定测试文件
pytest src/tests/test_auth.py -v

# 运行特定测试类
pytest src/tests/test_candidates_api.py::TestCandidateCRUD -v

# 运行特定测试方法
pytest src/tests/test_auth.py::TestAuthentication::test_jwt_login_success -v
```

## 测试配置

### 数据库配置
- 使用SQLite内存数据库进行测试
- 每个测试函数独立数据库环境
- 自动清理测试数据

### 覆盖率报告
- 生成HTML覆盖率报告：`htmlcov/index.html`
- 生成XML覆盖率报告：`coverage.xml`
- 终端显示未覆盖代码行

### 测试标记
- `@pytest.mark.slow`: 慢速测试
- `@pytest.mark.integration`: 集成测试
- `@pytest.mark.unit`: 单元测试
- `@pytest.mark.auth`: 认证测试
- `@pytest.mark.crud`: CRUD操作测试
- `@pytest.mark.api`: API端点测试

## 测试最佳实践

### ✅ 已实现
- 独立的测试数据库环境
- 完整的fixture设置
- 详细的错误信息
- 覆盖率报告
- 测试分类标记
- 自动化测试脚本

### 🔄 持续改进
- 定期更新测试用例
- 添加新的API端点测试
- 优化测试性能
- 增加边界条件测试

## 测试报告

运行测试后，你将获得：
1. **终端输出**: 详细的测试结果
2. **HTML报告**: 可视化覆盖率报告
3. **XML报告**: 可集成到CI/CD的覆盖率数据
4. **测试统计**: 通过/失败/跳过的测试数量

## 注意事项

1. **环境要求**: 确保安装了所有测试依赖
2. **数据库**: 测试使用独立的SQLite数据库
3. **网络**: 测试不依赖外部网络服务
4. **性能**: 测试应该在合理时间内完成

## 下一步

1. 运行测试验证功能
2. 根据测试结果修复问题
3. 添加更多边界条件测试
4. 集成到CI/CD流程中 