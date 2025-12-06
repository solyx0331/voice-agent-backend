"""
Main API Router
"""
from fastapi import APIRouter
from app.api.v1.endpoints import (
    health,
    dashboard,
    agents,
    calls,
    contacts,
    call_management,
    upload,
    settings,
    search
)

api_router = APIRouter()

# Include routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(calls.router, prefix="/calls", tags=["calls"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
api_router.include_router(call_management.router, prefix="/calls", tags=["call-management"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
api_router.include_router(search.router, prefix="/search", tags=["search"])


