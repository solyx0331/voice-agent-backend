# Supabase Connection Debugging Information

This document contains all the information needed to debug the SQLAlchemy connection to Supabase Postgres.

## 1. DATABASE_URL (Redacted)

**Current URL Format:**
```
postgresql://postgres:REDACTED@db.grxzzijboqadlibsaxqa.supabase.co:5432/postgres
```

**After URL preparation (converted to psycopg):**
```
postgresql+psycopg://postgres:REDACTED@db.grxzzijboqadlibsaxqa.supabase.co:5432/postgres?sslmode=require
```

**Note:** The URL is automatically converted from `postgresql://` to `postgresql+psycopg://` for async support, and SSL mode is added if not present.

## 2. Error Traceback

**Error Type:** Runtime Error (OperationalError)

**Error Message:**
```
psycopg.OperationalError: [Errno 11001] getaddrinfo failed
```

**Full Traceback:**
```
Traceback (most recent call last):
  File "D:\Projects\Voice AI agent (HR)\Backend\venv\Lib\site-packages\sqlalchemy\engine\base.py", line 146, in __init__
    self._dbapi_connection = engine.raw_connection()
  ...
  File "D:\Projects\Voice AI agent (HR)\Backend\venv\Lib\site-packages\psycopg\connection_async.py", line 114, in connect
    attempts = await conninfo_attempts_async(params)
  File "D:\Projects\Voice AI agent (HR)\Backend\venv\Lib\site-packages\psycopg\_conninfo_attempts_async.py", line 49, in conninfo_attempts_async
    raise e.OperationalError(str(last_exc))
sqlalchemy.exc.OperationalError: (psycopg.OperationalError) [Errno 11001] getaddrinfo failed
```

**Error Category:** Runtime error - DNS resolution failure

## 3. Engine/Session Configuration

### Engine Creation
**File:** `Backend/app/core/database.py`

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

database_url = prepare_database_url(settings.DATABASE_URL)

# SSL mode is automatically added if not present
if "sslmode" not in database_url.lower():
    separator = "&" if "?" in database_url else "?"
    database_url = f"{database_url}{separator}sslmode=require"

engine = create_async_engine(
    database_url,
    echo=settings.DATABASE_ECHO,  # False by default
    future=True,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=10,
)
```

### Session Maker
```python
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)
```

### FastAPI Dependency
```python
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
```

### Usage in FastAPI
```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

@router.get("/endpoint")
async def my_endpoint(db: AsyncSession = Depends(get_db)):
    # Use db session
    pass
```

## 4. SQLAlchemy Configuration

### Version Information
- **SQLAlchemy:** 2.0.36 (2.x)
- **Driver:** psycopg (psycopg3) version 3.2.3
- **Async Support:** Yes (using `sqlalchemy.ext.asyncio`)
- **ORM/Core:** Using SQLAlchemy ORM with async sessions

### Driver Details
- **Package:** `psycopg[binary,pool]==3.2.3`
- **URL Scheme:** `postgresql+psycopg://` (async psycopg3)
- **Connection Type:** Async (all operations are awaited)

### Code Pattern
- ✅ Using async SQLAlchemy (`create_async_engine`)
- ✅ Using async sessions (`AsyncSession`)
- ✅ All DB operations are awaited
- ✅ Proper async/await pattern throughout
- ✅ Using SQLAlchemy 2.0 style

## 5. Deployment Environment

**Environment:** Local development (Windows 10)
- **OS:** Windows 10 (win32 10.0.26100)
- **Python:** Python 3.13
- **Location:** Running locally, not deployed to remote host
- **Network:** Direct connection to Supabase (no proxy/VPN mentioned)

## 6. Current Issues Identified

### Primary Issue: DNS Resolution Failure
**Error:** `getaddrinfo failed` (Errno 11001)

**Possible Causes:**
1. Network connectivity issue
2. Incorrect database hostname
3. Supabase project might be paused or deleted
4. Firewall/proxy blocking the connection
5. DNS server issues

