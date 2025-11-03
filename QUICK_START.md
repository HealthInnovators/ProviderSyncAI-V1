# Quick Start Guide

## 🚀 Start the Application

### Option 1: Start Both Backend and Frontend
```bash
cd /home/kalyan/ProviderSyncAI
./START_ALL.sh
```

### Option 2: Start Separately

#### Start Backend (Terminal 1):
```bash
cd /home/kalyan/ProviderSyncAI/backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Start Frontend (Terminal 2):
```bash
cd /home/kalyan/ProviderSyncAI/frontend
npm run dev
```

## ✅ Verify Everything is Running

### 1. Check Backend Health
```bash
curl http://127.0.0.1:8000/api/health
```
Expected: `{"status":"ok"}`

### 2. Check Frontend
Open browser: http://localhost:5173

### 3. Check API Docs
Open browser: http://127.0.0.1:8000/docs

## 📍 Application URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 🔧 Troubleshooting

### Backend won't start
1. Make sure virtual environment is activated:
   ```bash
   cd backend
   source venv/bin/activate
   ```

2. Check if port 8000 is already in use:
   ```bash
   lsof -ti:8000 | xargs kill -9
   ```

### Frontend won't start
1. Make sure you're in the frontend directory:
   ```bash
   cd frontend  # NOT the root directory
   ```

2. Check if port 5173 is already in use:
   ```bash
   lsof -ti:5173 | xargs kill -9
   ```

### Database Issues
The database auto-initializes on first run. If you need to reset:
```bash
cd backend
rm providersync.db
# Restart server - it will recreate
```

## 🎯 Next Steps

1. ✅ Start both servers
2. ✅ Test health endpoint
3. ✅ Open frontend in browser
4. ✅ Try searching for providers
5. ✅ Explore API documentation at /docs

