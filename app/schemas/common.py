"""
Common schemas and base models
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class ResponseModel(BaseModel):
    """Base response model"""
    success: bool = True
    message: Optional[str] = None


class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)


class PaginatedResponse(BaseModel):
    """Paginated response wrapper"""
    items: List[Any]
    total: int
    page: int
    limit: int
    pages: int


class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    detail: str
    status_code: int

