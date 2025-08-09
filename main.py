# main.py - Simple Calculator API for learning CI/CD

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Union
import uvicorn

app = FastAPI(
    title="Simple Calculator API",
    description="A basic calculator for learning CI/CD",
    version="1.0.0"
)

# Request/Response models
class CalculationRequest(BaseModel):
    a: float
    b: float

class CalculationResponse(BaseModel):
    result: float
    operation: str
    inputs: dict

# Calculator functions
def add(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtract b from a"""
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    return a * b

def divide(a: float, b: float) -> float:
    """Divide a by b"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# API Routes
@app.get("/")
def root():
    return {
        "message": "Simple Calculator API",
        "version": "1.0.0",
        "endpoints": ["/add", "/subtract", "/multiply", "/divide", "/health"]
    }

@app.post("/add", response_model=CalculationResponse)
def add_numbers(request: CalculationRequest):
    result = add(request.a, request.b)
    return CalculationResponse(
        result=result,
        operation="addition",
        inputs={"a": request.a, "b": request.b}
    )

@app.post("/subtract", response_model=CalculationResponse)
def subtract_numbers(request: CalculationRequest):
    result = subtract(request.a, request.b)
    return CalculationResponse(
        result=result,
        operation="subtraction", 
        inputs={"a": request.a, "b": request.b}
    )

@app.post("/multiply", response_model=CalculationResponse)
def multiply_numbers(request: CalculationRequest):
    result = multiply(request.a, request.b)
    return CalculationResponse(
        result=result,
        operation="multiplication",
        inputs={"a": request.a, "b": request.b}
    )

@app.post("/divide", response_model=CalculationResponse)
def divide_numbers(request: CalculationRequest):
    try:
        result = divide(request.a, request.b)
        return CalculationResponse(
            result=result,
            operation="division",
            inputs={"a": request.a, "b": request.b}
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "calculator-api"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)