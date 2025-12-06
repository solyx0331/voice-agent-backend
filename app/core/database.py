"""
Database connection and session management
"""
import logging
from urllib.parse import quote_plus
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import OperationalError
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

engine = create_async_engine(
    database_url,
    echo=settings.DATABASE_ECHO,
    future=True,
    pool_pre_ping=True,
    pool_recycle=300,
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
    """Get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
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
        logger.error(f"Failed to connect to database: {e}")
        logger.warning("Application will continue without database connection. Some features may not work.")
    except Exception as e:
        logger.error(f"Unexpected error during database initialization: {e}")
        logger.warning("Application will continue without database connection. Some features may not work.")


async def close_db():
    """Close database connections"""
    await engine.dispose()
