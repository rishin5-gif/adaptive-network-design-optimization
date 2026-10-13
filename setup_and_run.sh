#!/bin/bash
# Adaptive Network Design and Optimization Framework
# Startup Automation Script

set -e

echo "================================================================="
echo " Adaptive Network Design & Optimization Framework (DAA Project 4)"
echo " AI ML Leopards • Faculty: Prof. Geeta Tripathi"
echo "================================================================="

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

# 1. Initialize Backend
echo "[1/3] Verifying Python Backend Environment..."
if [ ! -d "backend/venv" ]; then
    python3 -m venv backend/venv
    source backend/venv/bin/activate
    pip install -r backend/requirements.txt
else
    source backend/venv/bin/activate
fi

# Run backend tests to verify health
echo "[2/3] Running Automated Backend Tests..."
PYTHONPATH=backend python3 -m pytest backend/tests/ -q

# 2. Start Servers
echo "[3/3] Starting Backend and Frontend Servers..."

# Start Backend on Port 8000
PYTHONPATH=backend python3 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "Backend running at http://localhost:8000 (PID: $BACKEND_PID)"
echo "Interactive API Docs available at http://localhost:8000/docs"

# Start Frontend on Port 5173
cd frontend
npm run dev -- --host &
FRONTEND_PID=$!
echo "Frontend running at http://localhost:5173 (PID: $FRONTEND_PID)"

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true; exit" SIGINT SIGTERM

echo ""
echo "================================================================="
echo " Application is Live!"
echo " Web Dashboard:  http://localhost:5173"
echo " API Docs (Swagger): http://localhost:8000/docs"
echo " Press Ctrl+C to terminate both servers."
echo "================================================================="

wait
