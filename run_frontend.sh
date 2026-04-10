#!/usr/bin/env bash
# AgentMesh Frontend Startup Script for macOS/Linux

echo ""
echo "===================================================="
echo "  AgentMesh Frontend - Startup Script"
echo "===================================================="
echo ""

# Check if we're in the right directory
if [ ! -f "AgentMesh/UI/frontend/package.json" ]; then
    echo "ERROR: Frontend files not found!"
    echo "Please run this script from the project root directory."
    echo "Expected: ~/project/AgentMesh/"
    exit 1
fi

echo "[1/3] Checking Node.js installation..."
node --version
if [ $? -ne 0 ]; then
    echo "ERROR: Node.js is not installed!"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

echo "[2/3] Checking npm packages..."
cd AgentMesh/UI/frontend
if [ ! -d "node_modules" ]; then
    echo "Installing npm packages (this may take a minute)..."
    npm install
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install npm packages"
        exit 1
    fi
fi

if [ ! -f "public/styles.css" ]; then
    echo "Building Tailwind CSS..."
    npm run build
fi

echo "[3/3] Starting frontend server..."
echo ""
echo "Frontend Server:"
echo "  URL: http://localhost:8080"
echo "  Integration Dashboard: http://localhost:8080/integration.html"
echo "  Press Ctrl+C to stop"
echo ""
echo "TIP: Open frontend in your browser while backend is running (http://localhost:5000)"
echo ""

npm run dev
