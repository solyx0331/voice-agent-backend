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
│   │       ├── endpoints/          # API endpoints
│   │       │   ├── agents.py      # Voice agent endpoints
│   │       │   ├── calls.py       # Call endpoints
│   │       │   ├── contacts.py    # Contact endpoints
│   │       │   ├── dashboard.py   # Dashboard endpoints
│   │       │   ├── call_management.py  # Call management endpoints
│   │       │   ├── upload.py      # File upload endpoints
│   │       │   ├── settings.py    # Settings endpoints
│   │       │   ├── search.py      # Search endpoints
│   │       │   └── health.py      # Health check endpoints
│   │       └── api.py             # Main API router
│   ├── core/
│   │   ├── config.py              # Application configuration
│   │   ├── security.py            # Authentication & security utilities
│   │   ├── exceptions.py          # Exception handlers
│   │   ├── dependencies.py        # Common dependencies
│   │   └── database.py           # In-memory database (temporary)
│   ├── models/                    # Database models (for future use)
│   └── schemas/                   # Pydantic schemas
│       ├── common.py              # Common schemas
│       ├── agent.py               # Agent schemas
│       ├── call.py                # Call schemas
│       ├── contact.py             # Contact schemas
│       ├── dashboard.py           # Dashboard schemas
│       └── settings.py            # Settings schemas
├── main.py                        # Application entry point
├── run.py                         # Development server runner
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
└── README.md                      # This file
```

## Frontend Integration

The backend is fully configured for frontend integration:

- **CORS**: Configured to allow requests from `http://localhost:8080` (Vite dev server)
- **Static Files**: Uploaded files are served from `/uploads` directory
- **API Base URL**: All endpoints are prefixed with `/api/v1`
- **Error Handling**: Comprehensive error handling with proper HTTP status codes
- **File Upload**: Support for audio/voice file uploads (WAV, MP3, M4A, FLAC, OGG, AAC, WebM)

## Environment Variables

Create a `.env` file in the root directory:

```env
# Server Settings
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=True

# CORS Origins (comma-separated or JSON array)
BACKEND_CORS_ORIGINS=["http://localhost:8080","http://localhost:5173"]

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## API Endpoints

### Health Check
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/v1/health` - API health check
- `GET /api/v1/health/ready` - Readiness check
- `GET /api/v1/health/live` - Liveness check

### Dashboard
- `GET /api/v1/dashboard/stats` - Get dashboard statistics
- `GET /api/v1/dashboard/live-call` - Get current live call (if any)
- `GET /api/v1/dashboard/live-calls` - Get all active live calls
- `GET /api/v1/dashboard/analytics` - Get analytics data

### Voice Agents
- `GET /api/v1/agents` - Get all voice agents
- `GET /api/v1/agents/{agent_id}` - Get agent details
- `POST /api/v1/agents` - Create a new voice agent
- `PUT /api/v1/agents/{agent_id}` - Update a voice agent
- `PATCH /api/v1/agents/{agent_id}/status` - Update agent status
- `DELETE /api/v1/agents/{agent_id}` - Delete a voice agent
- `GET /api/v1/agents/{agent_id}/calls` - Get calls for an agent

### Calls
- `GET /api/v1/calls` - Get calls with optional filtering (search, agent, type, status, date range)
- `GET /api/v1/calls/{call_id}` - Get a specific call
- `POST /api/v1/calls` - Create a new call record
- `PUT /api/v1/calls/{call_id}` - Update a call record
- `DELETE /api/v1/calls/{call_id}` - Delete a call record
- `GET /api/v1/calls/{call_id}/recording` - Get call recording URL
- `POST /api/v1/calls/export` - Export calls (CSV/JSON)

### Call Management
- `POST /api/v1/calls/{call_id}/transfer` - Transfer a call to another agent
- `POST /api/v1/calls/{call_id}/hold` - Hold or unhold a call
- `POST /api/v1/calls/{call_id}/whisper` - Send whisper message to agent
- `POST /api/v1/calls/{call_id}/intervene` - Intervene in a call (human takeover)
- `POST /api/v1/calls/{call_id}/end` - End an active call
- `POST /api/v1/calls/{call_id}/mute` - Toggle mute on a call
- `PATCH /api/v1/calls/{call_id}/sentiment` - Update call sentiment

### Contacts
- `GET /api/v1/contacts` - Get contacts with optional filtering (search, status)
- `GET /api/v1/contacts/{contact_id}` - Get a specific contact
- `POST /api/v1/contacts` - Create a new contact
- `PUT /api/v1/contacts/{contact_id}` - Update a contact
- `DELETE /api/v1/contacts/{contact_id}` - Delete a contact
- `GET /api/v1/contacts/{contact_id}/calls` - Get calls for a contact

### File Upload
- `POST /api/v1/upload/voice` - Upload a voice file for custom voice
- `POST /api/v1/upload/audio` - Upload a general audio file

### Settings
- `PUT /api/v1/settings/profile` - Update user profile
- `PUT /api/v1/settings/voice` - Update voice settings
- `PUT /api/v1/settings/notifications` - Update notification settings
- `POST /api/v1/settings/password/change` - Change user password
- `POST /api/v1/settings/2fa/enable` - Enable two-factor authentication
- `POST /api/v1/settings/2fa/disable` - Disable two-factor authentication
- `POST /api/v1/settings/2fa/verify` - Verify 2FA code
- `GET /api/v1/settings/sessions` - Get active user sessions
- `DELETE /api/v1/settings/sessions/{session_id}` - Revoke a session
- `GET /api/v1/settings/billing` - Get billing information
- `PUT /api/v1/settings/billing/payment-method` - Update payment method
- `GET /api/v1/settings/invoices` - Get invoice history
- `POST /api/v1/settings/api-keys` - Create a new API key
- `GET /api/v1/settings/api-keys` - Get all API keys
- `DELETE /api/v1/settings/api-keys/{key_id}` - Delete an API key
- `POST /api/v1/settings/webhooks` - Create a new webhook
- `GET /api/v1/settings/webhooks` - Get all webhooks
- `PUT /api/v1/settings/webhooks/{webhook_id}` - Update a webhook
- `DELETE /api/v1/settings/webhooks/{webhook_id}` - Delete a webhook

### Search
- `GET /api/v1/search?query={query}` - Global search across agents, calls, and contacts

## Development

### Code Style

This project follows PEP 8 style guidelines. Consider using:
- `black` for code formatting
- `flake8` or `pylint` for linting
- `mypy` for type checking

## License

[Your License Here]


