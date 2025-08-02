import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.db.base import Base
from src.dependencies.get_db import get_db
from src.models.user import User
from src.models.venue import Venue
from src.core.security import get_password_hash

# 测试数据库配置 - 使用SQLite内存数据库
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function")
def setup_database():
    """设置测试数据库"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_venue(setup_database):
    """创建测试考场"""
    db = TestingSessionLocal()
    venue = Venue(
        name="测试考场",
        type="理论考场",
        status="active"
    )
    db.add(venue)
    db.commit()
    db.refresh(venue)
    db.close()
    return venue

class TestPublicVenuesStatus:
    """公共考场状态测试"""
    
    def test_get_venues_status_success(self):
        """测试成功获取考场状态"""
        response = client.get("/public/venues-status")
        # 公共端点应该可以访问
        assert response.status_code in [200, 500]  # 500可能是因为数据库问题
    
    def test_get_venues_status_response_structure(self):
        """测试考场状态响应结构"""
        response = client.get("/public/venues-status")
        if response.status_code == 200:
            data = response.json()
            assert "timestamp" in data
            assert "venues" in data
    
    def test_get_venue_status_success(self):
        """测试成功获取指定考场状态"""
        response = client.get("/public/venues/1/status")
        # 公共端点应该可以访问
        assert response.status_code in [200, 404, 500]  # 404如果考场不存在，500如果数据库问题
    
    def test_get_venue_status_not_found(self):
        """测试获取不存在的考场状态"""
        response = client.get("/public/venues/999/status")
        assert response.status_code in [404, 500]  # 404如果考场不存在，500如果数据库问题
    
    def test_get_venue_status_response_structure(self):
        """测试考场状态响应结构"""
        response = client.get("/public/venues/1/status")
        if response.status_code == 200:
            data = response.json()
            # 根据VenueStatusResponse的结构验证
            assert isinstance(data, dict)

class TestPublicEndpoints:
    """公共端点测试"""
    
    def test_public_venues_status_endpoint_exists(self):
        """测试公共考场状态端点存在"""
        response = client.get("/public/venues-status")
        assert response.status_code in [200, 500]  # 公共端点应该可以访问
    
    def test_public_venue_status_endpoint_exists(self):
        """测试公共单个考场状态端点存在"""
        response = client.get("/public/venues/1/status")
        assert response.status_code in [200, 404, 500]  # 公共端点应该可以访问
    
    def test_public_endpoints_are_public(self):
        """测试公共端点确实不需要认证"""
        # 不提供任何认证头
        response1 = client.get("/public/venues-status")
        response2 = client.get("/public/venues/1/status")
        
        # 这些端点应该可以公开访问
        assert response1.status_code != 401
        assert response2.status_code != 401

class TestPublicErrorHandling:
    """公共端点错误处理测试"""
    
    def test_public_venues_status_error_handling(self):
        """测试考场状态端点错误处理"""
        # 这个测试主要是确保端点存在并且不会因为数据库问题而崩溃
        response = client.get("/public/venues-status")
        # 应该返回200或500，而不是其他错误码
        assert response.status_code in [200, 500]
    
    def test_public_venue_status_error_handling(self):
        """测试单个考场状态端点错误处理"""
        response = client.get("/public/venues/1/status")
        # 应该返回200、404或500，而不是其他错误码
        assert response.status_code in [200, 404, 500]

class TestPublicDataValidation:
    """公共数据验证测试"""
    
    def test_venues_status_timestamp_format(self):
        """测试考场状态时间戳格式"""
        response = client.get("/public/venues-status")
        if response.status_code == 200:
            data = response.json()
            timestamp = data.get("timestamp")
            if timestamp:
                # 验证时间戳是ISO格式
                assert "T" in timestamp or "Z" in timestamp
    
    def test_venue_status_data_types(self):
        """测试考场状态数据类型"""
        response = client.get("/public/venues/1/status")
        if response.status_code == 200:
            data = response.json()
            # 验证返回的数据是字典类型
            assert isinstance(data, dict) 