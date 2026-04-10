#!/usr/bin/env bash
# AgentMesh Backend Startup Script for macOS/Linux

echo ""
echo "===================================================="
echo "  AgentMesh Backend - Startup Script"
echo "===================================================="
echo ""

# Check if we're in the right directory
if [ ! -f "AgentMesh/backend/rest_api_v2.py" ]; then
    echo "ERROR: Backend files not found!"
    echo "Please run this script from the project root directory."
    echo "Expected: ~/project/AgentMesh/"
    exit 1
fi

echo "[1/3] Checking Python installation..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

echo "[2/3] Checking required packages..."
python3 -c "import flask; import sqlalchemy; import jwt" >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: Required packages not installed"
    echo "Installing now..."
    pip install -q flask flask-cors pyjwt bcrypt sqlalchemy psycopg2-binary reportlab jinja2 pandas
fi

echo "[3/3] Starting backend server..."
echo ""
echo "Backend Server:"
echo "  URL: http://localhost:5000"
echo "  Press Ctrl+C to stop"
echo ""

cd AgentMesh
python3 -m backend.rest_api_v2 --debug --host 0.0.0.0 --port 5000
