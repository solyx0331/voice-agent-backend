"""
Database connection and session management
"""
import logging
from urllib.parse import quote_plus
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import (
    OperationalError,
    IntegrityError,
    ProgrammingError,
    DatabaseError,
    DisconnectionError,
    TimeoutError as SQLTimeoutError,
)
from fastapi import HTTPException
from app.core.config import settings

logger = logging.getLogger(__name__)


def prepare_database_url(url: str) -> str:
    """
    Encode database URL, handling special characters in password.
    Converts to postgresql+psycopg:// for async support.
    """
    if "://" not in url:
        return url
    
    scheme, rest = url.split("://", 1)
    
    if "@" not in rest:
        if scheme == "postgresql":
            return url.replace("postgresql://", "postgresql+psycopg://", 1)
        elif scheme == "postgresql+asyncpg":
            return url.replace("postgresql+asyncpg://", "postgresql+psycopg://", 1)
        return url
    
    parts = rest.rsplit("@", 1)
    if len(parts) != 2:
        return url
    
    credentials, host_part = parts
    
    if ":" in credentials:
        username, password = credentials.split(":", 1)
        username = quote_plus(username)
        password = quote_plus(password)
        encoded_url = f"{scheme}://{username}:{password}@{host_part}"
    else:
        username = quote_plus(credentials)
        encoded_url = f"{scheme}://{username}@{host_part}"
    
    if scheme == "postgresql":
        encoded_url = encoded_url.replace("postgresql://", "postgresql+psycopg://", 1)
    elif scheme == "postgresql+asyncpg":
        encoded_url = encoded_url.replace("postgresql+asyncpg://", "postgresql+psycopg://", 1)
    
    return encoded_url


database_url = prepare_database_url(settings.DATABASE_URL)

# Add SSL mode if not present (required for Supabase)
if "sslmode" not in database_url.lower():
    separator = "&" if "?" in database_url else "?"
    database_url = f"{database_url}{separator}sslmode=require"

engine = create_async_engine(
    database_url,
    echo=settings.DATABASE_ECHO,
    future=True,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=15,
    max_overflow=10,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


async def get_db() -> AsyncSession:
    """
    Get database session with proper error handling.
    
    Handles common SQLAlchemy exceptions:
    - OperationalError: Connection issues
    - IntegrityError: Constraint violations
    - ProgrammingError: SQL syntax errors
    - DisconnectionError: Connection lost
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            logger.error(f"Database integrity error: {e}")
            raise HTTPException(
                status_code=409,
                detail=f"Database constraint violation: {str(e)}"
            ) from e
        except OperationalError as e:
            await session.rollback()
            logger.error(f"Database operational error: {e}")
            raise HTTPException(
                status_code=503,
                detail="Database connection error. Please try again later."
            ) from e
        except DisconnectionError as e:
            await session.rollback()
            logger.error(f"Database disconnection error: {e}")
            raise HTTPException(
                status_code=503,
                detail="Database connection lost. Please try again."
            ) from e
        except SQLTimeoutError as e:
            await session.rollback()
            logger.error(f"Database timeout error: {e}")
            raise HTTPException(
                status_code=504,
                detail="Database operation timed out. Please try again."
            ) from e
        except DatabaseError as e:
            await session.rollback()
            logger.error(f"Database error: {e}")
            raise HTTPException(
                status_code=500,
                detail="An unexpected database error occurred."
            ) from e
        except Exception as e:
            await session.rollback()
            logger.error(f"Unexpected error in database session: {e}")
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database - create all tables"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully")
    except OperationalError as e:
        error_msg = str(e)
        logger.error(f"Failed to connect to database: {e}")
        
        # Provide helpful diagnostics
        if "getaddrinfo failed" in error_msg or "11001" in error_msg:
            logger.error("DNS resolution failed - cannot resolve database hostname")
            logger.error("Possible causes:")
            logger.error("  1. Network connectivity issue")
            logger.error("  2. Incorrect database hostname in DATABASE_URL")
            logger.error("  3. Supabase project might be paused or deleted")
            logger.error("  4. Firewall/proxy blocking the connection")
            logger.error(f"  5. Check your DATABASE_URL: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'N/A'}")
        elif "authentication failed" in error_msg.lower():
            logger.error("Database authentication failed - check your password")
        elif "connection refused" in error_msg.lower():
            logger.error("Connection refused - database server might be down or port blocked")
        
        logger.warning("Application will continue without database connection. Some features may not work.")
    except Exception as e:
        logger.error(f"Unexpected error during database initialization: {e}")
        logger.warning("Application will continue without database connection. Some features may not work.")


async def close_db():
    """Close database connections"""
    await engine.dispose()
