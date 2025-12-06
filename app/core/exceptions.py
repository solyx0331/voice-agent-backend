"""
Custom Exception Handlers
"""
import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from sqlalchemy.exc import (
    OperationalError,
    IntegrityError,
    ProgrammingError,
    DatabaseError,
    DisconnectionError,
    TimeoutError as SQLTimeoutError,
)

logger = logging.getLogger(__name__)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation exceptions"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "body": exc.body
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code
        }
    )


async def database_exception_handler(request: Request, exc: DatabaseError):
    """Handle SQLAlchemy database exceptions"""
    error_type = type(exc).__name__
    error_msg = str(exc)
    
    logger.error(f"Database error ({error_type}): {error_msg}")
    
    # Map SQLAlchemy exceptions to HTTP status codes
    if isinstance(exc, OperationalError):
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        detail = "Database connection error. Please try again later."
    elif isinstance(exc, IntegrityError):
        status_code = status.HTTP_409_CONFLICT
        detail = "Database integrity constraint violation. The operation conflicts with existing data."
    elif isinstance(exc, ProgrammingError):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        detail = "Database programming error. Please contact support."
    elif isinstance(exc, DisconnectionError):
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        detail = "Database connection lost. Please try again."
    elif isinstance(exc, SQLTimeoutError):
        status_code = status.HTTP_504_GATEWAY_TIMEOUT
        detail = "Database operation timed out. Please try again."
    else:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        detail = "An unexpected database error occurred."
    
    return JSONResponse(
        status_code=status_code,
        content={
            "detail": detail,
            "error_type": error_type,
            "status_code": status_code
        }
    )

