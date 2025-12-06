"""
Example Endpoints
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()


class ExampleResponse(BaseModel):
    """Example response model"""
    id: int
    name: str
    description: Optional[str] = None


@router.get("", response_model=List[ExampleResponse])
async def get_examples():
    """Get all examples"""
    return [
        ExampleResponse(id=1, name="Example 1", description="First example"),
        ExampleResponse(id=2, name="Example 2", description="Second example"),
    ]


@router.get("/{example_id}", response_model=ExampleResponse)
async def get_example(example_id: int):
    """Get a specific example by ID"""
    return ExampleResponse(
        id=example_id,
        name=f"Example {example_id}",
        description=f"Description for example {example_id}"
    )


@router.post("", response_model=ExampleResponse)
async def create_example(name: str, description: Optional[str] = None):
    """Create a new example"""
    return ExampleResponse(
        id=999,
        name=name,
        description=description
    )