### Secondary Issue: SSL Configuration
**Status:** ✅ Fixed - SSL mode is now automatically added

The code now automatically adds `?sslmode=require` to the connection URL if not present, which is required for Supabase connections.

## 7. Connection String Format

### Input (from .env or config):
```
postgresql://postgres:password@db.grxzzijboqadlibsaxqa.supabase.co:5432/postgres
```

### After Processing:
```
postgresql+psycopg://postgres:URL_ENCODED_PASSWORD@db.grxzzijboqadlibsaxqa.supabase.co:5432/postgres?sslmode=require
```

**Processing Steps:**
1. URL encoding for special characters in password
2. Conversion from `postgresql://` to `postgresql+psycopg://`
3. Addition of `?sslmode=require` if not present

## 8. Testing Steps

### Step 1: Test DNS Resolution
```bash
# Windows
ping db.grxzzijboqadlibsaxqa.supabase.co

# Or use nslookup
nslookup db.grxzzijboqadlibsaxqa.supabase.co
```

### Step 2: Test Port Connectivity
```bash
# Windows PowerShell
Test-NetConnection -ComputerName db.grxzzijboqadlibsaxqa.supabase.co -Port 5432
```

### Step 3: Test with psql (if available)
```bash
psql "postgresql://postgres:REDACTED@db.grxzzijboqadlibsaxqa.supabase.co:5432/postgres?sslmode=require"
```

### Step 4: Run Diagnostic Script
```bash
python scripts/test_db_connection.py
```

## 9. Recommended Fixes

### Fix 1: Verify Supabase Project Status
1. Log into Supabase dashboard
2. Check if project is active (not paused)
3. Verify the hostname matches: `db.grxzzijboqadlibsaxqa.supabase.co`
4. Check if database password is correct

### Fix 2: Verify Network Connectivity
1. Check internet connection
2. Verify no firewall is blocking port 5432
3. Check if corporate proxy/VPN is interfering
4. Try from a different network

### Fix 3: Use Connection Pooling Settings
The current configuration includes:
- `pool_pre_ping=True` - Verifies connections before use
- `pool_recycle=300` - Recycles connections after 5 minutes
- `pool_size=5` - Base pool size
- `max_overflow=10` - Maximum overflow connections

### Fix 4: Alternative Connection String Format
If DNS continues to fail, try using the IP address directly (if available from Supabase dashboard) or verify the exact connection string format from Supabase.

## 10. Code Snippets for Reference

### Minimal Test Script
```python
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def test_connection():
    url = "postgresql+psycopg://postgres:REDACTED@db.grxzzijboqadlibsaxqa.supabase.co:5432/postgres?sslmode=require"
    engine = create_async_engine(url)
    
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT version()"))
            print(f"Connected! Version: {result.scalar()}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await engine.dispose()

asyncio.run(test_connection())
```

## 11. Environment Variables

**Required in `.env` file:**
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.grxzzijboqadlibsaxqa.supabase.co:5432/postgres
```

**Note:** The code automatically:
- Converts to `postgresql+psycopg://` for async
- Adds `?sslmode=require` for SSL
- URL-encodes special characters in password

## 12. Dependencies

**From `requirements.txt`:**
```
sqlalchemy==2.0.36
psycopg[binary,pool]==3.2.3
alembic==1.14.0
fastapi==0.115.0
uvicorn[standard]==0.32.0
```

## Summary

- **SQLAlchemy Version:** 2.0.36 (2.x)
- **Driver:** psycopg3 (async)
- **URL Scheme:** `postgresql+psycopg://`
- **SSL:** ✅ Configured (`sslmode=require`)
- **Async:** ✅ Fully async implementation
- **Error:** DNS resolution failure (getaddrinfo failed)
- **Environment:** Local Windows development
- **Status:** SSL configuration fixed, DNS issue needs network troubleshooting

