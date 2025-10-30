#!/bin/bash

# Load environment variables
if [ -f "$HOME/infinity_secure/auto_keys.env" ]; then
    source "$HOME/infinity_secure/auto_keys.env"
    export DATABASE_URL
    export NEON_API_KEY
fi

# Start server
cd "$(dirname "$0")/.."
echo "🚀 Starting Argus Cloud Server..."
echo "📍 Server will be available at: http://0.0.0.0:8000"
echo "📍 API docs at: http://0.0.0.0:8000/docs"
echo ""

uvicorn server.app:app --host 0.0.0.0 --port 8000 --reload
