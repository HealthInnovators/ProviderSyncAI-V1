#!/bin/bash
# ProviderSyncAI Server Startup Script

cd "$(dirname "$0")/backend"

# Activate virtual environment
source venv/bin/activate

# Start the server
echo "🚀 Starting ProviderSyncAI Backend Server..."
echo "📍 Server will be available at: http://127.0.0.1:8000"
echo "📚 API Documentation: http://127.0.0.1:8000/docs"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

uvicorn main:app --reload --host 0.0.0.0 --port 8000

