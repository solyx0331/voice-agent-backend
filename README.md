# Voice AI Agent - Backend API

FastAPI backend application for Voice AI Agent HR system.

## Python Version

- **Python 3.13.11**

## Setup

### 1. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the example environment file and update as needed:

```bash
copy .env.example .env
# or on Linux/Mac: cp .env.example .env
```

Edit `.env` file with your configuration.

### 4. Run the Application

```bash
# Development mode (with auto-reload)
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
Backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/     # API endpoints
│   │       └── api.py         # Main API router
│   ├── core/
│   │   └── config.py          # Application configuration
│   ├── models/                # Database models (if needed)
│   └── schemas/               # Pydantic schemas
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Endpoints

### Health Check
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/v1/health` - API health check
- `GET /api/v1/health/ready` - Readiness check
- `GET /api/v1/health/live` - Liveness check

### Example
- `GET /api/v1/example` - Get all examples
- `GET /api/v1/example/{id}` - Get example by ID
- `POST /api/v1/example` - Create new example

## Development

### Code Style

This project follows PEP 8 style guidelines. Consider using:
- `black` for code formatting
- `flake8` or `pylint` for linting
- `mypy` for type checking

## License

[Your License Here]

