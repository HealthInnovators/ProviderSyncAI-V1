#!/bin/bash
# ProviderSyncAI - Start Both Backend and Frontend

echo "🚀 Starting ProviderSyncAI Full-Stack Application"
echo ""

# Start Backend
echo "📦 Starting Backend Server..."
cd "$(dirname "$0")/backend"
source venv/bin/activate

# Start backend in background
uvicorn main:app --reload --host 0.0.0.0 --port 8000 > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID) on http://127.0.0.1:8000"

# Wait a moment for backend to start
sleep 2

# Start Frontend
echo "🎨 Starting Frontend Server..."
cd ../frontend
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID) on http://localhost:5173"

echo ""
echo "════════════════════════════════════════════════════════"
echo "📍 Backend API:     http://127.0.0.1:8000"
echo "📍 API Docs:        http://127.0.0.1:8000/docs"
echo "📍 Frontend UI:     http://localhost:5173"
echo "════════════════════════════════════════════════════════"
echo ""
echo "📋 Logs:"
echo "   Backend:  tail -f logs/backend.log"
echo "   Frontend: tail -f logs/frontend.log"
echo ""
echo "Press CTRL+C to stop both servers"
echo ""

# Wait for interrupt
wait

