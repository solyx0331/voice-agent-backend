"""
Main API Router
"""
from fastapi import APIRouter
from app.api.v1.endpoints import health, example

api_router = APIRouter()

# Include routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(example.router, prefix="/example", tags=["example"])

