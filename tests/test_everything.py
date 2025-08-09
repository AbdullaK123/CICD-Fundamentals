# test_calculator.py - Comprehensive tests for CI/CD learning

import pytest
from fastapi.testclient import TestClient
from main import app, add, subtract, multiply, divide

# Create test client
client = TestClient(app)

# Test the core functions
class TestCalculatorFunctions:
    """Test the core calculator functions"""
    
    def test_add(self):
        assert add(2, 3) == 5
        assert add(-1, 1) == 0
        assert add(0.1, 0.2) == pytest.approx(0.3)
    
    def test_subtract(self):
        assert subtract(5, 3) == 2
        assert subtract(1, 1) == 0
        assert subtract(-1, -1) == 0
    
    def test_multiply(self):
        assert multiply(3, 4) == 12
        assert multiply(-2, 3) == -6
        assert multiply(0, 100) == 0
    
    def test_divide(self):
        assert divide(10, 2) == 5
        assert divide(7, 2) == 3.5
        assert divide(-10, 2) == -5
    
    def test_divide_by_zero(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(5, 0)

# Test the API endpoints
class TestCalculatorAPI:
    """Test the FastAPI endpoints"""
    
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Simple Calculator API"
        assert "endpoints" in data
    
    def test_health_endpoint(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_add_endpoint(self):
        response = client.post("/add", json={"a": 5, "b": 3})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 8
        assert data["operation"] == "addition"
        assert data["inputs"]["a"] == 5
        assert data["inputs"]["b"] == 3
    
    def test_subtract_endpoint(self):
        response = client.post("/subtract", json={"a": 10, "b": 4})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 6
        assert data["operation"] == "subtraction"
    
    def test_multiply_endpoint(self):
        response = client.post("/multiply", json={"a": 3, "b": 7})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 21
        assert data["operation"] == "multiplication"
    
    def test_divide_endpoint(self):
        response = client.post("/divide", json={"a": 15, "b": 3})
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == 5
        assert data["operation"] == "division"
    
    def test_divide_by_zero_endpoint(self):
        response = client.post("/divide", json={"a": 10, "b": 0})
        assert response.status_code == 400
        assert "Cannot divide by zero" in response.json()["detail"]
    
    def test_invalid_input(self):
        # Missing required field
        response = client.post("/add", json={"a": 5})
        assert response.status_code == 422
        
        # Invalid data type
        response = client.post("/add", json={"a": "not_a_number", "b": 5})
        assert response.status_code == 422

# Integration tests
class TestCalculatorIntegration:
    """Test complex workflows"""
    
    def test_calculation_chain(self):
        """Test multiple operations in sequence"""
        # Start with 10
        result = 10
        
        # Add 5 (= 15)
        response = client.post("/add", json={"a": result, "b": 5})
        assert response.status_code == 200
        result = response.json()["result"]
        assert result == 15
        
        # Multiply by 2 (= 30)
        response = client.post("/multiply", json={"a": result, "b": 2})
        assert response.status_code == 200
        result = response.json()["result"]
        assert result == 30
        
        # Divide by 3 (= 10)
        response = client.post("/divide", json={"a": result, "b": 3})
        assert response.status_code == 200
        result = response.json()["result"]
        assert result == 10
    
    def test_api_documentation_accessible(self):
        """Test that FastAPI docs are available"""
        response = client.get("/docs")
        assert response.status_code == 200
        
        response = client.get("/openapi.json")
        assert response.status_code == 200

# Performance tests (simple)
class TestCalculatorPerformance:
    """Basic performance tests"""
    
    def test_response_time(self):
        """Test that API responds quickly"""
        import time
        
        start_time = time.time()
        response = client.post("/add", json={"a": 1, "b": 1})
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 1.0  # Should respond in under 1 second
    
    def test_multiple_requests(self):
        """Test handling multiple requests"""
        for i in range(10):
            response = client.post("/add", json={"a": i, "b": i})
            assert response.status_code == 200
            assert response.json()["result"] == i * 2