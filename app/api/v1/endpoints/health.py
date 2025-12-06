"""
Health Check Endpoints
"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "voice-ai-agent-api"
    }


@router.get("/ready")
async def readiness():
    """Readiness check endpoint"""
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/live")
async def liveness():
    """Liveness check endpoint"""
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat()
    }

