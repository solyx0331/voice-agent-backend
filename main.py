"""
FastAPI Application Entry Point
"""
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from pathlib import Path
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.exceptions import (
    validation_exception_handler,
    http_exception_handler,
    database_exception_handler
)
from app.core.database import init_db, close_db
from app.api.v1.api import api_router
from sqlalchemy.exc import DatabaseError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    try:
        await init_db()
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        logger.warning("Application starting without database. Some features may not work.")
    yield
    try:
        await close_db()
    except Exception as e:
        logger.error(f"Error closing database connections: {e}")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(DatabaseError, database_exception_handler)

upload_dir = Path("uploads")
upload_dir.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(upload_dir)), name="uploads")

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Voice AI Agent API",
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    from app.core.database import engine
    from app.core.config import settings
    from sqlalchemy import text
    
    db_status = "unknown"
    db_error = None
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        error_str = str(e)
        db_status = "disconnected"
        if "getaddrinfo failed" in error_str or "11001" in error_str:
            db_error = "DNS resolution failed - cannot resolve database hostname"
        elif "authentication failed" in error_str.lower():
            db_error = "Authentication failed - check database credentials"
        elif "connection refused" in error_str.lower():
            db_error = "Connection refused - database server unreachable"
        else:
            db_error = error_str[:150]
    
    response = {
        "status": "healthy",
        "database": {
            "status": db_status,
        }
    }
    
    if db_error:
        response["database"]["error"] = db_error
        # Mask sensitive info from URL
        db_url = settings.DATABASE_URL
        if "@" in db_url:
            parts = db_url.split("@")
            response["database"]["host"] = parts[-1] if len(parts) > 1 else "N/A"
        else:
            response["database"]["host"] = "N/A"
    
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

