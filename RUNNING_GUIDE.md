# Running Guide - ProviderSyncAI

## Quick Start

### 1. Backend Setup (Already Done!)

The backend is ready to run. Your environment is configured:
- ✅ Virtual environment exists
- ✅ Dependencies installed
- ✅ .env file configured with GROK_API_KEY
- ✅ Settings loaded correctly

### 2. Start the Backend Server

Open a terminal and run:

```bash
cd /home/kalyan/ProviderSyncAI/backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or use the Python module directly:

```bash
cd /home/kalyan/ProviderSyncAI/backend
source venv/bin/activate
python main.py
```

**The server will:**
- Automatically initialize the database on first run
- Start on `http://127.0.0.1:8000`
- Enable auto-reload for development

### 3. Verify Backend is Running

Once started, you should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

Test the health endpoint:
```bash
curl http://127.0.0.1:8000/api/health
```

Expected response: `{"status":"ok"}`

### 4. Access API Documentation

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### 5. Start the Frontend (Optional)

Open a **new terminal** window:

```bash
cd /home/kalyan/ProviderSyncAI/frontend
npm install  # First time only
npm run dev
```

Frontend will start on: http://localhost:5173

## API Endpoints

### Basic Search (Original)
- `GET /api/health` - Health check
- `POST /api/search/providers` - Search providers

### Workflow Endpoints (New)
- `POST /api/workflows/contact-validation/batch` - Batch contact validation
- `POST /api/workflows/credential-verification` - Credential verification
- `POST /api/workflows/quality-assessment` - Quality assessment
- `POST /api/workflows/extract-pdf` - Extract data from PDF
- `GET /api/workflows/review-queue` - Get providers requiring review

### Metrics Endpoints (New)
- `GET /api/metrics` - Get quality metrics
- `GET /api/metrics/directory-quality` - Directory quality score

## Testing the API

### 1. Health Check
```bash
curl http://127.0.0.1:8000/api/health
```

### 2. Search Providers
```bash
curl -X POST http://127.0.0.1:8000/api/search/providers \
  -H "Content-Type: application/json" \
  -d '{
    "postal_code": "02142",
    "limit": 5
  }'
```

### 3. Batch Contact Validation
```bash
curl -X POST http://127.0.0.1:8000/api/workflows/contact-validation/batch \
  -H "Content-Type: application/json" \
  -d '[
    {
      "npi": "1234567890",
      "first_name": "John",
      "last_name": "Doe",
      "phone": "555-1234",
      "address_line1": "123 Main St",
      "city": "Boston",
      "state": "MA",
      "postal_code": "02115"
    }
  ]'
```

### 4. Get Review Queue
```bash
curl http://127.0.0.1:8000/api/workflows/review-queue?limit=10
```

### 5. Get Directory Quality Metrics
```bash
curl http://127.0.0.1:8000/api/metrics/directory-quality
```

## Common Issues & Solutions

### Issue: Import Errors
**Solution**: Make sure you're in the virtual environment:
```bash
source venv/bin/activate
```

### Issue: Database Errors
**Solution**: Database auto-initializes on startup. If issues persist:
```bash
rm providersync.db  # Delete old database
# Restart server - it will recreate
```

### Issue: GROK_API_KEY Not Found
**Solution**: Check your `.env` file in the backend directory:
```bash
cd backend
cat .env | grep GROK_API_KEY
```

### Issue: Port Already in Use
**Solution**: Kill the process using port 8000:
```bash
lsof -ti:8000 | xargs kill -9
# Or use a different port:
uvicorn main:app --reload --port 8001
```

## Database Location

The SQLite database will be created at:
```
/home/kalyan/ProviderSyncAI/backend/providersync.db
```

## Logs

The application uses structured logging. Check terminal output for:
- `[info]` - General information
- `[warning]` - Warnings (e.g., rate limits)
- `[error]` - Errors

## Next Steps

1. ✅ Start the backend server
2. ✅ Test API endpoints using curl or the Swagger UI
3. ✅ (Optional) Start the frontend
4. ✅ Try batch validation workflows
5. ✅ Check metrics and reports

## Production Deployment

For production:
1. Remove `--reload` flag
2. Use PostgreSQL instead of SQLite
3. Configure proper CORS origins
4. Set up environment variables securely
5. Use a process manager like systemd or supervisor

