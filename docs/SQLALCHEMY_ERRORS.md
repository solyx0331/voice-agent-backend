# SQLAlchemy Error Handling Guide

This document describes how SQLAlchemy errors are handled in the Voice AI Agent backend.

## Error Categories

SQLAlchemy errors fall into two main categories:

### 1. Programming-Time Errors
Errors that occur during development when functions are called with incorrect arguments or configuration issues. These are typically immediate and deterministic.

### 2. Runtime Errors
Errors that occur during program execution in response to arbitrary conditions like:
- Database connections being exhausted
- Network connectivity issues
- Data integrity violations
- Timeout conditions

## Handled Exceptions

The application handles the following SQLAlchemy exceptions:

### OperationalError
**When it occurs:** Database connection or operational issues
- DNS resolution failures
- Connection refused
- Authentication failures
- Network timeouts

**HTTP Status:** `503 Service Unavailable`

**Example:**
```python
# DNS resolution failed
OperationalError: [Errno 11001] getaddrinfo failed

# Connection refused
OperationalError: connection refused
```

**Handling:** The application logs detailed diagnostics and continues running, but database features are unavailable.

### IntegrityError
**When it occurs:** Database constraint violations
- Unique constraint violations
- Foreign key constraint violations
- Check constraint violations
- NOT NULL constraint violations

**HTTP Status:** `409 Conflict`

**Example:**
```python
IntegrityError: duplicate key value violates unique constraint
```

**Handling:** Returns user-friendly error message indicating the constraint violation.

### ProgrammingError
**When it occurs:** SQL syntax errors or programming mistakes
- Invalid SQL syntax
- Wrong number of parameters
- Invalid column references

**HTTP Status:** `500 Internal Server Error`

**Example:**
```python
ProgrammingError: syntax error at or near "FROM"
```

**Handling:** Logs the error and returns generic error message (details hidden from users).

### DisconnectionError
**When it occurs:** Database connection is lost during operation

**HTTP Status:** `503 Service Unavailable`

**Handling:** Returns error message prompting user to retry.

### TimeoutError (SQLTimeoutError)
**When it occurs:** Database operation exceeds timeout limit

**HTTP Status:** `504 Gateway Timeout`

**Handling:** Returns timeout error message.

## Error Handling Architecture

### 1. Global Exception Handlers (`app/core/exceptions.py`)

```python
async def database_exception_handler(request: Request, exc: DatabaseError):
    """Handle SQLAlchemy database exceptions globally"""
    # Maps SQLAlchemy exceptions to appropriate HTTP status codes
    # Returns user-friendly error messages
```

### 2. Database Session Error Handling (`app/core/database.py`)

The `get_db()` dependency handles errors at the session level:

```python
async def get_db() -> AsyncSession:
    """Get database session with proper error handling"""
    # Catches and converts SQLAlchemy exceptions to HTTPExceptions
    # Ensures proper rollback on errors
```

### 3. CRUD Operation Error Handling (`app/crud/base.py`)

Base CRUD operations include error handling for:
- `create()` - Handles IntegrityError and OperationalError
- `update()` - Handles IntegrityError and OperationalError

## Error Response Format

All database errors return JSON responses in this format:

```json
{
    "detail": "User-friendly error message",
    "error_type": "OperationalError",
    "status_code": 503
}
```

## Logging

All database errors are logged with:
- Error type
- Full error message
- Context (operation, model, etc.)

Log levels:
- **ERROR**: For all database exceptions
- **WARNING**: For recoverable issues (e.g., connection failures at startup)

## Best Practices

### 1. Always Use Transactions
```python
async with AsyncSessionLocal() as session:
    try:
        # Your operations
        await session.commit()
    except Exception:
        await session.rollback()
        raise
```

### 2. Handle Specific Exceptions
```python
try:
    # Database operation
except IntegrityError as e:
    # Handle constraint violations
except OperationalError as e:
    # Handle connection issues
```

### 3. Provide User-Friendly Messages
- Don't expose internal database details
- Provide actionable error messages
- Include relevant context when safe

### 4. Log Detailed Information
- Log full error details for debugging
- Include operation context
- Track error frequency for monitoring

## Common Error Scenarios

### Connection Failures
**Symptom:** `getaddrinfo failed` or `connection refused`

**Causes:**
- Network connectivity issues
- Incorrect database hostname
- Database server is down
- Firewall blocking connection

**Solution:**
- Verify network connectivity
- Check database URL configuration
- Verify database server status
- Check firewall rules

### Constraint Violations
**Symptom:** `IntegrityError: duplicate key value`

**Causes:**
- Attempting to create duplicate records
- Foreign key references non-existent records
- Violating NOT NULL constraints

**Solution:**
- Check for existing records before creating
- Validate foreign key references
- Ensure required fields are provided

### Timeout Errors
**Symptom:** `TimeoutError` or slow queries

**Causes:**
- Large dataset queries
- Missing database indexes
- Database server overload

**Solution:**
- Add appropriate indexes
- Optimize queries
- Consider pagination
- Increase timeout if appropriate

## Testing Error Handling

Use the diagnostic script to test database connectivity:

```bash
python scripts/test_db_connection.py
```

This script tests:
1. DNS resolution
2. Port connectivity
3. Database authentication
4. Query execution

## Monitoring

Monitor these metrics:
- Error rate by type
- Connection pool usage
- Query execution times
- Failed transaction rate

## References

- [SQLAlchemy Core Exceptions](https://docs.sqlalchemy.org/en/20/core/exceptions.html)
- [SQLAlchemy ORM Exceptions](https://docs.sqlalchemy.org/en/20/orm/exceptions.html)
- [Error Messages Documentation](https://docs.sqlalchemy.org/en/20/errors.html)

