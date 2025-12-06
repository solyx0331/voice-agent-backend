"""API endpoints"""
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

__all__ = [
    "health",
    "dashboard",
    "agents",
    "calls",
    "contacts",
    "call_management",
    "upload",
    "settings",
    "search"
]
