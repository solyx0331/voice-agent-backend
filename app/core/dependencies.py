"""
Common dependencies
"""
from typing import Generator
import aiofiles
import os
from pathlib import Path


# File upload directory
UPLOAD_DIR = Path("uploads")
AUDIO_DIR = UPLOAD_DIR / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


async def save_uploaded_file(file_content: bytes, filename: str, subdirectory: str = "audio") -> str:
    """Save uploaded file and return the file path"""
    upload_path = UPLOAD_DIR / subdirectory
    upload_path.mkdir(parents=True, exist_ok=True)
    
    file_path = upload_path / filename
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(file_content)
    
    return str(file_path.relative_to(Path.cwd()))


def get_file_url(file_path: str) -> str:
    """Get URL for uploaded file"""
    return f"/uploads/{file_path}"

