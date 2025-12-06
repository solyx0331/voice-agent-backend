"""
Application Configuration
"""
from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        env_ignore_empty=True,
    )
    
    # Project Info
    PROJECT_NAME: str = "Voice AI Agent API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Voice AI Agent HR Backend API"
    API_V1_STR: str = "/api/v1"
    
    # Server Settings
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    DEBUG: bool = True
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:8080",
        "http://localhost:5173",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if v is None or v == "":
            return []
        if isinstance(v, str):
            v = v.strip()
            if not v:
                return []
            if v.startswith("["):
                import json
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            return [i.strip() for i in v.split(",") if i.strip()]
        if isinstance(v, list):
            return v
        return v
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="after")
    @classmethod
    def ensure_list(cls, v):
        """Ensure the final value is always a list"""
        if isinstance(v, str):
            return [v]
        return v if isinstance(v, list) else []
    
    # Database Settings
    # Set DATABASE_URL in .env file or environment variable
    # Example for local: postgresql://postgres:postgres@localhost:5432/voice_ai_agent
    # Example for Supabase: postgresql://postgres:password@db.project.supabase.co:5432/postgres
    # NOTE: Do not hardcode credentials here - use .env file instead!
    # SSL will be automatically added for Supabase connections
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/voice_ai_agent"
    DATABASE_ECHO: bool = False
    
    # Security Settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list"""
        if isinstance(self.BACKEND_CORS_ORIGINS, list):
            return self.BACKEND_CORS_ORIGINS
        return [self.BACKEND_CORS_ORIGINS] if self.BACKEND_CORS_ORIGINS else []


settings = Settings()

