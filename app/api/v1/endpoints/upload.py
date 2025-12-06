"""
File upload endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
import aiofiles
from pathlib import Path
from datetime import datetime
import uuid
import os

router = APIRouter()

# Upload directories
UPLOAD_DIR = Path("uploads")
AUDIO_DIR = UPLOAD_DIR / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Allowed audio file types
ALLOWED_AUDIO_TYPES = {
    "audio/wav", "audio/wave", "audio/x-wav",
    "audio/mpeg", "audio/mp3",
    "audio/mp4", "audio/m4a",
    "audio/flac",
    "audio/ogg", "audio/oga",
    "audio/aac",
    "audio/webm"
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@router.post("/voice")
async def upload_voice_file(file: UploadFile = File(...)):
    """Upload a voice file for custom voice"""
    # Validate file type
    if file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_AUDIO_TYPES)}"
        )
    
    # Read file content
    content = await file.read()
    
    # Validate file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / (1024*1024)}MB"
        )
    
    # Generate unique filename
    file_extension = Path(file.filename).suffix if file.filename else ".wav"
    unique_filename = f"voice_{uuid.uuid4().hex}{file_extension}"
    file_path = AUDIO_DIR / unique_filename
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(content)
    
    # Generate URL
    file_url = f"/uploads/audio/{unique_filename}"
    voice_id = f"voice_{uuid.uuid4().hex}"
    
    return {
        "voice_id": voice_id,
        "url": file_url,
        "filename": unique_filename,
        "size": len(content),
        "content_type": file.content_type
    }


@router.post("/audio")
async def upload_audio_file(file: UploadFile = File(...)):
    """Upload a general audio file"""
    # Similar to voice upload but for general audio files
    if file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_AUDIO_TYPES)}"
        )
    
    content = await file.read()
    
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / (1024*1024)}MB"
        )
    
    file_extension = Path(file.filename).suffix if file.filename else ".wav"
    unique_filename = f"audio_{uuid.uuid4().hex}{file_extension}"
    file_path = AUDIO_DIR / unique_filename
    
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(content)
    
    file_url = f"/uploads/audio/{unique_filename}"
    
    return {
        "url": file_url,
        "filename": unique_filename,
        "size": len(content),
        "content_type": file.content_type
    }

